# Saga Orchestrée – Scénario métier
Le scénario métier implémente une commande client orchestrée en plusieurs étapes critiques :

Création du client s’il n’existe pas déjà.

Création du panier pour ce client.

Ajout des produits dans le panier.

Vérification du stock dans les magasins.

Confirmation de la commande.

Si une erreur survient à une étape, un rollback (compensation) est exécuté. Exemple : si le stock est insuffisant, on annule la commande.

# Machine d'état de la saga
CREEE --> CLIENT_CREE
CLIENT_CREE --> STOCK_VERIFIE
CLIENT_CREE --> PANIER_CREE
PANIER_CREE --> STOCK_VERIFIE
STOCK_VERIFIE --> COMMANDE_CONFIRMEE
STOCK_VERIFIE --> CHECKOUT_ECHOUE

# Mécanismes de compensation
Si erreur, alors :

Les items du panier sont enlevés

Aucun produit n’est vendu.

La commande est annulée dans l’orchestrateur.

Si la création du client ou du panier échoue, la saga s’arrête immédiatement, sans propagation.