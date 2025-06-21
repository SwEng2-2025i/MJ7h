import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


TASKS_URL = "http://localhost:5002/tasks"
USERS_URL = "http://localhost:5001/users"

def abrir_frontend(driver):
    driver.get("http://localhost:5000")
    time.sleep(2)

def crear_usuario(driver, wait):
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)
    user_result = driver.find_element(By.ID, "user-result").text
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
    print("Texto en task_result:", task_result.text)
    assert "Tarea creada con ID" in task_result.text
    task_id = ''.join(filter(str.isdigit, task_result.text))
    return task_id

def ver_tareas(driver):
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)
    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    assert response.status_code == 200, f"❌ Task {task_id} could not be deleted"

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    assert response.status_code == 200, f"❌ User {user_id} could not be deleted"

def verify_deletion(task_id, user_id):
    task_check = requests.get(f"{TASKS_URL}/{task_id}")
    assert task_check.status_code == 404, "❌ Task was not deleted properly"
    user_check = requests.get(f"{USERS_URL}/{user_id}")
    assert user_check.status_code == 404, "❌ User was not deleted properly"
    print("✅ Cleanup verified: user and task deleted.")

def generate_pdf_report(report_text, folder='reports'):
    os.makedirs(folder, exist_ok=True)
    existing = [f for f in os.listdir(folder) if f.startswith('report_') and f.endswith('.pdf')]
    next_num = 1 + max([int(f.split('_')[1].split('.')[0]) for f in existing] or [0])
    filename = os.path.join(folder, f'report_{next_num}.pdf')
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, f"Test Report #{next_num}")
    y = 730
    for line in report_text.split('\n'):
        c.drawString(100, y, line)
        y -= 15
    c.save()
    print(f"PDF report generated: {filename}")


def main():
    options = Options()
    driver = webdriver.Chrome(options=options)
    user_id = None
    task_id = None
    report_lines = []
    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        report_lines.append("Frontend opened.")
        user_id = crear_usuario(driver, wait)
        report_lines.append(f"User created: {user_id}")
        task_id = crear_tarea(driver, wait, user_id)
        report_lines.append(f"Task created: {task_id}")
        ver_tareas(driver)
        report_lines.append("Task verified in frontend.")
        time.sleep(3)
    except Exception as e:
        report_lines.append(f"❌ TEST FAILED: {str(e)}")
    finally:
        driver.quit()
        if task_id:
            try:
                delete_task(task_id)
                report_lines.append(f"Task {task_id} deleted")
            except Exception as e:
                report_lines.append(f"❌ Task {task_id} could not be deleted: {str(e)}")
        if user_id:
            try:
                delete_user(user_id)
                report_lines.append(f"User {user_id} deleted")
            except Exception as e:
                report_lines.append(f"❌ User {user_id} could not be deleted: {str(e)}")
        if task_id and user_id:
            try:
                verify_deletion(task_id, user_id)
                report_lines.append("Cleanup verified: user and task deleted.")
                report_lines.append("✅ TEST PASSED")
            except Exception as e:
                report_lines.append(f"❌ Cleanup verification failed: {str(e)}")
        generate_pdf_report('\n'.join(report_lines))


if __name__ == "__main__":
    main()