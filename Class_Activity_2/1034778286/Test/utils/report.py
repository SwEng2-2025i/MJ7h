import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_pdf_report(test_type: str, report_text: str) -> str:
    """
    Genera un PDF dentro de ./reports/ con nombre:
        <test_type>_report_<n>.pdf
    - test_type  : "frontend", "backend", etc.
    - report_text: texto (con \n) que se escribirá en el PDF.
    Devuelve la ruta completa del PDF creado.
    """
    # 1. Carpeta de salida
    os.makedirs("reports", exist_ok=True)

    # 2. Número secuencial
    existing = [
        f for f in os.listdir("reports")
        if f.startswith(f"{test_type}_report_") and f.endswith(".pdf")
    ]
    next_id = len(existing) + 1
    filename = f"reports/{test_type}_report_{next_id}.pdf"

    # 3. Escribir PDF
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    text_obj = c.beginText(40, height - 40)
    text_obj.setFont("Helvetica", 12)

    for line in report_text.splitlines():
        text_obj.textLine(line)

    c.drawText(text_obj)
    c.save()

    print(f"📄 Reporte generado: {filename}")
    return filename
