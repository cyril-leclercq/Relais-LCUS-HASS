# Guide d'Installation HACS - Volet Roulant Relais USB

## 📦 Installation via HACS

### Prérequis

1. **HACS installé** dans Home Assistant
2. **Module relais USB** connecté à votre serveur Home Assistant
3. **Port USB accessible** (voir [DOCKER_SETUP.md](DOCKER_SETUP.md) si vous utilisez Docker)

---

## 🚀 Installation

### Méthode 1 : Via l'interface HACS (recommandé)

1. **Ouvrez HACS** dans Home Assistant
2. Cliquez sur **Intégrations**
3. Cliquez sur les **3 points** en haut à droite
4. Sélectionnez **Dépôts personnalisés**
5. Ajoutez l'URL du dépôt :
   ```
   https://github.com/zunix/volet-relais-usb
   ```
6. Sélectionnez la catégorie **Integration**
7. Cliquez sur **Ajouter**
8. Recherchez **"Volet Roulant Relais USB"**
9. Cliquez sur **Télécharger**
10. **Redémarrez Home Assistant**

### Méthode 2 : Installation manuelle

```bash
# Dans votre répertoire config de Home Assistant
cd /config  # ou /opt/docker/hass/config si Docker

# Créer le répertoire custom_components s'il n'existe pas
mkdir -p custom_components

# Cloner le dépôt
git clone https://github.com/zunix/volet-relais-usb.git temp_volet
cp -r temp_volet/custom_components/volet_relais_usb custom_components/
rm -rf temp_volet

# Redémarrer Home Assistant
```

---

## ⚙️ Configuration

### Étape 1 : Ajouter l'intégration

1. **Paramètres** → **Appareils et services**
2. Cliquez sur **+ Ajouter une intégration**
3. Recherchez **"Volet Roulant Relais USB"**
4. Cliquez dessus pour lancer la configuration

### Étape 2 : Configurer le volet

Remplissez le formulaire :

- **Nom** : Le nom de votre volet (ex: "Volet Salon")
- **Port série USB** : Le chemin du port USB
  - Linux : `/dev/ttyUSB0` ou `/dev/volet_relais` (si règle udev)
  - macOS : `/dev/tty.usbserial-1110`
  - Windows : `COM3`
- **Temps de course** : Durée en secondes pour ouvrir/fermer complètement
  - Mesurez le temps réel et ajoutez une petite marge
  - Exemple : 28 secondes

### Étape 3 : Vérifier

1. L'intégration crée automatiquement une entité `cover.volet_roulant`
2. Testez l'ouverture, la fermeture et l'arrêt

---

## 🐳 Configuration Docker/Swarm

Si Home Assistant tourne dans un conteneur Docker, **le port USB doit être mappé**.

### docker-compose.yml

```yaml
services:
  homeassistant:
    # ... votre configuration ...
    devices:
      - /dev/ttyUSB0:/dev/ttyUSB0  # Mapper le port USB
      # OU avec règle udev :
      # - /dev/volet_relais:/dev/volet_relais
```

### Redéployer le stack

```bash
docker-compose up -d --force-recreate
# OU
docker stack deploy -c docker-compose.yml votre-stack
```

**Voir** [DOCKER_SETUP.md](DOCKER_SETUP.md) pour la configuration complète.

---

## 🔧 Utilisation

### Dans l'interface

- **Ouvrir** : Cliquez sur le bouton ⬆️
- **Fermer** : Cliquez sur le bouton ⬇️
- **Arrêter** : Cliquez sur le bouton ⏹️

### Dans les automatisations

```yaml
# Ouvrir le volet au lever du soleil
automation:
  - alias: "Ouvrir volet au lever du soleil"
    trigger:
      - platform: sun
        event: sunrise
    action:
      - service: cover.open_cover
        target:
          entity_id: cover.volet_roulant

# Fermer le volet au coucher du soleil
  - alias: "Fermer volet au coucher du soleil"
    trigger:
      - platform: sun
        event: sunset
        offset: "-00:30:00"  # 30 minutes avant
    action:
      - service: cover.close_cover
        target:
          entity_id: cover.volet_roulant
```

### Dans les scripts

