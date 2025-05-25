# Décision 
    Utiliser une architecture en couches:
        - UI (Console pour labo 1)

        - Service layer (gestion stocks et transactions)

        - DAO (acces via SQLite)

# Contexte :

    Séparer les responsabilités rend le code testable, maintenable et extensible.

    Plus de cohérence

# Conséquences :

    Le code de la logique métier peut être testé indépendamment de la console

    Les mécanismes de persistance sont facilement échangeables (JSON ou SQLite)

    La logique métier n'est pas couplée à la persistance

    Possibilité de remplacer la base de données ou d’ajouter une interface graphique plus tard