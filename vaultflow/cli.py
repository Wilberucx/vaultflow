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

if __name__ == '__main__':
    cli()
