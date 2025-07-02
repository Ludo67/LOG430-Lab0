
FROM python:3.11-slim

# Définir le dossier de travail
WORKDIR /app

# Copier le contenu du projet
COPY . .

# Définir le chemin Python pour l'import
ENV PYTHONPATH=/app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m data_access_layer.init_db   
RUN python -m data_access_layer.seed_db    

# Exposer le port par défaut de FastAPI/Uvicorn
EXPOSE 8000

# Lancer l'application avec uvicorn (accessible depuis l'extérieur)
CMD ["uvicorn", "presentation_layer.main:app", "--host", "0.0.0.0", "--port", "8000"]

