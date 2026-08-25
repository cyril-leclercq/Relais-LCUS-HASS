# Configuration Docker pour Home Assistant + Volet Roulant USB

## 🐳 Problème : Accès USB dans un conteneur Docker

Par défaut, les conteneurs Docker **n'ont pas accès aux périphériques USB** de l'hôte, même avec `privileged: true`. Vous devez mapper explicitement les devices.

---

## 📦 Exemples de configuration fournis

Ce projet inclut plusieurs exemples de configuration Docker adaptés à différents scénarios :

- **[docker-compose.yaml.example](docker-compose.yaml.example)** : Configuration complète Docker Compose avec Matter Server (production)
- **[docker-compose.swarm.yaml](docker-compose.swarm.yaml)** : Configuration Docker Swarm avec contraintes de placement

Choisissez le fichier correspondant à votre environnement et copiez-le :

```bash
# Docker Compose standalone
cp docker-compose.yaml.example docker-compose.yaml

# Docker Swarm
cp docker-compose.swarm.yaml docker-compose.yaml
```

---

## ✅ Solution 1 : Configuration testée en production

### Configuration avec Matter Server + Home Assistant

Cette configuration est testée et fonctionne en production :

```yaml
services:
  matter-server:
    image: ghcr.io/home-assistant-libs/python-matter-server:stable
    container_name: matter-server
    restart: unless-stopped
    network_mode: host
    security_opt:
      - apparmor:unconfined
    volumes:
      - /opt/docker/matter/data:/data
      - /run/dbus:/run/dbus:ro
      
  homeassistant:
    image: ghcr.io/home-assistant/home-assistant:2026.4.4
    container_name: homeassistant
    restart: unless-stopped
    privileged: true        # ← Accès aux périphériques
    network_mode: host      # ← Requis pour la découverte réseau
    volumes:
      - /opt/docker/hass/config:/config
      - /etc/localtime:/etc/localtime:ro
    devices:
      - /dev/ttyUSB0:/dev/ttyUSB0  # ← MAPPING USB CRITIQUE
    depends_on:
      - matter-server
```

**Points clés** :
- ✅ `privileged: true` : Donne accès aux périphériques système
- ✅ `network_mode: host` : Nécessaire pour mDNS et découverte réseau
- ✅ `devices` : Mapping explicite du port USB

---

## 🔍 Solution 2 : Identifier votre port USB

### Étape 1 : Identifier votre port USB sur l'hôte

```bash
# Sur l'hôte Docker (pas dans le conteneur)
ls /dev/tty* | grep -i usb

# Exemple de résultat:
# /dev/ttyUSB0  (Linux)
# /dev/tty.usbserial-1110  (macOS)
```

### Étape 2 : Modifier votre docker-compose.yml

Ajoutez la section `devices` à votre service `homeassistant` :

```yaml
services:
  homeassistant:
    # ... votre configuration existante ...
    devices:
      - /dev/ttyUSB0:/dev/ttyUSB0  # ← AJOUTER CETTE LIGNE
```

**Voir les exemples complets** :
- [docker-compose.yaml.example](docker-compose.yaml.example) pour Docker Compose
- [docker-compose.swarm.yaml](docker-compose.swarm.yaml) pour Docker Swarm

### Étape 3 : Redéployer le stack

```bash
# Si vous utilisez Docker Swarm
docker stack deploy -c docker-compose.yml votre-stack

# Ou avec docker-compose
docker-compose up -d
```

### Étape 4 : Vérifier l'accès dans le conteneur

```bash
# Entrer dans le conteneur
docker exec -it homeassistant bash

# Vérifier que le port est accessible
ls -l /dev/ttyUSB0

# Devrait afficher quelque chose comme:
# crw-rw---- 1 root dialout 188, 0 Jan 1 12:00 /dev/ttyUSB0
```

### Étape 5 : Configurer Home Assistant

Dans votre `configuration.yaml` (ou le fichier inclus):

