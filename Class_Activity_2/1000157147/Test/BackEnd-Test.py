import requests
from reportlab.pdfgen import canvas
import os
import datetime
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

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()

def integration_test():
    resultados = []
    try:
        # Step 1: Create user
        user_id = create_user("Camilo")
        resultados.append("✅ User created")

        # Step 2: Create task
        task_id = create_task(user_id, "Prepare presentation")
        resultados.append("✅ Task created")

        # Step 3: Verify task is linked to the user
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        assert any(t["id"] == task_id for t in user_tasks), "❌ Task was not correctly registered"
        print("✅ Task successfully registered and linked to user")
        resultados.append("✅ Task found in DB")

        # Step 4: Clean up
        delete_task(task_id)
        delete_user(user_id)
        print("✅ Cleanup completed")
        resultados.append("✅ Data deleted")

        # Step 5: Verify deletion
        tasks_after = get_tasks()
        assert not any(t["id"] == task_id for t in tasks_after), "❌ Task was not deleted"
        print("✅ Verification complete: task was deleted successfully")
        resultados.append("✅ Deletion verified")
    
    except Exception as e:
        resultados.append(f"❌ ERROR: {str(e)}")

    generar_reporte_pdf(resultados, nombre="backend")

def generar_reporte_pdf(resultados, nombre="backend"):
    carpeta = "reports"
    os.makedirs(carpeta, exist_ok=True)

    existentes = [f for f in os.listdir(carpeta) if f.startswith(f"{nombre}_") and f.endswith(".pdf")]
    next_num = len(existentes) + 1
    nombre_archivo = f"{carpeta}/{nombre}_{next_num}.pdf"

    c = canvas.Canvas(nombre_archivo)
    c.setFont("Helvetica", 12)
    c.drawString(50, 800, f"Integration Test Report - {nombre.capitalize()}")
    c.drawString(50, 780, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    y = 750
    for linea in resultados:
        c.drawString(50, y, linea)
        y -= 20
        if y < 50:
            c.showPage()
            y = 800

    c.save()
    print(f"🧾 PDF report generated: {nombre_archivo}")

if __name__ == "__main__":
    integration_test()