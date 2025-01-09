# Basis-Image
FROM python:3.9-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die requirements.txt in das Arbeitsverzeichnis
COPY ./requirements.txt /app/

# Installiere die Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den gesamten Backend-Code
COPY ./backend /app/backend

# Kopiere die Alembic-Konfiguration und Migrations
COPY ./alembic.ini /app/alembic.ini
COPY ./migrations /app/migrations

# Setze den PYTHONPATH, damit das Modul backend erkannt wird
ENV PYTHONPATH=/app

# Sicherstellen, dass das Modul backend korrekt importiert wird
ENV MODULE_NAME=backend.main:app

# Öffne den Port 8000
EXPOSE 8000

# Starte die FastAPI-App
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]


