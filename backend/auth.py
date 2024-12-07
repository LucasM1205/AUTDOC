from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from jose import jwt
from backend.models import Benutzer

# Geheime Schlüssel und Algorithmen für JWT
SECRET_KEY = "dein_geheimer_schlüssel"  # Ersetze durch eine sichere Zufallszeichenfolge
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(hashed_password: str, plain_password: str) -> bool:
    """
    Überprüft, ob ein gehashtes Passwort mit einem eingegebenen Klartextpasswort übereinstimmt.
    """
    return check_password_hash(hashed_password, plain_password)

def authenticate_user(db: Session, email: str, password: str):
    """
    Authentifiziert einen Benutzer anhand von E-Mail und Passwort.

    Args:
        db: Datenbank-Session.
        email: E-Mail-Adresse des Benutzers.
        password: Passwort des Benutzers.

    Returns:
        Benutzer-Objekt, wenn die Anmeldedaten korrekt sind, ansonsten None.
    """
    # Benutzer anhand der E-Mail suchen
    user = db.query(Benutzer).filter(Benutzer.email == email).first()

    # Überprüfen, ob Benutzer existiert und Passwort korrekt ist
    if not user or not verify_password(user.passwort, password):
        return None

    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Erstellt ein JWT-Access-Token.

    Args:
        data: Daten, die im Token enthalten sein sollen.
        expires_delta: Optionale Zeitdauer, wie lange das Token gültig sein soll.

    Returns:
        Ein JWT-Token als Zeichenkette.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
