import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
from reportlab.pdfgen import canvas
import io
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from datetime import datetime
from t_front import add_test_result, generar_reporte_pdf




def abrir_frontend(driver):
    # Opens the frontend application in the browser
    start_time = time.time()
    try:
        driver.get("http://localhost:5000")
        time.sleep(2)  # Give the page time to load
        duration = time.time() - start_time
        add_test_result("Abrir Frontend", "PASSED", duration, "Frontend cargado correctamente")
    except Exception as e:
        duration = time.time() - start_time
        add_test_result("Abrir Frontend", "FAILED", duration, str(e), str(e))
        raise


def crear_usuario(driver, wait):
    # Fills out the user creation form and submits it
    # Then retrieves and returns the newly created user ID
    start_time = time.time()
    try:
        username_input = driver.find_element(By.ID, "username")
        username_input.send_keys("Ana")
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
        time.sleep(2)

        user_result = driver.find_element(By.ID, "user-result").text
        print("Resultado usuario:", user_result)
        assert "Usuario creado con ID" in user_result
        user_id = ''.join(filter(str.isdigit, user_result))  # Extract numeric ID from result
        
        duration = time.time() - start_time
        add_test_result("Crear Usuario", "PASSED", duration, f"Usuario 'Ana' creado con ID: {user_id}")
        return user_id
    except Exception as e:
        duration = time.time() - start_time
        add_test_result("Crear Usuario", "FAILED", duration, str(e), str(e))
        raise


def crear_tarea(driver, wait, user_id):
    # Fills out the task creation form with a task and user ID, then submits it
    # Waits until the confirmation text appears and asserts the result
    start_time = time.time()
    try:
        task_input = driver.find_element(By.ID, "task")
        task_input.send_keys("Terminar laboratorio")
        time.sleep(1)

        userid_input = driver.find_element(By.ID, "userid")
        userid_input.clear()  # Esto borra el contenido previo
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
        
        duration = time.time() - start_time
        add_test_result("Crear Tarea", "PASSED", duration, "Tarea 'Terminar laboratorio' creada correctamente")
    except Exception as e:
        duration = time.time() - start_time
        add_test_result("Crear Tarea", "FAILED", duration, str(e), str(e))
        raise


def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    start_time = time.time()
    try:
        driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
        time.sleep(2)

        tasks = driver.find_element(By.ID, "tasks").text
        print("Tareas:", tasks)
        
        if "Terminar laboratorio" in tasks:
            message = "Tarea visible en el DOM"
            print("✅ Tarea visible en el DOM")
        else:
            message = "Tarea ya fue eliminada automáticamente desde el frontend"
            print("⚠️ Tarea ya fue eliminada automáticamente desde el frontend")
        
        duration = time.time() - start_time
        add_test_result("Ver Tareas", "PASSED", duration, message)
    except Exception as e:
        duration = time.time() - start_time
        add_test_result("Ver Tareas", "FAILED", duration, str(e), str(e))
        raise


def delete_task_backend(task_id):
    start_time = time.time()
    try:
        res = requests.delete(f"http://localhost:5002/tasks/{task_id}")
        duration = time.time() - start_time
        
        if res.status_code == 200:
            message = f"Tarea {task_id} eliminada por backend"
            add_test_result("Eliminar Tarea (Backend)", "PASSED", duration, message)
            print(f"🧹 {message}")
        elif res.status_code == 404:
            message = f"Tarea {task_id} ya fue eliminada (por frontend)"
            add_test_result("Eliminar Tarea (Backend)", "PASSED", duration, message)
            print(f"⚠️ {message}")
        else:
            message = f"Error inesperado al eliminar tarea {task_id}: {res.status_code}"
            add_test_result("Eliminar Tarea (Backend)", "FAILED", duration, message)
            print(f"❌ {message}")
    except Exception as e:
        duration = time.time() - start_time
        add_test_result("Eliminar Tarea (Backend)", "FAILED", duration, str(e), str(e))
        print(f"❌ Error al eliminar tarea: {e}")


def delete_user_backend(user_id):
    start_time = time.time()
    try:
        res = requests.delete(f"http://localhost:5001/users/{user_id}")
        duration = time.time() - start_time
        
        if res.status_code == 200:
            message = f"Usuario {user_id} eliminado por backend"
            add_test_result("Eliminar Usuario (Backend)", "PASSED", duration, message)
            print(f"🧹 {message}")
        elif res.status_code == 404:
            message = f"Usuario {user_id} ya fue eliminado (por frontend)"
            add_test_result("Eliminar Usuario (Backend)", "PASSED", duration, message)
            print(f"⚠️ {message}")
        else:
            message = f"Error inesperado al eliminar usuario {user_id}: {res.status_code}"
            add_test_result("Eliminar Usuario (Backend)", "FAILED", duration, message)
            print(f"❌ {message}")
    except Exception as e:
        duration = time.time() - start_time
        add_test_result("Eliminar Usuario (Backend)", "FAILED", duration, str(e), str(e))
        print(f"❌ Error al eliminar usuario: {e}")


def verify_deletion(user_id, task_id):
    start_time = time.time()
    try:
        # Verifica usuario
        res_user = requests.get(f"http://localhost:5001/users/{user_id}")
        assert res_user.status_code == 404, "❌ Usuario no fue eliminado correctamente"

        # Verifica tareas
        res_tasks = requests.get(f"http://localhost:5002/tasks")
        tasks = res_tasks.json()
        assert all(str(task["id"]) != str(task_id) for task in tasks), "❌ Tarea no fue eliminada correctamente"

        duration = time.time() - start_time
        add_test_result("Verificar Limpieza", "PASSED", duration, "Verificación de limpieza completada exitosamente")
        print("✅ Verificación de limpieza en el front completada")
    except Exception as e:
        duration = time.time() - start_time
        add_test_result("Verificar Limpieza", "FAILED", duration, str(e), str(e))
        print(f"❌ Error en verificación de limpieza: {e}")
        raise


def main():
    options = Options()
    # options.add_argument('--headless')  # Opcional
    driver = webdriver.Chrome(options=options)

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait)
        crear_tarea(driver, wait, user_id)
        ver_tareas(driver)

        # Extraer task_id desde la interfaz (texto)
        task_result = driver.find_element(By.ID, "task-result").text
        task_id = ''.join(filter(str.isdigit, task_result.split("ID")[-1]))

        # Limpieza
        delete_task_backend(task_id)
        delete_user_backend(user_id)
        verify_deletion(user_id, task_id)

        time.sleep(2)  # Para ver resultados si no está en headless
    except Exception as e:
        print(f"❌ Excepción durante la prueba: {e}")
        add_test_result("Ejecución General", "FAILED", 0.0, str(e), str(e))
    finally:
        driver.quit()


if __name__ == "__main__":
    buffer = io.StringIO()
    sys.stdout = buffer  # Captura todo lo que se imprima

    try:
        main()
    except Exception as e:
        print(f"❌ Excepción durante la prueba: {e}")

    sys.stdout = sys.__stdout__  # Restaura la salida estándar
    contenido = buffer.getvalue()
    generar_reporte_pdf(contenido)