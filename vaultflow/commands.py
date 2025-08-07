import click
import os
import json
from datetime import datetime
from rich.panel import Panel
from rich.console import Console
from .git_utils import *
from .config import register_vault, is_managed_vault, get_current_vault_info, get_managed_vaults, get_vault_name_from_path, auto_discover_and_register_vaults, cleanup_invalid_vaults
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
    
    # Verificar si ya estamos en un experimento (zona de seguridad)
    current_branch = get_current_branch()
    if current_branch and current_branch.startswith('exp/'):
        click.secho("✗ Error: Ya te encuentras en un experimento.", fg="red")
        click.secho(f"  Estás en la rama: {current_branch}", fg="red")
        click.secho("", fg="red")
        click.secho("  No puedes iniciar un experimento dentro de otro.", fg="red")
        click.secho("  Para empezar uno nuevo, primero finaliza el actual con 'vaultflow finish-experiment' o vuelve a la rama principal con 'git checkout main'.", fg="red")
        return
    
    exp_name = f"exp/{name}"
    if not name :
        return
    if  ' ' in name: 
        click.secho("\n✗ Error: El nombre del experimento contiene espacios ...", fg="red", bold=True),
        click.secho("  Por favor, usa un nombre sin espacios.", fg="yellow")
        return
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
    
    # Obtener información del vault actual
    vault_info = get_current_vault_info()
    managed_vaults = get_managed_vaults()
    
    # Sección de información del vault
    vault_section = f"[bold blue]Vault actual:[/] [cyan]{vault_info['name']}[/]\n"
    vault_section += f"[bold blue]Ubicación:[/] [dim]{vault_info['path']}[/]\n"
    if vault_info['total_managed_vaults'] > 1:
        vault_section += f"[bold blue]Vaults gestionados:[/] [yellow]{vault_info['total_managed_vaults']}[/]\n"
        vault_section += "[dim]Usa 'vaultflow vaults' para ver todos o cambiar de vault[/]\n"
    
    # Sección de Git
    git_section = f"\n[bold]Rama actual:[/] [cyan]{get_current_branch()}[/]\n"
    git_section += f"[bold]Ultimo backup:[/] [cyan]{get_last_commit()}[/]\n"
    
    # Sección de backups recientes
    backups = get_backup_commits(5)
    if backups:
        git_section += "\n[bold green]Backups recientes:[/]\n"
        for i, backup in enumerate(backups):
            marker = "[green]•[/]" if i == 0 else "[dim]•[/]"
            git_section += f"  {marker} [cyan]{backup['hash']}[/] - {backup['date']} - [dim]{backup['message']}[/]\n"
        git_section += "[dim]Usa 'vaultflow backups' para ver más opciones[/]\n"
    
    # Sección de estado de cambios
    status_section = ""
    structured_status = get_structured_git_status()
    if structured_status:
        status_section += "\n"
        if structured_status.get('staged'):
            status_section += "[bold]Cambios listos (staged):[/]\n"
            status_section += "".join(f"[green]  {l}[/]\n" for l in structured_status['staged'])
        if structured_status.get('modified'):
            status_section += "[bold]Cambios no preparados (modified):[/]\n"
            status_section += "".join(f"[yellow]  {l}[/]\n" for l in structured_status['modified'])
        if structured_status.get('untracked'):
            status_section += "[bold]Archivos no rastreados (untracked):[/]\n"
            status_section += "".join(f"[red]  {p}[/]\n" for p in structured_status['untracked'])
    else:
        status_section += "\n[bold]Estado:[/] [green]¡Tu vault esta al dia! No hay cambios pendientes.[/]"
    
    # Combinar todas las secciones
    full_status = vault_section + git_section + status_section
    
    console.print(Panel(
        full_status, 
        title="[bold magenta]Estado de vaultflow[/]", 
        expand=False, 
        border_style="magenta"
    ))

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

