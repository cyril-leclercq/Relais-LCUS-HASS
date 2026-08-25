# 🚀 Commandes à exécuter sur le SERVEUR Linux

## ✅ Votre docker-compose.yml est CORRECT

La configuration est bonne :
```yaml
devices:
  - /dev/lcus_relay:/dev/lcus_relay  # ✓ Nom persistant
```

**Le problème** : `/dev/lcus_relay` n'existe pas encore sur l'HÔTE.

---

## 📋 ÉTAPES À SUIVRE sur le serveur Linux

### 1️⃣ Vérifier que le module USB est branché

```bash
# SSH sur votre serveur
ssh user@votre-serveur

# Vérifier la détection USB
lsusb | grep 1a86

# Résultat attendu:
# Bus 001 Device 003: ID 1a86:7523 QinHeng Electronics CH340 serial converter
```

**Si rien n'apparaît** → Le module n'est pas branché ou pas reconnu.

---

### 2️⃣ Vérifier le port série de base

```bash
ls -l /dev/ttyUSB*

# Résultat attendu:
# crw-rw---- 1 root dialout 188, 0 Aug 25 10:30 /dev/ttyUSB0
```

**Si erreur "No such file"** → Le driver n'est pas chargé :
```bash
sudo modprobe ch341
sudo modprobe usbserial
```

---

### 3️⃣ Créer la règle udev pour `/dev/lcus_relay`

```bash
# Créer le fichier de règle
sudo nano /etc/udev/rules.d/99-lcus-relay.rules
```

**Copiez-collez exactement cette ligne** :
```
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", SYMLINK+="lcus_relay", MODE="0666", GROUP="dialout"
```

**Enregistrez** : `Ctrl+O` puis `Enter` puis `Ctrl+X`

---

### 4️⃣ Activer la règle udev

```bash
# Recharger les règles
sudo udevadm control --reload-rules
sudo udevadm trigger

# Vérifier que le device est créé
ls -l /dev/lcus_relay

# Résultat attendu:
# lrwxrwxrwx 1 root root 7 Aug 25 10:35 /dev/lcus_relay -> ttyUSB0
```

**Vérifier les permissions** :
```bash
ls -l /dev/ttyUSB0

# Doit afficher: crw-rw-rw- (grâce à MODE="0666")
```

---

### 5️⃣ Redémarrer le conteneur Home Assistant

```bash
# Si Docker Compose
cd /opt/docker/hass  # Ou votre répertoire
docker-compose down
docker-compose up -d

# Si Docker Swarm
docker service update --force hass_homeassistant
```

---

### 6️⃣ Vérifier dans le conteneur

```bash
# Le device doit être visible
docker exec homeassistant ls -l /dev/lcus_relay

# Résultat attendu:
# lrwxrwxrwx 1 root root 7 Aug 25 10:35 /dev/lcus_relay -> ttyUSB0

# Tester la connexion série
docker exec homeassistant python3 -c "
import serial
s = serial.Serial('/dev/lcus_relay', 9600, timeout=1)
print('✓ Connexion série OK\!')
s.close()
"
```

---

## 🔧 Alternative si la règle udev ne fonctionne pas

### Option A : Utiliser directement /dev/ttyUSB0

**Modifier docker-compose.yml** :
```yaml
devices:
  - /dev/ttyUSB0:/dev/ttyUSB0  # Port direct au lieu de lcus_relay
```

**Donner les permissions** :
```bash
sudo chmod 666 /dev/ttyUSB0
```

**Redémarrer le conteneur** :
```bash
docker-compose down && docker-compose up -d
```

---

## ❓ Dépannage

### La règle udev ne se déclenche pas

```bash
# Débrancher/rebrancher le module USB
# OU redémarrer le serveur
sudo reboot

# Après redémarrage, vérifier
ls -l /dev/lcus_relay
```

### Le port change de nom (ttyUSB0 → ttyUSB1)

```bash
# Vérifier tous les ports
ls -l /dev/ttyUSB*

# Voir les infos du bon port
udevadm info -a /dev/ttyUSB0 | grep -E 'idVendor|idProduct'

# Ajuster la règle udev si nécessaire
```

---

## ✅ Checklist finale

- [ ] `lsusb | grep 1a86` → Affiche le module
- [ ] `ls -l /dev/ttyUSB0` → Existe avec permissions rw-rw-rw-
- [ ] `ls -l /dev/lcus_relay` → Symlink vers ttyUSB0
- [ ] `docker exec homeassistant ls -l /dev/lcus_relay` → Visible dans le conteneur
- [ ] Test connexion série → "✓ Connexion série OK\!"

