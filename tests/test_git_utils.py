import os
import subprocess
import pytest
from vaultflow.git_utils import push_changes


def test_push_changes_fails_gracefully_without_remote(tmp_path):
    """Test que verifica que push_changes maneja correctamente la ausencia de un remote."""
    # Setup: Crear un subdirectorio para actuar como nuestro "vault de prueba"
    test_vault_dir = tmp_path / "test_vault"
    test_vault_dir.mkdir()
    
    # Cambiar al directorio de prueba
    original_cwd = os.getcwd()
    os.chdir(test_vault_dir)
    
    try:
        # Inicializar un repositorio Git limpio
        subprocess.run(['git', 'init'], capture_output=True, check=True)
        
        # Acción: Llamar a nuestra función push_changes
        success, message = push_changes()
        
        # Aserción: Verificar el comportamiento esperado
        assert success is False
        assert 'No configured push destination' in message
        
    finally:
        # Cleanup: Restaurar el directorio de trabajo original
        os.chdir(original_cwd)