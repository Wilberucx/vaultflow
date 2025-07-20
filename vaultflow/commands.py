import click
import os
import json
from datetime import datetime
from rich.panel import Panel
from rich.console import Console
from .git_utils import *
from .config import register_vault, is_managed_vault
from .logs import log_operation, get_log_file_path
# La importación clave que se había perdido:
from .git_utils import commit_changes as git_commit_util

VAULTFLOW_GITIGNORE_HEADER = "# === Bloque gestionado por vaultflow ==="
GITIGNORE_CONTENT = f"""
{VAULTFLOW_GITIGNORE_HEADER}
# Ignora archivos de sistema operativo
.DS_Store,.AppleDouble,.LSOverride,Thumbs.db,Desktop.ini,*~
# Ignora configuraciones de workspace y caches de Obsidian
.obsidian/workspace.json,.obsidian/workspaces.json,.obsidian/plugins/*/data.json
.obsidian/graph.json,.obsidian/starred.json,.obsidian/bookmarks.json
# Ignora archivos de servicios de sincronizacion
.stfolder,.stignore,.dropbox,.dropbox.attr,*.icloud
# Ignora entorno virtual de Python
venv/,__pycache__/,*.pyc
# Ignora el log de vaultflow
.vaultflow_log.json
""".replace(",", "\n")

# ... (Pega aquí la versión más reciente y completa de TODAS las funciones de `commands.py`,
# asegurándote de que `create_local_backup` y `commit_changes` usen `git_commit_util`)
def validation_guard():
    if is_managed_vault(): return True
    click.secho("✗ Error: Este directorio no esta gestionado por vaultflow.", fg="red")
    click.secho("  Por favor, ejecuta 'vaultflow init' en la raiz de tu vault para registrarlo.", fg="red")
    return False

def ensure_gitignore_is_updated():
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r+', encoding='utf-8') as f:
            content = f.read()
            if VAULTFLOW_GITIGNORE_HEADER not in content:
                click.echo("Actualizando .gitignore con las reglas de vaultflow...")
                f.write("\n" + GITIGNORE_CONTENT.strip() + "\n")
                click.secho("✓ .gitignore actualizado.", fg="green")
    else:
        click.echo("Creando archivo .gitignore profesional...")
        with open('.gitignore', 'w', encoding='utf-8') as f: f.write(GITIGNORE_CONTENT.strip())
        click.secho("✓ .gitignore creado.", fg="green")

def initialize_vault():
    click.echo("Iniciando vaultflow...")
    is_new_repo = not is_git_repository()
    if is_new_repo:
        if not click.confirm("Este directorio no es un repo Git. ¿Quieres inicializar uno?"):
            click.secho("Operacion cancelada.", fg="red"); log_operation("init", "El usuario cancelo la inicializacion", success=False); return
        git_init()
    repo_is_empty = "No hay commits todavia" in get_last_commit()
    if is_new_repo or repo_is_empty:
        click.secho("✓ Configurando un repositorio limpio para vaultflow...", fg="green")
        ensure_gitignore_is_updated(); stage_all_changes(); create_initial_commit()
        current_head = get_current_branch()
        if current_head and current_head != 'main': rename_branch(current_head, 'main')
    else:
        click.secho("✓ Repositorio Git con historial detectado.", fg="green")
        ensure_gitignore_is_updated()
        if not branch_exists('main'):
            if branch_exists('master'):
                click.secho("! No se encontro 'main', renombrando 'master'...", fg="yellow")
                rename_branch('master', 'main')
                click.secho("✓ Rama 'main' configurada.", fg="green")
    if not branch_exists('experiment'):
        click.secho("! Creando rama 'experiment'...", fg="yellow")
        create_branch('experiment')
    else: click.secho("✓ Rama 'experiment' encontrada.", fg="green")
    register_vault(os.getcwd())
    click.secho("\n✓ ¡Exito! Este vault ahora esta gestionado por vaultflow.", fg="green")
    log_operation("init", "Vault inicializado y registrado exitosamente.")

def create_local_backup():
    if not validation_guard(): return
    if not get_structured_git_status():
        click.secho("✓ ¡Tu vault ya esta al dia! No hay nada que respaldar.", fg="green")
        log_operation("backup", "No habia cambios para respaldar.")
        return
    click.echo("Iniciando backup local completo...")
    stage_all_changes()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    commit_message = f"Backup vaultflow - {timestamp}"
    if git_commit_util(commit_message):
        click.secho("\n✓ Backup local completado exitosamente.", fg="green")
        log_operation("backup", commit_message)
        show_status()
    else:
        click.secho("✗ Error al crear el backup.", fg="red")
        log_operation("backup", "Fallo al crear el backup (commit)", success=False)

def push_changes_to_remote():
    if not validation_guard(): return
    click.echo("Sincronizando con el repositorio remoto...")
    success, message = push_changes()
    if success:
        click.secho(f"✓ {message}", fg="green")
        log_operation("push", message)
    else:
        click.secho(f"✗ Error durante la sincronizacion:\n{message}", fg="red")
        log_operation("push", message, success=False)

