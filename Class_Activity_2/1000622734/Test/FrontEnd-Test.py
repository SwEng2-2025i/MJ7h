import time
import io
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fpdf import FPDF

def abrir_frontend(driver):
    # Opens the frontend application in the browser
    driver.get("http://localhost:5000")
    time.sleep(2)  # Give the page time to load

def crear_usuario(driver, wait, test_user):
    # Fills out the user creation form and submits it
    # Then retrieves and returns the newly created user ID
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys(test_user)
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    print(user_result)
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))  # Extract numeric ID from result
    return user_id

def crear_tarea(driver, wait, user_id, test_task):
    # Fills out the task creation form with a task and user ID, then submits it
    # Waits until the confirmation text appears and asserts the result
    task_input = driver.find_element(By.ID, "task")
    task_input.send_keys(test_task)
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
    print(task_result.text)
    assert "Tarea creada con ID" in task_result.text
    task_id = ''.join(filter(str.isdigit, task_result.text))  # Extract numeric ID from result
    return task_id

def verificar_tarea(driver, user_id, test_id, test_task):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Lista de tareas:\n" + tasks)
    assert f"{test_id}: {test_task} (Usuario con ID {user_id})" in tasks
    print("✅ La tarea registrada se encuentra en la lista de tareas.")

def eliminar_tarea(driver, task_id):
    # Deletes a task by its ID and verifies the deletion
    task_delete_input = driver.find_element(By.ID, "task-delete")
    task_delete_input.send_keys(task_id)
    time.sleep(1)

    eliminar_tarea_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Eliminar Tarea')]")
    eliminar_tarea_btn.click()
    time.sleep(2)

    task_delete_result = driver.find_element(By.ID, "task-delete-result").text
    print(task_delete_result)
    assert f"Tarea con ID {task_id} eliminada" in task_delete_result

def eliminar_usuario(driver, user_id):
    # Deletes a user by its ID and verifies the deletion
    user_delete_input = driver.find_element(By.ID, "userid-delete")
    user_delete_input.send_keys(user_id)
    time.sleep(1)

    eliminar_usuario_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Eliminar Usuario')]")
    eliminar_usuario_btn.click()
    time.sleep(2)

    user_delete_result = driver.find_element(By.ID, "user-delete-result").text
    print(user_delete_result)
    assert f"Usuario con ID {user_id} eliminado" in user_delete_result

def export_to_pdf(buffer, out_dir="./results/"):
    name = "FrontEnd-Test"
    os.makedirs(out_dir, exist_ok=True)

    # Simple sequential name logic
    i = 1
    while os.path.exists(os.path.join(out_dir, f"{name}_{i}.pdf")):
        i += 1
    filepath = os.path.join(out_dir, f"{name}_{i}.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Segoe UI", "", r"C:\Windows\Fonts\segoeui.ttf", uni=True)
    pdf.set_font("Segoe UI", size=12)
    for line in buffer.getvalue().splitlines():
        pdf.cell(0, 10, line, ln=True)
    pdf.output(filepath)

def main():
    # Main test runner that initializes the browser and runs the full E2E flow
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    # Test data
    test_user = "Camilo"
    test_task = "Terminar laboratorio"

    # Buffer to capture print statements
    buffer = io.StringIO()
    sys.stdout = buffer

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait, test_user)
        task_id = crear_tarea(driver, wait, user_id, test_task)
        verificar_tarea(driver, user_id, task_id, test_task)
        eliminar_tarea(driver, task_id)
        eliminar_usuario(driver, user_id)
        print("✅ Test completo: Usuario y tarea creados, verificados y eliminados correctamente.")
        time.sleep(3)  # Final delay to observe results if not running headless
    finally:
        driver.quit()  # Always close the browser at the end

    # Export captured print statements to PDF
    sys.stdout = sys.__stdout__
    export_to_pdf(buffer)

if __name__ == "__main__":
    main()
