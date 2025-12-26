import click
from .commands import (
    initialize_vault, show_status, stage_changes, 
    commit_changes, create_local_backup, push_changes_to_remote,
    start_experiment as start_experiment_command,
    finish_experiment as finish_experiment_command,
    show_logs, show_backups, show_vaults, discover_vaults  # <- Comando discover agregado
)
from .utils import display_banner
from .interactive import launch_interactive_menu

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """vaultflow es una herramienta CLI para gestionar Vaults de Obsidian con Git."""
    display_banner()
    if ctx.invoked_subcommand is None:
        launch_interactive_menu()

@cli.command()
def init():
    """Inicializa vaultflow en tu vault de Obsidian."""
    initialize_vault()

@cli.command()
@click.argument('name')
def start_experiment(name):
    """Inicia un nuevo experimento."""
    start_experiment_command(name)

@cli.command()
@click.argument('name')
def finish_experiment(name):
    """Finaliza un experimento."""
    finish_experiment_command(name)

@cli.command()
def backup():
    """Crea un backup local del vault."""
    create_local_backup()

@cli.command()
def push():
    """Sincroniza cambios con el repositorio remoto."""
    push_changes_to_remote()

@cli.command()
def status():
    """Muestra el estado actual del vault."""
    show_status()

@cli.command()
def stage():
    """Agrega todos los cambios al área de preparación."""
    stage_changes()

@cli.command()
def commit():
    """Crea un commit con los cambios preparados."""
    commit_changes()
    
@cli.command()
def log():
    """Muestra el historial de operaciones de vaultflow."""
    show_logs()

@cli.command()
def backups():
    """Muestra los backups disponibles."""
    show_backups()

@cli.command()
def vaults():
    """Muestra todos los vaults gestionados."""
    show_vaults()

@cli.command()
def discover():
    """Auto-descubre y registra vaults gestionados por vaultflow."""
    discover_vaults()

@cli.command()
def sysinfo():
    """Muestra información del sistema y verifica requisitos."""
    from .platform_utils import get_platform_info, verify_system_requirements
    from rich.console import Console
    from rich.panel import Panel
    
    console = Console()
    
    # Verificar requisitos
    success, messages = verify_system_requirements()
    
    # Obtener información de la plataforma
    platform_info = get_platform_info()
    
    # Construir el mensaje de salida
    output = "[bold cyan]Información del Sistema[/bold cyan]\n\n"
    
    # Requisitos
    output += "[bold]Requisitos:[/bold]\n"
    for msg in messages:
        output += f"{msg}\n"
    
    output += f"\n[bold]Configuración:[/bold]\n"
    output += f"Directorio de config: [cyan]{platform_info['config_dir']}[/cyan]\n"
    
    output += f"\n[bold]Detalles del Sistema:[/bold]\n"
    output += f"Sistema Operativo: {platform_info['system']} {platform_info['release']}\n"
    output += f"Arquitectura: {platform_info['machine']}\n"
    output += f"Python: {platform_info['python_version']}\n"
    
    # Determinar el color del borde según el éxito
    border_style = "green" if success else "red"
    status = "✓ Sistema compatible" if success else "✗ Requisitos faltantes"
    
    console.print(Panel(
        output,
        title=f"[bold]{status}[/bold]",
        border_style=border_style,
        expand=False
    ))
    
    if not success:
        console.print("\n[yellow]Por favor, instala los requisitos faltantes antes de usar vaultflow.[/yellow]")

if __name__ == '__main__':
    cli()
