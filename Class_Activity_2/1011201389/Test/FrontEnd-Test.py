import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

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

def delete_task(task_id):
    try:
        response = requests.delete(f"{TASKS_URL}/{task_id}")
        if response.status_code == 200:
            print(f"🗑️ Task {task_id} deleted.")
        else:
            print(f"⚠️ Could not delete task {task_id}: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception while deleting task: {e}")

def delete_user(user_id):
    try:
        response = requests.delete(f"{USERS_URL}/{user_id}")
        if response.status_code == 200:
            print(f"🗑️ User {user_id} deleted.")
        else:
            print(f"⚠️ Could not delete user {user_id}: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception while deleting user: {e}")

def main():
    driver = webdriver.Chrome()
    user_id = None
    task_id = None

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait)

        if user_id:
            task_id = crear_tarea(driver, wait, user_id)

        if task_id:
            ver_tareas(driver)
            time.sleep(3)  # Para observar el resultado

    except Exception as e:
        print(f"❌ Ocurrió un error durante el test: {e}")

    finally:
        # Solo eliminamos si fueron creados
        if task_id:
            delete_task(task_id)
        if user_id:
            delete_user(user_id)

        driver.quit()

if __name__ == "__main__":
    main()
