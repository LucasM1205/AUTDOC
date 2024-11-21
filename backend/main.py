from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from reportlab.pdfgen import canvas

# FastAPI-Anwendung erstellen
app = FastAPI()

# CORS-Middleware einbinden
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Erlaubt Anfragen von allen Domains
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
    doppelstudium_bachelor: str = None  # Optionales Feld

# PDF-Generierungs-Endpunkt
@app.post("/generate-pdf")
async def generate_pdf(data: JokerAntragData):
    try:
        # Dateiname für das PDF
        output_filename = "joker_antrag.pdf"

        # PDF erstellen
        c = canvas.Canvas(output_filename)
        c.setFont("Helvetica", 12)

        # PDF-Inhalte
        c.drawString(100, 800, "Antrag - Joker")
        c.drawString(100, 780, f"Vorname: {data.vorname}")
        c.drawString(100, 760, f"Nachname: {data.nachname}")
        c.drawString(100, 740, f"Matrikelnummer: {data.matrikelnummer}")
        c.drawString(100, 720, f"Fachbereich: {data.fachbereich}")
        c.drawString(100, 700, f"Bachelorstudiengang: {data.bachelorstudiengang}")
        c.drawString(100, 680, f"Fach: {data.fach}")
        c.drawString(100, 660, f"Prüfungsnummer: {data.pruefungsnummer}")
        c.drawString(100, 640, f"Fachbereich des Moduls: {data.fachbereich_modul}")
        c.drawString(100, 620, f"Prüfer: {data.pruefer}")
        c.drawString(100, 600, f"Joker-Status: {data.joker_status}")

        # Zusätzliche Eingabe für Doppelstudium
        if data.joker_status == "doppelstudium" and data.doppelstudium_bachelor:
            c.drawString(100, 580, f"Doppelstudium Bachelor: {data.doppelstudium_bachelor}")

        c.save()

        # PDF als Antwort zurückgeben
        return FileResponse(
            output_filename,
            media_type="application/pdf",
            filename="joker_antrag.pdf"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
