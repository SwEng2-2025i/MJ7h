import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

import requests
from report import generate_report

USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"


def abrir_frontend(driver):
    # Opens the frontend application in the browser
    driver.get("http://localhost:5000")
    time.sleep(2)  # Give the page time to load

def crear_usuario(driver, wait):
    username_input = driver.find_element(By.ID, "username")
    username_input.clear()
    username_input.send_keys("Ana")
    time.sleep(0.5)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "user-result"), "Usuario creado con ID"))
    user_result = driver.find_element(By.ID, "user-result").text
    print("Resultado usuario:", user_result)
    assert "Usuario creado con ID" in user_result
    return ''.join(filter(str.isdigit, user_result))


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

    # 🔑 Esperamos hasta que aparezca el mensaje de confirmación
    wait.until(
        EC.text_to_be_present_in_element((By.ID, "task-result"), "Tarea creada con ID")
    )

    task_text = driver.find_element(By.ID, "task-result").text
    print("Texto en task_result:", task_text)
    assert "Tarea creada con ID" in task_text
    task_id = ''.join(filter(str.isdigit, task_text))
    return task_id


def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

def main():
    options = Options()
    service = Service(r"C:\WebDriver\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        wait = WebDriverWait(driver, 10)

        # --- Flujo UI E2E ---
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait)
        task_id = crear_tarea(driver, wait, user_id)
        ver_tareas(driver)

        # --- Data cleanup vía API ---
        r1 = requests.delete(f"{TASKS_URL}/{task_id}")
        assert r1.status_code == 204
        r2 = requests.delete(f"{USERS_URL}/{user_id}")
        assert r2.status_code == 204
        print("✅ FrontEnd cleanup verified")

        # --- Generar PDF ---
        summary = (
            f"FrontEnd E2E Test\n"
            f"User ID: {user_id}\n"
            f"Task ID: {task_id}\n"
            "All steps passed and cleanup verified."
        )
        pdf_path = generate_report("FrontEnd E2E", summary)
        print(f"📄 Report generated at {pdf_path}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
