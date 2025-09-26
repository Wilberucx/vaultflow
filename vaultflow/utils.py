# Intentamos importar pyfiglet para usarlo como respaldo si no hay logo estático
try:
    import pyfiglet  # type: ignore
except Exception:
    pyfiglet = None  # Fallback si pyfiglet no está disponible

from rich.console import Console
from rich.text import Text

# Logo ASCII estático. Reemplázalo con tu arte ASCII preferido.
# Ejemplo:
# ASCII_LOGO = r"""
# __     __     _ _   _ _             
# \ \   / /___ | | |_(_) | ___  _ __  
#  \ \ / / _ \| | __| | |/ _ \| '_ \ 
#   \ V / (_) | | |_| | | (_) | | | |
#    \_/ \___/|_|\__|_|_|\___/|_| |_|
# """
ASCII_LOGO = r"""
██╗   ██╗ █████╗ ██╗   ██╗██╗  ████████╗███████╗██╗      ██████╗ ██╗    ██╗
██║   ██║██╔══██╗██║   ██║██║  ╚══██╔══╝██╔════╝██║     ██╔═══██╗██║    ██║
██║   ██║███████║██║   ██║██║     ██║   █████╗  ██║     ██║   ██║██║ █╗ ██║
╚██╗ ██╔╝██╔══██║██║   ██║██║     ██║   ██╔══╝  ██║     ██║   ██║██║███╗██║
 ╚████╔╝ ██║  ██║╚██████╔╝███████╗██║   ██║     ███████╗╚██████╔╝╚███╔███╔╝
  ╚═══╝  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝ 
                                                                           
"""

def _generate_banner_text() -> str:
    """Decide qué banner mostrar: estático, pyfiglet o un texto simple."""
    static = ASCII_LOGO.strip("\n")
    if static.strip():
        return static
    if pyfiglet is not None:
        try:
            return pyfiglet.figlet_format("VAULTFLOW", font="standard")
        except Exception:
            pass
    return "VAULTFLOW"


def display_banner():
    """
    Muestra un banner ASCII art con el nombre de la herramienta, alineado a la izquierda.
    """
    console = Console()
    banner_text = _generate_banner_text()

    # Texto del banner alineado a la izquierda por defecto
    text = Text(banner_text, style="bold magenta")

    console.print(text)
