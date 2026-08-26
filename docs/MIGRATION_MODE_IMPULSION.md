# Guide de Migration - Mode d'Impulsion

## Pour les utilisateurs existants

Si vous avez déjà installé l'intégration Volet Roulant Relais USB avant l'ajout du mode d'impulsion, voici comment mettre à jour votre configuration.

## Que change cette mise à jour ?

### Nouveaux paramètres disponibles

L'intégration propose maintenant deux modes de fonctionnement :

1. **Mode Impulsion Courte** (0.2 - 1 seconde)
   - Pour volets avec commande bouton poussoir
   - Activation brève du relais
   
2. **Mode Maintenu** (2 secondes - 2 minutes)
   - Pour volets nécessitant une alimentation continue
   - Le relais reste activé pendant toute la durée

## Migration automatique

**Bonne nouvelle !** Si vous ne faites rien, votre configuration existante continuera de fonctionner avec les valeurs par défaut :
- Mode : Impulsion courte
- Durée impulsion courte : 0.5 seconde
- Durée maintenu : 30 secondes

Votre paramètre "Temps de course" existant est conservé.

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
