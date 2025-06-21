import os
import re
from fpdf import FPDF
from datetime import datetime

def limpiar_texto(texto):
    return re.sub(r'[^\x00-\x7F]+', '', texto)  # Elimina emojis y caracteres no ASCII

def generar_reporte_pdf(texto):
    os.makedirs("reportes", exist_ok=True)

    existentes = [f for f in os.listdir("reportes") if f.startswith("reporte_") and f.endswith(".pdf")]
    numeros = [int(f.split('_')[1].split('.')[0]) for f in existentes]
    siguiente_num = max(numeros, default=0) + 1

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, f"Reporte de pruebas #{siguiente_num}", ln=True, align="C")
    pdf.cell(200, 10, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
    pdf.ln(10)

    max_line_length = 120
    for linea in limpiar_texto(texto).split('\n'):
        while len(linea) > max_line_length:
            pdf.set_x(10)
            pdf.multi_cell(0, 10, linea[:max_line_length], align='L')
            linea = linea[max_line_length:]
        pdf.set_x(10)
        pdf.multi_cell(0, 10, linea, align='L')


    nombre_archivo = f"reportes/reporte_{siguiente_num:03}.pdf"
    pdf.output(nombre_archivo)
    print(f"📄 Reporte guardado como {nombre_archivo}")
