import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PDF.creation_PDF import generar_pdf


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
    return user_id , ("(good) Resultado usuario:", user_result)  # Return user ID and result text for verification

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
    task_result = driver.find_element(By.ID, "task-result").text
    print("Texto en task_result:", task_result)
    assert "Tarea creada con ID" in task_result

    tarea_id = ''.join(filter(str.isdigit, task_result))  # Extract numeric ID from result
    return tarea_id, ("(good) Texto en task_result:", task_result)

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks
    return("Tareas:", tasks)


    
def borrar_tarea(driver, wait, task_id):
    # Fills out the task creation form with a task and user ID, then submits it
    # Waits until the confirmation text appears and asserts the result
    taskid_input = driver.find_element(By.ID, "taskid_delete")
    taskid_input.send_keys(task_id)
    taskid_input.send_keys('\t') # Force focus out of the input to trigger validation
    time.sleep(1)

    borrar_tarea_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Borrar Tarea']"))
    )
    borrar_tarea_btn.click()
    time.sleep(2)

    wait.until(
        EC.text_to_be_present_in_element((By.ID, "task-delete-result"), "Tarea Borrada con ID")
    )
    task_result = driver.find_element(By.ID, "task-delete-result")
    print("Texto en task_delete_result:", task_result.text)
    assert "Tarea Borrada con ID" in task_result.text
    return("(good) Texto en task_delete_result:", task_result.text)

def borrar_usuario(driver, wait, user_id):
    # Fills out the task creation form with a task and user ID, then submits it
    # Waits until the confirmation text appears and asserts the result
    taskid_input = driver.find_element(By.ID, "userid_delete")
    taskid_input.send_keys(user_id)
    taskid_input.send_keys('\t') # Force focus out of the input to trigger validation
    time.sleep(1)

    borrar_usuario_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Borrar Usuario']"))
    )
    borrar_usuario_btn.click()
    time.sleep(2)

    wait.until(
        EC.text_to_be_present_in_element((By.ID, "user-delete-result"), "Usuario Borrado con ID")
    )
    user_result = driver.find_element(By.ID, "user-delete-result")
    print("Texto en user_delete_result:", user_result.text)
    assert "Usuario Borrado con ID" in user_result.text
    return("(good) Texto en user_delete_result:", user_result.text)


def main():
    # Main test runner that initializes the browser and runs the full E2E flow
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    try:
        array = [] 
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        # Step 1: Create user
        user_id, text = crear_usuario(driver, wait)
        array.append(text)

        # Step 2: Create task
        tarea_id, text = crear_tarea(driver, wait, user_id)
        array.append(text)

        # Step 3: Verify task 
        text = ver_tareas(driver)
        array.append(text)

        # Step 4: Borar usuario y tarea 
        text = borrar_tarea(driver, wait, tarea_id)
        array.append(text)
        text = borrar_usuario(driver, wait, user_id)
        array.append(text)

        # Generar PDF con los resultados 
        generar_pdf("FrontEnd-Test", array)  # Generate PDF with results

        time.sleep(3)  # Final delay to observe results if not running headless

    finally:
        driver.quit()  # Always close the browser at the end


def integration_test_witherror():
    options = Options()
    driver = webdriver.Chrome(options=options)

    array = []
    wait = WebDriverWait(driver, 10)
    user_id = None
    tarea_id = None

    try:
        try:
            abrir_frontend(driver)
        except Exception as e:
            array.append(("(bad) Error al abrir el frontend:", str(e)))

        try:
            user_id, text = crear_usuario(driver, wait)
            array.append(text)
        except Exception as e:
            array.append(("(bad) Error al crear usuario:", str(e)))

        try:
            if user_id is not None:
                tarea_id, text = crear_tarea(driver, wait, user_id)
                array.append(text)
            else:
                array.append(("(bad) No se pudo crear la tarea porque no hay usuario.", ""))
        except Exception as e:
            array.append(("(bad) Error al crear tarea:", str(e)))

        try:
            text = ver_tareas(driver)
            array.append(text)
        except Exception as e:
            array.append(("(bad) Error al verificar tareas:", str(e)))

        try:
            if tarea_id is not None:
                text = borrar_tarea(driver, wait, tarea_id)
                array.append(text)
            else:
                array.append(("(bad) No se pudo borrar la tarea porque no existe.", ""))
        except Exception as e:
            array.append(("(bad) Error al borrar tarea:", str(e)))

        try:
            if user_id is not None:
                text = borrar_usuario(driver, wait, -1)
                array.append(text)
            else:
                array.append(("(bad) No se pudo borrar el usuario porque no existe.", ""))
        except Exception as e:
            array.append(("(bad) Error al borrar tarea:", str(e)))

    finally:
            generar_pdf("FrontEnd-Test", array)
            driver.quit()
            time.sleep(3)

if __name__ == "__main__":
    main()
    integration_test_witherror()
