# 🔧 Solution simple : /dev/serial/by-id/

## 🎯 Problème résolu

- Le port USB change de nom : `ttyUSB0` → `ttyUSB1`
- Besoin d'un nom stable sans créer de règles udev personnalisées

---

## ✅ SOLUTION SIMPLE : Utiliser /dev/serial/by-id/

Linux crée **automatiquement** des liens symboliques stables dans `/dev/serial/by-id/`.

### 1️⃣ Trouver votre device (sur l'HÔTE)

```bash
ls -l /dev/serial/by-id/

# Résultat exemple:
# usb-1a86_USB_Serial-if00-port0 -> ../../ttyUSB1
```

### 2️⃣ Configuration docker-compose.yml

```yaml
services:
  homeassistant:
    image: ghcr.io/home-assistant/home-assistant:2026.4.4
    privileged: true
    
    devices:
      # Docker crée /dev/lcus_relay dans le conteneur
      - /dev/serial/by-id/usb-1a86_USB_Serial-if00-port0:/dev/lcus_relay
```

### Redémarrer le conteneur :

```bash
docker-compose down && docker-compose up -d
```

### Vérifier :

```bash
# Le symlink doit être visible dans le conteneur
docker exec homeassistant ls -l /dev/lcus_relay

# Tester la connexion
docker exec homeassistant python3 -c "
import serial
s = serial.Serial('/dev/lcus_relay', 9600, timeout=1)
print('✓ Symlink fonctionne \!')
s.close()
"
```

---

## 📋 Explication

**`device_cgroup_rules`** :
- `c` = character device (périphérique série)
- `188` = Major number des devices ttyUSB* sous Linux
- `*` = Tous les minor numbers (ttyUSB0, ttyUSB1, ttyUSB2, etc.)
- `rwm` = Read, Write, Mknod (permissions complètes)

**Résultat** : Le conteneur peut maintenant accéder à **tous** les ports série USB, ce qui permet au symlink `/dev/lcus_relay` (qui pointe vers ttyUSB0 ou ttyUSB1) de fonctionner automatiquement.

---

## 🔄 Avantages

✅ **Automatique** : `/dev/serial/by-id/` créé par le système  
✅ **Stable** : Même si le port change (ttyUSB0 → ttyUSB1)  
✅ **Simple** : Aucune règle udev personnalisée requise  
✅ **Propre** : Docker crée `/dev/lcus_relay` directement dans le conteneur  

---

## 📋 Pourquoi ça fonctionne ?

`/dev/serial/by-id/` contient des liens symboliques créés automatiquement par `udev` basés sur :
- Vendor ID (idVendor)
- Product ID (idProduct)
- Numéro de série (si disponible)

Docker peut **mapper directement** ces liens et les créer dans le conteneur sous le nom de votre choix (`/dev/lcus_relay`).

---

## ✅ Configuration finale recommandée

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
    privileged: true
    network_mode: host
    
    # 🔑 CLÉ DU SUCCÈS : device_cgroup_rules
    device_cgroup_rules:
      - 'c 188:* rwm'  # Autoriser tous les ttyUSB*
    
    volumes:
      - /opt/docker/hass/config:/config
      - /etc/localtime:/etc/localtime:ro
    
    devices:
      - /dev/lcus_relay:/dev/lcus_relay  # Symlink udev
    
    depends_on:
      - matter-server
```

**Dans Home Assistant** : Utiliser le port `/dev/lcus_relay` ✓

---

## 🎉 Résultat attendu

```bash
cyril@odroid-m1s:~$ docker exec homeassistant ls -l /dev/lcus_relay
lrwxrwxrwx 1 root root 7 Aug 25 14:30 /dev/lcus_relay -> ttyUSB1

cyril@odroid-m1s:~$ docker exec homeassistant python3 -c "import serial; s=serial.Serial('/dev/lcus_relay', 9600); print('✓ OK'); s.close()"
✓ OK
```

Le port peut changer de `ttyUSB0` à `ttyUSB1`, mais `/dev/lcus_relay` suivra automatiquement \! 🚀
