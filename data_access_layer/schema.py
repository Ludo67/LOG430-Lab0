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
