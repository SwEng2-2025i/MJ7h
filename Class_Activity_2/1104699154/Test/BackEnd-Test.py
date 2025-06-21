import requests
import os
from fpdf import FPDF  # pip install fpdf
from datetime import datetime

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    return response.json()

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()

def generate_pdf_report(content):
    # Crear directorio si no existe
    os.makedirs("reports", exist_ok=True)

    # Numeración automática
    existing_reports = [f for f in os.listdir("reports") if f.startswith("report_") and f.endswith(".pdf")]
    report_number = len(existing_reports) + 1
    filename = f"reports/report_{report_number}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in content:
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.output(filename)
    print(f" Report saved to {filename}")

def integration_test():
    report_lines = []
    try:
        user_id = create_user("Camilo")
        report_lines.append(f" Usuario creado con ID {user_id}")

        task_id = create_task(user_id, "Prepare presentation")
        report_lines.append(f" Tarea creada con ID {task_id} para el usuario {user_id}")

        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        assert any(t["id"] == task_id for t in user_tasks), " La tarea no está registrada"
        report_lines.append(" La tarea está correctamente registrada y asociada al usuario")

        # Limpieza de datos
        delete_task(task_id)
        report_lines.append(f" Tarea {task_id} eliminada")

        delete_user(user_id)
        report_lines.append(f" Usuario {user_id} eliminado")

        # Verificación de limpieza
        remaining_tasks = get_tasks()
        assert all(t["id"] != task_id for t in remaining_tasks), " La tarea no fue eliminada"
        report_lines.append(" Verificación: la tarea fue eliminada correctamente")

        report_lines.append(" Prueba completada exitosamente.")

    except Exception as e:
        report_lines.append(f" Error durante la prueba: {str(e)}")

    finally:
        generate_pdf_report(report_lines)

if __name__ == "__main__":
    integration_test()
