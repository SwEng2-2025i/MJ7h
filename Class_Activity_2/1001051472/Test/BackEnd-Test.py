import requests
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
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
    print("✅ Task deleted:", response.json())
    return response

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    print("✅ User deleted:", response.json())
    return response

def generar_reporte_pdf(resultados):
    # Buscar el siguiente número de reporte
    report_dir = os.path.dirname(os.path.abspath(__file__))
    existing = [f for f in os.listdir(report_dir) if f.startswith('test_report_') and f.endswith('.pdf')]
    nums = [int(f.split('_')[-1].split('.')[0]) for f in existing if f.split('_')[-1].split('.')[0].isdigit()]
    next_num = max(nums) + 1 if nums else 1
    filename = os.path.join(report_dir, f"test_report_{next_num}.pdf")
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, f"Test Report #{next_num}")
    c.drawString(50, 735, f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y = 710
    for line in resultados:
        c.drawString(50, y, line)
        y -= 20
    c.save()
    print(f"PDF report generated: {filename}")

def integration_test():
    resultados = []
    try:
        # Step 1: Create user
        user_id = create_user("Camilo")
        resultados.append(f"Usuario creado con ID: {user_id}")

        # Step 2: Create task for that user
        task_id = create_task(user_id, "Prepare presentation")
        resultados.append(f"Tarea creada con ID: {task_id} para usuario {user_id}")

        # Step 3: Verify that the task is registered and associated with the user
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
        resultados.append("✅ La tarea fue correctamente registrada y asociada al usuario.")

        response = delete_task(task_id)
        assert response.status_code == 200, "❌ The task was not deleted successfully"
        resultados.append("✅ La tarea fue eliminada correctamente.")

        res = delete_user(user_id)
        assert res.status_code == 200, "❌ The user was not deleted successfully"
        resultados.append("✅ El usuario fue eliminado correctamente.")

        resultados.append("TEST PASSED")
        
        
        
        # TEST 2- PRUEBA DE  ELIMINAR USUARIO CON ID 0 FALLIDA
        
        # Step 1: Create user
        user_id = create_user("Camilo")
        resultados.append(f"Usuario creado con ID: {user_id}")

        # Step 2: Create task for that user
        task_id = create_task(user_id, "Prepare presentation")
        resultados.append(f"Tarea creada con ID: {task_id} para usuario {user_id}")

        # Step 3: Verify that the task is registered and associated with the user
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
        resultados.append("✅ La tarea fue correctamente registrada y asociada al usuario.")

        response = delete_task(task_id)
        assert response.status_code == 200, "❌ The task was not deleted successfully"
        resultados.append("✅ La tarea fue eliminada correctamente.")

        res = delete_user(0)
        assert res.status_code == 200, "❌ The user was not deleted successfully"
        resultados.append("✅ El usuario fue eliminado correctamente.")

        resultados.append("TEST PASSED")
        
        
        
    except AssertionError as e:
        resultados.append(str(e))
        resultados.append("TEST FAILED")
    except Exception as e:
        resultados.append(f"Error inesperado: {e}")
        resultados.append("TEST FAILED")
    finally:
        generar_reporte_pdf(resultados)

if __name__ == "__main__":
    integration_test()