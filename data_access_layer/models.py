"""Modèle de base SQLAlchemy pour les entités Produit et Vente."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# pylint: disable=too-few-public-methods
class Produit(Base):
    """Représente un produit en stock."""
    __tablename__ = "produits"

    id = Column(Integer)
    nom = Column(String)
    categorie = Column(String)
    prix = Column(Float)
    quantite = Column(Integer)
    magasin_id = Column(Integer)

    __table_args__ = (
        PrimaryKeyConstraint('id', 'magasin_id'),
    )

    ventes = relationship("Vente", back_populates="produit")

    def __repr__(self):
        return (
            f"<Produit(id={self.id}, nom='{self.nom}', catégorie='{self.categorie}', "
            f"prix={self.prix}, quantité={self.quantite}, magasin_id={self.magasin_id})>"
        )

# pylint: disable=too-few-public-methods
class Vente(Base):
    """Représente une vente d’un produit."""
    __tablename__ = "ventes"

    id = Column(Integer, primary_key=True)
    produit_id = Column(Integer, ForeignKey("produits.id"))
    magasin_id = Column(Integer)
    quantite = Column(Integer)
    prix_total = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    produit = relationship("Produit", back_populates="ventes")
