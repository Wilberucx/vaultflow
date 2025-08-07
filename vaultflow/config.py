import os
import json

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".vaultflow")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

def _ensure_config_exists():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f:
            json.dump({"managed_vaults": []}, f, indent=4)

def _load_config():
    _ensure_config_exists()
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"managed_vaults": []} # Si el archivo está corrupto, empezamos de cero

def _save_config(config_data):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config_data, f, indent=4)

def register_vault(vault_path):
    config = _load_config()
    abs_path = os.path.abspath(vault_path)
    if abs_path not in config["managed_vaults"]:
        config["managed_vaults"].append(abs_path)
        _save_config(config)
    return True

def get_managed_vaults():
    """Devuelve la lista de rutas de los vaults gestionados."""
    config = _load_config()
    return config.get("managed_vaults", [])

def is_managed_vault():
    """Verifica si el directorio actual está registrado."""
    current_path = os.path.abspath(os.getcwd())
    return current_path in get_managed_vaults()

def get_current_vault_info():
    """Obtiene información del vault actual."""
    current_path = os.path.abspath(os.getcwd())
    vault_name = os.path.basename(current_path)
    managed_vaults = get_managed_vaults()
    
    return {
        'name': vault_name,
        'path': current_path,
        'is_managed': current_path in managed_vaults,
        'total_managed_vaults': len(managed_vaults)
    }

def get_vault_name_from_path(path):
    """Extrae el nombre del vault desde su ruta."""
    return os.path.basename(path)
