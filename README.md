# Relais - Contrôle de Volet Roulant

Contrôle de relais via port série USB pour volet roulant (montée/descente), avec intégration Home Assistant.

## 🎯 Fonctionnalités

- Contrôle de volet roulant via module de relais USB
- Scripts indépendants pour monter, descendre et arrêter
- Intégration complète avec Home Assistant
- Protection anti-surchauffe avec durée maximale
- Arrêt d'urgence automatique

## 📋 Prérequis

- Python 3.x
- pyserial
- Module de relais USB (2 canaux minimum)
- Home Assistant (optionnel, pour l'intégration domotique)

## 🚀 Installation

### Installation automatique

```bash
chmod +x install.sh
./install.sh
```

### Installation manuelle

```bash
# Installer pyserial
pip install pyserial

# Rendre les scripts exécutables
chmod +x volet_*.py
```

## 💻 Utilisation en ligne de commande

### Utilisation directe

```python
from relais import bouger, arreter

# Monter le volet pendant 30 secondes
bouger('montee', 30)

# Descendre le volet pendant 25 secondes
bouger('descente', 25)

# Arrêter immédiatement
arreter()
```

### Scripts individuels

```bash
# Monter le volet (30 secondes par défaut)
python3 volet_monter.py

# Monter pendant une durée personnalisée
python3 volet_monter.py 25

# Descendre le volet
python3 volet_descendre.py

# Arrêter le volet
python3 volet_arreter.py
```

## 🏠 Intégration Home Assistant

### Configuration

1. **Modifiez les chemins dans `homeassistant_config.yaml`** :
   ```bash
   # Trouvez le chemin de Python
   which python3
   
   # Trouvez le chemin du projet
   pwd
   ```

2. **Copiez la configuration** dans votre `configuration.yaml` de Home Assistant :
   ```yaml
   # Voir le fichier homeassistant_config.yaml pour la configuration complète
   ```

3. **Ajustez les paramètres** :
   - Modifiez les chemins absolus vers les scripts
   - Le port USB est paramétrable via l'entité `input_text.volet_usb_port`
   - Ajustez la durée d'ouverture/fermeture selon votre volet
   - Personnalisez le nom et l'icône si souhaité

4. **Configurez le port USB** :
   - Via l'interface Home Assistant : Paramètres → Appareils et services → Entités
   - Cherchez `input_text.volet_usb_port`
   - Définissez votre port USB (ex: `/dev/ttyUSB0` pour Linux)

5. **Redémarrez Home Assistant**

### Utilisation dans Home Assistant

Une fois configuré, votre volet apparaîtra comme `cover.volet_roulant` :

- **Interface** : Contrôle via l'interface graphique
- **Configuration du port USB** : Modifiable via `input_text.volet_usb_port` sans redémarrage
- **Services** :
  ```yaml
  # Ouvrir
  service: cover.open_cover
  target:
    entity_id: cover.volet_roulant
  
  # Fermer
  service: cover.close_cover
  target:
    entity_id: cover.volet_roulant
  
  # Arrêter
  service: cover.stop_cover
  target:
    entity_id: cover.volet_roulant
  ```

- **Automatisations** : Utilisez l'entité dans vos automatisations (lever/coucher du soleil, horaires, etc.)

## ⚙️ Configuration matérielle

### Port USB

Le port USB est désormais **paramétrable** via variable d'environnement `RELAIS_USB_PORT`.

**Par défaut** : `/dev/tty.usbserial-1110`

**Configuration en ligne de commande** :
```bash
# Définir temporairement
export RELAIS_USB_PORT=/dev/ttyUSB0
python3 volet_monter.py

# Ou en une ligne
RELAIS_USB_PORT=/dev/ttyUSB0 python3 volet_monter.py
```

**Configuration dans Home Assistant** :
Le port est configurable via l'entité `input_text.volet_usb_port` (voir [homeassistant_config.yaml](homeassistant_config.yaml)).

**Ports courants** :
- **macOS** : `/dev/tty.usbserial-1110`
- **Linux** : `/dev/ttyUSB0`
- **Windows** : `COM3` (ou autre port COM)

Pour trouver votre port USB :
```bash
# Linux/macOS
ls /dev/tty* | grep -i usb

# Ou avec Python
python3 -m serial.tools.list_ports
```

### Canaux de relais

- **Canal 1** : Montée
- **Canal 2** : Descente

### Durée maximale

Par défaut, la durée maximale est de **40 secondes** pour éviter la surchauffe. Modifiez `DUREE_MAX` dans `relais.py` si nécessaire.

## 📁 Structure des fichiers

```
relais/
├── relais.py                    # Module principal de contrôle
├── volet_monter.py              # Script pour monter le volet
├── volet_descendre.py           # Script pour descendre le volet
├── volet_arreter.py             # Script pour arrêter le volet
├── homeassistant_config.yaml    # Configuration Home Assistant
├── install.sh                   # Script d'installation
├── .env.example                 # Exemple de configuration du port USB
├── .gitignore                   # Fichiers à ignorer par Git
└── README.md                    # Cette documentation
```

## 🔧 Dépannage

### Le port USB n'est pas trouvé
- Vérifiez que le module est branché
- Vérifiez les permissions : `sudo chmod 666 /dev/ttyUSB0` (Linux)
- Listez les ports disponibles : `ls /dev/tty*`

### Home Assistant ne trouve pas les scripts
- Vérifiez les chemins absolus dans `homeassistant_config.yaml`
- Vérifiez les permissions d'exécution : `chmod +x volet_*.py`
- Testez manuellement : `python3 volet_monter.py`

### Le volet ne s'arrête pas à la bonne position
- Ajustez la durée dans la configuration Home Assistant
- Mesurez la durée exacte d'ouverture/fermeture complète
- Utilisez cette valeur dans les paramètres `duree`

## 📄 Licence

Ce projet est libre d'utilisation.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.
