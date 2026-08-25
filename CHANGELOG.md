# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [Non publié]

### À venir
- Support de plusieurs volets (instances multiples)
- Calibration automatique du temps de course
- Détection de fin de course
- Position précise (0-100%)

## [1.0.0] - 2026-01-XX

### Ajouté
- 🎉 **Intégration HACS complète**
  - Configuration via l'interface utilisateur (UI)
  - Config flow avec validation du port série
  - Traductions complètes FR/EN
  - Métadonnées HACS (hacs.json, info.md)
  
- 📦 **Composant Custom Home Assistant**
  - Platform `cover` natif
  - Support des commandes open/close/stop
  - Gestion asynchrone (async/await)
  - Durée de course configurable
  
- 🐳 **Support Docker/Swarm**
  - Documentation complète du mapping USB
  - Règles udev pour nom persistant
  - Exemples docker-compose.yaml
  - Guide de dépannage
  
- 📚 **Documentation complète**
  - HACS_INSTALLATION.md : guide d'installation HACS
  - PUBLICATION_GITHUB.md : guide de publication GitHub
  - DOCKER_SETUP.md : configuration Docker/Swarm
  - CONFIGURATION_USB.md : configuration du port USB
  - README.md enrichi avec badges et sections HACS
  
- 🔧 **Scripts standalone**
  - volet_monter.py, volet_descendre.py, volet_arreter.py
  - Support shell_command Home Assistant
  - Configuration via variables d'environnement
  
- ⚙️ **Configuration flexible**
  - Port USB paramétrable (UI ou env var)
  - Temps de course ajustable
  - Protection anti-surchauffe (durée max)
  
- 📄 **Licence et conformité**
  - Licence MIT
  - .gitignore complet
  - Structure de projet professionnelle

### Changé
- Port USB par défaut : `/dev/ttyUSB0` (Linux) au lieu de `/dev/tty.usbserial-1110` (macOS)
- README.md : section HACS mise en avant
- .gitignore : ajout des fichiers de test et build

### Corrigé
- Gestion des erreurs de connexion série
- Validation du port USB avant configuration
- Encodage des chaînes de caractères

## [0.1.0] - 2026-01-XX

### Ajouté
- Script Python initial `relais.py`
- Contrôle basique de relais 2 canaux
- Support série USB 9600 bauds
- Fonctions `bouger()`, `arreter()`, `relais()`
- Dépendance pyserial

---

## Légende

- **Ajouté** : pour les nouvelles fonctionnalités
- **Changé** : pour les modifications de fonctionnalités existantes
- **Déprécié** : pour les fonctionnalités qui seront bientôt supprimées
- **Supprimé** : pour les fonctionnalités supprimées
- **Corrigé** : pour les corrections de bugs
- **Sécurité** : en cas de vulnérabilités

---

## Comment contribuer

Voir [PUBLICATION_GITHUB.md](PUBLICATION_GITHUB.md) pour les instructions de publication et de versioning.
