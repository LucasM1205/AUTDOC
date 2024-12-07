from fastapi import FastAPI, HTTPException, UploadFile, Form, Depends
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import os
import json
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from backend.database import SessionLocal
from backend.models import JokerAntrag, FachbereichSekretariat, Pruefungsausschuss, Student, DokumentenMetadaten, Benutzer
from backend.auth import authenticate_user, create_access_token

# FastAPI-Anwendung erstellen
app = FastAPI()

# CORS-Middleware hinzufügen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Datenbank-Sitzung
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Lade Konfiguration
def load_field_config():
    config_path = "assets/JokerAntrag_field_config.json"
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Konfigurationsdatei nicht gefunden: {config_path}")
    with open(config_path, "r") as file:
        return json.load(file)

# Endpunkt für die Anmeldung
@app.post("/token")
async def login_for_access_token(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Ungültige Anmeldedaten")

    access_token = create_access_token(data={"sub": user.email, "role": user.rolle})
    return {"access_token": access_token, "token_type": "bearer"}

# Endpunkt zur PDF-Generierung
@app.post("/generate-pdf")
async def generate_pdf(
    vorname: str = Form(...),
    nachname: str = Form(...),
    matrikelnummer: str = Form(...),
    fachbereich: str = Form(...),
    bachelorstudiengang: str = Form(...),
    fach: str = Form(...),
    pruefungsnummer: str = Form(...),
    fachbereich_modul: str = Form(...),
    pruefer: str = Form(...),
    joker_status: str = Form(...),
    doppelstudium_bachelor: str = Form(None),
    unterschrift: UploadFile = None
):
    session: Session = SessionLocal()
    try:
        field_config = load_field_config()

        # Überprüfen, ob der Student existiert, andernfalls erstellen
        student = session.query(Student).filter_by(matrikelnummer=matrikelnummer).first()
        if not student:
            student = Student(
                vorname=vorname,
                name=nachname,
                matrikelnummer=matrikelnummer,
                fachbereich=fachbereich,
                studiengang=bachelorstudiengang,
            )
            session.add(student)
            session.commit()

        # JokerAntrag erstellen
        joker_antrag = JokerAntrag(
            student_id=student.id,
            fach=fach,
            pruefungsnummer=pruefungsnummer,
            pruefer=pruefer,
            joker_verwendet=(joker_status.lower() == "ja"),
            doppelstudium=(doppelstudium_bachelor is not None),
            doppelstudium_name=doppelstudium_bachelor,
            status="Ausstehend",
            datum_erstellung=datetime.now(),
        )
        session.add(joker_antrag)
        session.commit()

        # PDF-Generierung
        input_pdf_path = "assets/JokerAntragTemplate.pdf"
        output_pdf_path = f"joker_antrag_{joker_antrag.id}.pdf"

        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()

        aktuelles_datum = datetime.now().strftime("%d.%m.%Y")
        temp_signature_path = None

        for page_num, page in enumerate(reader.pages):
            packet = BytesIO()
            overlay_canvas = canvas.Canvas(packet, pagesize=letter)

            if page_num == 0:
                for field, position in field_config.items():
                    if field == "unterschrift" and unterschrift:
                        unterschrift_data = await unterschrift.read()
                        temp_signature_path = f"unterschriften/{joker_antrag.id}_student.png"
                        with open(temp_signature_path, "wb") as temp_file:
                            temp_file.write(unterschrift_data)
                        overlay_canvas.drawImage(
                            temp_signature_path,
                            position["x"],
                            position["y"],
                            width=position.get("width", 100),
                            height=position.get("height", 50),
                            preserveAspectRatio=True,
                            mask="auto"
                        )
                    elif field == "datum":
                        overlay_canvas.drawString(position["x"], position["y"], aktuelles_datum)
                    else:
                        value = locals().get(field, None)
                        if value:
                            overlay_canvas.drawString(position["x"], position["y"], str(value))

            overlay_canvas.save()
            packet.seek(0)

            overlay_pdf = PdfReader(packet)
            overlay_page = overlay_pdf.pages[0]
            page.merge_page(overlay_page)
            writer.add_page(page)

        with open(output_pdf_path, "wb") as output_file:
            writer.write(output_file)

        if temp_signature_path and os.path.exists(temp_signature_path):
            joker_antrag.dokumenten_metadaten = DokumentenMetadaten(
                dokument_name=f"joker_antrag_{joker_antrag.id}.pdf",
                typ="PDF",
                erstelldatum=datetime.now(),
            )
            session.commit()

        return FileResponse(
            output_pdf_path,
            media_type="application/pdf",
            filename=f"joker_antrag_{joker_antrag.id}.pdf"
        )
    except Exception as e:
        session.rollback()
        print("Fehler beim Erstellen des PDFs:", e)
        raise HTTPException(status_code=500, detail="Fehler beim Erstellen des PDFs")
    finally:
        session.close()
    
@app.post("/preview-pdf")
async def preview_pdf(
    vorname: str = Form(...),
    nachname: str = Form(...),
    matrikelnummer: str = Form(...),
    fachbereich: str = Form(...),
    bachelorstudiengang: str = Form(...),
    fach: str = Form(...),
    pruefungsnummer: str = Form(...),
    fachbereich_modul: str = Form(...),
    pruefer: str = Form(...),
    joker_status: str = Form(...),
    doppelstudium_bachelor: str = Form(None),
    unterschrift: UploadFile = None
):
    try:
        # Pfad für die temporäre Vorschau-PDF
        temp_pdf_path = "temp_preview_joker_antrag.pdf"
        field_config = load_field_config()

        input_pdf_path = "assets/JokerAntragTemplate.pdf"

        # PDF-Reader und -Writer initialisieren
        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()
        aktuelles_datum = datetime.now().strftime("%d.%m.%Y")

        for page_num, page in enumerate(reader.pages):
            packet = BytesIO()
            overlay_canvas = canvas.Canvas(packet, pagesize=letter)

            if page_num == 0:
                for field, position in field_config.items():
                    if field == "unterschrift" and unterschrift:
                        # Unterschrift einfügen
                        unterschrift_data = await unterschrift.read()
                        temp_signature_path = "temp_signature.png"
                        with open(temp_signature_path, "wb") as temp_file:
                            temp_file.write(unterschrift_data)
                        overlay_canvas.drawImage(
                            temp_signature_path,
                            position["x"],
                            position["y"],
                            width=position.get("width", 100),
                            height=position.get("height", 50),
                            preserveAspectRatio=True,
                            mask="auto"
                        )
                        os.remove(temp_signature_path)
                    elif field == "datum":
                        # Datum hinzufügen
                        overlay_canvas.drawString(position["x"], position["y"], aktuelles_datum)
                    else:
                        # Andere Felder aus den Parametern einfügen
                        value = locals().get(field, None)
                        if value:
                            overlay_canvas.drawString(position["x"], position["y"], str(value))

            overlay_canvas.save()
            packet.seek(0)
            overlay_pdf = PdfReader(packet)
            overlay_page = overlay_pdf.pages[0]
            page.merge_page(overlay_page)
            writer.add_page(page)

        # PDF schreiben
        with open(temp_pdf_path, "wb") as temp_output_file:
            writer.write(temp_output_file)

        # Rückgabe der Vorschau-PDF
        return StreamingResponse(
            open(temp_pdf_path, "rb"),
            media_type="application/pdf",
            headers={"Content-Disposition": "inline; filename=temp_preview_joker_antrag.pdf"}
        )

    except Exception as e:
        print("Fehler bei der Vorschau:", e)
        raise HTTPException(status_code=500, detail="Fehler beim Erstellen der Vorschau")

@app.put("/jokerantrag/{antrag_id}/sekretariat")
async def bearbeite_antrag_sekretariat(
    antrag_id: int,
    joker_verfuegbar: bool = Form(...),
    bemerkungen: str = Form(None)
):
    session: Session = SessionLocal()
    try:
        # Antrag abrufen
        antrag = session.query(JokerAntrag).filter_by(id=antrag_id).first()
        if not antrag:
            raise HTTPException(status_code=404, detail="Antrag nicht gefunden")

        # Sekretariat-Bearbeitung updaten
        if not antrag.sek_vorgang:
            antrag.sek_vorgang = FachbereichSekretariat(joker_antrag_id=antrag.id)
        
        antrag.sek_vorgang.joker_verfuegbar = joker_verfuegbar
        antrag.sek_vorgang.bemerkungen = bemerkungen
        antrag.sek_vorgang.letzte_aenderung = datetime.now()
        session.commit()

        return {"message": "Antrag erfolgreich durch das Sekretariat bearbeitet"}
    except Exception as e:
        session.rollback()
        print("Fehler:", e)
        raise HTTPException(status_code=500, detail="Fehler bei der Bearbeitung des Antrags")
    finally:
        session.close()

@app.put("/jokerantrag/{antrag_id}/pruefungsausschuss")
async def bearbeite_antrag_pruefungsausschuss(
    antrag_id: int,
    unterschrift: UploadFile = None,
    bedenken: str = Form(None),
    entscheidung: str = Form(...)
):
    session: Session = SessionLocal()
    try:
        # Antrag abrufen
        antrag = session.query(JokerAntrag).filter_by(id=antrag_id).first()
        if not antrag:
            raise HTTPException(status_code=404, detail="Antrag nicht gefunden")

        # Prüfungsausschuss-Bearbeitung updaten
        if not antrag.pruefungsvorgang:
            antrag.pruefungsvorgang = Pruefungsausschuss(joker_antrag_id=antrag.id)
        
        antrag.pruefungsvorgang.bedenken = bedenken
        antrag.pruefungsvorgang.datum_bearbeitung = datetime.now()
        antrag.status = entscheidung

        if unterschrift:
            unterschrift_data = await unterschrift.read()
            unterschrift_path = f"unterschriften/{antrag_id}_pruefungsausschuss.png"
            with open(unterschrift_path, "wb") as f:
                f.write(unterschrift_data)
            antrag.pruefungsvorgang.unterschrift = unterschrift_path

        session.commit()
        return {"message": "Antrag erfolgreich durch den Prüfungsausschuss bearbeitet"}
    except Exception as e:
        session.rollback()
        print("Fehler:", e)
        raise HTTPException(status_code=500, detail="Fehler bei der Bearbeitung des Antrags")
    finally:
        session.close()

@app.get("/jokerantrag/{antrag_id}")
async def antrag_details(antrag_id: int):
    session: Session = SessionLocal()
    try:
        antrag = session.query(JokerAntrag).filter_by(id=antrag_id).first()
        if not antrag:
            raise HTTPException(status_code=404, detail="Antrag nicht gefunden")

        # Antrag inklusive Details aus Sekretariat und Prüfungsausschuss
        return {
            "id": antrag.id,
            "student": {
                "name": antrag.student.name,
                "vorname": antrag.student.vorname,
                "matrikelnummer": antrag.student.matrikelnummer,
            },
            "fach": antrag.fach,
            "status": antrag.status,
            "bemerkungen": antrag.bemerkungen,
            "sekretariat": {
                "joker_verfuegbar": antrag.sek_vorgang.joker_verfuegbar if antrag.sek_vorgang else None,
                "bemerkungen": antrag.sek_vorgang.bemerkungen if antrag.sek_vorgang else None,
                "letzte_aenderung": antrag.sek_vorgang.letzte_aenderung if antrag.sek_vorgang else None,
            },
            "pruefungsausschuss": {
                "unterschrift": antrag.pruefungsvorgang.unterschrift if antrag.pruefungsvorgang else None,
                "bedenken": antrag.pruefungsvorgang.bedenken if antrag.pruefungsvorgang else None,
                "datum_bearbeitung": antrag.pruefungsvorgang.datum_bearbeitung if antrag.pruefungsvorgang else None,
            }
        }
    finally:
        session.close()

@app.get("/jokerantrag/{antrag_id}/sekretariat")
async def get_antrag_sekretariat(antrag_id: int):
    session: Session = SessionLocal()
    try:
        # Antrag mit Studentendaten und Bearbeitungsverlauf laden
        antrag = (
            session.query(JokerAntrag)
            .options(
                joinedload(JokerAntrag.student),  # Lade Studentendaten
                joinedload(JokerAntrag.sek_vorgang)  # Lade Sekretariatsvorgang
            )
            .filter_by(id=antrag_id)
            .first()
        )

        if not antrag:
            raise HTTPException(status_code=404, detail="Antrag nicht gefunden")

        # JSON-kompatible Datenstruktur erstellen
        antrag_data = {
            "antrag_id": antrag.id,
            "status": antrag.status,
            "fach": antrag.fach,
            "pruefungsnummer": antrag.pruefungsnummer,
            "joker_verwendet": antrag.joker_verwendet,
            "doppelstudium": antrag.doppelstudium,
            "doppelstudium_name": antrag.doppelstudium_name,
            "datum_erstellung": antrag.datum_erstellung,
            "student": {
                "name": antrag.student.name,
                "vorname": antrag.student.vorname,
                "matrikelnummer": antrag.student.matrikelnummer,
                "fachbereich": antrag.student.fachbereich,
                "studiengang": antrag.student.studiengang,
            },
            "sekretariat": {
                "joker_verfuegbar": antrag.sek_vorgang.joker_verfuegbar if antrag.sek_vorgang else None,
                "bemerkungen": antrag.sek_vorgang.bemerkungen if antrag.sek_vorgang else None,
                "letzte_aenderung": antrag.sek_vorgang.letzte_aenderung if antrag.sek_vorgang else None,
            },
        }

        return antrag_data
    except Exception as e:
        print("Fehler:", e)
        raise HTTPException(status_code=500, detail="Fehler beim Abrufen des Antrags")
    finally:
        session.close()
