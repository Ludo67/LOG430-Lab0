import logging
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
import redis.asyncio as redis
from fastapi.middleware.cors import CORSMiddleware
from shared_data.database import SessionLocal
from shared_data.product_dao import ProduitDAO
from stock_service import StockService

from stock_route import router as stock_router
app = FastAPI()

@app.on_event("startup")
async def startup():
    redis_backend = redis.from_url("redis://redis:6379", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis_backend), prefix="fastapi-cache")

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

dao = ProduitDAO(SessionLocal())
stock_service = StockService(dao)

# Routes
app.include_router(stock_router(stock_service))
