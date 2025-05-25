"""Module d'accès aux données pour les produits (SQLite)."""

import os
import sqlite3
from data_access_layer.schema import CREATE_PRODUITS_TABLE

DB_PATH = os.path.join(os.path.dirname(__file__), "produits.db")

class ProduitDAO:
    """DAO pour gérer les produits dans une base SQLite."""

    def __init__(self, db_path=None):
        """Initialise la connexion et crée la table si nécessaire."""
        path = db_path or DB_PATH
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        """Crée la table 'produits' si elle n'existe pas."""
        with self.conn:
            self.conn.execute(CREATE_PRODUITS_TABLE)

    def get_all(self):
        """Retourne tous les produits sous forme de liste de dictionnaires."""
        cursor = self.conn.execute("SELECT * FROM produits")
        return [dict(row) for row in cursor.fetchall()]

    def get_by_id(self, produit_id):
        """Retourne un produit par son ID."""
        cursor = self.conn.execute(
            "SELECT * FROM produits WHERE id = ?", (produit_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def rechercher(self, terme):
        """Recherche un produit par id, nom ou catégorie (LIKE)."""
        cursor = self.conn.execute(
            """
            SELECT * FROM produits
            WHERE id LIKE ? OR nom LIKE ? OR categorie LIKE ?
            """,
            (f"%{terme}%", f"%{terme}%", f"%{terme}%")
        )
        return [dict(row) for row in cursor.fetchall()]

    def update(self, produit):
        """Insère ou met à jour un produit selon son ID."""
        with self.conn:
            self.conn.execute(
                """
                INSERT OR REPLACE INTO produits (id, nom, categorie, prix, quantite)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    produit["id"],
                    produit["nom"],
                    produit["categorie"],
                    produit["prix"],
                    produit["quantite"]
                )
            )

    def close(self):
        """Ferme la connexion à la base de données."""
        self.conn.close()
