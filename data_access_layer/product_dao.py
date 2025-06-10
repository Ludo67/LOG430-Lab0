"Data Access Object (DAO) pour gérer les opérations sur les produits dans la base de données."
import sqlite3
from data_access_layer.schema import create_tables


class ProduitDAO:
    """Classe permettant les opérations CRUD sur les produits."""

    def __init__(self, db_path="data_access_layer/produits.db"):
        """
        Initialise le DAO avec le chemin de la base de données.
        :param db_path: Chemin vers le fichier de base de données SQLite.
        """
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        """
        Crée les tables nécessaires dans la base de données.
        Cette méthode est appelée lors de l'initialisation du DAO.
        """
        create_tables(self.conn)

    def get_all(self):
        """
        Récupère tous les produits de la base de données.
        :return: Liste de dictionnaires représentant les produits.
        """
        cursor = self.conn.execute("SELECT * FROM produits")
        return [dict(row) for row in cursor.fetchall()]

    def get_by_id(self, produit_id, magasin_id):
        """
        Récupère un produit par son ID et l'ID du magasin.
        :param produit_id: ID du produit à récupérer.
        :param magasin_id: ID du magasin auquel le produit appartient.
        :return: Dictionnaire représentant le produit, ou None si non trouvé.
        """
        cursor = self.conn.execute(
            "SELECT * FROM produits WHERE id = ? AND magasin_id = ?", (produit_id, magasin_id)
        )
        return cursor.fetchone()

    def rechercher(self, terme):
        """
        Recherche des produits par un terme dans l'ID, le nom ou la catégorie.
        :param terme: Terme de recherche.
        :return: Liste de dictionnaires représentant les produits correspondants.
        """
        cursor = self.conn.execute("""
            SELECT * FROM produits
            WHERE id LIKE ? OR nom LIKE ? OR categorie LIKE ?
        """, (f"%{terme}%", f"%{terme}%", f"%{terme}%"))
        return [dict(row) for row in cursor.fetchall()]

    def update(self, produit):
        """
        Met à jour un produit dans la base de données.
        :param produit: Dictionnaire représentant le produit à mettre à jour.
        """
        self.conn.execute("""
            UPDATE produits SET nom = ?, categorie = ?, prix = ?, quantite = ?
            WHERE id = ? AND magasin_id = ?
        """, (produit["nom"], produit["categorie"], produit["prix"],
              produit["quantite"], produit["id"], produit["magasin_id"]))
        self.conn.commit()

    def insert(self, produit):
        """
        Insère un nouveau produit dans la base de données.
        :param produit: Dictionnaire représentant le produit à insérer.
        """
        self.conn.execute("""
            INSERT INTO produits (id, nom, categorie, prix, quantite, magasin_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (produit["id"], produit["nom"], produit["categorie"], produit["prix"],
               produit["quantite"], produit["magasin_id"]))
        self.conn.commit()

    def get_ventes_par_magasin(self):
        """
        Récupère le total des ventes par magasin.
        :return: Dictionnaire avec l'ID du magasin comme clé et le total des ventes comme valeur.
        """
        cursor = self.conn.execute("""
            SELECT magasin_id, SUM(quantite) as total
            FROM ventes
            GROUP BY magasin_id
        """)
        return {row["magasin_id"]: row["total"] for row in cursor.fetchall()}

    def close(self):
        """
        Ferme la connexion à la base de données.
        """
        self.conn.close()