def show_backups():
    """Muestra los backups disponibles con opciones interactivas."""
    if not validation_guard(): return
    
    console = Console()
    backups = get_backup_commits(15)  # Obtener más backups para la vista detallada
    
    if not backups:
        console.print("[yellow]No se encontraron backups de vaultflow en este vault.[/yellow]")
        return
    
    console.print("[bold magenta]Backups Disponibles[/bold magenta]")
    console.print("[magenta]" + "=" * 60 + "[/magenta]")
    
    for i, backup in enumerate(backups):
        status_indicator = "[green]● ACTUAL[/green]" if i == 0 else "[dim]○[/dim]"
        console.print(f"{status_indicator} [cyan]{backup['hash']}[/cyan] - [yellow]{backup['date']}[/yellow]")
        console.print(f"    [dim]{backup['message']}[/dim]")
        console.print()
    
    console.print("[dim]Para navegar a un backup específico, usa: git checkout <hash>[/dim]")
    console.print("[dim]Para volver al estado más reciente, usa: git checkout main[/dim]")

def show_vaults():
    """Muestra todos los vaults gestionados con opción de cambiar."""
    console = Console()
    managed_vaults = get_managed_vaults()
    current_vault = get_current_vault_info()
    
    if len(managed_vaults) == 0:
        console.print("[yellow]No hay vaults gestionados por vaultflow.[/yellow]")
        return
    elif len(managed_vaults) == 1:
        console.print(f"[yellow]Solo hay un vault gestionado: [cyan]{current_vault['name']}[/cyan][/yellow]")
        return
    
    console.print("[bold magenta]Vaults Gestionados por vaultflow[/bold magenta]")
    console.print("[magenta]" + "=" * 70 + "[/magenta]")
    
    for vault_path in managed_vaults:
        vault_name = get_vault_name_from_path(vault_path)
        is_current = vault_path == current_vault['path']
        
        if is_current:
            console.print(f"[green]● ACTUAL[/green] [bold cyan]{vault_name}[/bold cyan]")
            console.print(f"    [green]{vault_path}[/green]")
        else:
            console.print(f"[dim]○[/dim] [yellow]{vault_name}[/yellow]")
            console.print(f"    [dim]{vault_path}[/dim]")
        console.print()
    
    console.print("[dim]Para cambiar a otro vault, usa: cd \"ruta_del_vault\" && vaultflow[/dim]")
    console.print("[dim]O ejecuta vaultflow desde un directorio no gestionado y selecciona el vault deseado.[/dim]")

def discover_vaults():
    """Auto-descubre y registra vaults gestionados por vaultflow."""
    console = Console()
    
    console.print("[yellow]🔍 Buscando vaults gestionados por vaultflow...[/yellow]")
    
    # Limpiar vaults inválidos primero
    removed_count = cleanup_invalid_vaults()
    if removed_count > 0:
        console.print(f"[dim]✓ Se eliminaron {removed_count} vault(s) inválido(s) de la configuración[/dim]")
    
    # Auto-descubrir nuevos vaults
    discovered = auto_discover_and_register_vaults()
    
    if discovered:
        console.print(f"\n[green]✓ Se encontraron y registraron {len(discovered)} vault(s):[/green]")
        for vault_path in discovered:
            vault_name = get_vault_name_from_path(vault_path)
            console.print(f"  [cyan]•[/cyan] [bold]{vault_name}[/bold] - [dim]{vault_path}[/dim]")
        
        console.print(f"\n[bold]Total de vaults gestionados: {len(get_managed_vaults())}[/bold]")
        console.print("[dim]Usa 'vaultflow vaults' para ver todos los vaults registrados.[/dim]")
    else:
        managed_count = len(get_managed_vaults())
        if managed_count > 0:
            console.print(f"[green]✓ No se encontraron vaults nuevos. Ya tienes {managed_count} vault(s) registrado(s).[/green]")
        else:
            console.print("[yellow]⚠ No se encontraron vaults gestionados por vaultflow en ubicaciones comunes.[/yellow]")
            console.print("\n[dim]Ubicaciones buscadas:[/dim]")
            home = os.path.expanduser("~")
            locations = [
                os.path.join(home, "Documents"),
                os.path.join(home, "Obsidian.Vaults"),
                os.path.join(home, "vaults"),
                "C:\\Obsidian.Vaults",
                "/Users/Shared/Obsidian.Vaults",
                "/home/obsidian",
                home
            ]
            for location in locations:
                exists = "✓" if os.path.exists(location) else "✗"
                console.print(f"  [dim]{exists} {location}[/dim]")
            
            console.print("\n[cyan]💡 Sugerencias:[/cyan]")
            console.print("  • Ejecuta 'vaultflow init' en directorios que contengan vaults de Obsidian")
            console.print("  • Los vaults deben tener Git inicializado y commits de vaultflow para ser auto-detectados")
