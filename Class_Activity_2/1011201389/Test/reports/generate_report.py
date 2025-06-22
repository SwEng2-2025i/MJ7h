from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from datetime import datetime

def generate_pdf_report(content: str, report_dir="reports"):
    # Crear directorio si no existe
    os.makedirs(report_dir, exist_ok=True)

    # Buscar el siguiente número disponible
    existing_reports = [f for f in os.listdir(report_dir) if f.startswith("test_report_") and f.endswith(".pdf")]
    next_number = len(existing_reports) + 1
    filename = f"test_report_{next_number}.pdf"
    filepath = os.path.join(report_dir, filename)

    # Crear el PDF
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, "Integration Test Report")
    
    c.setFont("Helvetica", 12)
    c.drawString(72, height - 100, f"Report ID: {next_number}")
    c.drawString(72, height - 120, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Escribir líneas del contenido
    y = height - 160
    for line in content.splitlines():
        c.drawString(72, y, line)
        y -= 20
        if y < 72:
            c.showPage()
            y = height - 72

    c.save()
    print(f"📄 PDF report generated: {filepath}")

