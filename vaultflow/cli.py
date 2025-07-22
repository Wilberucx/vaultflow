import click
from .commands import (
    initialize_vault, show_status, stage_changes, 
    commit_changes, create_local_backup, push_changes_to_remote,
    start_experiment as start_experiment_command,
    finish_experiment as finish_experiment_command,
    show_logs # <-- Importaci—n restaurada
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

# ... (los comandos start-experiment, finish-experiment, backup, push, status, stage, commit se quedan igual)
@cli.command()
@click.argument('name')
def start_experiment(name):
    start_experiment_command(name)

@cli.command()
@click.argument('name')
def finish_experiment(name):
    finish_experiment_command(name)

@cli.command()
def backup():
    create_local_backup()

@cli.command()
def push():
    push_changes_to_remote()

@cli.command()
def status():
    show_status()

@cli.command()
def stage():
    stage_changes()

@cli.command()
def commit():
    commit_changes()
    
@cli.command()
def log():
    """Muestra el historial de operaciones de vaultflow."""
    show_logs() # <-- Comando restaurado

if __name__ == '__main__':
    cli()