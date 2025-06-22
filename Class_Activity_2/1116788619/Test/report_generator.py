import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
from datetime import datetime

# Ruta absoluta para evitar errores de ubicación
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # .../Test
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

def siguiente_nombre_pdf():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    existentes = [f for f in os.listdir(REPORTS_DIR) if f.startswith("report_") and f.endswith(".pdf")]
    numero = len(existentes) + 1
    return os.path.join(REPORTS_DIR, f"report_{numero}.pdf")

def generar_grafica(user, task, ruta_imagen):
    labels = ['Usuario', 'Tarea']
    valores = [1 if user else 0, 1 if task else 0]

    import numpy as np
    fig, ax = plt.subplots()
    ax.bar(labels, valores, color=['blue', 'green'])
    ax.set_ylabel('Creado (1 = sí)')
    ax.set_title('Resumen de creación de entidades')
    plt.savefig(ruta_imagen)
    plt.close()

def generar_reporte_backend(user, task):
    archivo_pdf = siguiente_nombre_pdf()
    imagen_temp = os.path.join(REPORTS_DIR, "temp_plot.png")

    generar_grafica(user, task, imagen_temp)

    c = canvas.Canvas(archivo_pdf, pagesize=letter)
    c.setFont("Helvetica", 14)
    c.drawString(50, 750, "Reporte de Prueba de Integración - Backend")
    c.setFont("Helvetica", 10)
    c.drawString(50, 730, f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, 710, f"Usuario creado: {user['name']} (ID: {user['id']})")
    c.drawString(50, 695, f"Tarea creada: {task['title']} (ID: {task['id']})")
    c.drawString(50, 675, "Resultado: ✅ Pruebas ejecutadas con éxito y datos eliminados correctamente")
    c.drawImage(imagen_temp, 50, 450, width=400, height=200)
    c.save()
    os.remove(imagen_temp)
    print(f"📄 Reporte PDF guardado en: {archivo_pdf}")

def generar_reporte_frontend(user_id, task_id):
    archivo_pdf = siguiente_nombre_pdf()

    c = canvas.Canvas(archivo_pdf, pagesize=letter)
    c.setFont("Helvetica", 14)
    c.drawString(50, 750, "Reporte de Prueba E2E - Frontend + Backend")
    c.setFont("Helvetica", 10)
    c.drawString(50, 730, f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, 710, f"ID de usuario creado: {user_id}")
    c.drawString(50, 695, f"ID de tarea creada: {task_id}")
    c.drawString(50, 675, "Resultado: ✅ Prueba E2E completada con éxito y datos limpiados")
    c.save()
    print(f"📄 Reporte PDF guardado en: {archivo_pdf}")
