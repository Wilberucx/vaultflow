import os
import json

# Define la ruta del directorio y archivo de configuración de vaultflow
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".vaultflow")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

def _ensure_config_exists():
    """Asegura que el directorio y el archivo de configuración existan."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f:
            json.dump({"managed_vaults": []}, f, indent=4)

def _load_config():
    """Carga el archivo de configuración."""
    _ensure_config_exists()
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def _save_config(config_data):
    """Guarda los datos en el archivo de configuración."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config_data, f, indent=4)

def register_vault(vault_path):
    """
    Registra la ruta absoluta de un nuevo vault en la configuración global.
    No añade duplicados.
    """
    config = _load_config()
    abs_path = os.path.abspath(vault_path)
    
    if abs_path not in config["managed_vaults"]:
        config["managed_vaults"].append(abs_path)
        _save_config(config)
        return True
    return False

def is_managed_vault():
    """
    Verifica si el directorio de trabajo actual está registrado como un vault gestionado.
    """
    config = _load_config()
    current_path = os.path.abspath(os.getcwd())
    
    return current_path in config["managed_vaults"]