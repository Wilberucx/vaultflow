# VaultFlow
<img width="1151" height="451" alt="image" src="https://github.com/user-attachments/assets/a032d1d5-1ec1-4485-8148-c8405e5cdc7c" />

Una herramienta CLI moderna y elegante para gestionar tus Vaults de Obsidian con Git de manera profesional y eficiente.

> 🌍 **Multiplataforma:** VaultFlow funciona perfectamente en Windows, Linux y macOS.

<details>
<summary><strong>Ver Tabla de Contenidos</strong></summary>

- [Características](#características)
- [Compatibilidad Multiplataforma](#compatibilidad-multiplataforma)
- [Instalación](#instalación)
- [Uso Rápido](#uso-rápido)
- [Testing y Desarrollo](#testing-y-desarrollo)
- [Contribuir](#contribuir)
- [Licencia](#licencia)
- [Agradecimientos](#agradecimientos)

</details>

## Características

- **🌍 Multiplataforma**: Funciona perfectamente en Windows, Linux y macOS
- **Gestión Git Automatizada**: Inicializa y configura repositorios Git optimizados para Obsidian
- **Sistema de Experimentos**: Crea y gestiona ramas experimentales para probar ideas sin riesgo
- **Backups Inteligentes**: Crea respaldos locales automáticos con timestamps
- **Sincronización Remota**: Push automático con configuración de upstream
- **Gestión de Múltiples Vaults**: Administra varios vaults desde cualquier ubicación
- **Navegación Automática**: Cambia automáticamente entre vaults sin salir de la herramienta
- **Auto-recuperación**: Detecta y restaura vaults existentes automáticamente
- **Interfaz Interactiva**: Menú intuitivo para usuarios que prefieren GUI
- **Logging Completo**: Historial detallado de todas las operaciones
- **Gitignore Profesional**: Configuración automática para ignorar archivos innecesarios
- **Detección Automática**: Encuentra y registra vaults en ubicaciones estándar de tu sistema
- **Verificación de Sistema**: Comando `sysinfo` para verificar requisitos y compatibilidad

## Compatibilidad Multiplataforma

VaultFlow está diseñado para funcionar de manera transparente en los tres principales sistemas operativos:

### ✅ Sistemas Operativos Soportados

| Sistema | Estado | Notas |
|---------|--------|-------|
| **Windows 10/11** | ✅ Soportado | PowerShell, CMD, Git Bash |
| **Linux** | ✅ Soportado | Todas las distribuciones principales |
| **macOS** | ✅ Soportado | Intel y Apple Silicon (M1/M2/M3) |

### 🔍 Características Multiplataforma

- **Detección automática de plataforma**: VaultFlow detecta tu sistema operativo y adapta su comportamiento
- **Rutas inteligentes**: Usa ubicaciones estándar según tu sistema (Documents, AppData, Library, etc.)
- **Codificación UTF-8 universal**: Maneja correctamente caracteres especiales en todas las plataformas
- **Verificación de requisitos**: Comando `vaultflow sysinfo` para verificar que tu sistema es compatible

### 📁 Ubicaciones de Configuración

VaultFlow usa directorios estándar según tu sistema operativo:

| Sistema | Ubicación de Configuración |
|---------|----------------------------|
| **Windows** | `%APPDATA%\vaultflow` |
| **macOS** | `~/Library/Application Support/vaultflow` |
| **Linux** | `~/.config/vaultflow` |

### 📚 Documentación Adicional

Para información detallada sobre compatibilidad multiplataforma:
- [Guía de Compatibilidad Multiplataforma](docs/CROSS_PLATFORM.md)
- [Guía de Migración](docs/MIGRATION_GUIDE.md)
- [Ejemplos por Plataforma](docs/PLATFORM_EXAMPLES.md)

## Instalación

### Requisitos del Sistema

- **Python 3.7 o superior** (recomendado 3.9+)
- **Git 2.0 o superior**

### Verificar Requisitos

Antes de instalar, verifica que tu sistema cumple con los requisitos:

```bash
# Verificar Python
python --version  # o python3 --version en Linux/macOS

# Verificar Git
git --version
```

### Instalación por Plataforma

#### 🪟 Windows

```powershell
# 1. Asegúrate de tener Python y Git instalados
# Python: https://www.python.org/downloads/
# Git: https://git-scm.com/download/win

# 2. Clonar e instalar VaultFlow
git clone https://github.com/Wilberucx/vaultflow.git
cd vaultflow
pip install -e .

# 3. Verificar instalación
vaultflow sysinfo
```

#### 🐧 Linux

**Ubuntu/Debian:**
```bash
# 1. Instalar dependencias
sudo apt update
sudo apt install python3 python3-pip git

# 2. Clonar e instalar VaultFlow
git clone https://github.com/Wilberucx/vaultflow.git
cd vaultflow
pip3 install -e .

# 3. Verificar instalación
vaultflow sysinfo
```

**Fedora/RHEL:**
```bash
# 1. Instalar dependencias
sudo dnf install python3 python3-pip git

# 2. Clonar e instalar VaultFlow
git clone https://github.com/Wilberucx/vaultflow.git
cd vaultflow
pip3 install -e .

# 3. Verificar instalación
vaultflow sysinfo
```

**Arch Linux:**
```bash
# 1. Instalar dependencias
sudo pacman -S python python-pip git

# 2. Clonar e instalar VaultFlow
git clone https://github.com/Wilberucx/vaultflow.git
cd vaultflow
pip install -e .

# 3. Verificar instalación
vaultflow sysinfo
```

#### 🍎 macOS

```bash
# 1. Instalar Homebrew si no lo tienes
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Instalar dependencias
brew install python git

# 3. Clonar e instalar VaultFlow
git clone https://github.com/Wilberucx/vaultflow.git
cd vaultflow
pip3 install -e .

# 4. Verificar instalación
vaultflow sysinfo
```

### Dependencias de Python

VaultFlow instala automáticamente las siguientes dependencias:

- Python 3.7+
- Git
- click
- inquirerpy
- rich
- pyfiglet

## Uso Rápido

### Primer Uso

Después de instalar, verifica que todo funciona correctamente:

```bash
# Verificar que VaultFlow está instalado correctamente
vaultflow sysinfo
```

Este comando mostrará:
- ✓ Versión de Python
- ✓ Disponibilidad de Git
- ✓ Sistema operativo detectado
- ✓ Directorio de configuración
- ✓ Arquitectura del sistema

### Inicializar un Vault

```bash
cd /ruta/a/tu/vault-obsidian
vaultflow init
```

### Comandos Principales

```bash
# Verificar sistema (NUEVO)
vaultflow sysinfo

# Ver estado del vault actual
vaultflow status

# Crear backup local
vaultflow backup

# Sincronizar con remoto
vaultflow push

# Ver todos los vaults gestionados
vaultflow vaults

# Ver backups disponibles
vaultflow backups

# Auto-descubrir vaults existentes (NUEVO)
vaultflow discover

# Ver historial de operaciones
vaultflow log

# Modo interactivo (menú visual)
vaultflow
```

### Sistema de Experimentos

```bash
# Iniciar un experimento (crea rama exp/nombre)
vaultflow start-experiment "nombre-experimento"

# Trabajar en tu experimento...
# Los cambios se guardan en la rama experimental

# Finalizar experimento y fusionar con main
vaultflow finish-experiment "nombre-experimento"
```

### Gestión de Múltiples Vaults

VaultFlow puede gestionar múltiples vaults de Obsidian de manera eficiente:

#### Navegación Automática
Si ejecutas `vaultflow` desde un directorio que no está gestionado, la herramienta:
- Detectará automáticamente tus vaults existentes
- Te permitirá seleccionar a cuál quieres ir
- Cambiará automáticamente al directorio del vault seleccionado
- Lanzará el menú interactivo desde allí

```bash
# Desde cualquier directorio
vaultflow
# → Selecciona un vault → Navega automáticamente → Menú interactivo
```

#### Comandos de Gestión

```bash
# Listar todos los vaults gestionados
vaultflow vaults
# Muestra: nombre, ubicación, y vault actual marcado

# Ver información detallada del vault actual
vaultflow status
# Incluye: backups recientes, cantidad de vaults, y estado git

# Explorar backups del vault actual
vaultflow backups
# Lista backups con instrucciones para navegar entre ellos
```

#### Auto-recuperación
Si pierdes tu configuración o instalas vaultflow en una nueva máquina:

```bash
# Busca automáticamente vaults existentes
vaultflow discover
```

Esto buscará en ubicaciones comunes y detectará vaults basándose en:
- Presencia de repositorio Git
- Archivo `.gitignore` con marcadores de vaultflow
- Historial de commits con patrones de backup de vaultflow

#### Flujo de Trabajo Recomendado

1. **Configuración inicial**: `vaultflow init` en cada vault
2. **Uso diario**: Ejecuta `vaultflow` desde cualquier lugar
3. **Cambio entre vaults**: Selecciona desde el menú o usa `vaultflow vaults`
4. **Recuperación**: Si pierdes configuración, usa `vaultflow discover`

## Testing y Desarrollo

Para contribuir al desarrollo de vaultflow o ejecutar la suite de tests localmente, sigue estos pasos.

### Instalación para Usuarios Finales

> ⚠️ **Nota**: vaultflow no está disponible en PyPI aún. Por ahora, solo se puede instalar desde el código fuente.

Los usuarios finales pueden instalar vaultflow directamente desde GitHub:

```bash
# Instalar la última versión desde GitHub
pip install git+https://github.com/Wilberucx/vaultflow.git

# Para actualizar a la última versión
pip install --upgrade git+https://github.com/Wilberucx/vaultflow.git
```

### 1. Configuración del Entorno

Es altamente recomendable utilizar un entorno virtual para aislar las dependencias del proyecto.

```bash
# Navega a la raíz del proyecto
cd vaultflow

# Crea un entorno virtual
python -m venv venv

# Activa el entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### 2. Instalación de Dependencias

Una vez activado el entorno virtual, instala el proyecto en "modo editable" junto con las dependencias de desarrollo (como pytest). Esto se hace con la opción `[test]`.

```bash
pip install -e ".[test]"
```

Este comando instala todas las dependencias necesarias para usar la herramienta y, además, las herramientas para ejecutar la suite de tests.

### 3. Ejecución de los Tests

Con las dependencias instaladas, puedes ejecutar la suite completa de tests automatizados con un simple comando:

```bash
pytest
```

Una salida exitosa mostrará un listado de los tests ejecutados y finalizará con un mensaje de "passed" en verde.

### 4. Script de Actualización para Desarrolladores

Para desarrolladores que trabajan con el código fuente y necesitan actualizar frecuentemente su instalación local de vaultflow, existe un script de conveniencia:

```bash
# Desde el directorio raíz del proyecto
python update_vaultflow.py
```

Este script:
- Desinstala automáticamente la versión anterior de vaultflow
- Reinstala la versión actual en modo desarrollo (`pip install -e .`)
- Verifica que la instalación fue exitosa
- Muestra información sobre las nuevas funcionalidades disponibles

> 📝 **Nota para desarrolladores**: Este script solo funciona si tienes el código fuente clonado localmente. Los usuarios finales deben usar las instrucciones de instalación desde GitHub mencionadas arriba.

### 5. Flujo de Desarrollo Recomendado

```bash
# 1. Clonar y configurar
git clone https://github.com/Wilberucx/vaultflow.git
cd vaultflow
python -m venv venv

# 2. Activar entorno virtual
# En Linux/macOS:
source venv/bin/activate

# En Windows PowerShell:
venv\Scripts\Activate.ps1

# En Windows CMD:
venv\Scripts\activate.bat

# 3. Instalación inicial
pip install -e ".[test]"

# 4. Verificar instalación
vaultflow sysinfo

# 5. Después de hacer cambios
python update_vaultflow.py  # Actualizar instalación
pytest                     # Ejecutar tests

# 6. Probar funcionalmente
vaultflow --help           # Verificar que funciona
```

### Testing Multiplataforma

Para probar en diferentes plataformas, consulta:
- [Checklist de Testing](docs/TESTING_CHECKLIST.md) - Guía completa de testing
- [Ejemplos por Plataforma](docs/PLATFORM_EXAMPLES.md) - Casos de uso específicos

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## Agradecimientos

- [Obsidian](https://obsidian.md/) - La increíble herramienta de notas
- [Click](https://click.palletsprojects.com/) - Framework CLI elegante
- [Rich](https://rich.readthedocs.io/) - Salida terminal hermosa
- [InquirerPy](https://inquirerpy.readthedocs.io/) - Menús interactivos

## Documentación Completa

### Guías de Usuario
- [README.md](README.md) - Este documento
- [Compatibilidad Multiplataforma](docs/CROSS_PLATFORM.md) - Guía detallada de compatibilidad
- [Guía de Migración](docs/MIGRATION_GUIDE.md) - Cómo migrar desde versiones anteriores
- [Ejemplos por Plataforma](docs/PLATFORM_EXAMPLES.md) - Ejemplos específicos para Windows, Linux y macOS

### Guías de Desarrollo
- [Checklist de Testing](docs/TESTING_CHECKLIST.md) - Cómo probar VaultFlow
- [CHANGELOG.md](CHANGELOG.md) - Historial de cambios
- [Resumen de Portabilidad](PORTABILITY_SUMMARY.md) - Resumen técnico de la implementación multiplataforma

---

**VaultFlow** - Gestiona tus ideas con la potencia de Git y la simplicidad de un click 🌍
