from pdfrw import PdfReader, PdfWriter, PageMerge
from reportlab.pdfgen import canvas
from io import BytesIO

# Pfade der PDF-Dateien
input_pdf_path = r"C:\Projekte\AUTDOC\assets\Verlaengerung Bachelorarbeit.pdf"
output_pdf_path = r"C:\Projekte\AUTDOC\assets\Verlaengerung_Bachelorarbeit_bearbeitet.pdf"

# PDF laden
reader = PdfReader(input_pdf_path)
writer = PdfWriter()

# LDAP-Daten zum Beispiel
ldap_data = {"displayName": "Lucas Kaczmarczyk"}

for page in reader.pages:
    # Overlay erstellen
    packet = BytesIO()
    c = canvas.Canvas(packet)
    
    # Position des Textes (diese Position anpassen)
    x_position = 300  # Beispiel: X-Koordinate
    y_position = 620  # Beispiel: Y-Koordinate
    c.drawString(x_position, y_position, ldap_data["displayName"])

    # Overlay speichern
    c.save()
    packet.seek(0)

    # Überlagerung der Seite mit dem Overlay
    overlay_pdf = PdfReader(packet)
    overlay_page = overlay_pdf.pages[0]
    PageMerge(page).add(overlay_page, prepend=False).render()

    # Seite zum Writer hinzufügen
    writer.addpage(page)

# Ausgabe speichern
with open(output_pdf_path, "wb") as f:
    writer.write(f)

print("Die PDF wurde erfolgreich mit den Formularfeldern ausgefüllt und gespeichert.")
