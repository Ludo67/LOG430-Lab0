FROM python:3.11-slim

WORKDIR /app

COPY . .

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r requirements.txt

# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# ⬇ Initialiser la base de données
RUN python -m data_access_layer.init_db   
RUN python -m data_access_layer.seed_db    

CMD ["python", "-m", "presentation_layer.main"]
