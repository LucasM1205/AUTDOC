from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import logging

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Datenbank-Verbindungsdetails aus der .env-Datei
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    logger.error("Fehlende Umgebungsvariablen für die Datenbankverbindung.")
    raise ValueError("Eine oder mehrere Datenbank-Umgebungsvariablen fehlen.")

# Zusammensetzen der PostgreSQL-URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
logger.info(f"Datenbank-URL: {SQLALCHEMY_DATABASE_URL}")

# Datenbank-Engine erstellen
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Session-Factory erstellen
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Basisklasse für Modelle definieren
Base = declarative_base()

# Datenbank-Sitzung bereitstellen
def get_db():
    """
    Stellt eine Datenbank-Sitzung bereit und schließt sie nach der Verwendung.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
