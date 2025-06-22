import requests
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    return user_data["id"]

def get_user(user_id):
    response = requests.get(f"{USERS_URL}/{user_id}")
    return response

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    return response

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    return task_data["id"]

def get_task(task_id):
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    for t in tasks:
        if t["id"] == task_id:
            return t
    return None

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    return response

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    return response.json()

def generar_pdf_reporte(resultados):
    base = "backend_test_report"
    n = 1
    while os.path.exists(f"{base}_{n}.pdf"):
        n += 1
    filename = f"{base}_{n}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Reporte de Pruebas Backend")
    c.setFont("Helvetica", 12)
    y = height - 90
    for linea in resultados:
        c.drawString(50, y, linea)
        y -= 20
    c.save()
    print(f"Reporte generado: {filename}")

def backend_tests():
    resultados = []
    # Test crear usuario
    try:
        user_id = create_user("TestUser")
        resultados.append(f"✅ Usuario creado con ID: {user_id}")
    except Exception as e:
        resultados.append(f"❌ Error al crear usuario: {e}")
        generar_pdf_reporte(resultados)
        return

    # Test obtener usuario
    resp = get_user(user_id)
    if resp.status_code == 200 and resp.json().get("id") == user_id:
        resultados.append(f"✅ Usuario obtenido correctamente: {resp.json()}")
    else:
        resultados.append(f"❌ Error al obtener usuario: {resp.text}")

    # Test crear tarea
    try:
        task_id = create_task(user_id, "Test Task")
        resultados.append(f"✅ Tarea creada con ID: {task_id}")
    except Exception as e:
        resultados.append(f"❌ Error al crear tarea: {e}")
        # Cleanup usuario antes de salir
        delete_user(user_id)
        generar_pdf_reporte(resultados)
        return

    # Test obtener tarea
    task = get_task(task_id)
    if task and task["id"] == task_id:
        resultados.append(f"✅ Tarea obtenida correctamente: {task}")
    else:
        resultados.append(f"❌ Error al obtener tarea con ID {task_id}")

    # Test eliminar tarea
    resp = delete_task(task_id)
    if resp.status_code == 200:
        resultados.append(f"✅ Tarea {task_id} eliminada correctamente.")
    else:
        resultados.append(f"❌ Error al eliminar tarea {task_id}: {resp.text}")

    # Verificar que la tarea fue eliminada
    task = get_task(task_id)
    if not task:
        resultados.append(f"✅ Verificado: la tarea {task_id} ya no existe.")
    else:
        resultados.append(f"❌ Error: la tarea {task_id} aún existe.")

    # Test eliminar usuario
    resp = delete_user(user_id)
    if resp.status_code == 200:
        resultados.append(f"✅ Usuario {user_id} eliminado correctamente.")
    else:
        resultados.append(f"❌ Error al eliminar usuario {user_id}: {resp.text}")

    # Verificar que el usuario fue eliminado
    resp = get_user(user_id)
    if resp.status_code == 404:
        resultados.append(f"✅ Verificado: el usuario {user_id} ya no existe.")
    else:
        resultados.append(f"❌ Error: el usuario {user_id} aún existe.")

    generar_pdf_reporte(resultados)

if __name__ == "__main__":
    backend_tests()