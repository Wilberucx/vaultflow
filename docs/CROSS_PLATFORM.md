# Compatibilidad Multiplataforma de VaultFlow

VaultFlow está diseñado para funcionar de manera transparente en **Windows**, **Linux** y **macOS**.

## Sistemas Operativos Soportados

### ✅ Windows
- Windows 10 y superior
- Windows Server 2016+
- Soporta PowerShell y CMD

### ✅ Linux
- Todas las distribuciones principales (Ubuntu, Debian, Fedora, Arch, etc.)
- Soporta tanto sistemas de escritorio como servidores

### ✅ macOS
- macOS 10.14 (Mojave) y superior
- Compatible con chips Intel y Apple Silicon (M1/M2/M3)

## Requisitos del Sistema

### Requisitos Básicos
- **Python 3.7+** (recomendado 3.9+)
- **Git 2.0+** instalado y disponible en el PATH del sistema

### Verificar Requisitos

Puedes verificar que tu sistema cumple con todos los requisitos ejecutando:

```bash
vaultflow sysinfo
```

Este comando mostrará:
- ✓ Estado de Python y su versión
- ✓ Estado de Git y su ubicación
- ✓ Sistema operativo detectado
- ✓ Directorio de configuración utilizado
- ✓ Detalles de la arquitectura del sistema

## Instalación por Plataforma

### Windows

#### Opción 1: Usando pip (Recomendado)
```powershell
# Desde el directorio del proyecto
pip install -e .
```

#### Opción 2: Instalación de Git
1. Descargar Git desde: https://git-scm.com/download/win
2. Instalar con las opciones por defecto
3. Reiniciar el terminal/PowerShell

#### Opción 3: Python
Si no tienes Python instalado:
1. Descargar desde: https://www.python.org/downloads/
2. **Importante**: Marcar "Add Python to PATH" durante la instalación

### Linux

#### Ubuntu/Debian
```bash
# Instalar dependencias
sudo apt update
sudo apt install python3 python3-pip git

# Instalar vaultflow
cd vaultflow
pip3 install -e .
```

#### Fedora/RHEL/CentOS
```bash
# Instalar dependencias
sudo dnf install python3 python3-pip git

# Instalar vaultflow
cd vaultflow
pip3 install -e .
```

#### Arch Linux
```bash
# Instalar dependencias
sudo pacman -S python python-pip git

# Instalar vaultflow
cd vaultflow
pip install -e .
```

### macOS

#### Usando Homebrew (Recomendado)
```bash
# Instalar Homebrew si no lo tienes
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar dependencias
brew install python git

# Instalar vaultflow
cd vaultflow
pip3 install -e .
```

#### Sin Homebrew
1. Python suele venir preinstalado en macOS, pero puedes descargarlo desde: https://www.python.org/downloads/
2. Git: descargar desde https://git-scm.com/download/mac o usar Xcode Command Line Tools:
```bash
xcode-select --install
```

## Diferencias entre Plataformas

### Rutas de Configuración

VaultFlow utiliza rutas de configuración estándar según la plataforma:

| Plataforma | Ruta de Configuración |
|------------|----------------------|
| **Windows** | `%APPDATA%\vaultflow` o `%USERPROFILE%\.vaultflow` |
| **macOS** | `~/Library/Application Support/vaultflow` |
| **Linux** | `~/.config/vaultflow` o `$XDG_CONFIG_HOME/vaultflow` |

### Rutas de Búsqueda de Vaults

El comando `vaultflow discover` busca automáticamente en ubicaciones estándar:

#### Windows
- `%USERPROFILE%\Documents`
- `%USERPROFILE%\Documentos` (Windows en español)
- `%USERPROFILE%\OneDrive\Documents`
- `%USERPROFILE%` (directorio home)

#### macOS
- `~/Documents`
- `~/Library/Mobile Documents/com~apple~CloudDocs` (iCloud Drive)
- `~` (directorio home)

#### Linux
- `~/Documents`
- `~/Documentos` (sistema en español)
- `$XDG_DOCUMENTS_DIR` (si está configurado)
- `~` (directorio home)

