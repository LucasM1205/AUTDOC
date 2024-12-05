from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from backend.database import Base, engine
from datetime import datetime

class Student(Base):
    __tablename__ = "studenten"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    vorname = Column(String, nullable=False)
    matrikelnummer = Column(String, unique=True, nullable=False, index=True)
    fachbereich = Column(String, nullable=False)
    studiengang = Column(String, nullable=False)  # Bachelor/Master-Studiengang
    unterschrift = Column(String, nullable=True)  # Dateipfad zur Signatur
    erstellt_am = Column(DateTime, default=datetime.utcnow)
    joker_beitraege = relationship("JokerAntrag", back_populates="student")

class JokerAntrag(Base):
    __tablename__ = "joker_antraege"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("studenten.id"), nullable=False)
    fach = Column(String, nullable=True)
    pruefungsnummer = Column(String, nullable=True)
    pruefer = Column(String, nullable=True)
    joker_verwendet = Column(Boolean, default=False)
    doppelstudium = Column(Boolean, default=False)
    doppelstudium_name = Column(String, nullable=True)
    datum_erstellung = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Ausstehend")
    bemerkungen = Column(Text, nullable=True)
    dokumenten_metadaten_id = Column(Integer, ForeignKey("dokumenten_metadaten.id"), nullable=True)
    dokumenten_metadaten = relationship("DokumentenMetadaten", back_populates="joker_antraege")
    student = relationship("Student", back_populates="joker_beitraege")
    sek_vorgang = relationship("FachbereichSekretariat", back_populates="joker_antrag", uselist=False)
    pruefungsvorgang = relationship("Pruefungsausschuss", back_populates="joker_antrag", uselist=False)

class FachbereichSekretariat(Base):
    __tablename__ = "fachbereich_sekretariat"
    id = Column(Integer, primary_key=True, index=True)
    joker_antrag_id = Column(Integer, ForeignKey("joker_antraege.id"), nullable=False)
    joker_verfuegbar = Column(Boolean, default=True)
    letzte_aenderung = Column(DateTime, default=datetime.utcnow)
    bemerkungen = Column(Text, nullable=True)
    joker_antrag = relationship("JokerAntrag", back_populates="sek_vorgang")

class Pruefungsausschuss(Base):
    __tablename__ = "pruefungsausschuss"
    id = Column(Integer, primary_key=True, index=True)
    joker_antrag_id = Column(Integer, ForeignKey("joker_antraege.id"), nullable=False)
    unterschrift = Column(String, nullable=True)  # Dateipfad zur Signatur
    bedenken = Column(Text, nullable=True)  # Textfeld für Bedenken
    datum_bearbeitung = Column(DateTime, default=datetime.utcnow)
    joker_antrag = relationship("JokerAntrag", back_populates="pruefungsvorgang")

class DokumentenMetadaten(Base):
    __tablename__ = "dokumenten_metadaten"
    id = Column(Integer, primary_key=True, index=True)
    dokument_name = Column(String, nullable=False)
    typ = Column(String, nullable=False)  # Typ des Dokuments (z. B. "PDF")
    erstelldatum = Column(DateTime, default=datetime.utcnow)
    joker_antraege = relationship("JokerAntrag", back_populates="dokumenten_metadaten")

# Debugging: Liste aller registrierten Tabellen
print(f"Tabellen vor Erstellung: {Base.metadata.tables.keys()}")

# Tabellen in der Datenbank erstellen
Base.metadata.create_all(bind=engine)

# Debugging: Überprüfe erneut die Tabellen
print(f"Tabellen nach Erstellung: {Base.metadata.tables.keys()}")
