import time
import requests
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reporting.pdf_generator import generate_pdf_report

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def abrir_frontend(driver):
    # Opens the frontend application in the browser
    driver.get("http://localhost:5000")
    time.sleep(2)  # Give the page time to load

def crear_usuario(driver, wait, logs):
    # Fills out the user creation form and submits it
    # Then retrieves and returns the newly created user ID
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    logs.append(f"Resultado usuario: {user_result}")
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))  # Extract numeric ID from result
    return user_id

def crear_tarea(driver, wait, user_id, logs):
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
    logs.append(f"Texto en task_result: {task_result.text}")
    assert "Tarea creada con ID" in task_result.text
    task_id = ''.join(filter(str.isdigit, task_result.text))
    return task_id

def ver_tareas(driver, logs):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    logs.append(f"Tareas: {tasks}")
    assert "Terminar laboratorio" in tasks

def main(logs):
    # Main test runner that initializes the browser and runs the full E2E flow
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)
    user_id = None
    task_id = None

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait, logs)
        task_id = crear_tarea(driver, wait, user_id, logs)
        ver_tareas(driver, logs)
        logs.append("\n✅ Frontend E2E test completed successfully.")
        time.sleep(3)
    finally:
        logs.append("\n🧹 Starting data cleanup...")
        if task_id:
            response = requests.delete(f"{TASKS_URL}/{task_id}")
            if response.status_code == 200:
                logs.append(f"✅ Task {task_id} deleted.")
                # Verify deletion
                verify_response = requests.get(f"{TASKS_URL}/{task_id}")
                assert verify_response.status_code == 404
                logs.append(f"✅ Task {task_id} verified as deleted.")
            else:
                logs.append(f"❌ Error deleting task {task_id}: {response.text}")

        if user_id:
            response = requests.delete(f"{USERS_URL}/{user_id}")
            if response.status_code == 200:
                logs.append(f"✅ User {user_id} deleted.")
                # Verify deletion
                verify_response = requests.get(f"{USERS_URL}/{user_id}")
                assert verify_response.status_code == 404
                logs.append(f"✅ User {user_id} verified as deleted.")
            else:
                logs.append(f"❌ Error deleting user {user_id}: {response.text}")

        driver.quit()  # Always close the browser at the end
        logs.append("\n✅ Cleanup finished. Test run complete.")


if __name__ == "__main__":
    logs = []
    try:
        main(logs)
    finally:
        for line in logs:
            print(line)
        generate_pdf_report("FrontEnd_Test", logs)
