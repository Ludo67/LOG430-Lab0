FROM python:3.11-slim

WORKDIR /app

COPY . .

CMD ["python", "-m", "presentation_layer.main"]
