import requests
import os
from datetime import datetime
from fpdf import FPDF, XPos, YPos

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("✅ User created:", user_data)
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("✅ Task created:", task_data)
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

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
            task_exists = any(t["id"] == task_id for t in tasks)
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
    while os.path.exists(f"reports/test_report_{report_number:03d}.pdf"):
        report_number += 1
    
    filename = f"reports/test_report_{report_number:03d}.pdf"
    
    # Create PDF with proper Unicode support
    pdf = FPDF()
    pdf.add_page()
    
    # Use Helvetica (built-in font) and avoid Unicode characters
    pdf.set_font("Helvetica", size=16)
    
    # Title
    pdf.cell(200, 10, "Integration Test Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
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

def integration_test():
    test_results = []
    user_id = None
    task_id = None
    
    try:
        # Step 1: Create user
        user_id = create_user("Camilo")
        test_results.append("User creation: PASSED")

        # Step 2: Create task for that user
        task_id = create_task(user_id, "Prepare presentation")
        test_results.append("Task creation: PASSED")

        # Step 3: Verify that the task is registered and associated with the user
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]

        assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
        test_results.append("Task verification: PASSED")
        print("✅ Test completed: task was successfully registered and linked to the user.")
        
    except Exception as e:
        error_msg = f"Test failed: {str(e)}"
        test_results.append(error_msg)
        print(f"❌ {error_msg}")
        return False
    
    finally:
        # Step 4: Clean up test data
        cleanup_test_data(user_id, task_id)
        
        # Step 5: Verify cleanup
        if verify_cleanup(user_id, task_id):
            test_results.append("Data cleanup: PASSED")
        else:
            test_results.append("Data cleanup: FAILED")
            return False
    
    # Generate PDF report
    generate_pdf_report(test_results)
    return True

if __name__ == "__main__":
    success = integration_test()
    if success:
        print("🎉 All tests passed successfully!")
    else:
        print("💥 Some tests failed!")
        exit(1)