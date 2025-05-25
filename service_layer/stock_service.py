"""Module de la couche service pour la gestion des produits en stock."""

from data_access_layer.product_dao import ProduitDAO

class StockService:
    """Service métier pour la gestion des produits en stock."""

    def __init__(self, dao=None):
        """Initialise le service avec un DAO de produit."""
        self.dao = dao or ProduitDAO()

    def rechercher_produit(self, terme):
        """Recherche des produits par nom, id ou catégorie."""
        return self.dao.rechercher(terme)

    def enregistrer_vente(self, produit_id, quantite):
        """
        Enregistre une vente de produit si le stock est suffisant.
        Soulève une exception si le produit est introuvable ou stock insuffisant.
        """
        produit = self.dao.get_by_id(produit_id)
        if produit and produit["quantite"] >= quantite:
            produit["quantite"] -= quantite
            self.dao.update(produit)
        else:
            raise ValueError("Stock insuffisant ou produit introuvable")

    def annuler_vente(self, produit_id, quantite):
        """
        Annule une vente en ajoutant à nouveau les quantités vendues au stock.
        Soulève une exception si le produit n'existe pas.
        """
        produit = self.dao.get_by_id(produit_id)
        if produit:
            produit["quantite"] += quantite
            self.dao.update(produit)
        else:
            raise ValueError("Produit introuvable")

    def lister_stock(self):
        """Retourne l'ensemble des produits en stock."""
        return self.dao.get_all()
