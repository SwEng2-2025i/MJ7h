import time
import io
import sys
from pdf_report import generar_reporte_pdf
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

def eliminar_tarea(driver, task_id):
    delete_taskid_input = driver.find_element(By.ID, "delete-taskid")
    delete_taskid_input.send_keys(task_id)
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Eliminar Tarea')]").click()
    time.sleep(2)
    delete_task_result = driver.find_element(By.ID, "delete-task-result").text
    print("Resultado eliminacion tarea:", delete_task_result)
    assert "Tarea eliminada exitosamente" in delete_task_result


def eliminar_usuario(driver, user_id):
    delete_userid_input = driver.find_element(By.ID, "delete-userid")
    delete_userid_input.send_keys(user_id)
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Eliminar Usuario')]").click()
    time.sleep(2)
    delete_user_result = driver.find_element(By.ID, "delete-user-result").text
    print("Resultado eliminacion usuario:", delete_user_result)
    assert "Usuario eliminado exitosamente" in delete_user_result

def crear_tarea_con_usuario_invalido(driver, wait, user_id):

        task_input = driver.find_element(By.ID, "task")
        task_input.clear()
        task_input.send_keys("Tarea inválida")
        time.sleep(1)

        userid_input = driver.find_element(By.ID, "userid")
        userid_input.clear()

        userid_input.send_keys(user_id)  # Usuario que no existe
        userid_input.send_keys('\t')
        time.sleep(1)

        crear_tarea_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']"))
        )
        crear_tarea_btn.click()
        time.sleep(2)

        wait.until(
        EC.text_to_be_present_in_element((By.ID, "task-result"), "Error: ID de usuario inválido")
        )

        error_message = driver.find_element(By.ID, "task-result").text

        assert "Tarea creada con ID" not in error_message, "Tarea fue creada con usuario inválido"
        assert "error" in error_message.lower() or "no existe" in error_message.lower(), "No se mostró mensaje de error esperado"
        print("Test negativo fue exitoso.")


def main():
    log = io.StringIO()
    original_stdout = sys.stdout
    sys.stdout = log
    # Main test runner that initializes the browser and runs the full E2E flow
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait)
        task_id = crear_tarea(driver, wait, user_id)
        ver_tareas(driver)
        time.sleep(3)  # Final delay to observe results if not running headless
        # Delete task and user through the frontend
        eliminar_tarea(driver, task_id)
        eliminar_usuario(driver, user_id)
        crear_tarea_con_usuario_invalido(driver, wait, user_id)  # Test negativo
    finally:
        driver.quit()  # Always close the browser at the end
        sys.stdout = original_stdout  # Restaurar salida
        generar_reporte_pdf(log.getvalue())
        log.close()

if __name__ == "__main__":
    main()
