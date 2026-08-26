# Utilisation avec un émetteur Somfy IZYMO io (réf. 5135163)

## Présentation

Le **Somfy IZYMO Transmitter io** (commercialisé sous plusieurs références selon les distributeurs, dont **5135163**, la référence Somfy d'origine étant 1822609) est un micro-émetteur qui se raccorde derrière un point de commande filaire (bouton poussoir ou interrupteur va-et-vient) et transforme cet appui en ordre radio **io-homecontrol** vers un volet roulant, un store ou un éclairage.

Ce module ne pilote pas le moteur directement : il se contente d'écouter deux entrées filaires (montée / descente ou ON / OFF) et de retransmettre l'ordre en radio. C'est exactement le rôle que joue une télécommande filaire classique — ce qui le rend compatible avec cette intégration : **le module relais USB vient simplement remplacer les boutons poussoirs physiques du point de commande**.

## Principe de câblage

Le relais USB ne se connecte donc pas au moteur, mais aux bornes d'entrée de l'IZYMO :

| Relais | IZYMO (bornes point de commande) |
|---|---|
| Canal 1 (Ouvrir) | Entrée « Montée » + Commun |
| Canal 2 (Fermer) | Entrée « Descente » + Commun |

Chaque canal du relais se comporte comme un appui bref sur le bouton poussoir correspondant. Les deux canaux partagent le fil commun du point de commande, exactement comme les deux boutons d'un interrupteur double.

⚠️ Coupez l'alimentation du point de commande avant toute intervention, et référez-vous à la notice Somfy fournie avec le module pour l'identification exacte des bornes (elle peut varier selon le mode de câblage : bouton poussoir simple, double bouton poussoir, ou va-et-vient).

## Mode de l'IZYMO

Par défaut, l'IZYMO est en **Mode 1 (Bouton poussoir)**, qui correspond à un appui court pour déclencher un ordre. C'est le mode à utiliser avec cette intégration — pas besoin de le modifier via l'appui long sur le bouton MODE du module.

## Configuration recommandée de l'intégration

Comme l'IZYMO attend une simple impulsion (et non un maintien), utilisez le **[mode Impulsion Courte](MODE_IMPULSION.md)** :

```
Mode : Impulsion courte
Durée impulsion courte : 500 ms
```

## Arrêt en cours de mouvement (position intermédiaire)

Comme la plupart des moteurs io-homecontrol / RTS, un volet piloté via l'IZYMO s'arrête en cours de course en recevant **un nouvel ordre dans le même sens** (ex. un second ordre « Montée » alors que le volet monte déjà), et non par une simple absence de signal. Un appui bref sur le bouton poussoir raccordé à l'IZYMO produit exactement ce comportement : premier appui = démarrage, second appui = arrêt.

L'intégration reproduit ce fonctionnement : `cover.stop_cover` renvoie une nouvelle impulsion sur le canal actuellement actif (montée ou descente) plutôt que de simplement couper un relais déjà retombé depuis longtemps après l'impulsion initiale. C'est ce qui permet à un script comme celui-ci de fonctionner :

```yaml
script:
  volet_mi_ouvert:
    sequence:
      - service: cover.open_cover
        target:
          entity_id: cover.volet_salon
      - delay:
          seconds: 15  # Moitié du temps de course
      - service: cover.stop_cover
        target:
          entity_id: cover.volet_salon
```

`cover.open_cover` déclenche l'impulsion « Montée » (relais actif ~500 ms puis relâché, le volet continue de monter tout seul comme avec le bouton poussoir physique), le `delay` s'écoule pendant que le volet monte, puis `cover.stop_cover` envoie une nouvelle impulsion « Montée » qui arrête réellement le volet à mi-course — comme un second appui sur le bouton poussoir raccordé à l'IZYMO.

## Dépannage spécifique

- **Le volet ne bouge pas** : vérifiez que l'IZYMO est bien apparié (associé) avec le moteur io du volet via la procédure Somfy standard (appui sur la touche PROG du moteur) — cette intégration ne fait que simuler l'appui bouton, elle ne gère pas l'appairage radio.
- **Un seul sens fonctionne** : contrôlez le câblage du canal concerné sur les bornes de l'IZYMO, ou inversez le canal défectueux via l'option **« Inverser le sens des relais »** dans la configuration de l'intégration.
- **Rien ne se passe malgré une impulsion correcte** : augmentez légèrement la durée d'impulsion (500 ms → 600 ms, la valeur maximale), certains IZYMO nécessitent un appui légèrement plus long que 200-300 ms pour être détectés comme un appui valide.
