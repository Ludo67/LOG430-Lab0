from fastapi import APIRouter, Depends
from api.auth import verify_api_key
from service_layer.stock_service import StockService
from api.schemas import VenteRequest, AnnulationRequest

stock_router = APIRouter()

def router(service: StockService) -> APIRouter:
    r = APIRouter(prefix="/stock", tags=["🧾 Stock"])

    @r.get("/", summary="📦 Lister les produits en stock", status_code=200, dependencies=[Depends(verify_api_key)])
    def lister_stock():
        """        Retourne la liste des produits en stock.
        """
        return service.lister_stock()

    @r.post("/vente", summary="🛒 Enregistrer une vente", status_code=200, dependencies=[Depends(verify_api_key)])
    def enregistrer_vente(vente: VenteRequest):
        """
        Enregistre une vente.

        - **produit_id**: ID du produit vendu
        - **quantite**: Quantité vendue
        - **magasin_id**: ID du magasin concerné
        """
        service.enregistrer_vente(vente.produit_id, vente.quantite, vente.magasin_id)
        return {"message": "Vente enregistrée"}

    @r.post("/annulation", summary="↩️ Annuler une vente", status_code=200, dependencies=[Depends(verify_api_key)])
    def annuler_vente(annulation: AnnulationRequest):
        """
        Annule une vente (restocke un produit).

        - **produit_id**: ID du produit
        - **quantite**: Quantité à réinjecter
        - **magasin_id**: ID du magasin
        """
        service.annuler_vente(annulation.produit_id, annulation.quantite, annulation.magasin_id)
        return {"message": "Vente annulée"}

    @r.get("/rechercher", summary="🔍 Rechercher un produit", status_code=200, dependencies=[Depends(verify_api_key)])
    def rechercher(terme: str):
        """
        Recherche des produits par un terme dans l'ID, le nom ou la catégorie.
        - **terme**: Terme de recherche (ID, nom ou catégorie)
        """
        return service.rechercher_produit(terme)

    return r
