import time
import os
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from fpdf import FPDF, XPos, YPos

# Endpoints for cleanup
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def abrir_frontend(driver):
    # Opens the frontend application in the browser
    driver.get("http://localhost:5000")
    time.sleep(2)  # Give the page time to load

def crear_usuario(driver, wait):
    # Fills out the user creation form and submits it
    # Then retrieves and returns the newly created user ID
    username_input = driver.find_element(By.ID, "username")
    username_input.clear()  # Clear any existing text
    username_input.send_keys("Ana")
    time.sleep(1)
    
    # Clear any existing result text
    user_result_div = driver.find_element(By.ID, "user-result")
    driver.execute_script("arguments[0].textContent = '';", user_result_div)
    
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    
    # Wait for the async request to complete
    wait.until(
        lambda driver: driver.find_element(By.ID, "user-result").text.strip() != ""
    )

    user_result = driver.find_element(By.ID, "user-result").text
    print("Resultado usuario:", user_result)
    
    if "Usuario creado con ID" in user_result:
        user_id = ''.join(filter(str.isdigit, user_result))  # Extract numeric ID from result
        return user_id
    else:
        raise Exception(f"User creation failed: {user_result}")

def crear_tarea(driver, wait, user_id):
    # Fills out the task creation form with a task and user ID, then submits it
    # Waits until the confirmation text appears and asserts the result
    task_input = driver.find_element(By.ID, "task")
    task_input.clear()  # Clear any existing text
    task_input.send_keys("Terminar laboratorio")
    time.sleep(1)

    userid_input = driver.find_element(By.ID, "userid")
    userid_input.clear()  # Clear any existing text
    userid_input.send_keys(user_id)
    time.sleep(1)

    # Clear any existing result text
    task_result_div = driver.find_element(By.ID, "task-result")
    driver.execute_script("arguments[0].textContent = '';", task_result_div)
    
    crear_tarea_btn = driver.find_element(By.XPATH, "//button[text()='Crear Tarea']")
    crear_tarea_btn.click()
    
    # Wait longer for the async request to complete and check for either success or error
    try:
        # Wait for either success or error message to appear
        wait.until(
            lambda driver: driver.find_element(By.ID, "task-result").text.strip() != ""
        )
        
        task_result = driver.find_element(By.ID, "task-result")
        result_text = task_result.text
        print("Texto en task_result:", result_text)
        
        if "Tarea creada con ID" in result_text:
            # Extract task ID for cleanup
            task_id = ''.join(filter(str.isdigit, result_text))
            return task_id
        else:
            raise Exception(f"Task creation failed: {result_text}")
            
    except Exception as e:
        # Get current page source for debugging
        print("❌ Current task-result content:", driver.find_element(By.ID, "task-result").text)
        print("❌ Page title:", driver.title)
        raise e

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    tasks_ul = driver.find_element(By.ID, "tasks")
    
    # Clear existing tasks
    driver.execute_script("arguments[0].innerHTML = '';", tasks_ul)
    
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    
    # Wait for tasks to be loaded (wait for at least one task to appear)
    wait = WebDriverWait(driver, 10)
    wait.until(
        lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "#tasks li")) > 0
    )

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    
    if "Terminar laboratorio" not in tasks:
        raise Exception(f"Expected task not found in task list: {tasks}")

def cleanup_test_data(user_id, task_id):
    """Clean up test data created during testing"""
    print(f"🧹 Cleaning up test data: User {user_id}, Task {task_id}")
    
    # Delete task first (due to foreign key relationship)
    if task_id:
        try:
            response = requests.delete(f"{TASKS_URL}/{task_id}")
            if response.status_code == 200:
                print(f"✅ Task {task_id} deleted successfully")
            else:
                print(f"⚠️ Failed to delete task {task_id}: {response.status_code}")
        except Exception as e:
            print(f"❌ Error deleting task {task_id}: {e}")
    
    # Delete user
    if user_id:
        try:
            response = requests.delete(f"{USERS_URL}/{user_id}")
            if response.status_code == 200:
                print(f"✅ User {user_id} deleted successfully")
            else:
                print(f"⚠️ Failed to delete user {user_id}: {response.status_code}")
        except Exception as e:
            print(f"❌ Error deleting user {user_id}: {e}")

