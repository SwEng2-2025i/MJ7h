import time
import requests
import os
from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def delete_task(task_id):
    requests.delete(f"{TASKS_URL}/{task_id}")

def delete_user(user_id):
    requests.delete(f"{USERS_URL}/{user_id}")

def get_tasks():
    return requests.get(TASKS_URL).json()

def generate_pdf_report(content):
    os.makedirs("reports", exist_ok=True)
    existing = [f for f in os.listdir("reports") if f.startswith("frontend_report_")]
    report_number = len(existing) + 1
    filename = f"reports/frontend_report_{report_number}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in content:
        pdf.cell(200, 10, txt=line, ln=True)
    pdf.output(filename)
    print(f"📄 Reporte guardado en {filename}")

def abrir_frontend(driver):
    driver.get("http://localhost:5000")
    time.sleep(2)

def crear_usuario(driver, wait, report_lines):
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)
    user_result = driver.find_element(By.ID, "user-result").text
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))
    report_lines.append(f" Usuario creado con ID {user_id}")
    return user_id

def crear_tarea(driver, wait, user_id, report_lines):
    task_input = driver.find_element(By.ID, "task")
    task_input.send_keys("Terminar laboratorio")
    time.sleep(1)
    userid_input = driver.find_element(By.ID, "userid")
    userid_input.send_keys(user_id)
    userid_input.send_keys('\t')
    time.sleep(1)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']"))).click()
    time.sleep(2)
    result = driver.find_element(By.ID, "task-result").text
    assert "Tarea creada con ID" in result
    task_id = ''.join(filter(str.isdigit, result))
    report_lines.append(f" Tarea creada con ID {task_id} para usuario {user_id}")
    return task_id

def ver_tareas(driver, report_lines):
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)
    tasks = driver.find_element(By.ID, "tasks").text
    assert "Terminar laboratorio" in tasks
    report_lines.append(" Tarea visible en el frontend")

def main():
    options = Options()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    report_lines = []

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait, report_lines)
        task_id = crear_tarea(driver, wait, user_id, report_lines)
        ver_tareas(driver, report_lines)

        # Limpieza
        delete_task(task_id)
        report_lines.append(f" Tarea {task_id} eliminada")

        delete_user(user_id)
        report_lines.append(f" Usuario {user_id} eliminado")

        # Verificación
        remaining = get_tasks()
        assert all(t["id"] != int(task_id) for t in remaining)
        report_lines.append(" Verificación: la tarea fue eliminada correctamente")
        report_lines.append(" Prueba de frontend completada exitosamente")

    except Exception as e:
        report_lines.append(f" Error en la prueba de frontend: {str(e)}")

    finally:
        driver.quit()
        generate_pdf_report(report_lines)

if __name__ == "__main__":
    main()
