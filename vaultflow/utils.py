import pyfiglet
from rich.console import Console
from rich.text import Text

def display_banner():
    """
    Muestra un banner ASCII art con el nombre de la herramienta, alineado a la izquierda.
    """
    console = Console()
    banner_text = pyfiglet.figlet_format("VAULTFLOW", font="standard")
    
    # Texto del banner alineado a la izquierda por defecto
    text = Text(banner_text, style="bold magenta")
    
    console.print(text)
