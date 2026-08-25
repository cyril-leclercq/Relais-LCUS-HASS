# Guide de Publication sur GitHub pour HACS

## 📋 Checklist avant publication

- [x] Intégration créée dans `custom_components/volet_relais_usb/`
- [x] Fichier `manifest.json` configuré
- [x] Fichier `hacs.json` créé
- [x] Documentation complète (README, HACS_INSTALLATION, etc.)
- [x] Traductions (FR/EN)
- [x] Licence ajoutée (MIT)
- [ ] Créer un dépôt GitHub
- [ ] Pousser le code
- [ ] Créer une release
- [ ] Soumettre à HACS (optionnel)

---

## 🚀 Étapes de publication

### 1. Créer un dépôt GitHub

1. Allez sur https://github.com/new
2. Nom du dépôt : `Relais-LCUS-HASS`
3. Description : "Intégration Home Assistant pour volet roulant via relais USB"
4. Public ✅
5. **Ne pas** initialiser avec README (on a déjà le nôtre)
6. Cliquez sur **Create repository**

### 2. Pousser le code vers GitHub

```bash
# Dans le répertoire /Users/zunix/Src/relais

# Configurer le remote
git remote add origin https://github.com/cyril-leclercq/Relais-LCUS-HASS.git

# Pousser le code
git push -u origin main
```

### 3. Créer une release (version)

#### Via l'interface GitHub

1. Allez dans votre dépôt GitHub
2. Cliquez sur **Releases** (à droite)
3. Cliquez sur **Create a new release**
4. Tag version : `v1.0.0`
5. Release title : `v1.0.0 - Version initiale`
6. Description :
   ```markdown
   ## 🎉 Première version

   ### Fonctionnalités
   - ✅ Configuration via l'UI Home Assistant
   - ✅ Support HACS
   - ✅ Compatible Docker/Swarm
   - ✅ Traductions FR/EN
   - ✅ Protection anti-surchauffe

   ### Installation
   Voir [HACS_INSTALLATION.md](HACS_INSTALLATION.md)
   ```
7. Cliquez sur **Publish release**

#### Via la ligne de commande

```bash
# Créer un tag
git tag -a v1.0.0 -m "Version initiale"

# Pousser le tag
git push origin v1.0.0
```

### 4. Vérifier l'installation HACS

#### Installation par vos utilisateurs

Vos utilisateurs pourront maintenant installer l'intégration :

1. **HACS** → **Intégrations**
2. **⋮** (3 points) → **Dépôts personnalisés**
3. URL : `https://github.com/cyril-leclercq/Relais-LCUS-HASS`
4. Catégorie : **Integration**
5. **Ajouter**

### 5. (Optionnel) Soumettre à HACS par défaut

Pour que votre intégration apparaisse directement dans HACS sans ajout manuel :

1. Fork https://github.com/hacs/default
2. Modifiez `integration` dans votre fork
3. Ajoutez votre dépôt :
   ```json
   {
     "name": "Volet Roulant Relais USB",
     "domain": "volet_relais_usb",
     "description": "Contrôle de volet roulant via relais USB"
   }
   ```
4. Créez une Pull Request
5. Attendez la validation HACS

**Note** : La validation peut prendre plusieurs jours. En attendant, les utilisateurs peuvent l'installer comme dépôt personnalisé.

---

## 📝 Mises à jour futures

### Créer une nouvelle version

```bash
# 1. Modifier le code
# 2. Mettre à jour manifest.json (version)
nano custom_components/volet_relais_usb/manifest.json
# Changez "version": "1.0.0" en "version": "1.1.0"

# 3. Commit
git add .
git commit -m "Version 1.1.0 - Ajout fonctionnalité X"

# 4. Tag
git tag -a v1.1.0 -m "Version 1.1.0"

# 5. Push
git push origin main
git push origin v1.1.0

# 6. Créer une release sur GitHub
```

### HACS détectera automatiquement la nouvelle version

Les utilisateurs verront une notification de mise à jour dans HACS.

---

## 🔍 Validation de l'intégration

### Vérifier que tout fonctionne

1. **Cloner le dépôt** dans un autre répertoire :
   ```bash
   cd /tmp
   git clone https://github.com/cyril-leclercq/Relais-LCUS-HASS.git
   ```

2. **Vérifier la structure** :
   ```bash
   cd volet-relais-usb
   tree custom_components/volet_relais_usb/
   ```

3. **Vérifier les fichiers requis** :
   - ✅ `manifest.json`
   - ✅ `__init__.py`
   - ✅ `config_flow.py`
   - ✅ `hacs.json`
   - ✅ `README.md`

4. **Tester l'installation HACS** :
   - Ajoutez le dépôt comme dépôt personnalisé dans HACS
   - Vérifiez que l'installation fonctionne
   - Vérifiez que la configuration UI s'affiche

---

## 📚 Ressources

- **HACS Documentation** : https://hacs.xyz/docs/publish/integration
- **Home Assistant Dev Docs** : https://developers.home-assistant.io/
- **Validation HACS** : https://github.com/hacs/default

---

## ✅ Résumé des commandes

```bash
# Configurer le remote GitHub
git remote add origin https://github.com/cyril-leclercq/Relais-LCUS-HASS.git

# Pousser le code
git push -u origin main

# Créer et pousser un tag
git tag -a v1.0.0 -m "Version initiale"
git push origin v1.0.0

# Mettre à jour
git commit -am "Mise à jour X"
git tag -a v1.1.0 -m "Version 1.1.0"
git push origin main
git push origin v1.1.0
```

---

## 🎉 Félicitations !

Votre intégration est maintenant disponible pour la communauté Home Assistant !

Les utilisateurs peuvent l'installer via HACS en ajoutant votre dépôt comme source personnalisée.
