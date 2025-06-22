import time
import os
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# Global variables to track created data for cleanup
created_users = []
created_tasks = []
test_results = []

def abrir_frontend(driver):
    # Opens the frontend application in the browser
    driver.get("http://localhost:5000")
    time.sleep(2)  # Give the page time to load
    test_results.append("✅ Frontend opened successfully")

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
    test_results.append(f"Usuario resultado: {user_result}")
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))  # Extract numeric ID from result
    created_users.append(int(user_id))  # Track for cleanup
    test_results.append(f"✅ User created with ID: {user_id}")
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
    test_results.append(f"Tarea resultado: {task_result.text}")
    assert "Tarea creada con ID" in task_result.text
    
    # Extract task ID for cleanup
    task_id = ''.join(filter(str.isdigit, task_result.text))
    created_tasks.append(int(task_id))
    test_results.append(f"✅ Task created with ID: {task_id}")

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    test_results.append(f"Tareas mostradas: {tasks}")
    assert "Terminar laboratorio" in tasks
    test_results.append("✅ Task verification completed - task appears in list")

def delete_user_via_api(user_id):
    """Delete a user via API call"""
    try:
        response = requests.delete(f"http://localhost:5001/users/{user_id}")
        if response.status_code == 200:
            print(f"✅ User {user_id} deleted successfully via API")
            test_results.append(f"✅ User {user_id} deleted successfully via API")
            return True
        else:
            print(f"❌ Failed to delete user {user_id}: {response.status_code}")
            test_results.append(f"❌ Failed to delete user {user_id}: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error deleting user {user_id}: {str(e)}")
        test_results.append(f"❌ Error deleting user {user_id}: {str(e)}")
        return False

def delete_task_via_api(task_id):
    """Delete a task via API call"""
    try:
        response = requests.delete(f"http://localhost:5002/tasks/{task_id}")
        if response.status_code == 200:
            print(f"✅ Task {task_id} deleted successfully via API")
            test_results.append(f"✅ Task {task_id} deleted successfully via API")
            return True
        else:
            print(f"❌ Failed to delete task {task_id}: {response.status_code}")
            test_results.append(f"❌ Failed to delete task {task_id}: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error deleting task {task_id}: {str(e)}")
        test_results.append(f"❌ Error deleting task {task_id}: {str(e)}")
        return False

def verify_data_deletion():
    """Verify that all test data has been properly deleted"""
    print("\n🔍 Verifying data deletion...")
    test_results.append("\n🔍 Verifying data deletion...")
    
    try:
        # Verify users are deleted
        users_response = requests.get("http://localhost:5001/users")
        if users_response.status_code == 200:
            users = users_response.json()
            remaining_users = [u for u in users if u["id"] in created_users]
            if remaining_users:
                print(f"❌ Some users were not deleted: {remaining_users}")
                test_results.append(f"❌ Some users were not deleted: {remaining_users}")
                return False
            else:
                print("✅ All test users successfully deleted")
                test_results.append("✅ All test users successfully deleted")
        
        # Verify tasks are deleted
        tasks_response = requests.get("http://localhost:5002/tasks")
        if tasks_response.status_code == 200:
            tasks = tasks_response.json()
            remaining_tasks = [t for t in tasks if t["id"] in created_tasks]
            if remaining_tasks:
                print(f"❌ Some tasks were not deleted: {remaining_tasks}")
                test_results.append(f"❌ Some tasks were not deleted: {remaining_tasks}")
                return False
            else:
                print("✅ All test tasks successfully deleted")
                test_results.append("✅ All test tasks successfully deleted")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying deletion: {str(e)}")
        test_results.append(f"❌ Error verifying deletion: {str(e)}")
        return False

def cleanup_test_data():
    """Clean up all data created during testing"""
    print("\n🧹 Starting data cleanup...")
    test_results.append("\n🧹 Starting data cleanup...")
    
    cleanup_success = True
    
    # Delete tasks first (due to foreign key constraints)
    for task_id in created_tasks:
        if not delete_task_via_api(task_id):
            cleanup_success = False
    
    # Then delete users
    for user_id in created_users:
        if not delete_user_via_api(user_id):
            cleanup_success = False
    
    # Verify deletion
    verification_success = verify_data_deletion()
    
    return cleanup_success and verification_success

