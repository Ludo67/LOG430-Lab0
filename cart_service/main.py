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
from shared_data.cart_dao import CartDAO
from cart_service import CartService
from cart_routes import router as cart_router

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

# Services initiaux (injection DAO unique par requête)
dao = CartDAO(session=SessionLocal())
cart_service = CartService(dao)
app.include_router(cart_router(cart_service))