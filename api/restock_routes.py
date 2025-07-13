import logging
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from api.auth import verify_api_key
from service_layer.restock_service import RestockService
from api.schemas import TransfertRequest

logging.basicConfig(
    level=logging.INFO,  # Change à DEBUG ou ERROR selon les besoins
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

restock_router = APIRouter()

def router(service: RestockService) -> APIRouter:
    r = APIRouter(prefix="/restock", tags=["🔄 Réapprovisionnement"])

    @r.post("/transferer", summary="📦➔📦 Transférer du stock", status_code=200, dependencies=[Depends(verify_api_key)])
    def transferer_stock(transfert: TransfertRequest):
        """
        Transfère une quantité donnée d’un produit d’un magasin source à un magasin destination.

        - **produit_id**: ID du produit à transférer
        - **quantite**: Quantité à transférer
        - **magasin_src**: ID du magasin source
        - **magasin_dst**: ID du magasin destination

        **Exemple de requête** :
        ```json
        {
            "produit_id": "A123",
            "quantite": 10,
            "magasin_src": 1,
            "magasin_dst": 2
        }
        """
        logger.info(f"Transfert de {transfert.quantite} unités du produit ID {transfert.produit_id} du magasin ID {transfert.magasin_source} vers le magasin ID {transfert.magasin_destination}.")
        service.transferer_stock(transfert.produit_id, transfert.quantite, transfert.magasin_source, transfert.magasin_destination)
        return {"message": "Stock transféré"}

    @r.get("/stock_par_magasin", summary="🏬 Voir le stock par magasin", status_code=200, dependencies=[Depends(verify_api_key)])
    @cache(expire=60)
    def stock_par_magasin(magasin_id: int):
        """
        Affiche les produits disponibles dans un magasin spécifique.
        - **magasin_id**: ID du magasin à consulter
        """
        logger.info(f"Récupération du stock pour le magasin ID: {magasin_id}")
        return service.get_stock_par_magasin(magasin_id)

    return r
