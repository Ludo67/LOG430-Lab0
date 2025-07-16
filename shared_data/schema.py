"""Définit le schéma de la base de données."""

def create_tables(conn):
    """Crée les tables dans la base de données."""
    with conn:
        # Table des magasins
        conn.execute("""
            CREATE TABLE IF NOT EXISTS magasins (
                id TEXT PRIMARY KEY,
                nom TEXT NOT NULL
            )
        """)

        # Table des produits
        conn.execute("""
            CREATE TABLE IF NOT EXISTS produits (
                id TEXT,
                nom TEXT,
                categorie TEXT,
                prix REAL,
                quantite INTEGER,
                magasin_id TEXT,
                PRIMARY KEY (id, magasin_id)
            )
        """)


        # Table des ventes
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ventes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produit_id TEXT,
                quantite INTEGER,
                magasin_id TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Table des clients
        conn.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id TEXT PRIMARY KEY,
                nom TEXT NOT NULL,
                courriel TEXT NOT NULL UNIQUE
            )
        """)

        # # Table des paniers
        # conn.execute("""
        #     CREATE TABLE IF NOT EXISTS paniers (
        #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         client_id TEXT NOT NULL,
        #         produit_id TEXT NOT NULL,
        #         quantite INTEGER NOT NULL,
        #         magasin_id TEXT NOT NULL,
        #         FOREIGN KEY (client_id) REFERENCES clients(id)
        #     )
        # """)

        # # Table des commandes
        # conn.execute("""
        #     CREATE TABLE IF NOT EXISTS commandes (
        #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         client_id TEXT NOT NULL,
        #         total REAL NOT NULL,
        #         date_commande DATETIME DEFAULT CURRENT_TIMESTAMP,
        #         statut TEXT DEFAULT 'en_attente',
        #         FOREIGN KEY (client_id) REFERENCES clients(id)
        #     )
        # """)
