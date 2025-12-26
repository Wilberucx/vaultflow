# 🧪 Checklist de Testing Multiplataforma

Esta lista te ayudará a verificar que VaultFlow funciona correctamente en tu plataforma.

---

## ✅ Testing Básico (Todas las Plataformas)

### 1. Verificación de Requisitos

- [ ] Python 3.7+ instalado
- [ ] Git instalado y en el PATH
- [ ] `vaultflow sysinfo` muestra información correcta
- [ ] No hay errores en la detección de plataforma

**Comando:**
```bash
vaultflow sysinfo
```

**Resultado esperado:**
- ✓ Python version detectada
- ✓ Git disponible con ruta
- ✓ Sistema operativo correcto
- ✓ Directorio de configuración apropiado

---

### 2. Instalación

- [ ] `pip install -e .` funciona sin errores
- [ ] Comando `vaultflow` está disponible
- [ ] `vaultflow --help` muestra ayuda
- [ ] No hay warnings de dependencias

**Comandos:**
```bash
pip install -e .
vaultflow --help
vaultflow --version
```

---

### 3. Inicialización de Vault

- [ ] `vaultflow init` en un directorio vacío funciona
- [ ] Se crea `.git/` correctamente
- [ ] Se crea `.vaultflow/` correctamente
- [ ] Se crea `.gitignore` con reglas apropiadas
- [ ] Se crea `vault.lock` dentro de `.vaultflow/`
- [ ] El vault se registra en la configuración

**Comandos:**
```bash
mkdir test-vault
cd test-vault
vaultflow init
ls -la  # Linux/macOS
dir /a  # Windows
```

**Verificar:**
```bash
# Debe existir:
# .git/
# .vaultflow/
# .vaultflow/vault.lock
# .vaultflow/config.json
# .gitignore
```

---

### 4. Operaciones Básicas

- [ ] `vaultflow status` muestra estado correcto
- [ ] `vaultflow backup` crea un commit
- [ ] `vaultflow log` muestra el historial
- [ ] `vaultflow backups` lista los backups
- [ ] `vaultflow vaults` muestra vaults registrados

**Comandos:**
```bash
cd test-vault
echo "# Test" > test.md
vaultflow status
vaultflow backup
vaultflow log
vaultflow backups
vaultflow vaults
```

---

### 5. Sistema de Experimentos

- [ ] `vaultflow start-experiment nombre` crea rama
- [ ] Git cambia a la rama `exp/nombre`
- [ ] No permite experimentos anidados
- [ ] `vaultflow finish-experiment nombre` fusiona correctamente
- [ ] Opción de borrar rama funciona

**Comandos:**
```bash
cd test-vault
vaultflow start-experiment prueba
git branch  # Debe mostrar exp/prueba
echo "# Experimento" > experimento.md
vaultflow backup
vaultflow finish-experiment prueba
git branch  # Debe volver a main
```

---

### 6. Gestión de Múltiples Vaults

- [ ] `vaultflow discover` encuentra vaults
- [ ] Vaults se registran correctamente
- [ ] `vaultflow vaults` lista todos
- [ ] Cambiar entre vaults funciona

**Comandos:**
```bash
# Crear segundo vault
mkdir test-vault-2
cd test-vault-2
vaultflow init

# Verificar
vaultflow vaults
vaultflow discover
```

---

### 7. Modo Interactivo

- [ ] `vaultflow` sin argumentos inicia menú
- [ ] Todas las opciones del menú funcionan
- [ ] Navegación con flechas funciona
- [ ] Salir del menú funciona correctamente

**Comando:**
```bash
cd test-vault
vaultflow
```

---

## 🪟 Testing Específico de Windows

### Configuración

- [ ] Directorio de config en `%APPDATA%\vaultflow`
- [ ] O en `%USERPROFILE%\.vaultflow` (fallback)
- [ ] Archivos usan CRLF para saltos de línea
- [ ] Caracteres especiales se manejan correctamente

**Verificar:**
```powershell
# Ver directorio de configuración
echo $env:APPDATA\vaultflow
dir $env:APPDATA\vaultflow

# Verificar saltos de línea
type .gitignore | findstr /r /c:"$"
```

### Rutas de Búsqueda

- [ ] Busca en `%USERPROFILE%\Documents`
- [ ] Busca en `%USERPROFILE%\Documentos`
- [ ] Busca en OneDrive si existe
- [ ] Maneja espacios en nombres de rutas

