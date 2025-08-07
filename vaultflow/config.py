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

def is_vaultflow_repository(path):
    """Verifica si un directorio es un repositorio gestionado por vaultflow."""
    try:
        # Verificar si tiene Git
        git_dir = os.path.join(path, '.git')
        if not os.path.exists(git_dir):
            return False
            
        # Verificar si tiene .gitignore con header de vaultflow
        gitignore_path = os.path.join(path, '.gitignore')
        if os.path.exists(gitignore_path):
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if "# === Bloque gestionado por vaultflow ===" in content:
                    return True
        
        # Verificar si tiene commits con patron de vaultflow
        import subprocess
        result = subprocess.run(
            ['git', 'log', '--grep=Backup vaultflow', '--oneline', '-1'],
            cwd=path,
            capture_output=True,
            text=True
        )
        return result.returncode == 0 and bool(result.stdout.strip())
        
    except Exception:
        return False

def scan_for_vaultflow_repos(search_paths=None):
    """Escanea directorios comunes buscando repositorios de vaultflow."""
    if search_paths is None:
        home = os.path.expanduser("~")
        search_paths = [
            os.path.join(home, "Documents"),
            os.path.join(home, "Obsidian.Vaults"),  # Obsidian default user home
            os.path.join(home, "vaults"),
            "C:\\Obsidian.Vaults",  # Obsidian default Windows global
            "/Users/Shared/Obsidian.Vaults",  # macOS shared
            "/home/obsidian",  # Linux common
            home  # Home directory itself
        ]
    
    found_vaults = []
    
    for base_path in search_paths:
        if not os.path.exists(base_path):
            continue
            
        # Buscar hasta 3 niveles de profundidad
        for root, dirs, files in os.walk(base_path):
            # Limitar profundidad para evitar escaneos muy lentos
            depth = root[len(base_path):].count(os.sep)
            if depth > 2:
                dirs[:] = []  # No buscar mas profundo
                continue
                
            if is_vaultflow_repository(root):
                found_vaults.append(os.path.abspath(root))
                dirs[:] = []  # No buscar dentro de vaults encontrados
    
    return found_vaults

def cleanup_invalid_vaults():
    """Limpia vaults que ya no existen del archivo de configuración."""
    config = _load_config()
    managed_vaults = config.get("managed_vaults", [])
    
    # Filtrar vaults que aún existen
    valid_vaults = []
    for vault_path in managed_vaults:
        if os.path.exists(vault_path) and is_vaultflow_repository(vault_path):
            valid_vaults.append(vault_path)
    
    # Actualizar configuración si hay cambios
    if len(valid_vaults) != len(managed_vaults):
        config["managed_vaults"] = valid_vaults
        _save_config(config)
        
    return len(managed_vaults) - len(valid_vaults)  # Cantidad eliminada

def auto_discover_and_register_vaults():
    """Auto-descubre vaults y los registra automáticamente."""
    # Limpiar vaults inválidos primero
    cleanup_invalid_vaults()
    
    # Obtener vaults actualmente registrados
    current_vaults = set(get_managed_vaults())
    
    # Escanear por nuevos vaults
    discovered_vaults = scan_for_vaultflow_repos()
    new_vaults = []
    
    for vault_path in discovered_vaults:
        if vault_path not in current_vaults:
            register_vault(vault_path)
            new_vaults.append(vault_path)
    
    return new_vaults
