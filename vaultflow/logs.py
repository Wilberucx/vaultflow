import os
import json
from datetime import datetime

LOG_FILE_NAME = ".vaultflow_log.json"

def get_log_file_path():
    """Busca el archivo de log en el directorio actual."""
    return os.path.join(os.getcwd(), LOG_FILE_NAME)

def log_operation(command, message, success=True):
    """Registra una operación en el archivo de log."""
    log_file = get_log_file_path()
    
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = [] # Si el archivo está corrupto, empezamos de nuevo
    else:
        logs = []

    new_entry = {
        "timestamp": datetime.now().isoformat(),
        "command": command,
        "success": success,
        "message": message
    }
    
    logs.insert(0, new_entry)
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=4)