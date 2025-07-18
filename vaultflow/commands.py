import click
import subprocess
import os
from datetime import datetime
from rich.panel import Panel
from rich.console import Console
from .git_utils import (
    is_git_repository, get_current_branch, get_last_commit,
    get_structured_git_status, stage_all_changes, git_init,
    create_initial_commit, rename_branch, branch_exists, create_branch,
    commit_changes as git_commit_util
)

GITIGNORE_CONTENT = """
# ============================================
# .gitignore para Vaults de Obsidian (VaultFlow)
# ============================================

########## SISTEMA OPERATIVO ##########
.DS_Store
.AppleDouble
.LSOverride
Thumbs.db
Desktop.ini
*~

########## OBSIDIAN CACHE Y WORKSPACES ##########
.obsidian/workspace.json
.obsidian/workspaces.json
.obsidian/plugins/*/data.json

# Frecuentemente, estos no necesitan ser versionados.
# Si usas configuraciones de workspace especificas que quieres guardar, comenta estas lineas.
.obsidian/graph.json
.obsidian/starred.json
.obsidian/bookmarks.json

########## SYNC SERVICES ##########
.stfolder
.stignore
.dropbox
.dropbox.attr
*.icloud

########## PYTHON ##########
venv/
__pycache__/
*.pyc
"""

def create_gitignore_if_not_exists():
    """Crea un archivo .gitignore profesional si no existe."""
    if not os.path.exists('.gitignore'):
        click.echo("Creando archivo .gitignore profesional...")
        with open('.gitignore', 'w', encoding='utf-8') as f:
            f.write(GITIGNORE_CONTENT.strip())
        click.secho("✓ .gitignore creado.", fg="green")

def initialize_vault():
    """
    Logica para el comando init.
    Inicializa Git y asegura que las ramas 'main' y 'experiment', y el .gitignore existan.
    """
    click.echo("Iniciando vaultflow...")
    
    if not is_git_repository():
        click.secho("! Este directorio no es un repositorio de Git.", fg="yellow")
        if click.confirm("¿Quieres inicializar un nuevo repositorio de Git aqui?"):
            if not git_init():
                click.secho("✗ Error al ejecutar 'git init'.", fg="red")
                return
            click.secho("✓ Repositorio de Git creado.", fg="green")
            
            create_gitignore_if_not_exists()
            stage_all_changes() # Stage el .gitignore
            create_initial_commit()
            
            rename_branch('master', 'main')
            create_branch('experiment')
            
            click.secho("\n✓ ¡vaultflow inicializado correctamente!", fg="green")
            click.echo("  - Rama principal: main")
            click.echo("  - Rama para pruebas: experiment")
        else:
            click.secho("Operacion cancelada.", fg="red")
    else:
        click.secho("✓ El directorio ya es un repositorio de Git.", fg="green")
        create_gitignore_if_not_exists()
        click.echo("Verificando configuracion de ramas...")
        
        if not branch_exists('main'): click.secho("! No se encontro la rama 'main'.", fg="yellow")
        else: click.secho("✓ Rama 'main' encontrada.", fg="green")

        if not branch_exists('experiment'):
            click.secho("! No se encontro la rama 'experiment'. Creandola...", fg="yellow")
            if create_branch('experiment'): click.secho("✓ Rama 'experiment' creada.", fg="green")
            else: click.secho("✗ No se pudo crear la rama 'experiment'.", fg="red")
        else:
            click.secho("✓ Rama 'experiment' encontrada.", fg="green")
        
        click.secho("\n✓ Verificacion completada.", fg="green")

def commit_changes():
    """
    Logica para el comando commit.
    Crea un commit con los cambios que estan en el area de preparacion (staged).
    """
    if not is_git_repository():
        click.secho("✗ Error: Este no es un repositorio de Git.", fg="red")
        return

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    commit_message = f"Backup vaultflow - {timestamp}"
    
    click.echo(f"Creando backup con mensaje: '{commit_message}'...")
    
    if git_commit_util(commit_message):
        click.secho("✓ Backup local creado exitosamente.", fg="green")
        click.echo("\nEstado final:")
        show_status()
    else:
        click.secho("✗ Error al crear el backup.", fg="red")
        click.echo("  Posible causa: No hay cambios preparados para hacer commit.")
        click.echo("  Ejecuta 'vaultflow stage' primero.")


def show_status():
    """Muestra el estado del repositorio de Git de forma amigable y coloreada."""
    # (El resto del archivo no necesita cambios, esta funcion y las siguientes permanecen igual)
    if not is_git_repository():
        click.secho("✗ Error: Este no es un repositorio de Git.", fg="red")
        click.echo("Por favor, ejecuta 'vaultflow init' primero.")
        return
    console = Console()
    branch = get_current_branch()
    last_commit = get_last_commit()
    structured_status = get_structured_git_status()
    status_text = f"[bold]Rama actual:[/] [cyan]{branch}[/]\n"
    status_text += f"[bold]Ultimo backup:[/] [cyan]{last_commit}[/]\n"
    if structured_status:
        status_text += "\n"
        if structured_status.get('staged'):
            status_text += "[bold]Cambios listos para backup (staged):[/]\n"
            for line in structured_status['staged']: status_text += f"[green]  {line}[/]\n"
        if structured_status.get('modified'):
            status_text += "[bold]Cambios no preparados (modified):[/]\n"
            for line in structured_status['modified']: status_text += f"[yellow]  {line}[/]\n"
        if structured_status.get('untracked'):
            status_text += "[bold]Archivos no rastreados (untracked):[/]\n"
            for path in structured_status['untracked']: status_text += f"[red]  {path}[/]\n"
    else:
        status_text += "\n[bold]Estado:[/] [green]¡Tu vault esta al dia! No hay cambios pendientes."
    console.print(Panel(status_text, title="[bold magenta]Estado de vaultflow[/]", expand=False, border_style="blue"))

def stage_changes():
    """Anade todos los cambios al area de preparacion (staging)."""
    if not is_git_repository():
        click.secho("✗ Error: Este no es un repositorio de Git.", fg="red")
        click.echo("Por favor, ejecuta 'vaultflow init' primero.")
        return
    click.echo("Anadiendo todos los cambios al area de preparacion...")
    if stage_all_changes():
        click.secho("✓ Todos los cambios han sido anadidos exitosamente.", fg="green")
        click.echo("\nVerificando estado actualizado:")
        show_status()
    else:
        click.secho("✗ Error: No se pudo ejecutar 'git add'.", fg="red")

def create_local_backup():
    """
    Logica para el comando backup.
    Combina 'stage' y 'commit' en una sola operacion.
    """
    if not is_git_repository():
        click.secho("✗ Error: Este no es un repositorio de Git.", fg="red")
        return

    # Primero, verificar si hay algo que sauvegardar.
    if not get_structured_git_status():
        click.secho("✓ ¡Tu vault ya esta al dia! No hay nada que respaldar.", fg="green")
        return

    click.echo("Iniciando backup local completo...")
    
    # Paso 1: Stage
    click.echo("  -> Preparando todos los cambios...")
    if not stage_all_changes():
        click.secho("✗ Error al preparar los cambios (git add).", fg="red")
        return
    
    # Paso 2: Commit
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    commit_message = f"Backup vaultflow - {timestamp}"
    click.echo(f"  -> Creando backup con mensaje: '{commit_message}'...")
    
    if git_commit_util(commit_message):
        click.secho("\n✓ Backup local completado exitosamente.", fg="green")
        click.echo("\nEstado final:")
        show_status()
    else:
        click.secho("✗ Error al crear el backup (git commit).", fg="red")