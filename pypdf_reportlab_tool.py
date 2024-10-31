from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

# LDAP-Daten
ldap_data = {
    "displayName": "Lucas Kaczmarczyk",
    # Weitere Daten können wir später hinzufügen
}

# Pfade der PDF-Dateien
input_pdf_path = r"C:\Projekte\AUTDOC\assets\Verlängerung Bachelorarbeit.pdf"
output_pdf_path = r"C:\Projekte\AUTDOC\assets\Verlängerung_Bachelorarbeit_bearbeitet.pdf"

# PDF-Reader und -Writer initialisieren
reader = PdfReader(input_pdf_path)
writer = PdfWriter()

# Wir gehen Seite für Seite durch
for page_num, page in enumerate(reader.pages):
    packet = BytesIO()
    # Ein Canvas-Objekt, um das Overlay zu erstellen
    overlay_canvas = canvas.Canvas(packet, pagesize=letter)

    # Position für den Namen (angepasst für das Dokument)
    if page_num == 0:  # Nur auf der ersten Seite einfügen
        x_position = 300  # X-Position in Punkten
        y_position = 620   # Y-Position in Punkten
        overlay_canvas.drawString(x_position, y_position, ldap_data["displayName"])

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

print("Das PDF wurde erfolgreich mit dem Namen ergänzt und gespeichert.")
