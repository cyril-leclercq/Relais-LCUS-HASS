# Volet Roulant Relais USB - Intégration Home Assistant

[\![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[\![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2023.1%2B-blue.svg)](https://www.home-assistant.io/)

Contrôlez votre volet roulant motorisé via un module relais USB 2 canaux dans Home Assistant.

## ✨ Fonctionnalités

- ✅ **Installation via HACS** en un clic
- ✅ **Configuration par interface** (pas de YAML)
- ✅ **Compatible Docker/Swarm**
- ✅ **Support Linux, macOS, Windows**
- ✅ **Multilingue** (FR/EN)

---

## 📦 Installation

### Via HACS (recommandé)

1. Ouvrez **HACS** dans Home Assistant
2. Allez dans **Intégrations**
3. Cliquez sur **⋮** (3 points) → **Dépôts personnalisés**
4. Ajoutez l'URL :
   ```
   https://github.com/cyril-leclercq/Relais-LCUS-HASS
   ```
5. Sélectionnez **Integration**
6. Cliquez sur **Ajouter**
7. Recherchez **"Volet Roulant Relais USB"**
8. Cliquez sur **Télécharger**
9. **Redémarrez** Home Assistant

### Installation manuelle

```bash
cd /config  # Répertoire config de Home Assistant
mkdir -p custom_components
git clone https://github.com/cyril-leclercq/Relais-LCUS-HASS.git temp
cp -r temp/custom_components/volet_relais_usb custom_components/
rm -rf temp
# Redémarrer Home Assistant
```

---

## ⚙️ Configuration

### 1. Ajouter l'intégration

1. **Paramètres** → **Appareils et services** → **+ Ajouter une intégration**
2. Recherchez **"Volet Roulant Relais USB"**
3. Configurez :
   - **Nom** : Nom de votre volet (ex: "Volet Salon")
   - **Port USB** : Voir section ci-dessous
   - **Temps de course** : Durée en secondes pour ouvrir/fermer complètement

### 2. Identifier le port USB

#### Sur Linux

```bash
# Méthode recommandée : utiliser l'ID stable du système
ls -l /dev/serial/by-id/

# Exemple de résultat :
# usb-1a86_USB_Serial-if00-port0 -> ../../ttyUSB0

# Copier le nom complet (ex: usb-1a86_USB_Serial-if00-port0)
# Ce lien est stable même si le port change (ttyUSB0 → ttyUSB1)
```

#### Sur macOS

```bash
ls /dev/tty.* | grep usb
# Résultat : /dev/tty.usbserial-1110
```

#### Sur Windows

Vérifiez dans le Gestionnaire de périphériques → Ports (COM & LPT)
```
COM3, COM4, etc.
```

### 3. Configuration Docker

Si Home Assistant est dans un conteneur :

```bash
# 1. Trouver l'ID stable du module USB (sur l'HÔTE)
ls -l /dev/serial/by-id/
# Résultat : usb-1a86_USB_Serial-if00-port0 -> ../../ttyUSB1
```

```yaml
# 2. Dans docker-compose.yml
services:
  homeassistant:
    privileged: true
    devices:
      # Docker crée automatiquement /dev/lcus_relay dans le conteneur
      - /dev/serial/by-id/usb-1a86_USB_Serial-if00-port0:/dev/lcus_relay
```

```bash
# 3. Redémarrer
docker-compose up -d --force-recreate
```

**✅ Avantages** : Nom stable même si le port change (ttyUSB0 → ttyUSB1), aucune règle udev requise.

**Voir** : [docker-compose.yaml.example](docker-compose.yaml.example) pour la configuration complète

---

## 🎮 Utilisation

### Interface

- **⬆️ Ouvrir** : Monte le volet
- **⬇️ Fermer** : Descend le volet  
- **⏹️ Arrêter** : Stoppe le mouvement

### Automatisations

```yaml
automation:
  - alias: "Ouvrir au lever du soleil"
    trigger:
      - platform: sun
        event: sunrise
    action:
      - service: cover.open_cover
        target:
          entity_id: cover.volet_salon

  - alias: "Fermer au coucher du soleil"
    trigger:
      - platform: sun
        event: sunset
    action:
      - service: cover.close_cover
        target:
          entity_id: cover.volet_salon
```

### Position intermédiaire

```yaml
script:
  volet_mi_ouvert:
    sequence:
      - service: cover.open_cover
        target:
          entity_id: cover.volet_salon
      - delay:
          seconds: 15  # Moitié du temps de course
      - service: cover.stop_cover
        target:
          entity_id: cover.volet_salon
```

---

## 🔧 Dépannage

### L'intégration n'apparaît pas

```bash
# Vérifier l'installation
ls /config/custom_components/volet_relais_usb/

# Vérifier les logs
# Paramètres → Système → Logs
```

### Erreur "Port série inaccessible"

**Linux** :
```bash
# Vérifier le port
ls -l /dev/ttyUSB0

# Ajouter les permissions
sudo usermod -aG dialout $USER
sudo chmod 666 /dev/ttyUSB0

# Se reconnecter pour appliquer
```

**Docker** :
```bash
# Vérifier le mapping
docker exec homeassistant ls -l /dev/ttyUSB0

# Si erreur : ajouter dans docker-compose.yml → devices
```

### Le volet ne répond pas

1. Vérifier que le module est branché et alimenté
2. Tester la connexion :
   ```bash
   python3 -c "import serial; s=serial.Serial('/dev/ttyUSB0', 9600); print('OK'); s.close()"
   ```
3. Vérifier les logs de l'intégration

### Le volet s'arrête trop tôt/tard

Reconfigurer le temps de course :
1. **Paramètres** → **Appareils et services**
2. Trouvez "Volet Roulant Relais USB"
3. **Configurer** → Ajustez le temps de course

---

## 📋 Matériel requis

- Module relais USB 2 canaux (9600 bauds)
- Volet roulant motorisé
- Home Assistant 2023.1+

---

## 🆘 Support

- 🐛 [Signaler un bug](https://github.com/cyril-leclercq/Relais-LCUS-HASS/issues)
- 💬 [Discussions](https://github.com/cyril-leclercq/Relais-LCUS-HASS/discussions)

---

## 📝 Licence

MIT License - voir [LICENSE](LICENSE)

---

## 🤝 Contribution

Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour contribuer au projet.