```yaml
input_text:
  volet_usb_port:
    name: Port USB du volet roulant
    initial: /dev/ttyUSB0  # Le même que dans devices
    icon: mdi:usb-port

shell_command:
  volet_monter: "RELAIS_USB_PORT=/dev/ttyUSB0 python3 /config/scripts/relais/volet_monter.py {{ duree|default(30) }}"
  volet_descendre: "RELAIS_USB_PORT=/dev/ttyUSB0 python3 /config/scripts/relais/volet_descendre.py {{ duree|default(30) }}"
  volet_arreter: "RELAIS_USB_PORT=/dev/ttyUSB0 python3 /config/scripts/relais/volet_arreter.py"
```

**Note**: Les scripts doivent être dans `/config/scripts/relais/` pour être accessibles dans le conteneur.

---

## ✅ Solution 2 : Mapper tous les ports USB (méthode robuste)

Si le port change parfois (ex: après redémarrage):

```yaml
services:
  homeassistant:
    # ... autres configurations ...
    devices:
      - /dev/ttyUSB0:/dev/ttyUSB0
      - /dev/ttyUSB1:/dev/ttyUSB1
      - /dev/ttyACM0:/dev/ttyACM0
      - /dev/ttyACM1:/dev/ttyACM1
```

---

## ✅ Solution 3 : Règle udev pour un nom persistant (RECOMMANDÉ)

### Sur l'hôte Docker

**1. Créer une règle udev permanente:**

```bash
# Brancher le module USB
# Identifier le numéro de série
udevadm info -a -n /dev/ttyUSB0 | grep '{serial}'

# Exemple de sortie:
# ATTRS{serial}=="A50285BI"
```

**2. Créer le fichier de règle:**

```bash
sudo nano /etc/udev/rules.d/99-volet-relais.rules
```

Contenu:
```
# Règle pour le module relais du volet roulant
SUBSYSTEM=="tty", ATTRS{serial}=="A50285BI", SYMLINK+="volet_relais", MODE="0666"
```

**3. Recharger les règles:**

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger

# Débrancher/rebrancher le câble USB
```

**4. Vérifier:**

```bash
ls -l /dev/volet_relais
# Devrait pointer vers /dev/ttyUSB0 ou similaire
```

**5. Modifier docker-compose.yml:**

```yaml
services:
  homeassistant:
    # ... autres configurations ...
    devices:
      - /dev/volet_relais:/dev/volet_relais  # Nom persistant !
```

**6. Configuration Home Assistant:**

```yaml
input_text:
  volet_usb_port:
    initial: /dev/volet_relais  # Nom stable
```

---

## 📁 Structure des fichiers dans le conteneur

### Placer les scripts Python dans le volume Home Assistant

Sur l'**hôte Docker**:
```bash
# Créer le dossier
mkdir -p /opt/docker/hass/config/scripts/relais

