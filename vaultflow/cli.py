import click
from .commands import initialize_vault

@click.group()
def cli():
    """
    vaultflow es una herramienta CLI para gestionar Vaults de Obsidian con Git.
    """
    pass

@cli.command()
def init():
    """
    Inicializa vaultflow en tu vault de Obsidian.
    """
    initialize_vault()

if __name__ == '__main__':
    cli()