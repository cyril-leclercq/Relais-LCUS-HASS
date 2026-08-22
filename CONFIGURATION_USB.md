# Guide de Configuration du Port USB

## 📍 Comment trouver votre port USB

### Sur Linux
```bash
# Lister tous les ports USB
ls /dev/tty* | grep -i usb

# Ou avec dmesg (après branchement)
dmesg | grep tty

# Résultat typique: /dev/ttyUSB0 ou /dev/ttyACM0
```

### Sur macOS
```bash
# Lister tous les ports série
ls /dev/tty.* | grep -i usb

# Résultat typique: /dev/tty.usbserial-XXXX
```

### Sur Windows
```
# Dans le Gestionnaire de périphériques:
Ports (COM et LPT) → chercher "USB Serial Port"

# Résultat typique: COM3, COM4, etc.
```

### Avec Python (toutes plateformes)
```bash
python3 -m serial.tools.list_ports
```

---

## 🔧 Méthodes de Configuration

### Méthode 1: Variable d'environnement locale (ligne de commande)

```bash
# Temporaire (session actuelle)
export RELAIS_USB_PORT=/dev/ttyUSB0
python3 volet_monter.py

# Ou en une seule ligne
RELAIS_USB_PORT=/dev/ttyUSB0 python3 volet_monter.py
```

### Méthode 2: Fichier .env (recommandé pour développement)

```bash
# Copier l'exemple
cp .env.example .env

# Éditer .env
nano .env
```

Contenu du fichier `.env`:
```bash
RELAIS_USB_PORT=/dev/ttyUSB0
```

Puis charger avant utilisation:
```bash
source .env
python3 volet_monter.py
```

### Méthode 3: Home Assistant (recommandé pour production)

Le port USB est configurable directement dans l'interface Home Assistant via l'entité `input_text.volet_usb_port`.

#### Configuration initiale:

Dans votre `configuration.yaml`, l'input_text est déjà défini:

```yaml
input_text:
  volet_usb_port:
    name: Port USB du volet roulant
    initial: /dev/tty.usbserial-1110  # ← Changez selon votre système
    icon: mdi:usb-port
```

#### Modifier le port via l'interface:

1. **Ouvrez Home Assistant**
2. **Paramètres** → **Appareils et services** → **Entités**
3. Cherchez `volet_usb_port` dans la barre de recherche
4. Cliquez sur l'entité
5. Modifiez la valeur (ex: `/dev/ttyUSB0`)
6. Testez le volet (pas besoin de redémarrer!)

#### Modifier le port via Developer Tools:

1. **Outils de développement** → **États**
2. Cherchez `input_text.volet_usb_port`
3. Cliquez sur **SET STATE**
4. Entrez le nouveau port dans **State**
5. Cliquez sur **SET STATE**

#### Modifier le port via un service:

```yaml
service: input_text.set_value
target:
  entity_id: input_text.volet_usb_port
data:
  value: /dev/ttyUSB0
```

---

## 🎯 Exemples par Système

### Raspberry Pi (Home Assistant OS)

```yaml
input_text:
  volet_usb_port:
    initial: /dev/ttyUSB0  # Typique pour Pi
```

### Mac mini / macOS

```yaml
input_text:
  volet_usb_port:
    initial: /dev/tty.usbserial-1110
```

### Serveur Linux

```yaml
input_text:
  volet_usb_port:
    initial: /dev/ttyUSB0  # ou /dev/ttyACM0
```

### Windows (moins courant pour Home Assistant)

```yaml
input_text:
  volet_usb_port:
    initial: COM3
```

---

## 🔍 Dépannage

### Le port change à chaque redémarrage (Linux)

Créez une règle udev pour un nom permanent:

```bash
# 1. Trouvez le ID du périphérique
udevadm info -a -n /dev/ttyUSB0 | grep '{serial}'

# 2. Créez une règle udev
sudo nano /etc/udev/rules.d/99-usb-serial.rules
```

Contenu:
```
SUBSYSTEM=="tty", ATTRS{serial}=="VOTRE_SERIAL_ICI", SYMLINK+="volet"
```

Puis:
```bash
sudo udevadm control --reload-rules
# Débranchez/rebranchez le câble USB
```

Maintenant utilisez `/dev/volet` comme port!

### Permissions d'accès au port (Linux)

```bash
# Ajouter l'utilisateur au groupe dialout
sudo usermod -a -G dialout $USER

# Ou donner les permissions (temporaire)
sudo chmod 666 /dev/ttyUSB0
```

### Tester le port

```bash
# Lire depuis le port
cat /dev/ttyUSB0

# Ou avec Python
python3 -c "import serial; p = serial.Serial('/dev/ttyUSB0', 9600); print('OK')"
```

---

## ✅ Validation

Après configuration, testez:

```bash
# Test direct
RELAIS_USB_PORT=/dev/ttyUSB0 python3 -c "from relais import port; print(f'Port: {port.port}')"

# Test avec un script
RELAIS_USB_PORT=/dev/ttyUSB0 python3 volet_arreter.py
```

Dans Home Assistant, testez avec:
```yaml
service: shell_command.volet_arreter
```

Si ça fonctionne, votre configuration est correcte! ✅
