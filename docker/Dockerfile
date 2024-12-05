# Basis-Image
FROM python:3.9-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere requirements.txt aus dem Hauptverzeichnis des Projekts
COPY ../requirements.txt .

# Installiere die Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den gesamten Backend-Code
COPY ../backend /app

# Öffne den Port 8000
EXPOSE 8000

# Starte die FastAPI-App
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
