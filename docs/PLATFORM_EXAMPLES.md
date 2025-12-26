# Ejemplos Prácticos por Plataforma

Esta guía contiene ejemplos específicos de cómo usar VaultFlow en diferentes sistemas operativos.

---

## 🪟 Windows

### Instalación

```powershell
# PowerShell - Instalación básica
cd C:\Users\TuUsuario\Projects\vaultflow
pip install -e .

# Verificar instalación
vaultflow sysinfo
```

### Rutas Típicas de Vaults

```powershell
# Vault en Documents
cd "C:\Users\TuUsuario\Documents\MiVault"
vaultflow init

# Vault en OneDrive
cd "C:\Users\TuUsuario\OneDrive\Documents\ObsidianVault"
vaultflow init

# Vault personalizado
cd "D:\Obsidian\MyVault"
vaultflow init
```

### Comandos Comunes

```powershell
# Ver información del sistema
vaultflow sysinfo

# Buscar vaults automáticamente
vaultflow discover

# Crear un backup
cd "C:\Users\TuUsuario\Documents\MiVault"
vaultflow backup

# Ver estado
vaultflow status

# Iniciar experimento
vaultflow start-experiment "nueva-idea"

# Finalizar experimento
vaultflow finish-experiment "nueva-idea"

# Sincronizar con remoto
vaultflow push
```

### Variables de Entorno (PowerShell)

```powershell
# Ver directorio de configuración
Write-Host $env:APPDATA\vaultflow

# Ver perfil de usuario
Write-Host $env:USERPROFILE

# Cambiar temporalmente la ubicación de config (avanzado)
$env:VAULTFLOW_CONFIG = "D:\MiConfigVaultflow"
```

### Configurar Git (Primera vez)

```powershell
# Configurar identidad de Git
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# Ver configuración actual
git config --global --list

# Configurar editor preferido
git config --global core.editor "code --wait"  # VS Code
# O
git config --global core.editor "notepad"  # Notepad
```

### Solución de Problemas en Windows

```powershell
# Si Git no se reconoce
# Opción 1: Reinstalar Git y marcar "Add to PATH"
# Opción 2: Agregar manualmente al PATH
$env:Path += ";C:\Program Files\Git\bin"

# Si Python no se reconoce
# Usar el launcher de Python
py -m pip install -e .
py -m vaultflow.cli sysinfo

# Permisos de ejecución en PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🐧 Linux

### Instalación

#### Ubuntu/Debian
```bash
# Instalar dependencias
sudo apt update
sudo apt install python3 python3-pip git

# Instalar VaultFlow
cd ~/Projects/vaultflow
pip3 install -e .

# O usar entorno virtual (recomendado)
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Verificar instalación
vaultflow sysinfo
```

#### Fedora/RHEL
```bash
# Instalar dependencias
sudo dnf install python3 python3-pip git

# Instalar VaultFlow
cd ~/Projects/vaultflow
pip3 install -e .

# Verificar instalación
vaultflow sysinfo
```

#### Arch Linux
```bash
# Instalar dependencias
sudo pacman -S python python-pip git

# Instalar VaultFlow
cd ~/Projects/vaultflow
pip install -e .

# Verificar instalación
vaultflow sysinfo
```

### Rutas Típicas de Vaults

```bash
# Vault en Documents
cd ~/Documents/MiVault
vaultflow init

# Vault en home
cd ~/ObsidianVault
vaultflow init

# Vault en ubicación personalizada
cd /data/vaults/MyVault
vaultflow init

# Vault con espacios en el nombre (usar comillas)
cd ~/Documents/"Mi Vault de Obsidian"
vaultflow init
```

### Comandos Comunes

```bash
# Ver información del sistema
vaultflow sysinfo

# Buscar vaults automáticamente
vaultflow discover

# Crear un backup
cd ~/Documents/MiVault
vaultflow backup

# Ver estado
vaultflow status

# Usar el modo interactivo
vaultflow

# Ver logs
vaultflow log

# Ver backups disponibles
vaultflow backups

# Listar todos los vaults gestionados
vaultflow vaults
```

### Alias Útiles (añadir a ~/.bashrc o ~/.zshrc)

```bash
# Alias para vaultflow
alias vf='vaultflow'
alias vfs='vaultflow status'
alias vfb='vaultflow backup'
alias vfp='vaultflow push'
alias vfi='vaultflow'  # Modo interactivo

# Función para cambiar rápidamente a un vault
vault() {
    if [ -z "$1" ]; then
        vaultflow vaults
    else
        cd "$1" && vaultflow status
    fi
}