# Copier les scripts
cp /chemin/vers/relais/*.py /opt/docker/hass/config/scripts/relais/

# Vérifier les permissions
chmod +x /opt/docker/hass/config/scripts/relais/volet_*.py
```

Dans le **conteneur**, les scripts seront à:
```
/config/scripts/relais/relais.py
/config/scripts/relais/volet_monter.py
/config/scripts/relais/volet_descendre.py
/config/scripts/relais/volet_arreter.py
```

---

## 🔧 Configuration Home Assistant complète (Docker)

```yaml
# Dans /opt/docker/hass/config/configuration.yaml

input_text:
  volet_usb_port:
    name: Port USB du volet roulant
    initial: /dev/volet_relais  # Ou /dev/ttyUSB0
    icon: mdi:usb-port

shell_command:
  volet_monter: "RELAIS_USB_PORT={{ states('input_text.volet_usb_port') }} python3 /config/scripts/relais/volet_monter.py {{ duree|default(30) }}"
  volet_descendre: "RELAIS_USB_PORT={{ states('input_text.volet_usb_port') }} python3 /config/scripts/relais/volet_descendre.py {{ duree|default(30) }}"
  volet_arreter: "RELAIS_USB_PORT={{ states('input_text.volet_usb_port') }} python3 /config/scripts/relais/volet_arreter.py"

cover:
  - platform: template
    covers:
      volet_roulant:
        device_class: shutter
        friendly_name: "Volet Roulant"
        open_cover:
          service: shell_command.volet_monter
          data:
            duree: 30
        close_cover:
          service: shell_command.volet_descendre
          data:
            duree: 30
        stop_cover:
          service: shell_command.volet_arreter
        icon_template: >-
          {% if is_state('cover.volet_roulant', 'open') %}
            mdi:window-shutter-open
          {% else %}
            mdi:window-shutter
          {% endif %}
```

---

## 🔍 Dépannage

### Erreur: "Permission denied" sur /dev/ttyUSB0

**Dans le conteneur:**
```bash
docker exec -it homeassistant bash
ls -l /dev/ttyUSB0
# crw-rw---- 1 root dialout 188, 0 Jan 1 12:00 /dev/ttyUSB0
```

**Solution 1 - Sur l'hôte (temporaire):**
```bash
sudo chmod 666 /dev/ttyUSB0
```

**Solution 2 - Règle udev avec MODE (permanent):**
```
SUBSYSTEM=="tty", ATTRS{serial}=="VOTRE_SERIAL", SYMLINK+="volet_relais", MODE="0666"
```

**Solution 3 - Groupe dialout dans le conteneur:**
```bash
# Dans docker-compose.yml
services:
  homeassistant:
    user: "0:20"  # root:dialout (le GID peut varier)
```

### Le device n'apparaît pas dans le conteneur

```bash
# Vérifier sur l'hôte
ls /dev/ttyUSB0

# Recréer le conteneur (pas juste restart)
docker-compose up -d --force-recreate

# Vérifier les logs
docker logs homeassistant
```

### "No module named 'serial'" dans le conteneur

```bash
# Entrer dans le conteneur
docker exec -it homeassistant bash

# Installer pyserial
pip install pyserial

# Ou créer un Dockerfile personnalisé (voir ci-dessous)
```

---

## 📦 Option : Image Docker personnalisée

Si vous devez installer des dépendances supplémentaires:

**Dockerfile:**
```dockerfile
FROM ghcr.io/home-assistant/home-assistant:2026.4.4

# Installer pyserial
RUN pip install --no-cache-dir pyserial

# Copier les scripts
COPY relais /config/scripts/relais
```

**docker-compose.yml:**
```yaml
services:
  homeassistant:
    build: .
    # ... reste de la configuration ...
```

---

## ✅ Checklist complète

- [ ] Identifier le port USB sur l'hôte (`ls /dev/tty*`)
- [ ] Ajouter `devices:` dans docker-compose.yml
- [ ] (Optionnel mais recommandé) Créer une règle udev
- [ ] Copier les scripts dans `/opt/docker/hass/config/scripts/relais/`
- [ ] Installer pyserial dans le conteneur (`pip install pyserial`)
- [ ] Configurer Home Assistant (configuration.yaml)
- [ ] Redéployer le stack
- [ ] Vérifier l'accès au device dans le conteneur
- [ ] Tester avec `service: shell_command.volet_arreter`

---

## 🎯 Résumé : Configuration minimale

```yaml
# docker-compose.yml
services:
  homeassistant:
    # ...
    devices:
      - /dev/ttyUSB0:/dev/ttyUSB0  # ← ESSENTIEL !
```

```bash
# Sur l'hôte
mkdir -p /opt/docker/hass/config/scripts/relais
cp *.py /opt/docker/hass/config/scripts/relais/

# Dans le conteneur
docker exec -it homeassistant bash
pip install pyserial
```

```yaml
# configuration.yaml
shell_command:
  volet_monter: "RELAIS_USB_PORT=/dev/ttyUSB0 python3 /config/scripts/relais/volet_monter.py 30"
```

C'est tout ! 🎉
