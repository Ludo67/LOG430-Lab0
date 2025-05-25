"""Définit le schéma SQL utilisé pour la base de données produits."""

CREATE_PRODUITS_TABLE = """
    CREATE TABLE IF NOT EXISTS produits (
        id TEXT PRIMARY KEY,
        nom TEXT NOT NULL,
        categorie TEXT,
        prix REAL,
        quantite INTEGER
    )
"""
