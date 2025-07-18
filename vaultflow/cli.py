import click
from .commands import (
    initialize_vault, show_status, stage_changes, 
    commit_changes, create_local_backup
)
from .utils import display_banner

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """
    vaultflow es una herramienta CLI para gestionar Vaults de Obsidian con Git.
    """
    display_banner()
    if ctx.invoked_subcommand is None:
        # Si se ejecuta 'vaultflow' sin subcomando, muestra el estado.
        ctx.invoke(status)

@cli.command()
def init():
    """Inicializa vaultflow en tu vault de Obsidian."""
    initialize_vault()

@cli.command()
def backup():
    """Realiza un backup local completo (stage + commit)."""
    create_local_backup()

@cli.command()
def status():
    """Muestra el estado actual de tu vault (rama, cambios, ultimo backup)."""
    show_status()

@cli.command()
def stage():
    """Prepara todos los cambios para el proximo backup (git add .)."""
    stage_changes()

@cli.command()
def commit():
    """Crea un backup local con los cambios preparados (git commit)."""
    commit_changes()

if __name__ == '__main__':
    cli()