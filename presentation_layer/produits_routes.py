from fastapi import APIRouter, HTTPException, Query, FastAPI
from service_layer.stock_service import StockService
from service_layer.reporting_service import ReportingService
from service_layer.restock_service import RestockService
from data_access_layer.product_dao import ProduitDAO

router = APIRouter()
dao = ProduitDAO()
stock_service = StockService(dao)
reporting_service = ReportingService(dao)
reappro_service = RestockService(dao)

@router.get("/produits")
def lister_produits():
    return stock_service.lister_stock()


@router.get("/produits/recherche")
def rechercher_produit(terme: str = Query(...)):
    return stock_service.rechercher_produit(terme)


@router.post("/ventes")
def enregistrer_vente(produit_id: str, quantite: int, magasin_id: str):
    try:
        stock_service.enregistrer_vente(produit_id, quantite, magasin_id)
        return {"message": "Vente enregistrée"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/ventes/annuler")
def annuler_vente(produit_id: str, quantite: int, magasin_id: str):
    try:
        stock_service.annuler_vente(produit_id, quantite, magasin_id)
        return {"message": "Vente annulée"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/rapport")
def rapport():
    return reporting_service.generer_tableau_de_bord()


@router.get("/dashboard")
def tableau_de_bord():
    return reporting_service.afficher_tableau_de_bord()


@router.post("/produits/update")
def mise_a_jour_produit(produit: dict):
    try:
        dao.update(produit)
        return {"message": "Produit mis à jour"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reapprovisionnement")
def reapprovisionnement(produit_id: str, quantite: int, magasin_source: str, magasin_cible: str):
    try:
        reappro_service.transferer_stock(produit_id, quantite, magasin_source, magasin_cible)
        return {"message": "Réapprovisionnement effectué"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))