def start_experiment(name):
    if not validation_guard(): return
    exp_name = f"exp/{name}"
    if not name or ' ' in name: click.secho("✗ ...", fg="red"); return
    if branch_exists(exp_name): click.secho(f"✗ Error: El experimento '{exp_name}' ya existe.", fg="red"); return
    success, msg = checkout_branch('main')
    if not success:
        click.secho(f"✗ Error al cambiar a 'main':\n  Git dice: {msg}", fg="red"); return
    if create_branch(exp_name) and checkout_branch(exp_name)[0]:
        msg = f"Iniciado nuevo experimento en rama '{exp_name}'."
        click.secho(f"\n✓ ¡Exito! {msg}", fg="green")
        log_operation("start-experiment", msg)
        show_status()
    else:
        click.secho("✗ Error al crear o cambiar a la nueva rama.", fg="red")
        log_operation("start-experiment", f"Fallo al crear la rama '{exp_name}'", success=False)

def finish_experiment(name):
    if not validation_guard(): return
    exp_name = f"exp/{name}"
    if not branch_exists(exp_name):
        click.secho(f"✗ Error: El experimento '{exp_name}' no existe.", fg="red"); return
    success, msg = checkout_branch('main')
    if not success:
        click.secho(f"✗ Error al cambiar a 'main'.\n  Git dice: {msg}", fg="red"); return
    status_code, merge_msg = merge_branch(exp_name)
    if status_code == 0:
        click.secho(f"✓ {merge_msg}", fg="green")
        log_operation("finish-experiment", f"Fusion de '{exp_name}' en 'main' exitosa.")
        if click.confirm(f"¿Quieres borrar la rama de experimento '{exp_name}'?"):
            if delete_branch(exp_name):
                click.secho("✓ Rama de experimento borrada.", fg="green")
                log_operation("finish-experiment", f"Rama '{exp_name}' borrada.")
    elif status_code == 1:
        click.secho(f"✗ {merge_msg}", fg="yellow")
        log_operation("finish-experiment", f"Conflicto de fusion al intentar finalizar '{exp_name}'.", success=False)
    else:
        click.secho(f"✗ {merge_msg}", fg="red")
        log_operation("finish-experiment", f"Error de fusion al intentar finalizar '{exp_name}': {merge_msg}", success=False)

def show_status():
    if not validation_guard(): return
    console = Console()
    status_text = f"[bold]Rama actual:[/] [cyan]{get_current_branch()}[/]\n[bold]Ultimo backup:[/] [cyan]{get_last_commit()}[/]\n"
    structured_status = get_structured_git_status()
    if structured_status:
        status_text += "\n"
        if structured_status.get('staged'): status_text += "[bold]Cambios listos (staged):[/]\n" + "".join(f"[green]  {l}[/]\n" for l in structured_status['staged'])
        if structured_status.get('modified'): status_text += "[bold]Cambios no preparados (modified):[/]\n" + "".join(f"[yellow]  {l}[/]\n" for l in structured_status['modified'])
        if structured_status.get('untracked'): status_text += "[bold]Archivos no rastreados (untracked):[/]\n" + "".join(f"[red]  {p}[/]\n" for p in structured_status['untracked'])
    else: status_text += "\n[bold]Estado:[/] [green]¡Tu vault esta al dia! No hay cambios pendientes."
    console.print(Panel(status_text, title="[bold magenta]Estado de vaultflow[/]", expand=False, border_style="magenta"))

def stage_changes():
    if not validation_guard(): return
    click.echo("Anadiendo todos los cambios al area de preparacion...")
    if stage_all_changes():
        click.secho("✓ Todos los cambios han sido anadidos.", fg="green")
        show_status()
    else: click.secho("✗ Error al ejecutar 'git add'.", fg="red")

def commit_changes():
    if not validation_guard(): return
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    commit_message = f"Backup vaultflow - {timestamp}"
    if git_commit_util(commit_message):
        click.secho("✓ Backup local creado exitosamente.", fg="green")
        show_status()
    else:
        click.secho("✗ Error al crear el backup. Posible causa: No hay cambios preparados.", fg="red")

def show_logs():
    if not validation_guard(): return
    log_file = get_log_file_path()
    if not os.path.exists(log_file):
        click.secho("No se ha encontrado ningun historial de operaciones.", fg="yellow"); return
    with open(log_file, 'r', encoding='utf-8') as f:
        logs = json.load(f)
    console = Console()
    console.print("[bold magenta]Historial de Operaciones de vaultflow[/]")
    console.print("[magenta]" + "-" * 60 + "[/magenta]")
    for entry in logs:
        status = "[green]✓ EXITO[/green]" if entry["success"] else "[red]✗ FALLO[/red]"
        ts = datetime.fromisoformat(entry["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')
        console.print(f"[{ts}] - {status} - [bold]{entry['command']}[/bold]: {entry['message']}")