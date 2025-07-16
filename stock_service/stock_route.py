import logging
from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi_cache import FastAPICache
from api.auth import verify_api_key
from stock_service import StockService
from api.schemas import VenteRequest, AnnulationRequest, MiseAJourProduitDTO, NouveauProduitDTO

logging.basicConfig(
    level=logging.INFO,  # Change à DEBUG ou ERROR selon les besoins
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

stock_router = APIRouter()

def router(service: StockService) -> APIRouter:
    r = APIRouter(prefix="/stock", tags=["🧾 Stock"])

    @r.get("/", summary="📦 Lister les produits en stock", status_code=200, dependencies=[Depends(verify_api_key)])
    def lister_stock():
        """        Retourne la liste des produits en stock.
        """
        logger.info("Récupération de tous les produits en stock.")
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
        logger.info(f"Vente enregistrée pour le produit ID {vente.produit_id}, quantité: {vente.quantite}, magasin ID: {vente.magasin_id}.")
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
        logger.info(f"Annulation de vente pour le produit ID {annulation.produit_id}, quantité: {annulation.quantite}, magasin ID: {annulation.magasin_id}.")
        return {"message": "Vente annulée"}

    @r.get("/rechercher", summary="🔍 Rechercher un produit", status_code=200, dependencies=[Depends(verify_api_key)])
    def rechercher(terme: str):
        """
        Recherche des produits par un terme dans l'ID, le nom ou la catégorie.
        - **terme**: Terme de recherche (ID, nom ou catégorie)
        """
        logger.info(f"Recherche de produit avec le terme: {terme}")
        return service.rechercher_produit(terme)

    @r.put("/update/{produit_id}/magasin/{magasin_id}", summary="📝 Mettre à jour un produit", status_code=200, dependencies=[Depends(verify_api_key)])
    async def mettre_a_jour_produit(produit_id: int, magasin_id: int, champs: MiseAJourProduitDTO = Body(...)):
        """        Met à jour un produit dans un magasin spécifique.
        - **produit_id**: ID du produit à mettre à jour
        - **magasin_id**: ID du magasin où le produit est stocké
        - **champs**: Champs à mettre à jour (nom, catégorie, prix, etc.)
        """
        try:
            logger.info(f"Mise à jour du produit ID {produit_id} dans le magasin ID {magasin_id} avec les champs: {champs}")
            service.mettre_a_jour_produit(produit_id, magasin_id, champs.dict(exclude_unset=True))
            await FastAPICache.clear(namespace="fastapi-cache")  # invalide tout
            return {"status": "updated"}
        except ValueError as e:
            logger.error(f"Erreur lors de la mise à jour du produit ID {produit_id} dans le magasin ID {magasin_id}: {str(e)}")
            raise HTTPException(status_code=404, detail=str(e))

    @r.post("/create", summary="Créer un produit", status_code=200, dependencies=[Depends(verify_api_key)])
    async def creer_produit(dto: NouveauProduitDTO):
        """        Crée un nouveau produit dans le stock.
        - **dto**: DTO contenant les informations du produit à créer
        """
        try:
            logger.info(f"Création du produit avec ID {dto.id} dans le magasin ID {dto.magasin_id}")
            service.ajouter_produit(dto.id, dto.nom, dto.categorie, dto.quantite, dto.prix, dto.magasin_id)
            await FastAPICache.clear(namespace="fastapi-cache")  # invalide tout
            return {"status": "created"}
        except ValueError as e:
            logger.error(f"Erreur lors de la création du produit ID {dto.id} dans le magasin ID {dto.magasin_id}: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

    return r
