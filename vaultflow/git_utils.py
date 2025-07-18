import os
import subprocess

def is_git_repository():
    """Verifica si el directorio actual es un repositorio de Git."""
    return os.path.isdir('.git')

def git_init():
    """Ejecuta 'git init'."""
    try:
        subprocess.run(['git', 'init'], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def create_initial_commit():
    """Crea un commit inicial vacio."""
    try:
        subprocess.run(['git', 'commit', '--allow-empty', '-m', 'Initial commit by vaultflow'], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def rename_branch(old_name, new_name):
    """Renombra una rama de Git."""
    try:
        subprocess.run(['git', 'branch', '-m', old_name, new_name], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def branch_exists(branch_name):
    """Verifica si una rama especifica existe."""
    try:
        result = subprocess.run(['git', 'show-ref', '--verify', f'refs/heads/{branch_name}'], check=True, capture_output=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False

def create_branch(branch_name):
    """Crea una nueva rama."""
    try:
        subprocess.run(['git', 'branch', branch_name], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_current_branch():
    """Obtiene el nombre de la rama actual de Git."""
    try:
        result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def get_last_commit():
    """Obtiene el ultimo commit en formato 'hash - mensaje'."""
    try:
        result = subprocess.run(['git', 'log', '-1', '--pretty=format:%h - %s'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "No hay commits todavia."

def get_structured_git_status():
    """Obtiene el estado de Git y lo clasifica."""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        if not output: return None
        status_map = {'staged': [], 'modified': [], 'untracked': []}
        for line in output.split('\n'):
            if not line: continue
            code, path = line[:2], line[3:]
            if code.startswith('??'): status_map['untracked'].append(path)
            else:
                if code[0] in ('A', 'M', 'D', 'R', 'C'): status_map['staged'].append(line.strip())
                if code[1] == 'M': status_map['modified'].append(line.strip())
        return status_map if any(status_map.values()) else None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def stage_all_changes():
    """Ejecuta 'git add .'."""
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def commit_changes(message):
    """Ejecuta 'git commit' con un mensaje."""
    try:
        subprocess.run(['git', 'commit', '-m', message], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False