**Comandos:**
```powershell
# Crear vault en ruta con espacios
mkdir "C:\Users\$env:USERNAME\Documents\Mi Vault"
cd "C:\Users\$env:USERNAME\Documents\Mi Vault"
vaultflow init
```

### Git en Windows

- [ ] Git Bash funciona
- [ ] PowerShell funciona
- [ ] CMD funciona
- [ ] Caracteres Unicode en mensajes de commit

**Comandos:**
```powershell
# Probar en diferentes shells
git --version
vaultflow sysinfo
```

### Casos Especiales Windows

- [ ] Funciona con rutas en diferentes unidades (C:, D:, etc.)
- [ ] Maneja rutas UNC (\\servidor\carpeta)
- [ ] Funciona con OneDrive
- [ ] Funciona con Google Drive

---

## 🐧 Testing Específico de Linux

### Configuración

- [ ] Directorio de config en `~/.config/vaultflow`
- [ ] O en `$XDG_CONFIG_HOME/vaultflow` si está configurado
- [ ] Archivos usan LF para saltos de línea
- [ ] Permisos correctos (700 para config)

**Verificar:**
```bash
# Ver directorio de configuración
echo ~/.config/vaultflow
ls -la ~/.config/vaultflow

# Verificar permisos
stat -c "%a %n" ~/.config/vaultflow

# Verificar saltos de línea
file .gitignore
```

### Rutas de Búsqueda

- [ ] Busca en `~/Documents`
- [ ] Busca en `~/Documentos`
- [ ] Busca en `$XDG_DOCUMENTS_DIR` si existe
- [ ] Maneja caracteres especiales en nombres

**Comandos:**
```bash
# Crear vault con caracteres especiales
mkdir ~/Documents/vault-test-ñ
cd ~/Documents/vault-test-ñ
vaultflow init
```

### Distribuciones

- [ ] Ubuntu/Debian - apt install funciona
- [ ] Fedora/RHEL - dnf install funciona
- [ ] Arch Linux - pacman -S funciona
- [ ] Funciona en WSL (Windows Subsystem for Linux)

**Verificar en tu distribución:**
```bash
# Ver información del sistema
cat /etc/os-release
uname -a
vaultflow sysinfo
```

### Casos Especiales Linux

- [ ] Funciona con home cifrado
- [ ] Funciona con symlinks
- [ ] Funciona en servidores sin GUI
- [ ] Funciona con diferentes shells (bash, zsh, fish)

---

## 🍎 Testing Específico de macOS

### Configuración

- [ ] Directorio de config en `~/Library/Application Support/vaultflow`
- [ ] Archivos usan LF para saltos de línea
- [ ] Funciona con Time Machine
- [ ] Funciona con FileVault (cifrado)

**Verificar:**
```bash
# Ver directorio de configuración
ls -la ~/Library/Application\ Support/vaultflow

# Verificar saltos de línea
file .gitignore
```

### Rutas de Búsqueda

- [ ] Busca en `~/Documents`
- [ ] Busca en iCloud Drive si existe
- [ ] Maneja espacios en nombres de carpetas
- [ ] Funciona con aplicaciones .app

**Comandos:**
```bash
# Probar con iCloud Drive
cd ~/Library/Mobile\ Documents/com~apple~CloudDocs
mkdir test-vault
cd test-vault
vaultflow init
```

### Arquitecturas

- [ ] Funciona en Intel (x86_64)
- [ ] Funciona en Apple Silicon (M1/M2/M3 - arm64)
- [ ] Rosetta 2 no es necesario

**Verificar:**
```bash
# Ver arquitectura
uname -m
arch

# Ver si es nativo
file $(which python3)
```

### Casos Especiales macOS

- [ ] Funciona con SIP (System Integrity Protection) activado
- [ ] Funciona con Gatekeeper
- [ ] Permisos de seguridad apropiados
- [ ] Integración con Keychain para Git

---

## 🔄 Testing de Integración

### Git Remoto

- [ ] `git remote add origin URL` funciona
- [ ] `vaultflow push` sube cambios
- [ ] Maneja errores de autenticación correctamente
- [ ] Configura upstream automáticamente

**Comandos:**
```bash
cd test-vault
git remote add origin https://github.com/usuario/repo.git
vaultflow push
```

### Sincronización

- [ ] Funciona con GitHub
- [ ] Funciona con GitLab
- [ ] Funciona con Bitbucket
- [ ] Funciona con servidores Git privados

---

## 🎨 Testing de Salida

### Colores y Formato

