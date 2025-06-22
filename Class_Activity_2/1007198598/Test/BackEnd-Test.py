import requests
import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

# Global variables to track created data for cleanup
created_users = []
created_tasks = []
test_results = []

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("✅ User created:", user_data)
    created_users.append(user_data["id"])  # Track for cleanup
    test_results.append(f"✅ User created: {user_data}")
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("✅ Task created:", task_data)
    created_tasks.append(task_data["id"])  # Track for cleanup
    test_results.append(f"✅ Task created: {task_data}")
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def get_users():
    response = requests.get(USERS_URL)
    response.raise_for_status()
    users = response.json()
    return users

def delete_user(user_id):
    """Delete a user by ID"""
    try:
        response = requests.delete(f"{USERS_URL}/{user_id}")
        if response.status_code == 200:
            print(f"✅ User {user_id} deleted successfully")
            test_results.append(f"✅ User {user_id} deleted successfully")
            return True
        else:
            print(f"❌ Failed to delete user {user_id}: {response.status_code}")
            test_results.append(f"❌ Failed to delete user {user_id}: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error deleting user {user_id}: {str(e)}")
        test_results.append(f"❌ Error deleting user {user_id}: {str(e)}")
        return False

def delete_task(task_id):
    """Delete a task by ID"""
    try:
        response = requests.delete(f"{TASKS_URL}/{task_id}")
        if response.status_code == 200:
            print(f"✅ Task {task_id} deleted successfully")
            test_results.append(f"✅ Task {task_id} deleted successfully")
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
    
    # Verify users are deleted
    users = get_users()
    remaining_users = [u for u in users if u["id"] in created_users]
    if remaining_users:
        print(f"❌ Some users were not deleted: {remaining_users}")
        test_results.append(f"❌ Some users were not deleted: {remaining_users}")
        return False
    else:
        print("✅ All test users successfully deleted")
        test_results.append("✅ All test users successfully deleted")
    
    # Verify tasks are deleted
    tasks = get_tasks()
    remaining_tasks = [t for t in tasks if t["id"] in created_tasks]
    if remaining_tasks:
        print(f"❌ Some tasks were not deleted: {remaining_tasks}")
        test_results.append(f"❌ Some tasks were not deleted: {remaining_tasks}")
        return False
    else:
        print("✅ All test tasks successfully deleted")
        test_results.append("✅ All test tasks successfully deleted")
    
    return True

def cleanup_test_data():
    """Clean up all data created during testing"""
    print("\n🧹 Starting data cleanup...")
    test_results.append("\n🧹 Starting data cleanup...")
    
    cleanup_success = True
    
    # Delete tasks first (due to foreign key constraints)
    for task_id in created_tasks:
        if not delete_task(task_id):
            cleanup_success = False
    
    # Then delete users
    for user_id in created_users:
        if not delete_user(user_id):
            cleanup_success = False
    
    # Verify deletion
    verification_success = verify_data_deletion()
    
    return cleanup_success and verification_success

def get_next_report_number():
    """Get the next sequential report number"""
    if not os.path.exists("test_reports"):
        os.makedirs("test_reports")
    
    existing_files = [f for f in os.listdir("test_reports") if f.startswith("backend_test_report_") and f.endswith(".pdf")]
    
    if not existing_files:
        return 1
    
    numbers = []
    for filename in existing_files:
        try:
            number = int(filename.replace("backend_test_report_", "").replace(".pdf", ""))
            numbers.append(number)
        except ValueError:
            continue
    
    return max(numbers) + 1 if numbers else 1

def generate_pdf_report(test_passed, cleanup_success):
    """Generate a PDF report with test results"""
    try:
        report_number = get_next_report_number()
        filename = f"test_reports/backend_test_report_{report_number:03d}.pdf"
        
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title = Paragraph(f"Backend Integration Test Report #{report_number}", styles['Title'])
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

def integration_test():
    test_passed = False
    cleanup_success = False
    
    try:
        print("🚀 Starting Backend Integration Test...")
        test_results.append("🚀 Starting Backend Integration Test...")
        
        # Step 1: Create user
        user_id = create_user("Camilo")

        # Step 2: Create task for that user
        task_id = create_task(user_id, "Prepare presentation")

        # Step 3: Verify that the task is registered and associated with the user
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]

        assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
        print("✅ Test completed: task was successfully registered and linked to the user.")
        test_results.append("✅ Test completed: task was successfully registered and linked to the user.")
        
        test_passed = True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        test_results.append(f"❌ Test failed: {str(e)}")
        test_passed = False
    
    finally:
        # Always attempt cleanup
        cleanup_success = cleanup_test_data()
        
        # Generate PDF report
        generate_pdf_report(test_passed, cleanup_success)
        
        # Final result
        if test_passed and cleanup_success:
            print("\n🎉 Integration test completed successfully with proper cleanup!")
        else:
            print("\n❌ Integration test failed or cleanup was unsuccessful!")
        
        return test_passed and cleanup_success

if __name__ == "__main__":
    integration_test()