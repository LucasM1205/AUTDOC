from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

# Pfade der PDF-Dateien
input_pdf_path = r"C:\Projekte\AUTDOC\assets\Verlaengerung Bachelorarbeit.pdf"
output_pdf_path = r"C:\Projekte\AUTDOC\assets\Verlaengerung_Bachelorarbeit_bearbeitet.pdf"

# PDF-Reader und -Writer initialisieren
reader = PdfReader(input_pdf_path)
writer = PdfWriter()

# Wir gehen Seite für Seite durch
for page_num, page in enumerate(reader.pages):
    packet = BytesIO()
    # Ein Canvas-Objekt, um das Overlay zu erstellen
    overlay_canvas = canvas.Canvas(packet, pagesize=letter)

    # Position für die Checkbox (angepasst für das Dokument)
    if page_num == 0:  # Nur auf der ersten Seite einfügen
        checkbox_x = 150  # X-Position
        checkbox_y = 320  # Y-Position
        checkbox_size = 15  # Größe der Checkbox

        # Zeichnet ein Quadrat als Checkbox
        overlay_canvas.rect(checkbox_x, checkbox_y, checkbox_size, checkbox_size, fill=0)

        # Optional: Ein Kreuz in die Checkbox zeichnen
        overlay_canvas.line(checkbox_x, checkbox_y, checkbox_x + checkbox_size, checkbox_y + checkbox_size)
        overlay_canvas.line(checkbox_x, checkbox_y + checkbox_size, checkbox_x + checkbox_size, checkbox_y)

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

print("Das PDF wurde erfolgreich mit der Checkbox ergänzt und gespeichert.")
