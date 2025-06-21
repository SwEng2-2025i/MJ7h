import requests
import os
import io
import sys
from fpdf import FPDF

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("User created:", user_data)
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("Task created:", task_data)
    return task_data["id"]

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()
    print(f"User with id {user_id} deleted.")

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()
    print(f"Task with id {task_id} deleted.")

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def generate_pdf_report(log_output):
    report_num = 1
    # The reports will be prefixed with Backend
    while os.path.exists(f"Reporte_Pruebas_Backend_{report_num}.pdf"):
        report_num += 1
    
    pdf = FPDF()
    pdf.add_page()
    
    try:
        pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
        pdf.set_font('DejaVu', '', 12)
    except FileNotFoundError:
        print("Warning: DejaVu font not found. Using Arial.")
        pdf.set_font("Arial", size=12)
    
    pdf.multi_cell(0, 10, log_output)

    report_name = f"Reporte_Pruebas_Backend_{report_num}.pdf"
    pdf.output(report_name)
    print(f"\nReport generated: {report_name}")

def integration_test():
    user_id = None
    task_id = None

    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    try:
        # Step 1: Create user
        user_id = create_user("Camilo")

        # Step 2: Create task for that user
        task_id = create_task(user_id, "Prepare presentation")

        # Step 3: Verify that the task is registered and associated with the user
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]

        assert any(t["id"] == task_id for t in user_tasks), "The task was not correctly registered"
        print("Test completed: task was successfully registered and linked to the user.")

    finally:
        sys.stdout = old_stdout
        log_output = captured_output.getvalue()
        print(log_output)
        if task_id:
            delete_task(task_id)
            # Verify that the task was deleted
            tasks = get_tasks()
            assert not any(t["id"] == task_id for t in tasks), "The task was not correctly deleted"
            print("Test completed: task was successfully deleted.")

        if user_id:
            delete_user(user_id)
            # Verify that the user was deleted
            response = requests.get(f"{USERS_URL}/{user_id}")
            assert response.status_code == 404, "The user was not correctly deleted"
            print("Test completed: user was successfully deleted.")
        
        generate_pdf_report(log_output)


if __name__ == "__main__":
    integration_test()