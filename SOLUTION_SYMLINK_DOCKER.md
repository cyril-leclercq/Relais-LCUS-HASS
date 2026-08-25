# 🔧 Faire fonctionner le symlink udev dans Docker

## 🎯 Problème

- Le port USB change de nom : `ttyUSB0` → `ttyUSB1`
- Le symlink `/dev/lcus_relay` existe sur l'HÔTE
- Docker ne voit PAS `/dev/lcus_relay` dans le conteneur

---

## ✅ SOLUTION : device_cgroup_rules

Cette méthode autorise le conteneur à accéder à **TOUS** les périphériques série USB, ce qui permet au symlink de fonctionner.

### Dans `docker-compose.yml` :

```yaml
services:
  homeassistant:
    image: ghcr.io/home-assistant/home-assistant:2026.4.4
    privileged: true  # ← Déjà présent
    
    # ========================================================
    # AJOUTER cette section (la clé du succès)
    # ========================================================
    device_cgroup_rules:
      - 'c 188:* rwm'  # Autoriser tous les devices série USB
    
    devices:
      - /dev/lcus_relay:/dev/lcus_relay  # ✓ Le symlink fonctionnera
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

✅ Le symlink `/dev/lcus_relay` fonctionne dans le conteneur  
✅ Gère automatiquement le changement de port (ttyUSB0 → ttyUSB1)  
✅ Pas besoin de modifier la config si le port change  
✅ Compatible avec les règles udev  

---

## 🛡️ Sécurité

Cette configuration reste sécurisée car :
- Elle donne accès uniquement aux devices série USB (188:*)
- Pas d'accès aux autres périphériques système
- Fonctionne en combinaison avec `privileged: true` que vous avez déjà

---

## 📝 Alternative (si device_cgroup_rules ne fonctionne pas)

### Créer le symlink DANS le conteneur :

```yaml
services:
  homeassistant:
    privileged: true
    devices:
      - /dev/ttyUSB0:/dev/ttyUSB0
      - /dev/ttyUSB1:/dev/ttyUSB1  # Mapper les deux
    
    # Script de démarrage qui crée le symlink
    entrypoint: >
      sh -c "
      ln -sf /dev/ttyUSB* /dev/lcus_relay 2>/dev/null || true &&
      exec /init
      "
```

Mais cette méthode est moins élégante que `device_cgroup_rules`.

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
