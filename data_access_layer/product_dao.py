"""Data Access Object (DAO) pour gérer les opérations sur les produits avec SQLAlchemy."""

from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from data_access_layer.models import Produit, Vente

class ProduitDAO:
    """Classe permettant les opérations CRUD sur les produits."""

    def __init__(self, session: Session):
        """
        Initialise le DAO avec une session SQLAlchemy.
        :param session: Session SQLAlchemy active.
        """
        self.session = session

    def get_all(self):
        """Récupère tous les produits."""
        return self.session.query(Produit).all()

    def get_by_id(self, produit_id, magasin_id):
        """Récupère un produit par son ID et son magasin."""
        return self.session.query(Produit).filter_by(id=produit_id, magasin_id=magasin_id).first()

    def rechercher(self, terme):
        """Recherche des produits par un terme dans l'ID, le nom ou la catégorie."""
        return self.session.query(Produit).filter(
            or_(
                Produit.id.like(f"%{terme}%"),
                Produit.nom.like(f"%{terme}%"),
                Produit.categorie.like(f"%{terme}%")
            )
        ).all()

    def update(self, produit: Produit):
        """Met à jour un produit déjà attaché à la session."""
        self.session.add(produit)
        self.session.commit()

    def insert(self, produit_dict):
        """Insère un nouveau produit."""
        nouveau = Produit(**produit_dict)
        self.session.add(nouveau)
        self.session.commit()

    def get_ventes_par_magasin(self):
        """Retourne un dictionnaire du total des ventes par magasin."""
        result = self.session.query(
            Vente.magasin_id,
            func.sum(Vente.quantite).label("total")
        ).group_by(Vente.magasin_id).all()

        return {r.magasin_id: r.total for r in result}
