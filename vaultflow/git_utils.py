import os
import subprocess

def is_git_repository():
    """Verifica si el directorio actual es un repositorio de Git."""
    return os.path.isdir('.git')

def git_init():
    try: subprocess.run(['git', 'init'], check=True, capture_output=True); return True
    except: return False

def create_initial_commit():
    try: subprocess.run(['git', 'commit', '--allow-empty', '-m', 'Initial commit by vaultflow'], check=True, capture_output=True); return True
    except: return False

def rename_branch(old, new):
    try: subprocess.run(['git', 'branch', '-m', old, new], check=True, capture_output=True); return True
    except: return False

def branch_exists(name):
    try: return subprocess.run(['git', 'show-ref', '--verify', f'refs/heads/{name}'], check=True, capture_output=True).returncode == 0
    except: return False

def create_branch(name):
    try: subprocess.run(['git', 'branch', name], check=True, capture_output=True); return True
    except: return False

def get_current_branch():
    try: return subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip()
    except: return None

def get_last_commit():
    try: return subprocess.run(['git', 'log', '-1', '--pretty=format:%h - %s'], capture_output=True, text=True, check=True).stdout.strip()
    except: return "No hay commits todavia."

def get_structured_git_status():
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
    except: return None

def stage_all_changes():
    try: subprocess.run(['git', 'add', '.'], check=True, capture_output=True); return True
    except: return False

def commit_changes(message):
    try: subprocess.run(['git', 'commit', '-m', message], check=True, capture_output=True); return True
    except: return False

def push_changes():
    """Intenta un git push, devolviendo el error específico si falla."""
    current_branch = get_current_branch()
    if not current_branch: return False, "No se pudo determinar la rama actual."
    try:
        subprocess.run(['git', 'push'], check=True, capture_output=True)
        return True, "Push exitoso."
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode()
        if 'No configured push destination' in error_msg:
            return False, """No se encontró un repositorio remoto (origin) configurado para este vault.
  Para poder sincronizar, primero debes añadirlo manualmente con:

  git remote add origin URL_DE_TU_REPOSITORIO

  Luego, intenta 'vaultflow push' de nuevo."""
        if 'has no upstream branch' in error_msg:
            try:
                subprocess.run(['git', 'push', '--set-upstream', 'origin', current_branch], check=True, capture_output=True)
                return True, "Se configuro el rastreo remoto y se realizo el push exitosamente."
            except subprocess.CalledProcessError as e2:
                return False, f"Fallo al configurar el upstream: {e2.stderr.decode()}"
        return False, error_msg

def checkout_branch(branch_name):
    """Intenta cambiar de rama, devolviendo el error específico si falla."""
    try:
        subprocess.run(['git', 'checkout', branch_name], check=True, capture_output=True)
        return True, "Checkout exitoso."
    except subprocess.CalledProcessError as e:
        return False, e.stderr.decode()

def merge_branch(branch_name):
    try:
        subprocess.run(['git', 'merge', '--no-ff', branch_name], check=True, capture_output=True)
        return 0, "Fusion completada exitosamente."
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode().lower()
        if 'conflicto' in error_msg or 'conflict' in error_msg:
            subprocess.run(['git', 'merge', '--abort'], check=False, capture_output=True)
            return 1, "Conflicto de fusion detectado. La fusion ha sido abortada."
        return 2, f"Error durante la fusion: {error_msg}"

def delete_branch(branch_name):
    try: subprocess.run(['git', 'branch', '-d', branch_name], check=True, capture_output=True); return True
    except: return False

def get_backup_commits(limit=10):
    """Obtiene los últimos commits que son backups de vaultflow."""
    try:
        result = subprocess.run(
            ['git', 'log', '--grep=Backup vaultflow', f'-{limit}', '--pretty=format:%h|%s|%ad', '--date=short'],
            capture_output=True, text=True, check=True
        )
        if not result.stdout.strip():
            return []
        
        backups = []
        for line in result.stdout.strip().split('\n'):
            parts = line.split('|', 2)
            if len(parts) == 3:
                hash_val, message, date = parts
                backups.append({
                    'hash': hash_val,
                    'message': message,
                    'date': date
                })
        return backups
    except:
        return []

def checkout_commit(commit_hash):
    """Hace checkout a un commit específico."""
    try:
        subprocess.run(['git', 'checkout', commit_hash], check=True, capture_output=True)
        return True, f"Cambiado a commit {commit_hash}"
    except subprocess.CalledProcessError as e:
        return False, e.stderr.decode()