### Codificación de Archivos

VaultFlow maneja automáticamente las diferencias de codificación:
- **Windows**: UTF-8 con BOM cuando es necesario
- **Unix (Linux/macOS)**: UTF-8 sin BOM
- Todos los archivos JSON se guardan con UTF-8

### Saltos de Línea

VaultFlow normaliza automáticamente los saltos de línea:
- **Windows**: CRLF (`\r\n`)
- **Unix (Linux/macOS)**: LF (`\n`)
- Git gestiona automáticamente las conversiones con `core.autocrlf`

## Comandos de Git Multiplataforma

VaultFlow ejecuta comandos de Git de manera consistente en todas las plataformas:

```bash
# Estos comandos funcionan igual en Windows, Linux y macOS
vaultflow init
vaultflow status
vaultflow backup
vaultflow push
```

No es necesario ajustar comandos según la plataforma - VaultFlow maneja las diferencias internamente.

## Problemas Comunes y Soluciones

### Windows

#### "Git no reconocido como comando"
**Solución**: 
1. Reinstalar Git marcando "Add Git to PATH"
2. O agregar manualmente Git al PATH:
   - Buscar "Variables de entorno" en el menú inicio
   - Agregar `C:\Program Files\Git\bin` al PATH

#### "Python no reconocido como comando"
**Solución**: 
1. Reinstalar Python marcando "Add Python to PATH"
2. O usar `py` en lugar de `python`:
```powershell
py -m pip install -e .
```

#### Permisos en PowerShell
Si recibes errores de permisos al ejecutar scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Linux

#### Permisos de pip
Si `pip install` falla por permisos, usa:
```bash
pip3 install --user -e .
```

O instala en un entorno virtual:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

#### Git no instalado
```bash
# Ubuntu/Debian
sudo apt install git

# Fedora
sudo dnf install git

# Arch
sudo pacman -S git
```

### macOS

#### Xcode Command Line Tools requeridas
Si Git no está disponible:
```bash
xcode-select --install
```

#### Problemas con Python del sistema
Es recomendable usar Homebrew para instalar una versión actualizada:
```bash
brew install python@3.11
```

#### Permisos de seguridad
Si macOS bloquea la ejecución, ve a:
Sistema → Privacidad y Seguridad → Permitir

## Testing Multiplataforma

Para ejecutar los tests en tu plataforma:

```bash
# Instalar dependencias de testing
pip install pytest

# Ejecutar tests
pytest tests/

# Con más detalles
pytest -v tests/
```

## Variables de Entorno

VaultFlow respeta las variables de entorno estándar de cada plataforma:

| Variable | Plataforma | Uso |
|----------|-----------|-----|
| `HOME` | Todas | Directorio del usuario |
| `APPDATA` | Windows | Datos de aplicaciones |
| `USERPROFILE` | Windows | Perfil del usuario |
| `XDG_CONFIG_HOME` | Linux | Configuración de usuario |
| `XDG_DOCUMENTS_DIR` | Linux | Directorio de documentos |

## Contribuir a la Compatibilidad

Si encuentras problemas específicos de tu plataforma:

1. Verifica tu configuración con `vaultflow sysinfo`
2. Reporta el issue incluyendo:
   - Sistema operativo y versión
   - Versión de Python (`python --version`)
   - Versión de Git (`git --version`)
   - Salida de `vaultflow sysinfo`
   - Mensaje de error completo

## Próximas Mejoras

Características multiplataforma planificadas:

- [ ] Integración con gestores de credenciales del sistema
- [ ] Notificaciones nativas por plataforma
- [ ] Instaladores nativos (.msi para Windows, .deb/.rpm para Linux, .dmg para macOS)
- [ ] Configuración de atajos de teclado específicos por plataforma
- [ ] Integración con exploradores de archivos nativos

---

**¿Necesitas ayuda?** Ejecuta `vaultflow sysinfo` para verificar tu configuración o abre un issue en GitHub.
