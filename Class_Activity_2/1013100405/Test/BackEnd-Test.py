import os
from datetime import datetime
import requests
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("✅ User created:", user_data)
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("✅ Task created:", task_data)
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()
    print(f"🗑️ Task {task_id} deleted")

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()
    print(f"🗑️ User {user_id} deleted")

def generar_reporte_pdf(contenido):
    carpeta = "test_reports"
    os.makedirs(carpeta, exist_ok=True)
    existentes = [f for f in os.listdir(carpeta) if f.startswith("reporte_test_") and f.endswith(".pdf")]
    numeros = [int(f.split("_")[-1].replace(".pdf", "")) for f in existentes]
    siguiente = max(numeros) + 1 if numeros else 1
    nombre_archivo = f"reporte_test_{siguiente:03}.pdf"
    ruta_completa = os.path.join(carpeta, nombre_archivo)

    c = canvas.Canvas(ruta_completa, pagesize=LETTER)
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, "Reporte de pruebas de integración - Backend")
    c.drawString(50, 730, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, 710, f"Reporte N° {siguiente}")

    y = 690
    for linea in contenido.splitlines():
        c.drawString(50, y, linea)
        y -= 20
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = 750

    c.save()
    print(f"✅ Reporte generado: {ruta_completa}")

def integration_test():
    user_id = None
    task_id = None
    estado = "✅ Exitoso"
    error = ""

    try:
        user_id = create_user("Camilo")
        task_id = create_task(user_id, "Prepare presentation")

        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
        print("✅ Test completed: task was successfully registered and linked to the user.")

    except Exception as e:
        estado = "❌ Fallido"
        error = str(e)
        print("⚠️ Error en el test:", error)

    finally:
        if task_id:
            try:
                delete_task(task_id)
            except Exception as e:
                print(f"❌ No se pudo eliminar la tarea: {e}")
        if user_id:
            try:
                delete_user(user_id)
            except Exception as e:
                print(f"❌ No se pudo eliminar el usuario: {e}")

        contenido = f"""
Resultado de prueba de integración:
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Estado: {estado}
Usuario ID: {user_id or 'N/A'}
Tarea ID: {task_id or 'N/A'}
Error (si ocurrió): {error or 'Ninguno'}
"""
        generar_reporte_pdf(contenido)

if __name__ == "__main__":
    integration_test()