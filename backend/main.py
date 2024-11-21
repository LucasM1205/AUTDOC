from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import os
import json

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

# Datenmodell für Nutzerdaten
class JokerAntragData(BaseModel):
    vorname: str
    nachname: str
    matrikelnummer: str
    fachbereich: str
    bachelorstudiengang: str
    fach: str
    pruefungsnummer: str
    fachbereich_modul: str
    pruefer: str
    joker_status: str
    doppelstudium_bachelor: str = None

# Lade Konfiguration
def load_field_config():
    config_path = "assets/JokerAntrag_field_config.json"
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Konfigurationsdatei nicht gefunden: {config_path}")
    with open(config_path, "r") as file:
        return json.load(file)

# PDF-Generierungs-Endpunkt
@app.post("/generate-pdf")
async def generate_pdf(data: JokerAntragData):
    try:
        # Feldkonfiguration laden
        field_config = load_field_config()

        # Dateipfade
        input_pdf_path = "assets/JokerAntragTemplate.pdf"
        output_pdf_path = "joker_antrag_ausgefuellt.pdf"

        # PDF-Reader und -Writer initialisieren
        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()

        for page_num, page in enumerate(reader.pages):
            packet = BytesIO()
            overlay_canvas = canvas.Canvas(packet, pagesize=letter)

            # Text hinzufügen (nur auf der ersten Seite)
            if page_num == 0:
                for field, position in field_config.items():
                    value = getattr(data, field, None)
                    if value:  # Nur Felder mit Daten drucken
                        overlay_canvas.drawString(position["x"], position["y"], str(value))

            # Overlay abschließen
            overlay_canvas.save()
            packet.seek(0)

            # Overlay-PDF lesen
            overlay_pdf = PdfReader(packet)
            overlay_page = overlay_pdf.pages[0]

            # Seiten kombinieren
            page.merge_page(overlay_page)
            writer.add_page(page)

        # Ergebnis speichern
        with open(output_pdf_path, "wb") as output_file:
            writer.write(output_file)

        # PDF als Antwort zurückgeben
        return FileResponse(
            output_pdf_path,
            media_type="application/pdf",
            filename="joker_antrag_ausgefuellt.pdf"
        )

    except FileNotFoundError as e:
        print("Fehler:", e)
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print("Fehler beim Erstellen des PDFs:", e)
        raise HTTPException(status_code=500, detail=str(e))
