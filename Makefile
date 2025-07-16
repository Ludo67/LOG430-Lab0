# Makefile pour projet multi-services FastAPI + PostgreSQL + Redis

.PHONY: build up down logs restart test init-db seed-db lint format

# Docker
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose down && docker-compose up -d --build

logs:
	docker-compose logs -f --tail=50

# DB
init-db:
	docker-compose run --rm setup python init_db.py

seed-db:
	docker-compose run --rm setup python seed_db.py

# Tests (si test client intégré dans les services)
test-stock:
	docker-compose run --rm stock_service pytest tests/

test-restock:
	docker-compose run --rm restock_service pytest tests/

test-reporting:
	docker-compose run --rm reporting_service pytest tests/

# Qualité
lint:
	ruff check .

format:
	black .
