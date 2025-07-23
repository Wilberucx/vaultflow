# VaultFlow
<img width="1151" height="451" alt="image" src="https://github.com/user-attachments/assets/a032d1d5-1ec1-4485-8148-c8405e5cdc7c" />

Una herramienta CLI moderna y elegante para gestionar tus Vaults de Obsidian con Git de manera profesional y eficiente.

<details>
<summary><strong>Ver Tabla de Contenidos</strong></summary>

- [Características](#características)
- [Instalación](#instalación)
- [Uso Rápido](#uso-rápido)
- [Testing y Desarrollo](#testing-y-desarrollo)
- [Contribuir](#contribuir)
- [Licencia](#licencia)
- [Agradecimientos](#agradecimientos)

</details>

## Características

- **Gestión Git Automatizada**: Inicializa y configura repositorios Git optimizados para Obsidian
- **Sistema de Experimentos**: Crea y gestiona ramas experimentales para probar ideas sin riesgo
- **Backups Inteligentes**: Crea respaldos locales automáticos con timestamps
- **Sincronización Remota**: Push automático con configuración de upstream
- **Interfaz Interactiva**: Menú intuitivo para usuarios que prefieren GUI
- **Logging Completo**: Historial detallado de todas las operaciones
- **Gitignore Profesional**: Configuración automática para ignorar archivos innecesarios

## Instalación

### Desde el código fuente

```bash
git clone https://github.com/Wilberucx/vaultflow.git
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

## Uso Rápido

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
```

## Testing y Desarrollo

Para contribuir al desarrollo de vaultflow o ejecutar la suite de tests localmente, sigue estos pasos.

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

---

**VaultFlow** - Gestiona tus ideas con la potencia de Git y la simplicidad de un click