```yaml
# Script pour position intermédiaire
script:
  volet_mi_ouvert:
    alias: "Volet mi-ouvert"
    sequence:
      - service: cover.open_cover
        target:
          entity_id: cover.volet_roulant
      - delay:
          seconds: 15  # Moitié du temps de course
      - service: cover.stop_cover
        target:
          entity_id: cover.volet_roulant
```

---

## 🔍 Dépannage

### L'intégration n'apparaît pas

1. Vérifiez que HACS a bien téléchargé l'intégration :
   ```bash
   ls /config/custom_components/volet_relais_usb/
   ```

2. Redémarrez Home Assistant

3. Vérifiez les logs :
   ```
   Paramètres → Système → Logs
   ```

### Erreur "Impossible de se connecter au port série"

1. **Vérifiez le port USB** :
   ```bash
   # Sur l'hôte (pas dans le conteneur)
   ls /dev/tty* | grep -i usb
   ```

2. **Docker** : Vérifiez le mapping du device
   ```bash
   docker exec homeassistant ls -l /dev/ttyUSB0
   ```

3. **Permissions** :
   ```bash
   sudo chmod 666 /dev/ttyUSB0
   # OU avec règle udev (permanent)
   ```

### Le volet ne réagit pas

1. Vérifiez que le module relais est branché et alimenté
2. Testez la connexion :
   ```bash
   python3 -c "import serial; s=serial.Serial('/dev/ttyUSB0', 9600); print('OK')"
   ```
3. Consultez les logs de l'intégration

### Le volet s'arrête trop tôt ou trop tard

1. **Reconfigurer l'intégration** :
   - Paramètres → Appareils et services
   - Trouvez "Volet Roulant Relais USB"
   - Cliquez sur **Configurer**
   - Ajustez le **Temps de course**

---

## 📱 Interface utilisateur avancée

### Carte personnalisée

```yaml
type: entities
entities:
  - entity: cover.volet_roulant
    name: Volet Salon
    secondary_info: last-changed
```

### Carte avec slider (position manuelle)

```yaml
type: vertical-stack
cards:
  - type: entities
    entities:
      - entity: cover.volet_roulant
  - type: horizontal-stack
    cards:
      - type: button
        name: "25%"
        tap_action:
          action: call-service
          service: script.volet_position
          service_data:
            position: 25
      - type: button
        name: "50%"
        tap_action:
          action: call-service
          service: script.volet_position
          service_data:
            position: 50
      - type: button
        name: "75%"
        tap_action:
          action: call-service
          service: script.volet_position
          service_data:
            position: 75
```

---

## 🔄 Mise à jour

### Via HACS

1. **HACS** → **Intégrations**
2. Trouvez **"Volet Roulant Relais USB"**
3. Cliquez sur **Mettre à jour** si disponible
4. **Redémarrez Home Assistant**

### Manuellement

```bash
cd /config/custom_components
rm -rf volet_relais_usb
git clone https://github.com/zunix/volet-relais-usb.git temp
cp -r temp/custom_components/volet_relais_usb .
rm -rf temp
# Redémarrer Home Assistant
```

---

## 📚 Documentation complémentaire

- **[README.md](README.md)** - Documentation générale
- **[DOCKER_SETUP.md](DOCKER_SETUP.md)** - Configuration Docker complète
- **[CONFIGURATION_USB.md](CONFIGURATION_USB.md)** - Configuration du port USB

---

## 🤝 Support

- **Issues** : https://github.com/zunix/volet-relais-usb/issues
- **Discussions** : https://github.com/zunix/volet-relais-usb/discussions

---

## ✅ Checklist d'installation

- [ ] HACS installé
- [ ] Module relais USB branché
- [ ] Port USB mappé (si Docker)
- [ ] Intégration téléchargée via HACS
- [ ] Home Assistant redémarré
- [ ] Intégration ajoutée via l'UI
- [ ] Port série configuré correctement
- [ ] Temps de course mesuré et configuré
- [ ] Test d'ouverture réussi
- [ ] Test de fermeture réussi
- [ ] Test d'arrêt réussi

Votre volet est maintenant intégré à Home Assistant ! 🎉
