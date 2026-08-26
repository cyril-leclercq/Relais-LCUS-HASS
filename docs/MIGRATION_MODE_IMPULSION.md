# Guide de Migration - Mode d'Impulsion

## Pour les utilisateurs existants

Si vous avez déjà installé l'intégration Volet Roulant Relais USB avant l'ajout du mode d'impulsion, voici comment mettre à jour votre configuration.

## Que change cette mise à jour ?

### Nouveaux paramètres disponibles

L'intégration propose maintenant deux modes de fonctionnement :

1. **Mode Impulsion Courte** (50 - 600 ms)
   - Pour volets avec commande bouton poussoir
   - Activation brève du relais
   
2. **Mode Maintenu** (2 secondes - 2 minutes)
   - Pour volets nécessitant une alimentation continue
   - Le relais reste activé pendant toute la durée

## Migration automatique

**Bonne nouvelle !** Si vous ne faites rien, votre configuration existante continuera de fonctionner avec les valeurs par défaut :
- Mode : Impulsion courte
- Durée impulsion courte : 500 ms
- Durée maintenu : 30 secondes

ℹ️ **Paramètre "Temps de course" retiré** : ce champ n'était en réalité jamais utilisé par l'intégration (aucun calcul de position n'en dépendait) et a été retiré du formulaire. Aucune action requise si vous l'aviez configuré : il est simplement ignoré.

ℹ️ **Unité de la durée d'impulsion courte** : ce champ est désormais exprimé en millisecondes (50 à 600 ms) plutôt qu'en secondes. Si votre configuration existante stockait encore une valeur en secondes (ex: 0.5), elle est automatiquement convertie en millisecondes (500 ms) à l'ouverture de l'intégration — aucune action requise.

ℹ️ **Formulaire en deux étapes** : lors de la configuration ou de la modification des options, seul le champ de durée correspondant au mode d'impulsion choisi s'affiche désormais (plus besoin de voir "Durée impulsion courte" quand vous êtes en mode Maintenu, et inversement).

## Mettre à jour votre configuration

### Option 1 : Via l'interface Home Assistant

1. Allez dans **Paramètres** → **Appareils et services**
2. Trouvez **Volet Roulant Relais USB**
3. Cliquez sur **Configurer**
4. Vous verrez les nouveaux paramètres :
   - Mode d'impulsion
   - Durée impulsion courte
   - Durée maintenu
5. Ajustez selon vos besoins
6. Cliquez sur **Soumettre**

### Option 2 : Réinstallation complète (recommandé pour une configuration propre)

1. **Supprimez** l'intégration existante
2. **Ajoutez** à nouveau l'intégration
3. Configurez tous les paramètres incluant les nouveaux modes

⚠️ **Note** : Vous perdrez l'historique de l'entité avec cette méthode.

## Compatibilité

### Si votre volet fonctionnait avant

Votre configuration existante devrait continuer de fonctionner. Les valeurs par défaut sont conçues pour être compatibles avec la plupart des installations.

### Si vous rencontrez des problèmes après la mise à jour

1. **Le volet ne répond plus** :
   - Passez en mode "Maintenu"
   - Configurez une durée égale à votre ancien "temps de course"

2. **Le comportement a changé** :
   - Vérifiez les nouveaux paramètres dans la configuration
   - Ajustez le mode selon votre type de motorisation

## Vérification post-migration

Testez les fonctions de base :
- ✅ Ouvrir le volet
- ✅ Fermer le volet
- ✅ Arrêter le volet

Si tout fonctionne, la migration est réussie !

## Optimisation recommandée

Pour tirer le meilleur parti de la nouvelle fonctionnalité :

1. **Identifiez votre type de moteur** (voir [MODE_IMPULSION.md](MODE_IMPULSION.md))
2. **Sélectionnez le mode approprié**
3. **Ajustez finement les durées** selon vos tests

## Besoin d'aide ?

Consultez la documentation complète : [MODE_IMPULSION.md](MODE_IMPULSION.md)
