"""Service de gestion des opérations sur le stock avec SQLAlchemy."""

from sqlalchemy.orm import Session
from data_access_layer.product_dao import ProduitDAO
from data_access_layer.models import Produit, Vente



class StockService:
    """Service permettant la gestion des produits en stock et des ventes."""

    def __init__(self, dao: ProduitDAO):
        """Initialise le service avec un DAO de produit."""
        self.dao = dao
        self.session: Session = dao.session

    def rechercher_produit(self, terme: str):
        """Recherche un produit par mot-clé."""
        return self.dao.rechercher(terme)

    def enregistrer_vente(self, produit_id: int, quantite: int, magasin_id: int):
        """Enregistre une vente en décrémentant le stock et en loguant l'opération."""
        produit = self.dao.get_by_id(produit_id, magasin_id)
        if not produit:
            raise ValueError("Produit introuvable")

        if produit.quantite < quantite:
            raise ValueError("Stock insuffisant")

        produit.quantite -= quantite
        self.dao.update(produit)
        self._log_vente(produit_id, quantite, magasin_id)

    def annuler_vente(self, produit_id: int, quantite: int, magasin_id: int):
        """Annule une vente en restaurant le stock du produit."""
        produit = self.dao.get_by_id(produit_id, magasin_id)
        if not produit:
            raise ValueError("Produit introuvable")

        produit.quantite += quantite
        self.dao.update(produit)

    def lister_stock(self):
        """Retourne tous les produits en stock."""
        return self.session.query(Produit).filter(Produit.quantite > 0).all()

    def _log_vente(self, produit_id: int, quantite: int, magasin_id: int):
        """Ajoute une entrée de vente dans la base de données."""
        vente = Vente(produit_id=produit_id, quantite=quantite, magasin_id=magasin_id)
        self.session.add(vente)
        self.session.commit()
