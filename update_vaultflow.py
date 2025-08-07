#!/usr/bin/env python3
"""
Script para actualizar vaultflow en las variables de entorno
desde el repositorio local de desarrollo.

Este script:
1. Instala/reinstala la versión actual del repositorio
2. Actualiza la instalación en las variables de entorno
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Ejecuta un comando y maneja errores."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}")
        print(f"   Error: {e.stderr.strip()}")
        return False

def main():
    """Función principal."""
    print("🚀 Actualizando vaultflow desde el repositorio local...")
    print("=" * 60)
    
    # Verificar que estamos en el directorio correcto
    if not Path("setup.py").exists():
        print("❌ Error: No se encontró setup.py. Ejecuta este script desde el directorio raíz del proyecto.")
        sys.exit(1)
    
    # Desinstalar versión anterior (si existe)
    print("🗑️  Desinstalando versión anterior...")
    subprocess.run(["pip", "uninstall", "vaultflow", "-y"], capture_output=True)
    
    # Instalar versión actual en modo desarrollo
    if not run_command("pip install -e .", "Instalación en modo desarrollo"):
        sys.exit(1)
    
    # Verificar instalación
    if not run_command("vaultflow --help", "Verificación de instalación"):
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 ¡vaultflow actualizado exitosamente!")
    print("💡 La nueva funcionalidad de navegación automática ya está disponible.")
    print("   Pruébala ejecutando 'vaultflow' en un directorio no gestionado.")

if __name__ == "__main__":
    main()
