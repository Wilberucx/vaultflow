# Guía de Migración a VaultFlow Multiplataforma

Esta guía te ayudará a entender los cambios realizados para hacer VaultFlow compatible con Windows, Linux y macOS.

## 🎯 Resumen de Cambios

VaultFlow ahora es **completamente multiplataforma**. Si anteriormente usabas VaultFlow solo en Windows, ahora puedes usarlo en Linux y macOS sin ningún cambio en tu flujo de trabajo.

## ✅ ¿Necesito Hacer Algo?

**No, en la mayoría de los casos.** Los cambios son transparentes para los usuarios existentes:

- ✓ Tus vaults existentes seguirán funcionando
- ✓ Tu configuración existente se respeta
- ✓ Todos los comandos funcionan igual
- ✓ No hay cambios en la sintaxis

## 🔄 Cambios Automáticos

### Ubicación de Configuración

VaultFlow ahora usa ubicaciones estándar según tu sistema operativo:

**Antes (todas las plataformas):**
```
~/.vaultflow/config.json
```

**Ahora:**

| Sistema | Ubicación Nueva |
|---------|----------------|
| **Windows** | `%APPDATA%\vaultflow\config.json` |
| **macOS** | `~/Library/Application Support/vaultflow/config.json` |
| **Linux** | `~/.config/vaultflow/config.json` |

### ¿Qué Pasa con Mi Configuración Antigua?

VaultFlow detecta automáticamente configuraciones en la ubicación antigua (`~/.vaultflow`) y las respeta. No necesitas mover nada manualmente.

Si quieres migrar a la nueva ubicación:

**En Linux:**
```bash
# Si tienes configuración en ~/.vaultflow
mkdir -p ~/.config/vaultflow
cp ~/.vaultflow/config.json ~/.config/vaultflow/config.json
```

**En macOS:**
```bash
# Si tienes configuración en ~/.vaultflow
mkdir -p ~/Library/Application\ Support/vaultflow
cp ~/.vaultflow/config.json ~/Library/Application\ Support/vaultflow/config.json
```

**En Windows (PowerShell):**
```powershell
# Si tienes configuración en %USERPROFILE%\.vaultflow
New-Item -ItemType Directory -Force -Path "$env:APPDATA\vaultflow"
Copy-Item "$env:USERPROFILE\.vaultflow\config.json" "$env:APPDATA\vaultflow\config.json"
```

## 🆕 Nuevas Características

### Comando `sysinfo`

Nuevo comando para verificar la compatibilidad de tu sistema:

```bash
vaultflow sysinfo
```

Esto muestra:
- ✓ Versión de Python instalada
- ✓ Disponibilidad de Git
- ✓ Sistema operativo detectado
- ✓ Directorio de configuración en uso
- ✓ Arquitectura del sistema

### Búsqueda Inteligente de Vaults

El comando `vaultflow discover` ahora busca en ubicaciones específicas de tu plataforma:

**Windows:**
- Documents/Documentos
- OneDrive/Documents
- Directorio home

**macOS:**
- Documents
- iCloud Drive
- Directorio home

**Linux:**
- Documents/Documentos
- $XDG_DOCUMENTS_DIR
- Directorio home

## 🔧 Para Desarrolladores

### Importaciones Nuevas

Si estás contribuyendo al proyecto, hay un nuevo módulo:

```python
from vaultflow.platform_utils import (
    get_platform,
    is_windows,
    is_unix,
    is_linux,
    is_macos,
    get_config_dir,
    get_default_documents_paths,
    open_file_safe,
    is_git_available,
    verify_system_requirements,
    get_platform_info
)
```

### Uso de `open_file_safe()`

Para abrir archivos de manera segura en todas las plataformas:

```python
# Antes
with open('archivo.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Ahora (recomendado)
from vaultflow.platform_utils import open_file_safe

with open_file_safe('archivo.json', 'r') as f:
    data = json.load(f)
```

Esta función:
- ✓ Usa UTF-8 por defecto
- ✓ Maneja saltos de línea automáticamente
- ✓ Es consistente en todas las plataformas

### Verificación de Git

Antes de usar comandos de Git:

```python
from vaultflow.platform_utils import is_git_available

if not is_git_available():
    raise RuntimeError("Git no está instalado")
```

## 🐛 Problemas Conocidos Resueltos

### ✅ Codificación UTF-8
**Antes:** Podía haber problemas con caracteres especiales en Windows.  
**Ahora:** UTF-8 funciona correctamente en todas las plataformas.

### ✅ Rutas Hardcodeadas
**Antes:** `~/Documents` estaba hardcodeado.  
**Ahora:** Se usan rutas específicas de cada plataforma.

### ✅ Saltos de Línea
**Antes:** Podía haber inconsistencias entre Windows (CRLF) y Unix (LF).  
**Ahora:** Manejados automáticamente.

### ✅ Errores de Subprocess
**Antes:** Errores al decodificar salidas de Git en algunos sistemas.  
**Ahora:** Decodificación robusta con fallback.

## 📦 Instalación en Nuevas Plataformas

### Si Eras Usuario de Windows y Ahora Usas Linux/macOS

1. Instala las dependencias del sistema:

**Ubuntu/Debian:**
```bash
sudo apt install python3 python3-pip git
```

**macOS (con Homebrew):**
```bash
brew install python git
```

2. Instala VaultFlow:
```bash
cd vaultflow
pip3 install -e .
```

3. (Opcional) Copia tu configuración antigua si la tienes.

### Si Eras Usuario de Linux/macOS y Ahora Usas Windows

1. Instala Python: https://www.python.org/downloads/
   - ⚠️ Marca "Add Python to PATH"

2. Instala Git: https://git-scm.com/download/win

3. Instala VaultFlow:
```powershell
cd vaultflow
pip install -e .
```

## 🧪 Verificación Post-Migración

Después de actualizar VaultFlow, verifica que todo funciona:

```bash
# 1. Verificar requisitos del sistema
vaultflow sysinfo

# 2. Ver tus vaults registrados
vaultflow vaults

# 3. (Opcional) Buscar vaults automáticamente
vaultflow discover

# 4. Verificar status en un vault
cd /ruta/a/tu/vault
vaultflow status
```

## 📞 ¿Necesitas Ayuda?

Si encuentras problemas durante la migración:

1. Ejecuta `vaultflow sysinfo` y guarda la salida
2. Verifica la documentación en `docs/CROSS_PLATFORM.md`
3. Abre un issue en GitHub incluyendo:
   - Sistema operativo y versión
   - Salida de `vaultflow sysinfo`
   - Descripción del problema
   - Mensaje de error completo

## 🎉 ¡Eso es Todo!

VaultFlow ahora funciona perfectamente en Windows, Linux y macOS. Disfruta de la libertad de usar tus vaults de Obsidian en cualquier plataforma.

---

**Documentación relacionada:**
- [Compatibilidad Multiplataforma](CROSS_PLATFORM.md)
- [Changelog](../CHANGELOG.md)
- [README Principal](../README.md)
