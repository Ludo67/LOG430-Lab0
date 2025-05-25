"""Initialise la base SQLite avec des produits de test."""

import os
import sqlite3
from data_access_layer.schema import CREATE_PRODUITS_TABLE

DB_PATH = os.path.join(os.path.dirname(__file__), "produits.db")

PRODUITS = [
    ("P001", "Clavier Logitech", "Périphérique", 39.99, 20),
    ("P002", "Souris HP", "Périphérique", 24.99, 35),
    ("P003", "Écran Samsung 24\"", "Affichage", 149.99, 10),
    ("P004", "Ordinateur portable Dell", "Informatique", 999.99, 5),
    ("P005", "Casque audio Sony", "Audio", 59.99, 15)
]

def init_db():
    """Crée la table produits et insère des entrées de test."""
    conn = sqlite3.connect(DB_PATH)
    try:
        with conn:
            conn.execute(CREATE_PRODUITS_TABLE)
            for produit in PRODUITS:
                print(f"Insertion de : {produit}")
                conn.execute(
                    "INSERT OR REPLACE INTO produits VALUES (?, ?, ?, ?, ?)",
                    produit
                )
        print("✅ Données insérées avec succès.")
    except sqlite3.Error as error:
        print(f"❌ Erreur SQLite : {error}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
