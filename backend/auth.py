from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from backend.models import Benutzer
from dotenv import load_dotenv
import os
from ldap3 import Server, Connection, Tls, ALL
import ssl
from dotenv import load_dotenv


# .env-Datei laden
load_dotenv()

# Geheime Schlüssel und Algorithmen für JWT aus der .env-Datei
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_key_fuer_dev")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# OAuth2-Schema für Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# LDAP-Server-Konfiguration aus .env-Datei laden
LDAP_SERVER = os.getenv("LDAP_SERVER", "ldap://ldap.fh-giessen.de")
SEARCH_BASE = os.getenv("LDAP_SEARCH_BASE", "dc=fh-giessen-friedberg,dc=de")

def verify_password(hashed_password: str, plain_password: str) -> bool:
    return check_password_hash(hashed_password, plain_password)


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(Benutzer).filter(Benutzer.email == email).first()
    if not user or not verify_password(user.passwort, password):
        return None
    return user

def authenticate_ldap(username: str, password: str) -> bool:
    """
    Authentifiziert einen Benutzer gegen den LDAP-Server.
    Gibt True zurück, wenn die Anmeldung erfolgreich ist, sonst False.
    """
    try:
        # Lade Konfigurationen
        ldap_server = os.getenv("LDAP_SERVER", "ldap://ldap.fh-giessen.de")
        search_base = os.getenv("SEARCH_BASE", "ou=People,ou=MND,ou=Friedberg,dc=fh-giessen-friedberg,dc=de")
        tls_config = Tls(validate=ssl.CERT_NONE)

        # Debugging-Ausgabe
        print(f"DEBUG: Verbinde zu LDAP-Server: {ldap_server}")
        print(f"DEBUG: Benutzer-DN: uid={username},{search_base}")

        # LDAP-Server konfigurieren
        server = Server(ldap_server, get_info=ALL, tls=tls_config)

        # Verbindung herstellen
        conn = Connection(server, user=f"uid={username},{search_base}", password=password)
        conn.open()
        conn.start_tls()

        if not conn.bind():
            print(f"⛔ DEBUG: Bind fehlgeschlagen für Benutzer: {username}")
            return False

        print(f"✅ DEBUG: LDAP-Anmeldung erfolgreich für Benutzer: {username}")
        return True
    except Exception as e:
        print(f"⚠️ DEBUG: Fehler bei der LDAP-Authentifizierung für Benutzer {username}: {e}")
        return False

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends()):
    """
    Extrahiert den aktuellen Benutzer basierend auf dem JWT-Token.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Ungültige Anmeldedaten",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(Benutzer).filter(Benutzer.email == email).first()
    if user is None:
        raise credentials_exception
    return user
