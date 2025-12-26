import os
import json
from .platform_utils import get_config_dir, get_default_documents_paths, open_file_safe

CONFIG_DIR = get_config_dir()
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

def _ensure_config_exists():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    if not os.path.exists(CONFIG_FILE):
        with open_file_safe(CONFIG_FILE, 'w') as f:
            json.dump({"managed_vaults": []}, f, indent=4)

def _load_config():
    _ensure_config_exists()
    try:
        with open_file_safe(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"managed_vaults": []} # Si el archivo está corrupto, empezamos de cero

def _save_config(config_data):
    with open_file_safe(CONFIG_FILE, 'w') as f:
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
    """Verifica si el directorio actual está registrado o es un vault válido."""
    current_path = os.path.abspath(os.getcwd())
    
    # Verificar primero en el caché (config.json)
    if current_path in get_managed_vaults():
        return True
    
    # Si no está en el caché, verificar si es un vault válido
    if is_vaultflow_repository(current_path):
        # Auto-registrar vault encontrado
        register_vault(current_path)
        return True
    
    return False

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
        # Verificar si tiene la carpeta .vaultflow con el marcador
        vaultflow_dir = os.path.join(path, '.vaultflow')
        vault_lock_file = os.path.join(vaultflow_dir, 'vault.lock')
        
        # El marcador principal es el archivo vault.lock
        if os.path.exists(vault_lock_file):
            return True
            
        # Fallback: verificar si tiene Git y marcadores legacy
        git_dir = os.path.join(path, '.git')
        if not os.path.exists(git_dir):
            return False
        
        # Verificar marcador legacy en .gitignore (para compatibilidad)
        gitignore_path = os.path.join(path, '.gitignore')
        if os.path.exists(gitignore_path):
            with open_file_safe(gitignore_path, 'r') as f:
                content = f.read()
                if "# === Bloque gestionado por vaultflow ===" in content:
                    return True
        
        return False
        
    except Exception:
        return False

def scan_for_vaultflow_repos(search_paths=None):
    """Escanea directorios especificados buscando repositorios de vaultflow."""
    if search_paths is None:
        # Usar las rutas específicas de cada plataforma
        search_paths = get_default_documents_paths()
    
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

def create_vault_marker(vault_path):
    """Crea el marcador de vault y la estructura .vaultflow."""
    try:
        from datetime import datetime
        
        vaultflow_dir = os.path.join(vault_path, '.vaultflow')
        os.makedirs(vaultflow_dir, exist_ok=True)
        
        # Crear archivo vault.lock como marcador principal
        vault_lock_file = os.path.join(vaultflow_dir, 'vault.lock')
        if not os.path.exists(vault_lock_file):
            lock_data = {
                "created": datetime.now().isoformat(),
                "version": "1.0",
                "vault_name": os.path.basename(vault_path),
                "vault_path": os.path.abspath(vault_path)
            }
            with open_file_safe(vault_lock_file, 'w') as f:
                json.dump(lock_data, f, indent=2)
        
        # Crear archivo de configuración local del vault
        config_file = os.path.join(vaultflow_dir, 'config.json')
        if not os.path.exists(config_file):
            local_config = {
                "vault_name": os.path.basename(vault_path),
                "created": datetime.now().isoformat(),
                "settings": {
                    "auto_backup": True,
                    "backup_frequency": "daily"
                }
            }
            with open_file_safe(config_file, 'w') as f:
                json.dump(local_config, f, indent=2)
        
        return True
    except Exception as e:
        return False

def get_local_vault_dir(vault_path=None):
    """Obtiene la ruta del directorio .vaultflow local."""
    if vault_path is None:
        vault_path = os.getcwd()
    return os.path.join(vault_path, '.vaultflow')

def get_vault_lock_info(vault_path=None):
    """Obtiene información del archivo vault.lock."""
    if vault_path is None:
        vault_path = os.getcwd()
    
    vault_lock_file = os.path.join(vault_path, '.vaultflow', 'vault.lock')
    if not os.path.exists(vault_lock_file):
        return None
    
    try:
        with open_file_safe(vault_lock_file, 'r') as f:
            return json.load(f)
    except:
        return None
