# Guide de Contribution

Merci de votre intérêt pour contribuer à ce projet ! 🎉

---

## 🏗️ Structure du projet

```
relais/
├── custom_components/volet_relais_usb/  # Intégration HACS
│   ├── __init__.py                      # Setup de l'intégration
│   ├── manifest.json                    # Métadonnées
│   ├── config_flow.py                   # Configuration UI
│   ├── cover.py                         # Entité cover
│   ├── const.py                         # Constantes
│   ├── strings.json                     # Textes UI
│   └── translations/                    # Traductions FR/EN
├── relais.py                            # Module principal (standalone)
├── volet_*.py                           # Scripts CLI
├── docker-compose.yaml.example          # Config Docker Compose
├── docker-compose.swarm.yaml            # Config Docker Swarm
└── hacs.json                            # Métadonnées HACS
```

---

## 🛠️ Développement local

### Prérequis

- Python 3.9+
- Home Assistant (pour tester l'intégration)
- Module relais USB (ou émulateur série)

### Installation

```bash
# Cloner le dépôt
git clone https://github.com/cyril-leclercq/Relais-LCUS-HASS.git
cd Relais-LCUS-HASS

# Installer les dépendances
pip install pyserial

# Tester le module standalone
python3 relais.py
```

### Tester l'intégration dans Home Assistant

```bash
# Créer un lien symbolique dans votre config HA
ln -s $(pwd)/custom_components/volet_relais_usb \
      /config/custom_components/volet_relais_usb

# Redémarrer Home Assistant
```

---

## 🧪 Tests

### Test du module relais

```python
# test_relais.py
from relais import bouger, arreter

# Test montée
bouger('montee', 5)

# Test descente
bouger('descente', 5)

# Test arrêt
arreter()
```

### Test de la connexion série

```bash
python3 -c "
import serial
s = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
# Commande test : activer relais 1
s.write(bytes([0xA0, 0x01, 0x01, 0xA2]))
s.close()
print('✅ Test réussi')
"
```

---

## 📝 Convention de code

### Python

- **Style** : PEP 8
- **Docstrings** : Google style
- **Type hints** : Recommandés

```python
def bouger(direction: str, duree: int) -> None:
    """Active le relais pour déplacer le volet.
    
    Args:
        direction: 'montee' ou 'descente'
        duree: Durée en secondes
    """
    pass
```

### Commits

Format : `Type: Description courte`

Types :
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `refactor`: Refactorisation
- `test`: Tests

Exemple :
```bash
git commit -m "feat: Ajout support position intermédiaire"
git commit -m "fix: Correction timeout connexion série"
git commit -m "docs: Mise à jour guide Docker"
```

---

## 🔄 Workflow de contribution

### 1. Fork et branche

```bash
# Forker le dépôt sur GitHub
# Puis cloner votre fork
git clone https://github.com/VOTRE-USERNAME/Relais-LCUS-HASS.git
cd Relais-LCUS-HASS

# Créer une branche
git checkout -b feature/ma-fonctionnalite
```

### 2. Développer

```bash
# Faire vos modifications
# Tester localement

# Ajouter les fichiers
git add .

# Committer
git commit -m "feat: Ma nouvelle fonctionnalité"
```

### 3. Pousser et Pull Request

```bash
# Pousser vers votre fork
git push origin feature/ma-fonctionnalite

# Créer une Pull Request sur GitHub
# Depuis votre fork vers le dépôt principal
```

---

## 📦 Publication d'une version

### 1. Mettre à jour la version

```bash
# Modifier manifest.json
nano custom_components/volet_relais_usb/manifest.json
# Changer "version": "1.0.0" → "1.1.0"

# Mettre à jour CHANGELOG.md
nano CHANGELOG.md
# Ajouter les changements de la version
```

### 2. Créer un tag et une release

```bash
# Committer les changements
git add .
git commit -m "chore: Version 1.1.0"
git push origin main

# Créer un tag
git tag -a v1.1.0 -m "Version 1.1.0 - Description"
git push origin v1.1.0
```

### 3. Créer une release sur GitHub

1. Allez sur https://github.com/cyril-leclercq/Relais-LCUS-HASS/releases
2. **Draft a new release**
3. Tag : `v1.1.0`
4. Title : `v1.1.0 - Titre de la release`
5. Description : Copiez depuis CHANGELOG.md
6. **Publish release**

HACS détectera automatiquement la nouvelle version.

---

## 🐳 Configuration Docker pour le développement

### docker-compose.dev.yml

```yaml
services:
  homeassistant:
    image: ghcr.io/home-assistant/home-assistant:dev
    container_name: hass-dev
    privileged: true
    network_mode: host
    volumes:
      - ./config:/config
      - ./custom_components:/config/custom_components
    devices:
      - /dev/ttyUSB0:/dev/ttyUSB0
```

```bash
# Lancer
docker-compose -f docker-compose.dev.yml up -d

# Voir les logs
docker-compose -f docker-compose.dev.yml logs -f
```

---

## 🌍 Ajouter une traduction

### 1. Créer le fichier de traduction

```bash
# Exemple pour l'espagnol
cp custom_components/volet_relais_usb/translations/en.json \
   custom_components/volet_relais_usb/translations/es.json
```

### 2. Traduire

```json
{
  "config": {
    "step": {
      "user": {
        "title": "Configurar persiana enrollable USB",
        "description": "Configuración del módulo de relé USB",
        ...
      }
    }
  }
}
```

### 3. Tester

Changez la langue dans Home Assistant et vérifiez l'interface.

---

## 🔌 Protocole série du module LCUS

### Format de commande

```
[0xA0, canal, état, checksum]
```

- **0xA0** : Code de commande
- **canal** : 0x01 (montée) ou 0x02 (descente)
- **état** : 0x01 (ON) ou 0x00 (OFF)
- **checksum** : XOR des 3 premiers octets

### Exemples

```python
# Activer montée (canal 1)
bytes([0xA0, 0x01, 0x01, 0xA2])  # 0xA0 ^ 0x01 ^ 0x01 = 0xA2

# Désactiver montée
bytes([0xA0, 0x01, 0x00, 0xA1])  # 0xA0 ^ 0x01 ^ 0x00 = 0xA1

# Activer descente (canal 2)
bytes([0xA0, 0x02, 0x01, 0xA3])  # 0xA0 ^ 0x02 ^ 0x01 = 0xA3

# Désactiver descente
bytes([0xA0, 0x02, 0x00, 0xA2])  # 0xA0 ^ 0x02 ^ 0x00 = 0xA2
```

### Débit et configuration

- **Débit** : 9600 bauds
- **Data bits** : 8
- **Parity** : None
- **Stop bits** : 1
- **Flow control** : None

---

## 📚 Ressources

### Documentation Home Assistant

- [Developer Docs](https://developers.home-assistant.io/)
- [Integration Quality Scale](https://developers.home-assistant.io/docs/integration_quality_scale_index/)
- [Cover Entity](https://developers.home-assistant.io/docs/core/entity/cover/)

### Documentation HACS

- [HACS Documentation](https://hacs.xyz/docs/publish/integration)
- [Default Repository Requirements](https://hacs.xyz/docs/publish/include)

### PySerial

- [Documentation PySerial](https://pyserial.readthedocs.io/)

---

## ❓ Questions

Si vous avez des questions sur la contribution :

- Ouvrez une [Discussion](https://github.com/cyril-leclercq/Relais-LCUS-HASS/discussions)
- Consultez les [Issues](https://github.com/cyril-leclercq/Relais-LCUS-HASS/issues)

Merci de contribuer ! 🙏
