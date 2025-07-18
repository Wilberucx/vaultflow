import click
from .git_utils import is_git_repository
import subprocess

def initialize_vault():
    """
    Lógica para el comando init.
    Verifica si es un repo de Git, si no, lo inicializa.
    """
    click.echo("Iniciando la inicialización de vaultflow...")
    
    if is_git_repository():
        click.secho("✓ El directorio ya es un repositorio de Git.", fg="green")
    else:
        click.secho("! Este directorio no es un repositorio de Git.", fg="yellow")
        if click.confirm("¿Quieres inicializar un nuevo repositorio de Git aquí?"):
            try:
                subprocess.run(['git', 'init'], check=True)
                click.secho("✓ Repositorio de Git creado exitosamente.", fg="green")
            except (subprocess.CalledProcessError, FileNotFoundError):
                click.secho("✗ Error: No se pudo ejecutar 'git init'. Asegúrate de que Git esté instalado y en tu PATH.", fg="red")
                return
        else:
            click.secho("Operación cancelada. vaultflow requiere un repositorio de Git para funcionar.", fg="red")
            return

    click.echo("\nLógica adicional (crear ramas, config) por implementar.")