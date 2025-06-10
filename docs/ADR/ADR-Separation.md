## Statut : Accepté
## Date : 2025-06-09
## Décision
    Utilisation d’une architecture en 3 couches (présentation, service, accès aux données).
## Contexte :
    Le projet devait s'étendre dans les labos suivants, notamment pour prendre en charge de nouveaux UC (UC4–UC7 qui n'ont pas été implémentées encore à cette étape). La modularité et la testabilité devenaient cruciales.

## Choix possibles

    Application monolithique dans un seul fichier (rapide, mais non maintenable).

    Architecture MVC : autre option possible et interessante (plus utile pour utilisation web)

    Architecture en couches : claire, modulaire, évolutive.

## Conséquences

    Le dossier presentation_layer gère l'IHM en console.

    Le dossier service_layer isole la logique métier.

    Le dossier data_access_layer encapsule les opérations SQLite.

    Les tests peuvent être faits indépendamment sur chaque couche.