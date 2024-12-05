from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Datenbank-Verbindungsdetails aus der .env-Datei
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Zusammensetzen der PostgreSQL-URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Datenbank-Engine erstellen
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Session-Factory erstellen
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Basisklasse für Modelle definieren
Base = declarative_base()
