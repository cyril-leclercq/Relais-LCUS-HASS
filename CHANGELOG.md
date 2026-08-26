# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [Non publié]

### Ajouté
- ⚡ **Mode d'impulsion configurable**
  - Mode "Impulsion courte" (50-600 ms) pour commandes momentanées
  - Mode "Maintenu" (2s-2min) pour course complète du volet
  - Sliders de configuration pour ajuster les durées
  - UI professionnelle avec descriptions détaillées
  - Explications des différences entre les modes
  - Documentation complète (MODE_IMPULSION.md)
  - Guide de migration pour utilisateurs existants (MIGRATION_MODE_IMPULSION.md)
  - Paramètres identiques en installation et configuration
  - Support des traductions FR/EN

### Corrigé
- 🛑 **Arrêt réel du volet en mode Impulsion courte**
  - `stop_cover` renvoie désormais une impulsion sur le canal actif (montée ou descente) au lieu de simplement couper un relais déjà retombé
  - Corrige l'arrêt en cours de course pour les moteurs qui s'arrêtent par un nouvel appui sur le bouton déjà actif
  - Nécessaire pour les scripts de type "position intermédiaire" (`delay` + `cover.stop_cover`) en mode Impulsion courte
  - `is_opening`/`is_closing` reflètent maintenant le mouvement réel (le volet est considéré en mouvement jusqu'à l'arrêt effectif, pas seulement pendant la durée de l'impulsion)

### Modifié
- 🎛️ **Formulaire de configuration en plusieurs étapes**
  - Le champ de durée n'affiche désormais que l'option pertinente pour le mode d'impulsion choisi (plus de "Durée impulsion courte" visible en mode Maintenu, et inversement) — que ce soit à l'installation initiale ou via **Configurer** dans les options
- ⏱️ **Durée d'impulsion courte exprimée en millisecondes**
  - Plage réduite et plus précise : 50 à 600 ms (au lieu de 0.2 à 1 seconde), valeur par défaut inchangée (500 ms)
  - Les configurations existantes (stockées en secondes) sont automatiquement converties en millisecondes à la volée, sans action requise

### Supprimé
- 🗑️ **Paramètre "Temps de course total"**
  - Retiré du formulaire de configuration et des options : il n'était jamais lu par le code (aucun calcul de position n'en dépendait)
  - Les configurations existantes qui le contenaient continuent de fonctionner normalement, la valeur est simplement ignorée

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
