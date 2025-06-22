import time
import os
import requests
from reportlab.pdfgen import canvas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URLs de API para limpieza
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

# Reportes
REPORT_DIR = 'frontend_reports'
os.makedirs(REPORT_DIR, exist_ok=True)

def get_next_report_number():
    existing = [f for f in os.listdir(REPORT_DIR) if f.startswith('report_') and f.endswith('.pdf')]
    nums = [int(f.split('_')[1].split('.')[0]) for f in existing]
    return max(nums) + 1 if nums else 1

def generate_pdf_report(passed: bool, details: str):
    num = get_next_report_number()
    filepath = os.path.join(REPORT_DIR, f'report_{num}.pdf')
    c = canvas.Canvas(filepath)
    c.drawString(50, 800, f'FrontEnd Test Report #{num}')
    c.drawString(50, 780, f'Passed: {passed}')
    text = c.beginText(50, 750)
    for line in details.splitlines():
        text.textLine(line)
    c.drawText(text)
    c.save()
    print(f'✅ PDF report generated: {filepath}')

# Funciones auxiliares de limpieza

def delete_task(task_id): return requests.delete(f"{TASKS_URL}/{task_id}")
#def delete_user(user_id): return requests.delete(f"{USERS_URL}/{user_id}")

def main():
    options = Options()
    driver = webdriver.Chrome(options=options)
    details = []
    passed = False
    user_id = None
    task_id = None
    try:
        wait = WebDriverWait(driver, 10)
        # Flujo E2E
        driver.get("http://localhost:5000"); time.sleep(2)
        # Crear usuario
        driver.find_element(By.ID, "username").send_keys("Ana"); time.sleep(1)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click(); time.sleep(2)
        res_u = driver.find_element(By.ID, "user-result").text
        assert "Usuario creado con ID" in res_u
        user_id = ''.join(filter(str.isdigit, res_u))
        details.append(f"Created user {user_id}")

        # Crear tarea
        driver.find_element(By.ID, "task").send_keys("Terminar laboratorio"); time.sleep(1)
        driver.find_element(By.ID, "userid").send_keys(user_id + "\t"); time.sleep(1)
        driver.find_element(By.XPATH, "//button[text()='Crear Tarea']").click();
        wait.until(EC.text_to_be_present_in_element((By.ID, "task-result"), "Tarea creada con ID"))
        res_t = driver.find_element(By.ID, "task-result").text
        assert "Tarea creada con ID" in res_t
        task_id = ''.join(filter(str.isdigit, res_t))
        details.append(f"Created task {task_id}")

        # Ver lista de tareas
        driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click(); time.sleep(2)
        tasks_text = driver.find_element(By.ID, "tasks").text
        assert "Terminar laboratorio" in tasks_text
        details.append("Verified task appears in list")

        # Limpieza UI-backend
        r_tdel = delete_task(task_id)
        assert r_tdel.status_code == 200
        details.append(f"Deleted task {task_id}")
        #r_udel = delete_user(user_id)
        #assert r_udel.status_code == 200
        #details.append(f"Deleted user {user_id}")

        # Verificar que UI ya no muestra la tarea
        driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click(); time.sleep(2)
        tasks_text2 = driver.find_element(By.ID, "tasks").text
        assert "Terminar laboratorio" not in tasks_text2
        details.append("Verified cleanup on UI")

        passed = True
        print("✅ Frontend tests passed")
    except AssertionError as e:
        details.append(f"❌ AssertionError: {e}")
        raise
    finally:
        generate_pdf_report(passed, "\n".join(details))
        driver.quit()

if __name__ == '__main__':
    main()
