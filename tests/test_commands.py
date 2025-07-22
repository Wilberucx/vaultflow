import pytest
import subprocess
import os
from vaultflow.commands import initialize_vault, start_experiment


def test_cannot_start_experiment_when_already_in_experiment(tmp_path, capsys):
    """
    Test que verifica que vaultflow impide iniciar un nuevo experimento 
    cuando el usuario ya se encuentra en una rama de experimento.
    """
    # Setup (Preparación del entorno)
    test_dir = tmp_path / "test_vault"
    test_dir.mkdir()
    os.chdir(test_dir)
    
    # Configurar un repositorio vaultflow válido
    initialize_vault()
    
    # Entrar en un estado de experimento inicial
    start_experiment('primer-experimento')
    
    # Acción (Intento de anidamiento)
    start_experiment('segundo-experimento-fallido')
    
    # Aserción (Verificación del resultado)
    captured = capsys.readouterr()
    
    # Verificar que el mensaje de error está presente
    assert 'Error: Ya te encuentras en un experimento' in captured.out
    
    # Verificar que el nombre de la rama del primer experimento está presente
    assert 'exp/primer-experimento' in captured.out
    
    # Verificar que la rama actual sigue siendo exp/primer-experimento
    result = subprocess.run(['git', 'branch', '--show-current'], 
                          capture_output=True, text=True)
    current_branch = result.stdout.strip()
    assert current_branch == 'exp/primer-experimento'