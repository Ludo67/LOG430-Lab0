import requests
import logging
import os
from shared_data.models import Panier, ProduitPanier, Produit
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from shared_data.cart_dao import CartDAO
from api.schemas import PanierDetail, ProduitDansPanier

logging.basicConfig(
    level=logging.INFO,  # Change à DEBUG ou ERROR selon les besoins
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

STOCK_SERVICE_URL = "http://stock_service:8000"


class CartService:
    def __init__(self, dao: CartDAO):
        self.dao = dao
        self.session: Session = dao.session

    def creer_panier(self, client_id: int):
        """Crée un nouveau panier pour un client."""
        if self.dao.get_by_id(client_id):
            logger.error(f"Panier pour le client ID {client_id} déjà existant.")
            raise ValueError("Panier déjà existant")
        
        logger.info(f"Création du panier pour le client ID {client_id}.")
        nouveau = Panier(client_id=client_id, date_creation=datetime.utcnow())
        return self.dao.creer_panier(nouveau)

    def ajouter_produit(self, panier_id: int, produit: ProduitPanier) -> Panier:
        logger.info(f"Ajout du produit ({produit.produit_id}, magasin {produit.magasin_id}) au panier ID {panier_id}.")
        panier = self.dao.get_by_id(panier_id)
        if not panier:
            raise ValueError(f"Panier {panier_id} introuvable")
        return self.dao.ajouter_produit(panier, produit)
    
    # def get_panier(self, panier_id: int) -> Panier:
    #     logger.info(f"Récupération du panier ID {panier_id}.")
    #     panier = self.dao.get_panier(panier_id)
    #     if not panier:
    #         raise ValueError(f"Panier {panier_id} introuvable")
    #     return panier
    
    def get_panier(self, panier_id: int) -> PanierDetail:
        logger.info(f"Récupération du panier ID {panier_id}.")
        panier = self.dao.get_panier(panier_id)
        if not panier:
            raise ValueError(f"Panier {panier_id} introuvable")

        # Récupérer les produits avec quantités
        produits_dans_panier = (
            self.dao.session.query(ProduitPanier, Produit)
            .join(Produit, (Produit.id == ProduitPanier.produit_id) & (Produit.magasin_id == ProduitPanier.magasin_id))
            .filter(ProduitPanier.panier_id == panier_id)
            .all()
        )

        produits = [
            ProduitDansPanier(
                produit_id=prod.id,
                magasin_id=prod.magasin_id,
                nom=prod.nom,
                prix=prod.prix,
                quantite=pp.quantite
            )
            for pp, prod in produits_dans_panier
        ]

        return PanierDetail(
            id=panier.id,
            client_id=panier.client_id,
            date_creation=panier.date_creation,
            produits=produits
        )

    def checkout_panier(self, panier_id: int) -> float:
        logger.info(f"Checkout du panier ID {panier_id}.")
        panier = self.get_panier(panier_id)

        if not panier or not panier.produits:
            raise ValueError("Le panier est vide ou introuvable.")

        total = 0.0
        headers = {"X-API-Key": "topsecret123"}

        for produit in panier.produits:
            payload = {
                "produit_id": str(produit.produit_id),
                "quantite": produit.quantite,
                "magasin_id": produit.magasin_id
            }

            logger.info(f"Enregistrement de la vente pour produit ID {produit.produit_id}.")
            logger.debug(f"Payload envoyé au stock service: {payload}")

            try:
                response = requests.post(f"{STOCK_SERVICE_URL}/stock/vente", json=payload, headers=headers)
                response.raise_for_status()
            except requests.RequestException as e:
                raise HTTPException(status_code=500, detail=f"Erreur lors de l'enregistrement de la vente pour produit ID {produit.produit_id} : {str(e)}")

            logger.debug(f"Produit vendu: {produit.nom} (ID: {produit.produit_id}, Qte: {produit.quantite}, Prix unitaire: {produit.prix})")
            total += produit.quantite * produit.prix

        logger.info(f"Vente complétée pour le panier ID {panier_id}, total: {total:.2f}.")

        self.dao.vider_panier(panier_id)

        return total


