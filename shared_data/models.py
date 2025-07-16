"""Modèle de base SQLAlchemy pour les entités Produit et Vente."""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey, DateTime,
    PrimaryKeyConstraint, ForeignKeyConstraint, Table
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class ProduitPanier(Base):
    __tablename__ = "produits_paniers"

    panier_id = Column(Integer, ForeignKey("paniers.id"), primary_key=True)
    produit_id = Column(Integer, primary_key=True)
    magasin_id = Column(Integer, primary_key=True)
    quantite = Column(Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ["produit_id", "magasin_id"],
            ["produits.id", "produits.magasin_id"]
        ),
    )

    panier = relationship("Panier", back_populates="produits_associes")
    produit = relationship("Produit")

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
    # paniers = relationship(
    #     "Panier",
    #     secondary=produits_paniers,
    #     back_populates="produits"
    # )

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
    produit_id = Column(Integer)
    magasin_id = Column(Integer)
    quantite = Column(Integer)
    prix_total = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        ForeignKeyConstraint(
            ['produit_id', 'magasin_id'],
            ['produits.id', 'produits.magasin_id']
        ),
    )

    produit = relationship("Produit", back_populates="ventes")

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    adresse = Column(String, nullable=False)
    paniers = relationship("Panier", back_populates="client")

class Panier(Base):
    __tablename__ = "paniers"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    date_creation = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="paniers")
    produits_associes = relationship("ProduitPanier", back_populates="panier")

