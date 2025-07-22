# VaultFlow 🌊

Una herramienta CLI moderna y elegante para gestionar tus Vaults de Obsidian con Git de manera profesional y eficiente.

## 🚀 Características

- **Gestión Git Automatizada**: Inicializa y configura repositorios Git optimizados para Obsidian
- **Sistema de Experimentos**: Crea y gestiona ramas experimentales para probar ideas sin riesgo
- **Backups Inteligentes**: Crea respaldos locales automáticos con timestamps
- **Sincronización Remota**: Push automático con configuración de upstream
- **Interfaz Interactiva**: Menú intuitivo para usuarios que prefieren GUI
- **Logging Completo**: Historial detallado de todas las operaciones
- **Gitignore Profesional**: Configuración automática para ignorar archivos innecesarios

## 📦 Instalación

### Desde el código fuente

```bash
git clone https://github.com/tu_usuario/vaultflow.git
cd vaultflow
pip install -e .
```

### Dependencias

- Python 3.7+
- Git
- click
- inquirerpy
- rich
- pyfiglet

## 🎯 Uso Rápido

### Inicializar un Vault

```bash
cd /ruta/a/tu/vault-obsidian
vaultflow init
```

### Comandos Principales

```bash
# Ver estado del vault
vaultflow status

# Crear backup local
vaultflow backup

# Sincronizar con remoto
vaultflow push

# Preparar cambios
vaultflow stage

# Crear commit
vaultflow commit

# Ver historial
vaultflow log

# Modo interactivo
vaultflow
```

### Sistema de Experimentos

```bash
# Iniciar un experimento
vaultflow start-experiment mi-idea

# Finalizar y fusionar experimento
vaultflow finish-experiment mi-idea
```

## 🖥️ Modo Interactivo

Ejecuta `vaultflow` sin argumentos para acceder al menú interactivo:

```
VAULTFLOW

Bienvenido a vaultflow, una herramienta para gestionar tus vaults de Obsidian con Git.

============================================================
? ¿Qué te gustaría hacer?
❯ Ver Estado del Vault
  Crear Backup Local
  Sincronizar con Remoto (Push)
  Iniciar un Nuevo Experimento
  Finalizar un Experimento
  Salir
```

## 🏗️ Arquitectura del Proyecto

```
vaultflow/
├── cli.py          # Interfaz de línea de comandos (Click)
├── commands.py     # Lógica de negocio principal
├── git_utils.py    # Operaciones Git encapsuladas
├── interactive.py  # Menú interactivo (InquirerPy)
├── config.py       # Gestión de configuración
├── logs.py         # Sistema de logging
└── utils.py        # Utilidades generales
```

## ⚙️ Configuración Automática

VaultFlow configura automáticamente:

### Estructura de Ramas
- **main**: Rama principal estable
- **experiment**: Rama base para experimentos
- **exp/[nombre]**: Ramas de experimentos específicos

### Gitignore Inteligente
```gitignore
# Archivos de sistema operativo
.DS_Store
Thumbs.db
Desktop.ini

# Configuraciones de Obsidian
.obsidian/workspace.json
.obsidian/workspaces.json
.obsidian/plugins/*/data.json

# Servicios de sincronización
.dropbox
*.icloud
.stfolder

# VaultFlow
.vaultflow_log.json
```

## 📊 Sistema de Logging

Todas las operaciones se registran en `.vaultflow_log.json`:

```json
[
  {
    "timestamp": "2024-01-15T10:30:00",
    "command": "backup",
    "success": true,
    "message": "Backup vaultflow - 2024-01-15 10:30:00"
  }
]
```

## 🔧 Comandos Detallados

### `vaultflow init`
Inicializa VaultFlow en tu vault:
- Crea/configura repositorio Git
- Establece estructura de ramas
- Configura .gitignore optimizado
- Registra el vault en la configuración

### `vaultflow status`
Muestra el estado actual:
- Rama activa
- Último commit
- Cambios pendientes (staged/modified/untracked)

### `vaultflow backup`
Crea un backup local completo:
- Añade todos los cambios al staging
- Crea commit con timestamp
- Muestra estado actualizado

### `vaultflow push`
Sincroniza con repositorio remoto:
- Configura upstream automáticamente si es necesario
- Maneja errores de conexión
- Reporta estado de la operación

## 🎨 Características Visuales

- **Banner ASCII**: Logo elegante con pyfiglet
- **Colores Rich**: Salida colorizada y formateada
- **Paneles Informativos**: Estado organizado en paneles
- **Indicadores de Estado**: ✓ Éxito, ✗ Error, ! Advertencia

## 🛡️ Validaciones y Seguridad

- Verificación de vault gestionado antes de operaciones
- Validación de nombres de experimentos
- Manejo seguro de conflictos de merge
- Backup automático antes de operaciones críticas

## 📝 Ejemplos de Uso

### Flujo de Trabajo Típico

```bash
# 1. Inicializar vault
cd mi-vault-obsidian
vaultflow init

# 2. Trabajar normalmente en Obsidian
# ... editar notas ...

# 3. Crear backup periódico
vaultflow backup

# 4. Experimentar con una idea
vaultflow start-experiment nueva-estructura

# 5. Trabajar en el experimento
# ... hacer cambios experimentales ...

# 6. Si funciona, fusionar
vaultflow finish-experiment nueva-estructura

# 7. Sincronizar con remoto
vaultflow push
```

### Gestión Multi-Vault

```bash
# VaultFlow recuerda múltiples vaults
cd /ruta/vault-personal
vaultflow init

cd /ruta/vault-trabajo  
vaultflow init

# El menú interactivo permite navegar entre vaults registrados
vaultflow
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🙏 Agradecimientos

- [Obsidian](https://obsidian.md/) - La increíble herramienta de notas
- [Click](https://click.palletsprojects.com/) - Framework CLI elegante
- [Rich](https://rich.readthedocs.io/) - Salida terminal hermosa
- [InquirerPy](https://inquirerpy.readthedocs.io/) - Menús interactivos

---

**VaultFlow** - Gestiona tus ideas con la potencia de Git y la simplicidad de un click 🌊