import os
from reportlab.pdfgen import canvas

REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)

def _next_report_number():
    existing = [f for f in os.listdir(REPORT_DIR) if f.startswith("report_") and f.endswith(".pdf")]
    if not existing:
        return 1
    nums = sorted(int(f.split("_")[1].split(".")[0]) for f in existing)
    return nums[-1] + 1

def next_report_path():
    num = _next_report_number()
    return os.path.join(REPORT_DIR, f"report_{num}.pdf")

def generate_report(test_name: str, summary: str):
    """
    Crea un PDF con un encabezado (test_name) y el texto de summary.
    Devuelve la ruta al archivo creado.
    """
    path = next_report_path()
    c = canvas.Canvas(path)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 800, f"Integration Test Report: {test_name}")
    c.setFont("Helvetica", 12)
    y = 760
    for line in summary.splitlines():
        c.drawString(50, y, line)
        y -= 20
    c.save()
    return path
