from fastapi import APIRouter, Depends
from api.auth import verify_api_key
from service_layer.reporting_service import ReportingService

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
        return service.rapport_ventes()

    @r.get("/ruptures", summary="⚠️ Produits en rupture", status_code=200, dependencies=[Depends(verify_api_key)])
    def produits_en_rupture():
        """
        Retourne les produits dont la quantité en stock est inférieure ou égale à un seuil.
        """
        return service.get_out_of_stock()

    @r.get("/dashboard", summary="📊 Tableau de bord (texte)", status_code=200, dependencies=[Depends(verify_api_key)])
    def generer_tableau_de_bord():
        """
        Génère et affiche un tableau de bord contenant :
        - ventes par produit
        - ruptures de stock
        - surstocks
        - chiffre d'affaires total
        - tendances hebdomadaires
        """
        service.generer_tableau_de_bord()
        return {"message": "Tableau de bord généré (voir logs)"}

    return r
    