def verify_cleanup(user_id, task_id):
    """Verify that test data has been properly cleaned up"""
    print("🔍 Verifying data cleanup...")
    
    # Verify user is deleted
    try:
        response = requests.get(f"{USERS_URL}/{user_id}")
        if response.status_code == 404:
            print("✅ User cleanup verified")
        else:
            print("❌ User cleanup verification failed")
            return False
    except Exception as e:
        print(f"❌ Error verifying user cleanup: {e}")
        return False
    
    # Verify task is deleted
    try:
        response = requests.get(f"{TASKS_URL}")
        if response.status_code == 200:
            tasks = response.json()
            task_exists = any(t["id"] == int(task_id) for t in tasks)
            if not task_exists:
                print("✅ Task cleanup verified")
            else:
                print("❌ Task cleanup verification failed")
                return False
        else:
            print("❌ Error getting tasks for cleanup verification")
            return False
    except Exception as e:
        print(f"❌ Error verifying task cleanup: {e}")
        return False
    
    return True

def generate_pdf_report(test_results):
    """Generate PDF report with sequential numbering"""
    # Create reports directory if it doesn't exist
    if not os.path.exists("reports"):
        os.makedirs("reports")
    
    # Find next report number
    report_number = 1
    while os.path.exists(f"reports/frontend_test_report_{report_number:03d}.pdf"):
        report_number += 1
    
    filename = f"reports/frontend_test_report_{report_number:03d}.pdf"
    
    # Create PDF with proper Unicode support
    pdf = FPDF()
    pdf.add_page()
    
    # Use Helvetica (built-in font) and avoid Unicode characters
    pdf.set_font("Helvetica", size=16)
    
    # Title
    pdf.cell(200, 10, "Frontend Integration Test Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(10)
    
    # Report details
    pdf.set_font("Helvetica", size=12)
    pdf.cell(200, 10, f"Report Number: {report_number:03d}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(200, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)
    
    # Test results
    pdf.cell(200, 10, "Test Results:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", size=10)
    
    for result in test_results:
        # Replace Unicode bullet with simple dash
        clean_result = result.replace("✅", "-").replace("❌", "-")
        pdf.cell(200, 8, f"- {clean_result}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.output(filename)
    print(f"📄 PDF report generated: {filename}")
    return filename

def main():
    # Main test runner that initializes Firefox browser and runs the full E2E flow
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    
    # Use Firefox with automatic driver management
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    
    test_results = []
    user_id = None
    task_id = None

    try:
        wait = WebDriverWait(driver, 10)
        
        # Step 1: Open frontend
        abrir_frontend(driver)
        test_results.append("Frontend access: PASSED")
        
        # Step 2: Create user
        user_id = crear_usuario(driver, wait)
        test_results.append("User creation: PASSED")
        
        # Step 3: Create task
        task_id = crear_tarea(driver, wait, user_id)
        test_results.append("Task creation: PASSED")
        
        # Step 4: Verify tasks
        ver_tareas(driver)
        test_results.append("Task verification: PASSED")
        
        time.sleep(3)  # Final delay to observe results if not running headless
        
    except Exception as e:
        error_msg = f"Test failed: {str(e)}"
        test_results.append(error_msg)
        print(f"❌ {error_msg}")
        return False
    
    finally:
        driver.quit()  # Always close the browser at the end
        
        # Step 5: Clean up test data
        cleanup_test_data(user_id, task_id)
        
        # Step 6: Verify cleanup
        if verify_cleanup(user_id, task_id):
            test_results.append("Data cleanup: PASSED")
        else:
            test_results.append("Data cleanup: FAILED")
            return False
    
    # Generate PDF report
    generate_pdf_report(test_results)
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("🎉 All frontend tests passed successfully!")
    else:
        print("💥 Some frontend tests failed!")
        exit(1)
