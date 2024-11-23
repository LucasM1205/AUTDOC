from fastapi import FastAPI, HTTPException, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import os
import json
from datetime import datetime

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

# Lade Konfiguration
def load_field_config():
    config_path = "assets/JokerAntrag_field_config.json"
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Konfigurationsdatei nicht gefunden: {config_path}")
    with open(config_path, "r") as file:
        return json.load(file)

# PDF-Generierungs-Endpunkt
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
    try:
        # Feldkonfiguration laden
        field_config = load_field_config()

        # Dateipfade
        input_pdf_path = "assets/JokerAntragTemplate.pdf"
        output_pdf_path = "joker_antrag_ausgefuellt.pdf"

        # PDF-Reader und -Writer initialisieren
        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()

        # Datum hinzufügen
        aktuelles_datum = datetime.now().strftime("%d.%m.%Y")

        # Temporäre Datei für die Unterschrift
        temp_signature_path = None

        for page_num, page in enumerate(reader.pages):
            packet = BytesIO()
            overlay_canvas = canvas.Canvas(packet, pagesize=letter)

            # Text hinzufügen (nur auf der ersten Seite)
            if page_num == 0:
                for field, position in field_config.items():
                    if field == "unterschrift" and unterschrift:
                        # Unterschrift als Bild einfügen
                        unterschrift_position = field_config.get("unterschrift")
                        if unterschrift_position:
                            unterschrift_data = await unterschrift.read()
                            temp_signature_path = "temp_signature.png"
                            
                            # Temporäre Datei speichern
                            with open(temp_signature_path, "wb") as temp_file:
                                temp_file.write(unterschrift_data)
                            
                            # Unterschrift ins PDF einfügen
                            overlay_canvas.drawImage(
                                temp_signature_path,
                                unterschrift_position["x"],
                                unterschrift_position["y"],
                                width=unterschrift_position.get("width", 100),
                                height=unterschrift_position.get("height", 50),
                                preserveAspectRatio=True,
                                mask="auto"
                            )
                    elif field == "datum":
                        # Datum hinzufügen
                        datum_position = position
                        overlay_canvas.drawString(
                            datum_position["x"], datum_position["y"], aktuelles_datum
                        )
                    else:
                        # Andere Felder
                        value = locals().get(field, None)
                        if value:
                            overlay_canvas.drawString(
                                position["x"], position["y"], str(value)
                            )

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

        # Temporäre Datei löschen, falls vorhanden
        if temp_signature_path and os.path.exists(temp_signature_path):
            os.remove(temp_signature_path)

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
