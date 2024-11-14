import json
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

# PDF-Pfade direkt im Code festlegen
input_pdf_path = r"C:\Projekte\AUTDOC\assets\Verlaengerung Bachelorarbeit.pdf"
output_pdf_path = r"C:\Projekte\AUTDOC\assets\Verlaengerung_Bachelorarbeit_bearbeitet.pdf"
signature_image_path = r"C:\Projekte\AUTDOC\assets\Unterschrift.png"

# JSON-Konfigurationsdatei einlesen
with open(r"C:\Projekte\AUTDOC\config.json", "r") as f:
    config = json.load(f)

# Konfiguration für Textfelder und Unterschrift aus der JSON-Datei
text_field = config["text_fields"]["displayName"]
signature_field = config["signature_field"]

# PDF-Reader und -Writer initialisieren
reader = PdfReader(input_pdf_path)
writer = PdfWriter()

# Durchlaufen der Seiten
for page_num, page in enumerate(reader.pages):
    packet = BytesIO()
    overlay_canvas = canvas.Canvas(packet, pagesize=letter)

    # Text hinzufügen
    if page_num == 0:
        overlay_canvas.drawString(text_field["x"], text_field["y"], text_field["text"])

        # Unterschrift hinzufügen
        overlay_canvas.drawImage(
            signature_image_path,
            signature_field["x"],
            signature_field["y"],
            width=signature_field["width"],
            height=signature_field["height"]
        )

    # Overlay abschließen
    overlay_canvas.save()
    packet.seek(0)

    # Overlay-PDF lesen und als neue Seite hinzufügen
    overlay_pdf = PdfReader(packet)
    overlay_page = overlay_pdf.pages[0]

    # Überlagerte Seite dem Writer hinzufügen
    page.merge_page(overlay_page)
    writer.add_page(page)

# Ausgabe speichern
with open(output_pdf_path, "wb") as output_file:
    writer.write(output_file)

print("Das PDF wurde erfolgreich mit den Text- und Unterschriftsfeldern ergänzt und gespeichert.")
