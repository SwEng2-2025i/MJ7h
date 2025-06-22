import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from report_generator import generate_pdf_report

def abrir_frontend(driver):
    driver.get("http://localhost:5000")
    time.sleep(2)

def crear_usuario(driver, wait):
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    
    user_result_element = wait.until(
        EC.presence_of_element_located((By.ID, "user-result"))
    )
    user_result = user_result_element.text
    print("Resultado usuario:", user_result)
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))
    return user_id

def crear_tarea(driver, wait, user_id):
    task_input = driver.find_element(By.ID, "task")
    task_input.send_keys("Terminar laboratorio")
    time.sleep(1)

    userid_input = driver.find_element(By.ID, "userid")
    userid_input.send_keys(user_id)
    time.sleep(1)

    driver.find_element(By.XPATH, "//button[text()='Crear Tarea']").click()

    task_result_element = wait.until(
        EC.presence_of_element_located((By.ID, "task-result"))
    )
    task_result = task_result_element.text
    print("Resultado tarea:", task_result)
    assert "Tarea creada con ID" in task_result
    task_id = ''.join(filter(str.isdigit, task_result))
    return task_id

def ver_tareas(driver, wait):
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='tasks']/li")))
    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

def main():
    options = Options()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    
    user_id = None
    task_id = None
    results = []

    try:
        results.append("--- Starting Frontend E2E Test ---")
        wait = WebDriverWait(driver, 10)
        
        abrir_frontend(driver)
        results.append("✅ Opened frontend at http://localhost:5000.")

        user_id = crear_usuario(driver, wait)
        results.append(f"✅ UI: User created with ID {user_id}")

        task_id = crear_tarea(driver, wait, user_id)
        results.append(f"✅ UI: Task created with ID {task_id}")

        ver_tareas(driver, wait)
        results.append("✅ UI: Verified task appears in the list.")
        
        time.sleep(3)

    except Exception as e:
        results.append(f"❌ TEST FAILED: {e}")
    finally:
        if driver:
            driver.quit()
        
        results.append("\n--- Starting Cleanup ---")
        try:
            # Cleanup via API calls
            if task_id:
                requests.delete(f"http://localhost:5002/tasks/{task_id}")
                results.append(f"✅ API Cleanup: Deleted task {task_id}")
                verify_response = requests.get(f"http://localhost:5002/tasks/{task_id}")
                assert verify_response.status_code == 404
                results.append("✅ API Cleanup: Verified task deletion.")

            if user_id:
                requests.delete(f"http://localhost:5001/users/{user_id}")
                results.append(f"✅ API Cleanup: Deleted user {user_id}")
                verify_response = requests.get(f"http://localhost:5001/users/{user_id}")
                assert verify_response.status_code == 404
                results.append("✅ API Cleanup: Verified user deletion.")
            results.append("--- Cleanup Successful ---")
        except Exception as e:
            results.append(f"❌ CLEANUP FAILED: {e}")

        generate_pdf_report("Frontend_E2E_Test", results)

if __name__ == "__main__":
    main()