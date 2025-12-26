# Changelog de VaultFlow

Todos los cambios notables en este proyecto serán documentados en este archivo.

## [Unreleased] - Compatibilidad Multiplataforma

### ✨ Nuevas Características

#### Soporte Multiplataforma Completo
- **Nuevo módulo `platform_utils.py`**: Sistema completo de detección y adaptación multiplataforma
- **Soporte para Windows, Linux y macOS**: El proyecto ahora funciona nativamente en los tres sistemas operativos principales
- **Detección automática de plataforma**: Detecta el sistema operativo y adapta el comportamiento automáticamente

#### Nuevos Comandos
- **`vaultflow sysinfo`**: Nuevo comando para verificar requisitos del sistema y mostrar información de la plataforma
  - Muestra la versión de Python
  - Verifica disponibilidad de Git
  - Muestra directorios de configuración
  - Informa sobre compatibilidad del sistema

### 🔧 Mejoras

#### Gestión de Rutas Multiplataforma
- **Rutas de configuración adaptadas**:
  - Windows: `%APPDATA%\vaultflow` o `%USERPROFILE%\.vaultflow`
  - macOS: `~/Library/Application Support/vaultflow`
  - Linux: `~/.config/vaultflow` o `$XDG_CONFIG_HOME/vaultflow`

- **Búsqueda inteligente de documentos**:
  - Windows: Documents, Documentos, OneDrive/Documents
  - macOS: Documents, iCloud Drive
  - Linux: Documents, Documentos, $XDG_DOCUMENTS_DIR

#### Manejo de Archivos Mejorado
- **Codificación UTF-8 universal**: Todos los archivos se manejan con UTF-8 de manera consistente
- **Normalización de saltos de línea**: Manejo automático de CRLF (Windows) vs LF (Unix)
- **Función `open_file_safe()`**: Nueva función para abrir archivos de manera segura en todas las plataformas

#### Ejecución de Comandos Git Mejorada
- **Manejo robusto de errores**: Mejor decodificación de salidas de Git en diferentes sistemas
- **Verificación de disponibilidad**: Comprueba que Git esté instalado antes de usarlo
- **Mensajes de error más claros**: Errores específicos por plataforma

### 📝 Archivos Modificados

#### Nuevos Archivos
- `vaultflow/platform_utils.py`: Módulo completo de utilidades multiplataforma
- `docs/CROSS_PLATFORM.md`: Documentación detallada sobre compatibilidad multiplataforma
- `CHANGELOG.md`: Este archivo

#### Archivos Actualizados
- `vaultflow/config.py`: 
  - Usa `get_config_dir()` para rutas de configuración
  - Usa `get_default_documents_paths()` para búsqueda de vaults
  - Usa `open_file_safe()` para operaciones de archivos
  
- `vaultflow/git_utils.py`:
  - Importa funciones de verificación de Git
  - Mejora el manejo de errores en subprocess
  - Decodificación UTF-8 robusta con fallback
  
- `vaultflow/commands.py`:
  - Usa `open_file_safe()` para .gitignore
  - Importa utilidades de plataforma
  - Usa rutas multiplataforma en discover_vaults
  
- `vaultflow/logs.py`:
  - Usa `open_file_safe()` para archivos de log
  
- `vaultflow/cli.py`:
  - Nuevo comando `sysinfo`

### 🐛 Correcciones de Bugs

- **Problemas de codificación en Windows**: Corregidos usando UTF-8 explícito
- **Rutas hardcodeadas**: Eliminadas y reemplazadas con funciones multiplataforma
- **Errores de decodificación en subprocess**: Manejados con fallback 'replace'

### 🧪 Testing

- Verificado funcionamiento en Linux (WSL2)
- Script de prueba creado para validar compatibilidad
- Todos los requisitos del sistema se verifican correctamente

### 📚 Documentación

- **Nueva documentación completa** en `docs/CROSS_PLATFORM.md`:
  - Instrucciones de instalación por plataforma
  - Diferencias entre sistemas operativos
  - Solución de problemas comunes
  - Variables de entorno soportadas
  - Guía de testing multiplataforma

### 🔄 Cambios Internos

#### Funciones Nuevas en `platform_utils.py`
- `get_platform()`: Detecta el sistema operativo
- `is_windows()`, `is_unix()`, `is_linux()`, `is_macos()`: Verificadores de plataforma
- `get_default_documents_paths()`: Rutas de documentos por plataforma
- `get_config_dir()`: Directorio de configuración apropiado
- `is_git_available()`: Verifica disponibilidad de Git
- `get_git_command()`: Obtiene la ruta del ejecutable de Git
- `normalize_path()`: Normaliza rutas multiplataforma
- `open_file_safe()`: Abre archivos con codificación segura
- `get_platform_info()`: Información completa del sistema
- `verify_system_requirements()`: Verifica requisitos

### ⚠️ Cambios de Compatibilidad

- **Sin cambios breaking**: Todas las funcionalidades anteriores se mantienen
- **Mejoras transparentes**: Los usuarios no necesitan cambiar su forma de usar vaultflow
- **Retrocompatible**: Funciona con configuraciones existentes

### 🎯 Próximos Pasos

- [ ] Agregar instaladores nativos (.msi, .deb, .rpm, .dmg)
- [ ] Integración con gestores de credenciales del sistema
- [ ] Notificaciones nativas por plataforma
- [ ] Testing automatizado en GitHub Actions para todas las plataformas
- [ ] Configuración de atajos de teclado específicos por plataforma

---

## [0.1.0] - Versión Inicial

### Características Iniciales
- Gestión Git automatizada
- Sistema de experimentos con ramas
- Backups inteligentes
- Sincronización remota
- Gestión de múltiples vaults
- Interfaz interactiva
- Logging completo
- Gitignore profesional

---

**Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/)**
