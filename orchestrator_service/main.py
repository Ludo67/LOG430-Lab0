
from fastapi import FastAPI, HTTPException
import httpx
import uuid
from enum import Enum
import logging
import time
from prometheus_client import Summary, Counter
from prometheus_fastapi_instrumentator import Instrumentator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("saga")

app = FastAPI()
Instrumentator().instrument(app).expose(app)

saga_duration = Summary("saga_commande_duree_secondes", "Durée totale d'exécution de la saga de commande")

etat_commande_counter = Counter(
    "saga_commande_etat_total",
    "Nombre de commandes par état atteint",
    ["etat"]
)

class EtatCommande(str, Enum):
    CREEE = "CommandeCréée"
    CLIENT_CREE = "ClientCréé"
    STOCK_VERIFIE = "StockVérifié"
    PANIER_CREE = "PanierCréé"
    COMMANDE_CONFIRMEE = "CommandeConfirmée"
    CHECKOUT_ECHOUE = "CheckoutÉchoué"
    ECHEC = "Échec"

etat_commande = {}

STOCK_URL = "http://stock_service:8000"
CART_URL = "http://cart_service_1:8000"
CUSTOMER_URL = "http://customer_service:8000"
headers = {"X-API-Key": "topsecret123"}

@app.post("/orchestrateur/commande")
async def creer_commande(produit_id: int, magasin_id: int, client_id: int, quantite: int):
    start_time = time.time()
    commande_id = f"{client_id}-{produit_id}-{magasin_id}"
    etat_commande[commande_id] = EtatCommande.CREEE
    etat_commande_counter.labels(etat=EtatCommande.CREEE).inc()
    logger.info("Commande créée", extra={"commande_id": commande_id})

    async with httpx.AsyncClient() as client:
        try:
            # Vérifier si le client existe
            try:
                res = await client.get(f"{CUSTOMER_URL}/clients/{client_id}", headers=headers)
                if res.status_code == 200:
                    logger.info("Client existant utilisé", extra={"commande_id": commande_id})
                else:
                    client_data = {
                        "id": client_id,
                        "nom": "Dupont",
                        "prenom": "Jean",
                        "email": f"client{client_id}@example.com",
                        "adresse": "123 Rue Exemple"
                    }
                    res = await client.post(f"{CUSTOMER_URL}/clients/", json=client_data, headers=headers)
                    res.raise_for_status()
                    logger.info("Client créé", extra={"commande_id": commande_id})
                etat_commande[commande_id] = EtatCommande.CLIENT_CREE
                etat_commande_counter.labels(etat=EtatCommande.CLIENT_CREE).inc()
            except httpx.RequestError as e:
                logger.error(f"[{commande_id}] ❌ Service client injoignable: {e}")
                raise HTTPException(status_code=500, detail="Service client indisponible")

            # Vérification du stock
            res = await client.get(f"{STOCK_URL}/stock/", headers=headers)
            res.raise_for_status()
            produits = res.json()
            produit = next((p for p in produits if p["id"] == produit_id and p["magasin_id"] == magasin_id), None)
            if not produit or produit["quantite"] < quantite:
                raise HTTPException(status_code=400, detail="Stock insuffisant")
            etat_commande[commande_id] = EtatCommande.STOCK_VERIFIE
            etat_commande_counter.labels(etat=EtatCommande.STOCK_VERIFIE).inc()

            # Création du panier
            try:
                # Vérifie s’il existe déjà un panier pour ce client
                res = await client.get(f"{CART_URL}/panier/client/{client_id}", headers=headers)
                if res.status_code == 200:
                    panier_id = res.json()["id"]
                    logger.info("Panier existant utilisé", extra={"commande_id": commande_id})
                else:
                    raise httpx.HTTPStatusError("Panier non trouvé", request=res.request, response=res)

            except httpx.HTTPStatusError:
                # Sinon crée un nouveau panier
                res = await client.post(f"{CART_URL}/panier/", json={"client_id": client_id}, headers=headers)
                res.raise_for_status()
                panier_id = res.json()["id"]
                logger.info("Panier créé", extra={"commande_id": commande_id})
            panier_id = res.json()["id"]
            etat_commande[commande_id] = EtatCommande.PANIER_CREE
            etat_commande_counter.labels(etat=EtatCommande.PANIER_CREE).inc()

            # Ajout produit au panier
            await client.post(
                f"{CART_URL}/panier/{panier_id}/produit",
                json={"id": produit_id, "magasin_id": magasin_id, "quantite": quantite},
                headers=headers
            )

            # Checkout
            await client.post(
                f"{CART_URL}/panier/panier/{panier_id}/checkout",
                headers=headers
            )

            etat_commande[commande_id] = EtatCommande.COMMANDE_CONFIRMEE
            etat_commande_counter.labels(etat=EtatCommande.COMMANDE_CONFIRMEE).inc()
            saga_duration.observe(time.time() - start_time)

            return {"commande_id": commande_id, "etat": etat_commande[commande_id]}

        except httpx.HTTPStatusError as e:
            logger.error(f"[{commande_id}] ❌ Échec de la commande: {e}")
            if "checkout" in str(e.request.url):
                etat_commande[commande_id] = EtatCommande.CHECKOUT_ECHOUE
                etat_commande_counter.labels(etat=EtatCommande.CHECKOUT_ECHOUE).inc()
            else:
                etat_commande[commande_id] = EtatCommande.ECHEC
                etat_commande_counter.labels(etat=EtatCommande.ECHEC).inc()

            try:
                await client.post(
                    f"{STOCK_URL}/stock/annulation",
                    json={"produit_id": produit_id, "magasin_id": magasin_id, "quantite": quantite},
                    headers=headers
                )
                logger.warning(f"[{commande_id}] 🧯 Rollback: stock libéré")
            except Exception as rollback_err:
                logger.error(f"[{commande_id}] ❗ Rollback échoué: {rollback_err}")

            saga_duration.observe(time.time() - start_time)
            return {
                "commande_id": commande_id,
                "etat": etat_commande[commande_id],
                "erreur": str(e)
            }
