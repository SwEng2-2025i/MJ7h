import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from selenium.webdriver.common.keys import Keys

def abrir_frontend(driver):
    # Opens the frontend application in the browser
    driver.get("http://localhost:5000")
    time.sleep(2)  # Give the page time to load

def crear_usuario(driver, wait):
    # Fills out the user creation form and submits it
    # Then retrieves and returns         the newly created user ID
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys(Keys.CONTROL + "a")
    username_input.send_keys(Keys.DELETE)
    username_input.send_keys("Ana")

    # username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    print("Resultado usuario:", user_result)
    assert "Usuario creado con ID" in user_result, '❌ El usuario no fue creado correctamente'
    user_id = ''.join(filter(str.isdigit, user_result))   # Extract numeric ID from result
    return user_id

def crear_tarea(driver, wait, user_id):
    # Fills out the task creation form with a task and user ID, then submits it
    # Waits until the confirmation text appears and asserts the result
    task_input = driver.find_element(By.ID, "task")
    task_input.send_keys(Keys.CONTROL + "a")
    task_input.send_keys(Keys.DELETE)
    task_input.send_keys("Terminar laboratorio")
    time.sleep(1)

    userid_input = driver.find_element(By.ID, "userid")
    userid_input.send_keys(Keys.CONTROL + "a")
    userid_input.send_keys(Keys.DELETE)
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
    assert "Tarea creada con ID" in task_result.text, '❌ La tarea no fue creada correctamente'
    # Extraer el ID de la tarea del mensaje
    task_id = ''.join(filter(str.isdigit, task_result.text))
    return task_id

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    # assert "Terminar laboratorio" in tasks
    return tasks  # Return the tasks text for further verification if needed

def ver_usuarios(driver):
    # Hace clic en el botón para actualizar la lista de usuarios y devuelve el texto
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de usuarios')]").click()
    time.sleep(2)
    users = driver.find_element(By.ID, "users").text
    print("Usuarios:", users)
    return users

def eliminar_usuario(driver, wait, user_id):
    # Elimina un usuario por ID usando el frontend
    delete_user_input = driver.find_element(By.ID, "delete-userid")
    delete_user_input.send_keys(Keys.CONTROL + "a")
    delete_user_input.send_keys(Keys.DELETE)
    delete_user_input.send_keys(user_id)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Eliminar Usuario')]").click()
    time.sleep(2)
    result = driver.find_element(By.ID, "delete-user-result").text
    print("Resultado eliminar usuario:", result)
    assert "Usuario eliminado correctamente" in result, '❌ El usuario no fue eliminado correctamente'

def eliminar_tarea(driver, wait, task_id):
    # Elimina una tarea por ID usando el frontend
    delete_task_input = driver.find_element(By.ID, "delete-taskid")
    delete_task_input.send_keys(Keys.CONTROL + "a")
    delete_task_input.send_keys(Keys.DELETE)
    delete_task_input.send_keys(task_id)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Eliminar Tarea')]").click()
    time.sleep(2)
    result = driver.find_element(By.ID, "delete-task-result").text
    print("Resultado eliminar tarea:", result)
    assert "✅ Tarea eliminada correctamente" in result, '❌ La tarea no fue eliminada correctamente'

def generar_reporte_pdf(resultados):
    report_dir = os.path.dirname(os.path.abspath(__file__))
    existing = [f for f in os.listdir(report_dir) if f.startswith('frontend_report_') and f.endswith('.pdf')]
    nums = [int(f.split('_')[-1].split('.')[0]) for f in existing if f.split('_')[-1].split('.')[0].isdigit()]
    next_num = max(nums) + 1 if nums else 1
    filename = os.path.join(report_dir, f"frontend_report_{next_num}.pdf")
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, f"Frontend Test Report #{next_num}")
    c.drawString(50, 735, f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y = 710
    for line in resultados:
        c.drawString(50, y, line)
        y -= 20
    c.save()
    print(f"PDF report generated: {filename}")

def main():
    # Main test runner that initializes the browser and runs the full E2E flow
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    resultados = []
    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        intial_task = ver_tareas(driver)
        intial_users = ver_usuarios(driver)
        resultados.append(f"Tareas iniciales: {intial_task}")
        resultados.append(f"Usuarios iniciales: {intial_users}")
        user_id = crear_usuario(driver, wait)
        resultados.append(f"Usuario creado con ID: {user_id}")
        task_id = crear_tarea(driver, wait, user_id)
        resultados.append(f"Tarea creada con ID: {task_id} para usuario {user_id}")
        eliminar_tarea(driver, wait, task_id)
        resultados.append(f"Tarea eliminada con ID: {task_id}")
        eliminar_usuario(driver, wait, user_id)
        resultados.append(f"Usuario eliminado con ID: {user_id}")
        final_taks = ver_tareas(driver)
        final_users = ver_usuarios(driver)
        resultados.append(f"Tareas finales: {final_taks}")
        resultados.append(f"Usuarios finales: {final_users}")
        assert intial_task == final_taks, "❌ Las tareas no coinciden después de eliminar la tarea"
        assert user_id not in final_users, "❌ El usuario no fue eliminado correctamente"
        
        
        resultados.append("TEST PASSED")
        
      
      
        # TEST 2 - FALLE EN ELIMAR USUARIO  CON ID 0
        time.sleep(3)  # Final delay to observe results if not running headless
        intial_task = ver_tareas(driver)
        intial_users = ver_usuarios(driver)
        resultados.append(f"Tareas iniciales: {intial_task}")
        resultados.append(f"Usuarios iniciales: {intial_users}")
        user_id = crear_usuario(driver, wait)
        resultados.append(f"Usuario creado con ID: {user_id}")
        task_id = crear_tarea(driver, wait, user_id)
        resultados.append(f"Tarea creada con ID: {task_id} para usuario {user_id}")
        eliminar_tarea(driver, wait, task_id) # Eliminar tarea con ID 0 para probar la eliminación de una tarea inexistente
        resultados.append(f"Tarea eliminada con ID: {task_id}")
        eliminar_usuario(driver, wait, 0)# Eliminar usuario con ID 0 para probar la eliminación de un usuario inexistente
        resultados.append(f"Usuario eliminado con ID: {user_id}")
        final_taks = ver_tareas(driver)
        final_users = ver_usuarios(driver)
        resultados.append(f"Tareas finales: {final_taks}")
        resultados.append(f"Usuarios finales: {final_users}")
        assert intial_task == final_taks, "❌ Las tareas no coinciden después de eliminar la tarea"
        assert user_id not in final_users, "❌ El usuario no fue eliminado correctamente"
        
        
        resultados.append("TEST PASSED")
        
        
        
        
        
        
        
        
    except AssertionError as e:
        resultados.append(str(e))
        resultados.append("TEST FAILED")
    except Exception as e:
        resultados.append(f"Error inesperado: {e}")
        resultados.append("TEST FAILED")
    finally:
        generar_reporte_pdf(resultados)
        driver.quit()  # Always close the browser at the end

if __name__ == "__main__":
    main()
