import logging
from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
from shared_data.models import ProduitPanier
# from shared_data.cart_dao import CartDAO
from cart_service import CartService
from api.auth import verify_api_key
from api.schemas import PanierCreate, ProduitSimple, PanierDetail, PanierOut

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/panier", tags=["Panier"])

def router(service: CartService) -> APIRouter:
    r = APIRouter(prefix="/panier", tags=["🛒 Panier"])

    @r.post("/", summary="➕ Créer un panier", response_model=PanierOut, status_code=201, dependencies=[Depends(verify_api_key)])
    def creer_panier(data: PanierCreate):
        """
        Crée un nouveau panier pour un client.

        **Paramètres** :
        - `client_id`: ID du client pour lequel le panier est créé

        **Exemple de réponse** :
        ```json
        {
            "id": 1,
            "client_id": 1,
            "date_creation": "2023-10-01T12:00:00Z"
        }
        ```
        """
        return service.creer_panier(data.client_id)

    @r.post("/{panier_id}/produit", summary="➕ Ajouter un produit au panier", status_code=200, dependencies=[Depends(verify_api_key)])
    def ajouter_produit(panier_id: int, produit: ProduitSimple):
        """
        Ajoute un produit à un panier existant.

        **Paramètres** :
        - `panier_id`: ID du panier
        - `produit`: Détails du produit à ajouter

        **Exemple de réponse** :
        ```json
        {
            "message": "Produit ajouté"
        }
        ```
        """
        produit_obj = ProduitPanier(
            produit_id=produit.id,
            magasin_id=produit.magasin_id,
            quantite=produit.quantite
        )
        produit_obj.panier_id = panier_id

        logger.info(f"Ajout du produit ID {produit.id} au panier ID {panier_id}.")
        return service.ajouter_produit(panier_id, produit_obj)

    @r.get("/panier/{panier_id}", response_model=PanierDetail, status_code=200)
    def get_panier(panier_id: int):
        try:
            panier = service.get_panier(panier_id)
            return panier
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        
    @r.post("/panier/{panier_id}/checkout", status_code=200)
    def checkout_panier(panier_id: int):
        return service.checkout_panier(panier_id)

    @r.get("/whoami", status_code=200)
    def whoami():
        return {"instance": os.getenv("INSTANCE_ID", "unknown")}

        
    return r
