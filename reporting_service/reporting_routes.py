import logging
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from api.auth import verify_api_key
from reporting_service import ReportingService

logging.basicConfig(
    level=logging.INFO,  # Change à DEBUG ou ERROR selon les besoins
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

reporting_router = APIRouter()

def router(service: ReportingService) -> APIRouter:
    r = APIRouter(prefix="/reporting", tags=["📊 Rapports"])

    @r.get("/ventes", summary="📈 Rapport des ventes", status_code=200, dependencies=[Depends(verify_api_key)])
    def rapport_ventes():
        """
        Retourne un résumé des ventes groupées par magasin et produit.

        **Exemple de réponse** :
        ```json
        [
            { "magasin_id": 1, "produit_id": "A123", "total_vendu": 25 }
        ]
        """
        logger.info("Génération du rapport des ventes par magasin et produit.")
        return service.rapport_ventes()

    @r.get("/ruptures", summary="⚠️ Produits en rupture", status_code=200, dependencies=[Depends(verify_api_key)])
    def produits_en_rupture():
        """
        Retourne les produits dont la quantité en stock est inférieure ou égale à un seuil.
        """
        logger.info("Récupération des produits en rupture de stock.")
        return service.get_out_of_stock()

    @r.get("/dashboard", summary="📊 Tableau de bord (texte)", status_code=200, dependencies=[Depends(verify_api_key)])
    @cache(expire=60)
    def generer_tableau_de_bord():
        """
        Génère et affiche un tableau de bord contenant :
        - ventes par produit
        - ruptures de stock
        - surstocks
        - chiffre d'affaires total
        - tendances hebdomadaires
        """
        logger.info("Génération du tableau de bord consolidé.")
        return service.generer_tableau_de_bord()

    return r
    