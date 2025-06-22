import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fpdf import FPDF
import os

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

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

def delete_task_api(task_id):
    response = requests.delete(f"http://localhost:5002/tasks/{task_id}")
    if response.status_code == 404:
        print(f"Task {task_id} already deleted or not found.")
    else:
        response.raise_for_status()
        print(f"✅ Task {task_id} deleted (API).")

def delete_user_api(user_id):
    response = requests.delete(f"http://localhost:5001/users/{user_id}")
    if response.status_code == 404:
        print(f"User {user_id} already deleted or not found.")
    else:
        response.raise_for_status()
        print(f"✅ User {user_id} deleted (API).")

def save_pdf_report(test_results, report_dir="reports"):
    os.makedirs(report_dir, exist_ok=True)
    # Find next sequential number
    existing = [f for f in os.listdir(report_dir) if f.startswith("report_") and f.endswith(".pdf")]
    nums = [int(f.split("_")[1].split(".")[0]) for f in existing if f.split("_")[1].split(".")[0].isdigit()]
    next_num = max(nums) + 1 if nums else 1
    filename = os.path.join(report_dir, f"report_{next_num}.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "FrontEnd Test Report", ln=True, align="C")
    pdf.ln(10)
    for line in test_results:
        pdf.multi_cell(0, 10, clean_text(line))
    pdf.output(filename)
    print(f"PDF report saved as {filename}")

def clean_text(text):
    return text.replace("✅", "[OK]").replace("❌", "[FAIL]")

# Modify your main() to collect results and call save_pdf_report
def main():
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    user_id = None
    task_id = None
    test_results = []
    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait)
        test_results.append("[OK] User creation: OK")
        crear_tarea(driver, wait, user_id)
        test_results.append("✅ Task creation: OK")
        # Get task_id from the UI result
        task_result = driver.find_element(By.ID, "task-result").text
        task_id = ''.join(filter(str.isdigit, task_result))
        ver_tareas(driver)
        test_results.append("✅ Task listing: OK")
        time.sleep(3)  # Final delay to observe results if not running headless
    except Exception as e:
        test_results.append(f"❌ Test failed: {str(e)}")
        raise
    finally:
        driver.quit()  # Always close the browser at the end
        # Cleanup: delete created task and user
        if task_id:
            try:
                delete_task_api(task_id)
                test_results.append("✅ Task deletion: OK")
            except Exception as e:
                test_results.append(f"❌ Task deletion failed: {str(e)}")
        if user_id:
            try:
                delete_user_api(user_id)
                test_results.append("✅ User deletion: OK")
            except Exception as e:
                test_results.append(f"❌ User deletion failed: {str(e)}")
        # Optionally, verify deletion
        try:
            tasks = requests.get("http://localhost:5002/tasks").json()
            assert not any(t["id"] == int(task_id) for t in tasks), "❌ Task was not deleted!"
            test_results.append("✅ Task deletion verified (UI test).")
        except Exception as e:
            test_results.append(f"❌ Task deletion verification failed: {str(e)}")
        try:
            user_resp = requests.get(f"http://localhost:5001/users/{user_id}")
            assert user_resp.status_code == 404, "❌ User was not deleted!"
            test_results.append("✅ User deletion verified (UI test).")
        except Exception as e:
            test_results.append(f"❌ User deletion verification failed: {str(e)}")
        # Save PDF report
        save_pdf_report(test_results)

if __name__ == "__main__":
    main()
