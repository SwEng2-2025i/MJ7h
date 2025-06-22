import time
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import requests

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
    # Extraer el ID de la tarea creada
    task_id = ''.join(filter(str.isdigit, task_result.text))
    return task_id

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

def eliminar_tarea_api(task_id):
    r = requests.delete(f"http://localhost:5002/tasks/{task_id}")
    print("Eliminando tarea:", r.json())
    return r.status_code == 200

def verificar_tarea_eliminada(task_id):
    r = requests.get("http://localhost:5002/tasks")
    if r.status_code == 200:
        tareas = r.json()
        return all(str(t["id"]) != str(task_id) for t in tareas)
    return False

def eliminar_usuario_api(user_id):
    r = requests.delete(f"http://localhost:5001/users/{user_id}")
    print("Eliminando usuario:", r.json())
    return r.status_code == 200

def verificar_usuario_eliminado(user_id):
    r = requests.get(f"http://localhost:5001/users/{user_id}")
    return r.status_code == 404

def generar_pdf_reporte(resultados):
    # Buscar el siguiente número de reporte disponible
    base = "test_report"
    n = 1
    while os.path.exists(f"{base}_{n}.pdf"):
        n += 1
    filename = f"{base}_{n}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Reporte de Pruebas E2E")
    c.setFont("Helvetica", 12)
    y = height - 90
    for linea in resultados:
        c.drawString(50, y, linea)
        y -= 20
    c.save()
    print(f"Reporte generado: {filename}")

def main():
    resultados = []
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait)
        resultados.append(f"Usuario creado con ID: {user_id}")
        task_id = crear_tarea(driver, wait, user_id)
        resultados.append(f"Tarea creada con ID: {task_id}")
        ver_tareas(driver)
        resultados.append("La tarea aparece en la lista correctamente.")

        # Limpieza de datos
        if eliminar_tarea_api(task_id):
            resultados.append(f"Tarea {task_id} eliminada correctamente.")
        else:
            resultados.append(f"Error al eliminar la tarea {task_id}.")

        if verificar_tarea_eliminada(task_id):
            resultados.append(f"Verificado: la tarea {task_id} ya no existe.")
        else:
            resultados.append(f"Error: la tarea {task_id} aún existe.")

        if eliminar_usuario_api(user_id):
            resultados.append(f"Usuario {user_id} eliminado correctamente.")
        else:
            resultados.append(f"Error al eliminar el usuario {user_id}.")

        if verificar_usuario_eliminado(user_id):
            resultados.append(f"Verificado: el usuario {user_id} ya no existe.")
        else:
            resultados.append(f"Error: el usuario {user_id} aún existe.")

        resultados.append("Prueba completada exitosamente.")
        time.sleep(2)  # Final delay to observe results if not running headless
    except Exception as e:
        resultados.append(f"Error durante la prueba: {str(e)}")
        raise
    finally:
        driver.quit()
        generar_pdf_reporte(resultados)

if __name__ == "__main__":
    main()