# Recargar el archivo
source ~/.bashrc  # o source ~/.zshrc
```

### Configurar Git (Primera vez)

```bash
# Configurar identidad de Git
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# Ver configuración actual
git config --global --list

# Configurar editor preferido
git config --global core.editor "nano"  # Nano
# O
git config --global core.editor "vim"   # Vim
# O
git config --global core.editor "code --wait"  # VS Code
```

### Permisos y Seguridad

```bash
# Ver permisos del directorio de configuración
ls -la ~/.config/vaultflow

# Asegurar que solo tu usuario puede acceder
chmod 700 ~/.config/vaultflow

# Ver permisos de un vault
ls -la ~/Documents/MiVault
```

### Solución de Problemas en Linux

```bash
# Si pip install falla por permisos
pip3 install --user -e .

# O usar entorno virtual
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Si Git no está instalado
sudo apt install git  # Ubuntu/Debian
sudo dnf install git  # Fedora
sudo pacman -S git    # Arch

# Verificar que vaultflow está en el PATH
which vaultflow

# Si no está en PATH, agregar al ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

## 🍎 macOS

### Instalación

#### Con Homebrew (Recomendado)
```bash
# Instalar Homebrew si no lo tienes
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar dependencias
brew install python git

# Instalar VaultFlow
cd ~/Projects/vaultflow
pip3 install -e .

# Verificar instalación
vaultflow sysinfo
```

#### Sin Homebrew
```bash
# Instalar Xcode Command Line Tools (incluye Git)
xcode-select --install

# Python suele venir preinstalado, pero puedes descargarlo de python.org

# Instalar VaultFlow
cd ~/Projects/vaultflow
pip3 install -e .

# Verificar instalación
vaultflow sysinfo
```

### Rutas Típicas de Vaults

```bash
# Vault en Documents
cd ~/Documents/MiVault
vaultflow init

# Vault en iCloud Drive
cd ~/Library/Mobile\ Documents/com~apple~CloudDocs/Obsidian/MiVault
vaultflow init

# O de forma más corta
cd ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/MiVault
vaultflow init

# Vault en Desktop
cd ~/Desktop/ObsidianVault
vaultflow init
```

### Comandos Comunes

```bash
# Ver información del sistema
vaultflow sysinfo

# Buscar vaults automáticamente
vaultflow discover

# Crear un backup
cd ~/Documents/MiVault
vaultflow backup

# Ver estado
vaultflow status

# Modo interactivo con menú visual
vaultflow

# Push a remoto
vaultflow push
```

### Alias Útiles (añadir a ~/.zshrc o ~/.bash_profile)

```bash
# Alias para vaultflow
alias vf='vaultflow'
alias vfs='vaultflow status'
alias vfb='vaultflow backup'
alias vfp='vaultflow push'

# Función para abrir vault en Obsidian
obsidian-vault() {
    open "obsidian://open?path=$1"
}

# Recargar el archivo
source ~/.zshrc  # macOS Catalina+ usa zsh por defecto
```

### Configurar Git (Primera vez)

```bash
# Configurar identidad de Git
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# Configurar credential helper para macOS
git config --global credential.helper osxkeychain

# Configurar editor preferido
git config --global core.editor "nano"  # Nano
# O
git config --global core.editor "code --wait"  # VS Code
# O
git config --global core.editor "vim"  # Vim
```

### Integración con macOS

```bash
# Abrir ubicación de configuración en Finder
open ~/Library/Application\ Support/vaultflow

# Crear alias de Finder para acceso rápido al vault
# (Arrastra la carpeta del vault a la barra lateral del Finder)

# Usar Quick Look para ver archivos
cd ~/Documents/MiVault
qlmanage -p README.md
```

### Solución de Problemas en macOS

```bash
# Si Git no está disponible
xcode-select --install

# Si pip no se encuentra
python3 -m ensurepip --upgrade
python3 -m pip install -e .

# Si hay problemas con permisos en /usr/local
# Usar entorno virtual
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Si macOS bloquea la ejecución por seguridad
# Ir a: Sistema → Privacidad y Seguridad → Permitir

# Para chips Apple Silicon (M1/M2/M3)
# La mayoría de paquetes funcionan nativamente, pero si hay problemas:
arch -x86_64 pip install -e .  # Instalar en modo Rosetta
```

---

## 🔄 Ejemplos Multiplataforma

### Mismo Vault en Diferentes Sistemas

Imagina que tienes un vault sincronizado con Git en diferentes máquinas:

**En Windows (trabajo):**
```powershell
cd C:\Users\Juan\Documents\MiVault
vaultflow backup
vaultflow push
```

**En Linux (casa):**
```bash
cd ~/Documents/MiVault
git pull  # Actualizar cambios
vaultflow status
vaultflow backup
```

