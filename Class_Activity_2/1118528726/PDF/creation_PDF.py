from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
import os  

import requests

# Endpoints
PDF_URL = "http://localhost:5004/pdf/logs"

def create_log_pdf(name):
    response = requests.post(PDF_URL, json={"title": name})
    response.raise_for_status()
    log_data = response.json()
    print("✅ log pdf save correcttly:", log_data)
    return log_data["id"]

def get_next_id():
    response = requests.get(f"{PDF_URL}/getId")
    response.raise_for_status()
    tasks = response.json()
    return tasks


def generar_pdf(nombreTest:str, datos):

    # Obtener el ID del log desde el backend
    log_data = get_next_id()
    id = log_data["id"]
    nameFile= nombreTest + "_" + str(id) + ".pdf"
    rutaSalida = os.path.join("PDF_TEST", nameFile)

    # Crear carpetas si no existen
    os.makedirs(os.path.dirname(rutaSalida), exist_ok=True)

    print(f"Generando PDF en: {rutaSalida}")


    c = canvas.Canvas(rutaSalida, pagesize=LETTER)
    c.setFont("Helvetica", 12)

    x = 50
    y = 750  # Coordenada inicial (parte superior)

    c.drawString(x+200,y , nombreTest + "_" + str(id))

    y -= 30

    for etiqueta, texto in datos:
        # Dibujar la etiqueta
        c.drawString(x, y, etiqueta)
        y -= 15

        # Dibujar el contenido, línea por línea si hay saltos de línea
        for linea in texto.split('\n'):
            c.drawString(x + 20, y, linea)
            y -= 15

        y -= 10  # Espacio entre bloques

        # Si se acaba la página
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = 750

    c.save()
    # Guardar el log en la base de datos 
    create_log_pdf(nameFile)
    print(f"PDF generado: {nameFile}")
