import os

def is_git_repository():
    """Verifica si el directorio actual es un repositorio de Git."""
    return os.path.isdir('.git')