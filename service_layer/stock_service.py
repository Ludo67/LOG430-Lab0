"""Service de gestion des opérations sur le stock."""

from data_access_layer.product_dao import ProduitDAO


class StockService:
    """Service permettant la gestion des produits en stock et des ventes."""

    def __init__(self, dao: ProduitDAO):
        """Initialise le service avec un DAO de produit."""
        self.dao = dao

    def rechercher_produit(self, terme: str):
        """Recherche un produit par mot-clé."""
        return self.dao.rechercher(terme)

    def enregistrer_vente(self, produit_id: int, quantite: int, magasin_id: int):
        """Enregistre une vente."""
        produit = dict(self.dao.get_by_id(produit_id, magasin_id))
        if not produit or int(produit["quantite"]) < quantite:
            raise ValueError("Stock insuffisant ou produit introuvable")
        produit["quantite"] = int(produit["quantite"]) - quantite
        self.dao.update(produit)
        self._log_vente(produit_id, quantite, magasin_id)

    def annuler_vente(self, produit_id: int, quantite: int, magasin_id: int):
        """Annule une vente."""
        produit = dict(self.dao.get_by_id(produit_id, magasin_id))
        if not produit:
            raise ValueError("Produit introuvable")
        produit["quantite"] = int(produit["quantite"]) + quantite
        self.dao.update(produit)

    def lister_stock(self):
        """Retourne tous les produits en stock."""
        return self.dao.get_all()

    def _log_vente(self, produit_id: int, quantite: int, magasin_id: int):
        """Insère un enregistrement de vente dans la base de données."""
        self.dao.conn.execute(
            "INSERT INTO ventes (produit_id, quantite, magasin_id) VALUES (?, ?, ?)",
            (produit_id, quantite, magasin_id)
        )
        self.dao.conn.commit()
