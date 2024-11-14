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
input_pdf_path = r"C:\Projekte\AUTDOC\assets\Verlaengerung Bachelorarbeit.pdf"
output_pdf_path = r"C:\Projekte\AUTDOC\assets\Verlaengerung_Bachelorarbeit_bearbeitet.pdf"
signature_image_path = r"C:\Projekte\AUTDOC\assets\Unterschrift.png"  # Pfad zur Unterschrift

# PDF-Reader und -Writer initialisieren
reader = PdfReader(input_pdf_path)
writer = PdfWriter()

# Wir gehen Seite für Seite durch
for page_num, page in enumerate(reader.pages):
    packet = BytesIO()
    # Ein Canvas-Objekt, um das Overlay zu erstellen
    overlay_canvas = canvas.Canvas(packet, pagesize=letter)

    # Text hinzufügen
    if page_num == 0:  # Nur auf der ersten Seite einfügen
        x_position_text = 300  # X-Position für den Namen
        y_position_text = 620   # Y-Position für den Namen
        overlay_canvas.drawString(x_position_text, y_position_text, ldap_data["displayName"])

        # Unterschrift hinzufügen
        x_position_signature = 139  # X-Position für die Unterschrift
        y_position_signature = 320  # Y-Position für die Unterschrift
        overlay_canvas.drawImage(signature_image_path, x_position_signature, y_position_signature, width=100, height=50)

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

print("Das PDF wurde erfolgreich mit dem Namen und der Unterschrift ergänzt und gespeichert.")
