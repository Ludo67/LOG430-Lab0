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

test-stock:
	docker-compose run --rm -e PYTHONPATH=/app stock_service pytest tests/

test-restock:
	docker-compose run --rm -e PYTHONPATH=/app restock_service pytest tests/

test-reporting:
	docker-compose run --rm -e PYTHONPATH=/app reporting_service pytest tests/

test-customer:
	docker-compose run --rm -e PYTHONPATH=/app customer_service pytest tests/

test-cart:
	docker-compose run --rm -e PYTHONPATH=/app cart_service pytest tests/

test-shared:
	docker-compose run --rm -e PYTHONPATH=/app setup pytest shared_data/tests/

# Qualité
lint:
	ruff check .

format:
	black .
