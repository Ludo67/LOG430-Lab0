from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data_access_layer.database import SessionLocal
from data_access_layer.product_dao import ProduitDAO
from service_layer.stock_service import StockService
from service_layer.restock_service import RestockService
from service_layer.reporting_service import ReportingService
from api import stock_route, restock_routes, reporting_routes

app = FastAPI()

# Autorise tous les domaines (en développement uniquement !)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplacez par ["https://monclient.com"] en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services initiaux (injection DAO unique par requête)
dao = ProduitDAO(session=SessionLocal())
stock_service = StockService(dao)
restock_service = RestockService(dao)
reporting_service = ReportingService(dao)

# Inclusion des routes
app.include_router(stock_route.router(stock_service))
app.include_router(restock_routes.router(restock_service))
app.include_router(reporting_routes.router(reporting_service))
