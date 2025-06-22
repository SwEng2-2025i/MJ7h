import requests
import platform
from fpdf import FPDF
from datetime import datetime
import os
import sys


# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

# Create
def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print(f"Usuario creado: {user_data['id']} - {user_data['name']}")
    return user_data['id']

def create_task(user_id, title):
    response = requests.post(TASKS_URL, json={"user_id": user_id, "title": title})
    response.raise_for_status()
    task_data = response.json()
    print(f"Tarea creada: {task_data['id']} - {task_data['title']}")
    return task_data['id']

# Delete
def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()
    print(f"Usuario eliminado: {user_id}")
    return response.json()

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()
    print(f"Tarea eliminada: {task_id}")
    return response.json()

# Get
def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    print("Tareas:")
    for task in tasks:
        print(f"ID: {task['id']}, Título: {task['title']}, Usuario ID: {task['user_id']}")
    return tasks

def get_user(user_id):
    response = requests.get(f"{USERS_URL}/{user_id}")
    if response.status_code == 404:
        print(f"Usuario no encontrado: {user_id}")
        return None
    response.raise_for_status()
    user = response.json()
    print(f"Usuario encontrado: {user['id']} - {user['name']}")
    return user

# Generate PDF
def generate_pdf(test_data):
    # Crear directorio si no existe
    os.makedirs("reports", exist_ok=True)

    # Numeración automática
    existing_reports = [f for f in os.listdir("reports") if f.startswith("report_") and f.endswith(".pdf")]
    report_number = len(existing_reports) + 1
    filename = f"reports/report_{report_number}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in test_data:
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.output(filename)
    print(f" Report saved to {filename}")

# integration test():

def integration_test():
    report_lines = []
    try:
        # Create user
        user_id = create_user("Ana")
        report_lines.append(f"Usuario creado: {user_id}")

        # Create task
        task_id = create_task(user_id, "Terminar laboratorio")
        report_lines.append(f"Tarea creada: {task_id}")

        
        tasks = get_tasks()
        report_lines.append(f"Tareas creadas con ID:  {[task['id'] for task in tasks]} para el usuario {user_id}")
        assert len(tasks) > 0, "No se encontraron tareas"
        report_lines.append("Todas las tareas obtenidas correctamente.")

        # cleean up data
        delete_task(task_id)
        report_lines.append(f"Tarea eliminada: {task_id}")

        delete_user(user_id)
        report_lines.append(f"Usuario eliminado: {user_id}")

        #verify clean up
        remaining_tasks = get_tasks()
        assert all(t["id"] != task_id for t in remaining_tasks), "No se eliminaron todas las tareas"
        report_lines.append("Todas las tareas eliminadas correctamente.")

        report_lines.append("Test de integración exitoso.")

    
    except requests.RequestException as e:
        report_lines.append(f"Error en la solicitud: {e}")
    
    finally:
        # Generate PDF report
        generate_pdf(report_lines)


# Main test function
if __name__ == "__main__":
    print("Iniciando test de integración...")
    integration_test()
    print("Test de integración completado.")