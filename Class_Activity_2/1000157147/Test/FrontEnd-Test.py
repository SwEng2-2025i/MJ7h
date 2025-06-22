import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests 
from reportlab.pdfgen import canvas
import os
import datetime

USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()

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
    task_id = ''.join(filter(str.isdigit, task_result.text))  # 👈 Extrae ID
    return task_id

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

def main():
    resultados = []
    # Main test runner that initializes the browser and runs the full E2E flow
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        resultados.append("✅ Frontend opened")

        user_id = crear_usuario(driver, wait)
        resultados.append(f"✅ User created with ID {user_id}")

        task_id = crear_tarea(driver, wait, user_id)
        resultados.append(f"✅ Task created with ID {task_id}")

        ver_tareas(driver)
        resultados.append("✅ Task appeared in frontend list")

        time.sleep(3)  # Final delay to observe results if not running headless
        delete_task(task_id)
        delete_user(user_id)
        resultados.append("✅ Data cleaned up")
        print("✅ Data cleaned up")
    except Exception as e:
        resultados.append(f"❌ ERROR: {str(e)}")
        print(f"❌ ERROR: {str(e)}")

    finally:
        driver.quit()  # Always close the browser at the end
        generar_reporte_pdf(resultados, nombre="frontend")

def generar_reporte_pdf(resultados, nombre="frontend"):
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
    main()
