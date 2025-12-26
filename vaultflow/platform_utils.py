"""
Utilidades para manejar diferencias entre plataformas (Windows, Linux, macOS).
Proporciona funciones para detectar el sistema operativo y adaptar comportamientos.
"""

import os
import sys
import platform
import shutil
from pathlib import Path
from typing import List, Optional


def get_platform() -> str:
    """
    Detecta y retorna el sistema operativo actual.
    
    Returns:
        str: 'windows', 'linux', 'darwin' (macOS), o 'unknown'
    """
    system = platform.system().lower()
    if system == 'windows':
        return 'windows'
    elif system == 'linux':
        return 'linux'
    elif system == 'darwin':
        return 'darwin'
    else:
        return 'unknown'


def is_windows() -> bool:
    """Verifica si el sistema es Windows."""
    return get_platform() == 'windows'


def is_unix() -> bool:
    """Verifica si el sistema es Unix-like (Linux o macOS)."""
    return get_platform() in ['linux', 'darwin']


def is_macos() -> bool:
    """Verifica si el sistema es macOS."""
    return get_platform() == 'darwin'


def is_linux() -> bool:
    """Verifica si el sistema es Linux."""
    return get_platform() == 'linux'


def get_default_documents_paths() -> List[str]:
    """
    Retorna las rutas típicas donde los usuarios guardan documentos
    según el sistema operativo.
    
    Returns:
        List[str]: Lista de rutas a verificar
    """
    home = os.path.expanduser("~")
    paths = []
    
    if is_windows():
        # Windows: Documents, Documentos (español)
        paths.extend([
            os.path.join(home, "Documents"),
            os.path.join(home, "Documentos"),
            os.path.join(home, "OneDrive", "Documents"),
            os.path.join(home, "OneDrive", "Documentos"),
        ])
    elif is_macos():
        # macOS: Documents, iCloud Drive
        paths.extend([
            os.path.join(home, "Documents"),
            os.path.join(home, "Library", "Mobile Documents", "com~apple~CloudDocs"),
        ])
    elif is_linux():
        # Linux: Documents, Documentos, y ubicaciones comunes de XDG
        paths.extend([
            os.path.join(home, "Documents"),
            os.path.join(home, "Documentos"),
        ])
        
        # Intentar obtener la ruta XDG_DOCUMENTS_DIR
        try:
            xdg_docs = os.path.expandvars("$XDG_DOCUMENTS_DIR")
            if xdg_docs and xdg_docs != "$XDG_DOCUMENTS_DIR":
                paths.append(xdg_docs)
        except:
            pass
    
    # Agregar el home directory como último recurso
    paths.append(home)
    
    # Retornar solo las rutas que existen
    return [p for p in paths if os.path.exists(p)]


def get_config_dir() -> str:
    """
    Retorna el directorio de configuración apropiado según el sistema operativo.
    
    Returns:
        str: Ruta al directorio de configuración
    """
    home = os.path.expanduser("~")
    
    if is_windows():
        # Windows: %APPDATA%\.vaultflow o %USERPROFILE%\.vaultflow
        appdata = os.getenv('APPDATA')
        if appdata:
            return os.path.join(appdata, "vaultflow")
        return os.path.join(home, ".vaultflow")
    
    elif is_macos():
        # macOS: ~/Library/Application Support/vaultflow
        return os.path.join(home, "Library", "Application Support", "vaultflow")
    
    elif is_linux():
        # Linux: $XDG_CONFIG_HOME/vaultflow o ~/.config/vaultflow
        xdg_config = os.getenv('XDG_CONFIG_HOME')
        if xdg_config:
            return os.path.join(xdg_config, "vaultflow")
        return os.path.join(home, ".config", "vaultflow")
    
    else:
        # Fallback para sistemas desconocidos
        return os.path.join(home, ".vaultflow")


def is_git_available() -> bool:
    """
    Verifica si Git está disponible en el sistema.
    
    Returns:
        bool: True si git está instalado y accesible
    """
    return shutil.which("git") is not None


def get_git_command() -> Optional[str]:
    """
    Obtiene la ruta completa del comando git.
    
    Returns:
        Optional[str]: Ruta al ejecutable de git o None si no está disponible
    """
    return shutil.which("git")


def normalize_path(path: str) -> str:
    """
    Normaliza una ruta para que funcione en cualquier plataforma.
    
    Args:
        path: Ruta a normalizar
        
    Returns:
        str: Ruta normalizada
    """
    return os.path.normpath(os.path.expanduser(path))


def get_path_separator() -> str:
    """
    Retorna el separador de rutas del sistema operativo.
    
    Returns:
        str: ';' para Windows, ':' para Unix
    """
    return ';' if is_windows() else ':'


def get_line_ending() -> str:
    """
    Retorna el tipo de salto de línea del sistema operativo.
    
    Returns:
        str: '\r\n' para Windows, '\n' para Unix
    """
    return '\r\n' if is_windows() else '\n'


def open_file_safe(filepath: str, mode: str = 'r', **kwargs):
    """
    Abre un archivo de manera segura con la codificación correcta.
    
    Args:
        filepath: Ruta al archivo
        mode: Modo de apertura
        **kwargs: Argumentos adicionales para open()
        
    Returns:
        File object
    """
    # Asegurar que siempre usamos UTF-8
    if 'encoding' not in kwargs:
        kwargs['encoding'] = 'utf-8'
    
    # En modo texto, manejar saltos de línea de manera universal
    if 'b' not in mode and 'newline' not in kwargs:
        kwargs['newline'] = None  # Python maneja automáticamente \r\n y \n
    
    return open(filepath, mode, **kwargs)


def get_platform_info() -> dict:
    """
    Obtiene información completa sobre la plataforma.
    
    Returns:
        dict: Diccionario con información de la plataforma
    """
    return {
        'system': platform.system(),
        'platform': get_platform(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'python_version': platform.python_version(),
        'is_windows': is_windows(),
        'is_unix': is_unix(),
        'is_macos': is_macos(),
        'is_linux': is_linux(),
        'git_available': is_git_available(),
        'git_path': get_git_command(),
        'config_dir': get_config_dir(),
    }


def verify_system_requirements() -> tuple[bool, list[str]]:
    """
    Verifica que el sistema cumple con los requisitos para ejecutar vaultflow.
    
    Returns:
        tuple[bool, list[str]]: (éxito, lista de mensajes/errores)
    """
    messages = []
    success = True
    
    # Verificar Python
    py_version = sys.version_info
    if py_version < (3, 7):
        success = False
        messages.append(f"❌ Python 3.7+ requerido. Versión actual: {platform.python_version()}")
    else:
        messages.append(f"✓ Python {platform.python_version()}")
    
    # Verificar Git
    if not is_git_available():
        success = False
        messages.append("❌ Git no está instalado o no está en el PATH")
        messages.append("   Instala Git desde: https://git-scm.com/downloads")
    else:
        git_path = get_git_command()
        messages.append(f"✓ Git disponible: {git_path}")
    
    # Información del sistema
    messages.append(f"✓ Sistema operativo: {platform.system()} {platform.release()}")
    
    return success, messages
