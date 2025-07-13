import logging
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
import redis.asyncio as redis
from fastapi.middleware.cors import CORSMiddleware
from data_access_layer.database import SessionLocal
from data_access_layer.product_dao import ProduitDAO
from service_layer.stock_service import StockService
from service_layer.restock_service import RestockService
from service_layer.reporting_service import ReportingService
from api import stock_route, restock_routes, reporting_routes

app = FastAPI()

@app.on_event("startup")
async def startup():
    redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")

instrumentator = Instrumentator()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

Instrumentator().instrument(app).expose(app)

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
