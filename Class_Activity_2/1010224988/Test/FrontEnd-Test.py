from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import time
import requests
import os

def abrir_frontend(driver):
    # Opens the frontend application in the browser
    driver.get("http://localhost:5000")
    time.sleep(2)  # Give the page time to load

def crear_usuario(driver, wait):
    # Fills out the user creation form and submits it
    # Then retrieves and returns the newly created user ID
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    print("Resultado usuario:", user_result)
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))  # Extract numeric ID from result
    return user_id

def crear_tarea(driver, wait, user_id):
    # Fills out the task creation form with a task and user ID, then submits it
    # Waits until the confirmation text appears and asserts the result
    task_input = driver.find_element(By.ID, "task")
    task_input.send_keys("Terminar laboratorio")
    time.sleep(1)

    userid_input = driver.find_element(By.ID, "userid")
    userid_input.send_keys(user_id)
    userid_input.send_keys('\t')  # Force focus out of the input to trigger validation
    time.sleep(1)

    crear_tarea_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']"))
    )
    crear_tarea_btn.click()
    time.sleep(2)

    wait.until(
        EC.text_to_be_present_in_element((By.ID, "task-result"), "Tarea creada con ID")
    )
    task_result = driver.find_element(By.ID, "task-result")
    print("Texto en task_result:", task_result.text)
    assert "Tarea creada con ID" in task_result.text

    task_id = ''.join(filter(str.isdigit, task_result.text))
    return task_id

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

def eliminar_tarea(task_id):
    response = requests.delete(f"http://localhost:5002/tasks/{task_id}")
    if response.status_code == 200:
        print(f"🗑️ Tarea {task_id} eliminada")
    else:
        print(f"⚠️ No se pudo eliminar la tarea {task_id}: {response.text}")

def eliminar_usuario(user_id):
    response = requests.delete(f"http://localhost:5001/users/{user_id}")
    if response.status_code == 200:
        print(f"🗑️ Usuario {user_id} eliminado")
    else:
        print(f"⚠️ No se pudo eliminar el usuario {user_id}: {response.text}")

def verificar_eliminacion_tarea(task_id):
    response = requests.get("http://localhost:5002/tasks")
    response.raise_for_status()
    tasks = response.json()
    return all(str(task["id"]) != str(task_id) for task in tasks)

def verificar_eliminacion_usuario(user_id):
    response = requests.get("http://localhost:5001/users")
    response.raise_for_status()
    users = response.json()
    return all(str(user["id"]) != str(user_id) for user in users)

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_frontend_pdf_report(user_id, task_id, test_result="Success", error_details=None, start_time=None, end_time=None):
    reports_dir = "test_reports"
    os.makedirs(reports_dir, exist_ok=True)

    existing_reports = [f for f in os.listdir(reports_dir) if f.startswith("front_test_report_") and f.endswith(".pdf")]
    next_number = 1
    if existing_reports:
        numbers = [int(f.split("_")[-1].split(".")[0]) for f in existing_reports if f.split("_")[-1].split(".")[0].isdigit()]
        next_number = max(numbers) + 1 if numbers else 1

    report_name = f"front_test_report_{next_number:03}.pdf"
    report_path = os.path.join(reports_dir, report_name)

    formatted_start = start_time.strftime("%Y-%m-%d %H:%M:%S") if start_time else "N/A"
    formatted_end = end_time.strftime("%Y-%m-%d %H:%M:%S") if end_time else "N/A"
    duration = (end_time - start_time).total_seconds() if start_time and end_time else None

    c = canvas.Canvas(report_path, pagesize=letter)
    c.setFont("Helvetica", 12)

    c.drawString(50, 770, f"🧪 Frontend Test Report #{next_number}")
    c.drawString(50, 750, f"Date: {formatted_start}")
    c.drawString(50, 735, f"End: {formatted_end}")
    if duration:
        c.drawString(50, 720, f"Duration: {duration:.2f} seconds")
    c.drawString(50, 700, f"Result: {test_result}")

    y = 680
    c.drawString(50, y, f"User ID created: {user_id}")
    y -= 20
    c.drawString(50, y, f"Task ID created: {task_id}")

    y -= 30
    if test_result == "Failure" and error_details:
        c.drawString(50, y, "❌ Error details:")
        for line in error_details.splitlines():
            y -= 20
            c.drawString(70, y, line)

    y -= 40
    c.drawString(50, y, "✅ Cleanup: User and task were deleted after test.")
    c.save()

    print(f"📄 Reporte frontend test guardado como: {report_path}")

def main():

    start_time = datetime.now()

    # Main test runner that initializes the browser and runs the full E2E flow
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    user_id = None
    task_id = None

    error_details = None
    result = "Success"

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)

        user_id = crear_usuario(driver, wait)
        task_id = crear_tarea(driver, wait, user_id)
        
        ver_tareas(driver)
        time.sleep(3)  # Final delay to observe results if not running headless

    except Exception as e:
        result = "Failure"
        error_details = str(e)
        print("❌ Error durante la prueba:", error_details)

    finally:
        driver.quit()  # Always close the browser at the end

        if task_id:
            eliminar_tarea(task_id)
            assert verificar_eliminacion_tarea(task_id), f"❌ La tarea {task_id} no fue eliminada correctamente"
            print(f"✅ Verificada eliminación de tarea {task_id}")

        if user_id:
            eliminar_usuario(user_id)
            assert verificar_eliminacion_usuario(user_id), f"❌ El usuario {user_id} no fue eliminado correctamente"
            print(f"✅ Verificada eliminación de usuario {user_id}")

        end_time = datetime.now()

        # Generar PDF de reporte frontend
        generate_frontend_pdf_report(
            user_id=user_id,
            task_id=task_id,
            test_result=result,
            error_details=error_details,
            start_time=start_time,
            end_time=end_time
        )

if __name__ == "__main__":
    main()
