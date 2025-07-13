## Configuration du cache et du load balancer

### 1. Cache Redis (FastAPI + fastapi-cache2)

- **Bibliothèque utilisée** : `fastapi-cache2`
- **Backend** : Redis, lancé dans un conteneur Docker
- **Endpoints mis en cache** :
  - `GET /reporting/dashboard`
  - `GET /restock/stock_par_magasin`
  - `POST /stock/create`
  - `PUT /stock/update`
- **Durée de vie des caches (TTL)** : 60 secondes pour les appels de lecture.
- **Bénéfices** :
  - Réduction de la latence observée sur les endpoints de lecture
  - Diminution du nombre d'accès à la base de données

**Exemple de code d'initialisation** :
```python
from fastapi_cache2 import FastAPICache
from fastapi_cache2.backends.redis import RedisBackend
import redis.asyncio as redis

@app.on_event("startup")
async def startup():
    redis_client = redis.Redis(host="redis", port=6379, db=0)
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
