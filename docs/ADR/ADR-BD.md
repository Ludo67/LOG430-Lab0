## Statut : Accepté
## Date : 2025-06-09
## Décision 
    Utilisation de SQLite comme base de données relationnelle locale.

## Contexte
    Le système de gestion de stock devait persister les produits, magasins et ventes. Les exigences précisaient qu’aucun serveur HTTP ou API REST n'était requis, et que la base devait fonctionner localement sur la VM.

## Choix possibles

    JSON/CSV : trop fragile pour la cohérence transactionnelle.

    MongoDB (NoSQL) et PostgreSQL: trop complexe pour un usage local et non nécessaire.

    SQLite : simple, léger, intégré avec Python, supporte les contraintes (clés primaires composées, jointures).

## Conséquences

    Facile à intégrer sans configuration serveur.

    Compatible avec le module sqlite3 natif.

    Limite la scalabilité en cas d’accès concurrent élevé