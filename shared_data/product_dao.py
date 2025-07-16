"""Data Access Object (DAO) pour gérer les opérations sur les produits avec SQLAlchemy."""

from sqlalchemy.orm import Session
from sqlalchemy import or_, func, cast, String
from shared_data.models import Produit, Vente

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
                cast(Produit.id, String).like(f"%{terme}%"),
                Produit.nom.ilike(f"%{terme}%"),
                Produit.categorie.ilike(f"%{terme}%")
            )
        ).all()

    def update(self, produit: Produit):
        """Met à jour un produit déjà attaché à la session."""
        self.session.add(produit)
        self.session.commit()

    def insert(self, produit: Produit | dict):
        if isinstance(produit, dict):
            produit = Produit(**produit)
        self.session.add(produit)
        self.session.commit()


    def update_product(self, produit_id: int, magasin_id: int, champs: dict):
        produit = self.get_by_id(produit_id, magasin_id)
        if not produit:
            return None

        for key, value in champs.items():
            if hasattr(produit, key):
                setattr(produit, key, value)

        self.session.commit()
        return produit


    def get_ventes_par_magasin(self):
        """Retourne un dictionnaire du total des ventes par magasin."""
        result = self.session.query(
            Vente.magasin_id,
            func.sum(Vente.quantite).label("total")
        ).group_by(Vente.magasin_id).all()

        return {r.magasin_id: r.total for r in result}
