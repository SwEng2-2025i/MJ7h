import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from report_generator import TestReportGenerator

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

def borrar_usuario(driver, wait, user_id):
    # Fills out the user deletion form with a user ID and submits it
    # Waits until the confirmation text appears and asserts the result
    delete_userid_input = driver.find_element(By.ID, "delete-userid")
    delete_userid_input.send_keys(user_id)
    time.sleep(1)

    eliminar_usuario_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Eliminar Usuario')]"))
    )
    eliminar_usuario_btn.click()
    time.sleep(2)

    wait.until(
        EC.text_to_be_present_in_element((By.ID, "delete-user-result"), "Usuario eliminado con ID")
    )
    delete_user_result = driver.find_element(By.ID, "delete-user-result")
    print("Resultado eliminación usuario:", delete_user_result.text)
    assert "Usuario eliminado con ID" in delete_user_result.text

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
    return ''.join(filter(str.isdigit, task_result.text))  # Extract numeric ID from result

def borrar_tarea(driver, wait, task_id):
    # Fills out the task deletion form with a task ID and submits it
    # Waits until the confirmation text appears and asserts the result
    delete_taskid_input = driver.find_element(By.ID, "delete-taskid")
    delete_taskid_input.send_keys(task_id)
    time.sleep(1)

    eliminar_tarea_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Eliminar Tarea')]"))
    )
    eliminar_tarea_btn.click()
    time.sleep(2)

    wait.until(
        EC.text_to_be_present_in_element((By.ID, "delete-task-result"), "Tarea eliminada con ID")
    )
    delete_task_result = driver.find_element(By.ID, "delete-task-result")
    print("Resultado eliminación tarea:", delete_task_result.text)
    assert "Tarea eliminada con ID" in delete_task_result.text

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

def results_template(name, status, test_start, details=None):
    results = {
            'name': name,
            'status': status,
            'duration': round(time.time() - test_start, 2),
        }
    results['details'] = details if details else results['details']
    return results

def main():
    results = []
    start_time = time.time()
    # Main test runner that initializes the browser and runs the full E2E flow
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    try:
        wait = WebDriverWait(driver, 10)
        #1 abrir el frontend
        test_start = time.time()
        abrir_frontend(driver)
        details = f"Frontend opened at {driver.current_url}"
        results.append(results_template("Open Frontend", "PASS", test_start, details))
        #2 crear un usuario
        test_start = time.time()
        user_id = crear_usuario(driver, wait)
        details = f"User created with ID: {user_id}"
        results.append(results_template("Create User (UI)", "PASS", test_start,details ))
        #3 crear tarea
        test_start = time.time()
        task_id = crear_tarea(driver, wait, user_id)
        details = f"Task created with ID: {task_id}"
        results.append(results_template("Create Task (UI)", "PASS", test_start, details))
        #4 Verificar tareas
        test_start = time.time()
        ver_tareas(driver)
        details = f"Task created with ID: {task_id}"
        results.append(results_template("Create Task (UI)", "PASS", test_start, details))
        time.sleep(2)  # Allow time to see the tasks before deletion
        #5 borrar tarea
        test_start = time.time()
        details = f"Task {task_id} deleted successfully"
        borrar_tarea(driver, wait, task_id)
        results.append(results_template("Delete Task (UI)", "PASS", test_start, details))
        #6 borrar usuario
        test_start = time.time()
        details = f"User {user_id} deleted successfully"
        borrar_usuario(driver, wait, user_id)
        results.append(results_template("Delete User (UI)", "PASS", test_start, details))
        time.sleep(3)  # Final delay to observe results if not running headless
        print("✅ Integration Test completed successfully.")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        results.append(results_template("Integration Test", "FAIL", time.time() - start_time, str(e)))
    finally:
        driver.quit()  # Always close the browser at the end
    
    generator = TestReportGenerator()
    generator.generate_report(results,"Frontend E2E Test Report")

if __name__ == "__main__":
    main()
