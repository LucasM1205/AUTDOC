from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Student(Base):
    __tablename__ = "studenten"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    vorname = Column(String, nullable=False)
    matrikelnummer = Column(String, unique=True, nullable=False)
    fachbereich = Column(String, nullable=False)
    bachelorstudiengang = Column(String, nullable=False)
    unterschrift = Column(String)  # Dateipfad zur Signatur
    joker_beitraege = relationship("JokerAntrag", back_populates="student")

class JokerAntrag(Base):
    __tablename__ = "joker_antraege"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("studenten.id"), nullable=False)
    fach = Column(String)
    pruefungsnummer = Column(String)
    pruefer = Column(String)
    joker_verwendet = Column(Boolean, default=False)
    doppelstudium = Column(Boolean, default=False)
    doppelstudium_name = Column(String)
    datum_erstellung = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Ausstehend")  # Status des Antrags
    dokumenten_metadaten_id = Column(Integer, ForeignKey("dokumenten_metadaten.id"))
    dokumenten_metadaten = relationship("DokumentenMetadaten", back_populates="joker_antraege")
    student = relationship("Student", back_populates="joker_beitraege")
    sek_vorgang = relationship("FachbereichSekretariat", back_populates="joker_antrag", uselist=False)
    pruefungsvorgang = relationship("Pruefungsausschuss", back_populates="joker_antrag", uselist=False)

class FachbereichSekretariat(Base):
    __tablename__ = "fachbereich_sekretariat"
    id = Column(Integer, primary_key=True, index=True)
    joker_antrag_id = Column(Integer, ForeignKey("joker_antraege.id"))
    joker_verfuegbar = Column(Boolean, default=True)
    joker_antrag = relationship("JokerAntrag", back_populates="sek_vorgang")

class Pruefungsausschuss(Base):
    __tablename__ = "pruefungsausschuss"
    id = Column(Integer, primary_key=True, index=True)
    joker_antrag_id = Column(Integer, ForeignKey("joker_antraege.id"))
    unterschrift = Column(String)  # Dateipfad zur Signatur
    bedenken = Column(Text)  # Textfeld für Bedenken
    datum_bearbeitung = Column(DateTime, default=datetime.utcnow)
    joker_antrag = relationship("JokerAntrag", back_populates="pruefungsvorgang")

class DokumentenMetadaten(Base):
    __tablename__ = "dokumenten_metadaten"
    id = Column(Integer, primary_key=True, index=True)
    dokument_name = Column(String, nullable=False)
    typ = Column(String, nullable=False)
    erstelldatum = Column(DateTime, default=datetime.utcnow)
    joker_antraege = relationship("JokerAntrag", back_populates="dokumenten_metadaten")