- [ ] Colores se muestran correctamente
- [ ] Rich panels se renderizan bien
- [ ] ASCII art del banner se ve correcto
- [ ] Emojis se muestran (si el terminal los soporta)

**Comando:**
```bash
vaultflow
vaultflow status
vaultflow sysinfo
```

### Diferentes Terminales

- [ ] Terminal predeterminado del sistema
- [ ] VS Code integrated terminal
- [ ] Terminal en SSH
- [ ] Git Bash (Windows)
- [ ] PowerShell (Windows)
- [ ] iTerm2 (macOS)
- [ ] GNOME Terminal (Linux)
- [ ] Konsole (Linux)

---

## 📊 Testing de Performance

### Velocidad

- [ ] `vaultflow init` completa en < 5 segundos
- [ ] `vaultflow status` responde instantáneamente
- [ ] `vaultflow backup` completa en < 10 segundos
- [ ] `vaultflow discover` completa en tiempo razonable

### Carga

- [ ] Funciona con vaults grandes (1000+ archivos)
- [ ] Funciona con archivos grandes (imágenes, PDFs)
- [ ] No hay memory leaks
- [ ] No hay procesos zombies

**Probar:**
```bash
# Crear vault grande
cd test-vault
for i in {1..100}; do echo "# File $i" > "file$i.md"; done
vaultflow status
vaultflow backup
```

---

## 🐛 Testing de Manejo de Errores

### Errores Comunes

- [ ] Git no instalado - mensaje claro
- [ ] Python version vieja - mensaje claro
- [ ] Sin permisos de escritura - mensaje claro
- [ ] Vault no inicializado - mensaje claro
- [ ] Sin conexión a internet (push) - mensaje claro

**Probar:**
```bash
# Intentar usar sin init
cd /tmp/not-a-vault
vaultflow status  # Debe dar error claro

# Intentar push sin remoto
cd test-vault
vaultflow push  # Debe explicar cómo configurar remoto
```

### Recuperación

- [ ] Se puede reintentar después de un error
- [ ] Los archivos no se corrompen
- [ ] El estado de Git permanece consistente
- [ ] Los logs registran los errores

---

## 🔒 Testing de Seguridad

### Archivos Sensibles

- [ ] `.gitignore` se crea correctamente
- [ ] Archivos sensibles no se commitean
- [ ] Configuración de usuario se respeta
- [ ] No se exponen credenciales

**Verificar .gitignore incluye:**
```
.DS_Store (macOS)
Thumbs.db (Windows)
*.icloud
.obsidian/workspace.json
```

### Permisos

- [ ] Configuración solo legible por usuario
- [ ] Git hooks tienen permisos correctos
- [ ] Archivos de vault tienen permisos apropiados

---

## 📝 Checklist de Testing por Plataforma

### Windows
- [ ] ✅ Instalación exitosa
- [ ] ✅ Todos los comandos funcionan
- [ ] ✅ Rutas con espacios funcionan
- [ ] ✅ OneDrive funciona
- [ ] ✅ PowerShell y CMD funcionan

### Linux
- [ ] ✅ Instalación exitosa (verificado en WSL)
- [ ] ✅ Todos los comandos funcionan
- [ ] ✅ Permisos correctos
- [ ] ✅ Funciona en tu distribución
- [ ] ✅ Shell preferido funciona

### macOS
- [ ] ⏳ Instalación pendiente
- [ ] ⏳ Intel pendiente de probar
- [ ] ⏳ Apple Silicon pendiente de probar
- [ ] ⏳ iCloud Drive pendiente de probar

---

## 🎯 Checklist Final

Antes de considerar el testing completo:

- [ ] Todas las pruebas básicas pasan
- [ ] Al menos 2 plataformas completamente probadas
- [ ] Documentación revisada y actualizada
- [ ] No hay errores críticos
- [ ] Performance es aceptable
- [ ] Manejo de errores es robusto
- [ ] Seguridad verificada

---

## 📞 Reportar Problemas

Si encuentras un bug durante el testing:

1. **Ejecuta:**
   ```bash
   vaultflow sysinfo > sysinfo.txt
   ```

2. **Incluye en el reporte:**
   - Sistema operativo y versión
   - Contenido de `sysinfo.txt`
   - Pasos exactos para reproducir
   - Mensaje de error completo
   - Output esperado vs output real

3. **Dónde reportar:**
   - GitHub Issues
   - Con etiqueta "bug" y etiqueta de plataforma

---

**Fecha de última actualización:** 2025-01-20  
**Versión de VaultFlow:** 0.2.0-dev (Multiplataforma)
