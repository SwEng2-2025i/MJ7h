import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from report_generator import TestLogger, generate_report

# Endpoints para limpieza
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def delete_user_cleanup(user_id):
    try:
        response = requests.delete(f"{USERS_URL}/{user_id}")
        if response.status_code == 200:
            print(f"✅ Usuario {user_id} eliminado en limpieza")
        else:
            print(f"⚠️ No se pudo eliminar usuario {user_id}")
    except Exception as e:
        print(f"⚠️ Error al eliminar usuario: {e}")

def delete_task_cleanup(task_id):
    try:
        response = requests.delete(f"{TASKS_URL}/{task_id}")
        if response.status_code == 200:
            print(f"✅ Tarea {task_id} eliminada en limpieza")
        else:
            print(f"⚠️ No se pudo eliminar tarea {task_id}")
    except Exception as e:
        print(f"⚠️ Error al eliminar tarea: {e}")

def abrir_frontend(driver):
    print("🌐 Abriendo frontend...")
    driver.get("http://localhost:5000")
    time.sleep(2)

def crear_usuario(driver, wait):
    print("👤 Creando usuario...")
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    print("Resultado usuario:", user_result)
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))
    print(f"✅ Usuario creado con ID: {user_id}")
    return user_id

def crear_tarea(driver, wait, user_id):
    print("📝 Creando tarea...")
    task_input = driver.find_element(By.ID, "task")
    task_input.send_keys("Terminar laboratorio")
    time.sleep(1)

    userid_input = driver.find_element(By.ID, "userid")
    userid_input.send_keys(user_id)
    userid_input.send_keys('\t')
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
    print("Resultado tarea:", task_result.text)
    assert "Tarea creada con ID" in task_result.text
    
    # Extraer task_id del resultado
    task_id = ''.join(filter(str.isdigit, task_result.text))
    print(f"✅ Tarea creada con ID: {task_id}")
    return task_id

def ver_tareas(driver):
    print("📋 Verificando lista de tareas...")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas encontradas:", tasks)
    assert "Terminar laboratorio" in tasks
    print("✅ Tarea verificada en la lista")

def main():
    logger = TestLogger()
    user_id = None
    task_id = None
    test_status = "❌ FAILED"
    
    options = Options()
    driver = webdriver.Chrome(options=options)

    try:
        logger.start_capture()
        print("🚀 Iniciando pruebas E2E del frontend...")
        
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait)
        task_id = crear_tarea(driver, wait, user_id)
        ver_tareas(driver)
        
        print("✅ Todas las pruebas frontend completadas exitosamente")
        test_status = "✅ PASSED"
        time.sleep(3)
        
    except Exception as e:
        print(f"❌ Error en pruebas frontend: {str(e)}")
        test_status = "❌ FAILED"
        
    finally:
        driver.quit()
        
        print("\n Iniciando limpieza de recursos...")
        if task_id:
            delete_task_cleanup(task_id)
        if user_id:
            delete_user_cleanup(user_id)
        print("✅ Limpieza completada")
        
        logger.stop_capture()
        
        if __name__ == "__main__":
            generate_report(logger.logs, test_status, "Frontend")

if __name__ == "__main__":
    main()