**En macOS (portátil):**
```bash
cd ~/Documents/MiVault
git pull
vaultflow status
```

### Script de Backup Automatizado

**Windows (PowerShell):**
```powershell
# backup-vault.ps1
$vaultPath = "C:\Users\TuUsuario\Documents\MiVault"
cd $vaultPath
vaultflow backup
if ($LASTEXITCODE -eq 0) {
    vaultflow push
    Write-Host "✓ Backup completado y sincronizado" -ForegroundColor Green
}
```

**Linux/macOS (Bash):**
```bash
#!/bin/bash
# backup-vault.sh
VAULT_PATH="$HOME/Documents/MiVault"
cd "$VAULT_PATH"
vaultflow backup
if [ $? -eq 0 ]; then
    vaultflow push
    echo "✓ Backup completado y sincronizado"
fi
```

### Tarea Programada / Cron Job

**Windows (Tarea Programada):**
```powershell
# Crear tarea que ejecuta backup diario a las 9 PM
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File C:\Scripts\backup-vault.ps1"
$trigger = New-ScheduledTaskTrigger -Daily -At 9PM
Register-ScheduledTask -TaskName "VaultFlowBackup" -Action $action -Trigger $trigger
```

**Linux/macOS (Cron):**
```bash
# Editar crontab
crontab -e

# Agregar línea para backup diario a las 9 PM
0 21 * * * cd ~/Documents/MiVault && /usr/local/bin/vaultflow backup >> ~/vaultflow-backup.log 2>&1
```

---

## 📱 Integración con Servicios en la Nube

### Obsidian Sync + VaultFlow

```bash
# Todas las plataformas
cd /ruta/a/vault/sincronizado
vaultflow init
vaultflow backup

# VaultFlow y Obsidian Sync funcionan en paralelo
# VaultFlow maneja el control de versiones con Git
# Obsidian Sync maneja la sincronización en tiempo real
```

### iCloud Drive (macOS)

```bash
# Vault en iCloud Drive
cd ~/Library/Mobile\ Documents/com~apple~CloudDocs/MiVault
vaultflow init

# Los cambios se sincronizan automáticamente entre dispositivos Apple
# VaultFlow proporciona control de versiones adicional
```

### OneDrive (Windows/macOS/Linux)

```bash
# Windows
cd C:\Users\TuUsuario\OneDrive\Documents\MiVault

# macOS
cd ~/OneDrive/Documents/MiVault

# Linux (si tienes el cliente de OneDrive)
cd ~/OneDrive/Documents/MiVault

# En todos:
vaultflow init
vaultflow backup
```

---

## 🎓 Casos de Uso Avanzados

### Múltiples Vaults en un Script

**Bash (Linux/macOS):**
```bash
#!/bin/bash
# backup-all-vaults.sh

VAULTS=(
    "$HOME/Documents/VaultTrabajo"
    "$HOME/Documents/VaultPersonal"
    "$HOME/Documents/VaultEstudios"
)

for vault in "${VAULTS[@]}"; do
    echo "Procesando: $vault"
    cd "$vault"
    vaultflow backup
    vaultflow push
    echo "---"
done

echo "✓ Todos los vaults respaldados"
```

**PowerShell (Windows):**
```powershell
# backup-all-vaults.ps1

$vaults = @(
    "C:\Users\TuUsuario\Documents\VaultTrabajo",
    "C:\Users\TuUsuario\Documents\VaultPersonal",
    "C:\Users\TuUsuario\Documents\VaultEstudios"
)

foreach ($vault in $vaults) {
    Write-Host "Procesando: $vault"
    cd $vault
    vaultflow backup
    vaultflow push
    Write-Host "---"
}

Write-Host "✓ Todos los vaults respaldados" -ForegroundColor Green
```

---

## 📝 Notas Importantes

### Compatibilidad de Rutas

- Usa **rutas absolutas** cuando sea posible
- En scripts, usa variables de entorno (`$HOME`, `%USERPROFILE%`)
- Evita caracteres especiales en nombres de vaults
- Usa comillas para rutas con espacios

### Performance

- La búsqueda automática (`discover`) puede tardar en directorios grandes
- Considera usar rutas específicas en lugar de búsqueda automática
- Los vaults en SSD son más rápidos que en HDD

### Seguridad

- No subas archivos sensibles a repositorios públicos
- Usa `.gitignore` apropiadamente
- Considera usar repositorios privados para vaults personales
- En empresas, verifica las políticas de control de versiones

---

**¿Necesitas más ejemplos?** Revisa la documentación completa en `docs/CROSS_PLATFORM.md`
