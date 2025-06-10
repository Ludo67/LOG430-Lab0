"""Initialisation de la base de données."""
import sqlite3
import os
from data_access_layer.schema import create_tables

db_path = os.path.join(os.path.dirname(__file__), "produits.db")
conn = sqlite3.connect(db_path)

# Créer les tables
create_tables(conn)

# Remplir quelques magasins et produits
with conn:
    conn.execute("INSERT OR IGNORE INTO magasins (id, nom) VALUES (?, ?)", ("M001", "Magasin A"))
    conn.execute("INSERT OR IGNORE INTO magasins (id, nom) VALUES (?, ?)", ("M002", "Magasin B"))

    produits = [
        ("P001", "Clavier Logitech", "Périphérique", 39.99, 20, "M001"),
        ("P002", "Souris HP", "Périphérique", 24.99, 35, "M001"),
        ("P003", "Écran Samsung 24\"", "Affichage", 149.99, 10, "M002"),
        ("P004", "Ordinateur portable Dell", "Informatique", 999.99, 5, "M002"),
        ("P005", "Casque audio Sony", "Audio", 59.99, 15, "M001")
    ]

    for p in produits:
        conn.execute("INSERT OR REPLACE INTO produits VALUES (?, ?, ?, ?, ?, ?)", p)

print("✅ Base initialisée avec magasins, produits et structure des ventes.")
conn.close()