def get_next_report_number():
    """Get the next sequential report number"""
    if not os.path.exists("test_reports"):
        os.makedirs("test_reports")
    
    existing_files = [f for f in os.listdir("test_reports") if f.startswith("frontend_test_report_") and f.endswith(".pdf")]
    
    if not existing_files:
        return 1
    
    numbers = []
    for filename in existing_files:
        try:
            number = int(filename.replace("frontend_test_report_", "").replace(".pdf", ""))
            numbers.append(number)
        except ValueError:
            continue
    
    return max(numbers) + 1 if numbers else 1

def generate_pdf_report(test_passed, cleanup_success):
    """Generate a PDF report with test results"""
    try:
        report_number = get_next_report_number()
        filename = f"test_reports/frontend_test_report_{report_number:03d}.pdf"
        
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title = Paragraph(f"Frontend Integration Test Report #{report_number}", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Test information
        test_info = Paragraph(f"<b>Test Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
        story.append(test_info)
        story.append(Spacer(1, 12))
        
        # Test summary
        status = "PASSED" if test_passed and cleanup_success else "FAILED"
        color = "green" if test_passed and cleanup_success else "red"
        summary = Paragraph(f"<b>Test Status:</b> <font color='{color}'>{status}</font>", styles['Normal'])
        story.append(summary)
        story.append(Spacer(1, 12))
        
        # Cleanup summary
        cleanup_status = "SUCCESS" if cleanup_success else "FAILED"
        cleanup_color = "green" if cleanup_success else "red"
        cleanup_summary = Paragraph(f"<b>Data Cleanup:</b> <font color='{cleanup_color}'>{cleanup_status}</font>", styles['Normal'])
        story.append(cleanup_summary)
        story.append(Spacer(1, 12))
        
        # Test details
        details_title = Paragraph("<b>Test Execution Details:</b>", styles['Heading2'])
        story.append(details_title)
        story.append(Spacer(1, 12))
        
        for result in test_results:
            detail = Paragraph(result, styles['Normal'])
            story.append(detail)
            story.append(Spacer(1, 6))
        
        # Created data summary
        summary_title = Paragraph("<b>Test Data Summary:</b>", styles['Heading2'])
        story.append(summary_title)
        story.append(Spacer(1, 12))
        
        users_summary = Paragraph(f"<b>Users Created:</b> {len(created_users)} (IDs: {created_users})", styles['Normal'])
        story.append(users_summary)
        
        tasks_summary = Paragraph(f"<b>Tasks Created:</b> {len(created_tasks)} (IDs: {created_tasks})", styles['Normal'])
        story.append(tasks_summary)
        
        doc.build(story)
        print(f"📄 PDF report generated: {filename}")
        test_results.append(f"📄 PDF report generated: {filename}")
        
        return True
    except Exception as e:
        print(f"❌ Error generating PDF report: {str(e)}")
        test_results.append(f"❌ Error generating PDF report: {str(e)}")
        return False

def main():
    # Main test runner that initializes the browser and runs the full E2E flow
    test_passed = False
    cleanup_success = False
    
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    try:
        print("🚀 Starting Frontend Integration Test...")
        test_results.append("🚀 Starting Frontend Integration Test...")
        
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait)
        crear_tarea(driver, wait, user_id)
        ver_tareas(driver)
        time.sleep(3)  # Final delay to observe results if not running headless
        
        print("✅ Frontend test completed successfully!")
        test_results.append("✅ Frontend test completed successfully!")
        test_passed = True
        
    except Exception as e:
        print(f"❌ Frontend test failed: {str(e)}")
        test_results.append(f"❌ Frontend test failed: {str(e)}")
        test_passed = False
        
    finally:
        driver.quit()  # Always close the browser at the end
        
        # Always attempt cleanup
        cleanup_success = cleanup_test_data()
        
        # Generate PDF report
        generate_pdf_report(test_passed, cleanup_success)
        
        # Final result
        if test_passed and cleanup_success:
            print("\n🎉 Frontend integration test completed successfully with proper cleanup!")
        else:
            print("\n❌ Frontend integration test failed or cleanup was unsuccessful!")
        
        return test_passed and cleanup_success

if __name__ == "__main__":
    main()
