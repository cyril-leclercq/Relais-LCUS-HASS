# Mode d'Impulsion - Documentation

## Vue d'ensemble

L'intégration Volet Roulant Relais USB propose deux modes de fonctionnement pour contrôler vos volets roulants. Ces modes permettent d'adapter le comportement de l'intégration à votre type de motorisation.

## Les Deux Modes

### ⚡ Mode Impulsion Courte (50 - 600 ms)

**Utilisation recommandée :** Volets motorisés avec électronique de contrôle intégrée.

Ce mode active le relais très brièvement, simulant un appui sur un bouton poussoir. C'est l'équivalent d'une impulsion électrique courte.

**Caractéristiques :**
- Durée réglable : 50 à 600 millisecondes
- Valeur par défaut : 500 ms
- Le relais s'active puis se désactive automatiquement après la durée configurée

**Cas d'usage typiques :**
- Moteurs de volets avec commande filaire à bouton poussoir
- Motorisations avec fin de course automatique
- Systèmes où une simple impulsion déclenche le mouvement complet

**Avantages :**
- ✅ Économie d'énergie
- ✅ Moins de sollicitation du relais
- ✅ Compatible avec la plupart des moteurs modernes
- ✅ Évite les blocages en fin de course

### ⏱️ Mode Maintenu (2 secondes - 2 minutes)

**Utilisation recommandée :** Volets nécessitant une alimentation continue pendant le mouvement.

Ce mode garde le relais activé pendant toute la durée configurée, fournissant une alimentation continue au moteur.

**Caractéristiques :**
- Durée réglable : 2 secondes à 2 minutes (120 secondes)
- Valeur par défaut : 30 secondes
- Le relais reste activé pendant toute la durée

**Cas d'usage typiques :**
- Moteurs nécessitant une alimentation continue
- Volets sans fin de course automatique
- Motorisations anciennes ou basiques
- Contrôle manuel de la durée de mouvement

**Avantages :**
- ✅ Contrôle précis de la durée de mouvement
- ✅ Compatible avec les moteurs simples
- ✅ Permet un positionnement partiel du volet

## Configuration

### Lors de l'installation initiale

1. Allez dans **Paramètres** → **Appareils et services**
2. Cliquez sur **Ajouter une intégration**
3. Recherchez **Volet Roulant Relais USB**
4. Remplissez le formulaire :
   - **Nom** : Nom de votre volet (ex: "Volet Salon")
   - **Port USB** : Port série du module relais (ex: /dev/ttyUSB0)
   - **Mode d'impulsion** : Choisissez entre "Impulsion courte" ou "Maintenu"
   - **Inverser le sens** : Cochez si montée/descente sont inversés
5. À l'étape suivante, seul le champ de durée correspondant au mode choisi s'affiche :
   - **Durée impulsion courte (ms)** si vous avez choisi "Impulsion courte"
   - **Durée maintenu (secondes)** si vous avez choisi "Maintenu"

### Modification des paramètres

1. Allez dans **Paramètres** → **Appareils et services**
2. Trouvez votre intégration **Volet Roulant Relais USB**
3. Cliquez sur **Configurer**
4. Modifiez les paramètres selon vos besoins
5. Cliquez sur **Soumettre**

Les modifications sont appliquées immédiatement après le rechargement de l'intégration.

## Comment choisir le bon mode ?

### Utilisez le Mode Impulsion Courte si :
- ❓ Votre volet fonctionne avec des boutons poussoirs (et non des interrupteurs)
- ❓ Le moteur continue de tourner après avoir relâché le bouton
- ❓ Le volet s'arrête automatiquement en fin de course
- ❓ Une impulsion suffit pour déclencher le mouvement complet

### Utilisez le Mode Maintenu si :
- ❓ Votre volet nécessite de maintenir le bouton appuyé pour bouger
- ❓ Le moteur s'arrête dès que vous relâchez le bouton
- ❓ Le volet n'a pas de fin de course automatique
- ❓ Vous devez contrôler manuellement la durée du mouvement

## Réglage fin des durées

### Pour le Mode Impulsion Courte

Commencez par une valeur basse et augmentez progressivement :

1. **50 ms** : Pour les systèmes très réactifs
2. **500 ms** : Valeur recommandée par défaut
3. **600 ms** : Si le système nécessite une impulsion plus longue

**Test :** Après chaque changement, testez l'ouverture et la fermeture. Si le volet ne réagit pas, augmentez légèrement la durée.

### Pour le Mode Maintenu

La durée doit correspondre au temps nécessaire pour une course complète :

1. **Chronométrez** le temps que met votre volet pour monter ou descendre complètement
2. **Ajoutez une marge** de sécurité de 2-3 secondes
3. **Testez** et ajustez si nécessaire

**Exemple :** Si votre volet met 28 secondes à se fermer complètement, configurez 30 secondes.

## Dépannage

### Le volet ne réagit pas aux commandes
- ✔️ Vérifiez que le bon mode est sélectionné
- ✔️ En mode impulsion courte : augmentez la durée (500 ms → 600 ms)
- ✔️ Vérifiez le câblage et les connexions du relais

### Le volet ne s'arrête pas en fin de course
- ✔️ Assurez-vous que votre moteur a des fins de course automatiques
- ✔️ Si non, passez en mode maintenu avec une durée adaptée

### Le volet s'inverse tout seul
- ✔️ Activez l'option "Inverser le sens des relais"
- ✔️ Vérifiez le câblage des canaux du relais

### Le mouvement est incomplet
- ✔️ En mode impulsion courte : augmentez légèrement la durée
- ✔️ En mode maintenu : augmentez la durée configurée

## Sécurité

⚠️ **Durée maximale de sécurité** : Le système limite automatiquement la durée d'activation à 120 secondes (2 minutes) pour éviter tout dysfonctionnement.

## Exemples de configuration

### Configuration 1 : Volet moderne avec moteur radio
```
Mode : Impulsion courte
Durée impulsion courte : 500 ms
```

### Configuration 2 : Volet ancien sans fin de course
```
Mode : Maintenu
Durée maintenu : 35 secondes
```

### Configuration 3 : Store banne motorisé
```
Mode : Impulsion courte
Durée impulsion courte : 600 ms
```

### Configuration 4 : Volet radio via émetteur Somfy IZYMO io (réf. 5135163)
```
Mode : Impulsion courte
Durée impulsion courte : 500 ms
```
Voir le guide dédié : [SOMFY_IZYMO.md](SOMFY_IZYMO.md)

## Support

Pour toute question ou problème, consultez :
- Le README principal du projet
- Les issues sur GitHub
- La documentation Home Assistant
