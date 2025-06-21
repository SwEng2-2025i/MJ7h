
import requests
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    if response.status_code == 200:
        print(f"✅ Task {task_id} deleted")
    else:
        print(f"❌ Task {task_id} could not be deleted")

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    if response.status_code == 200:
        print(f"✅ User {user_id} deleted")
    else:
        print(f"❌ User {user_id} could not be deleted")

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

def integration_test():
    report_lines = []
    try:
        user_id = create_user("Camilo")
        report_lines.append(f"User created: {user_id}")
        task_id = create_task(user_id, "Prepare presentation")
        report_lines.append(f"Task created: {task_id}")
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
        report_lines.append("Task correctly registered and linked to user.")
        delete_task(task_id)
        report_lines.append(f"Task {task_id} deleted")
        delete_user(user_id)
        report_lines.append(f"User {user_id} deleted")
        task_check = requests.get(f"{TASKS_URL}/{task_id}")
        assert task_check.status_code == 404, "❌ Task was not deleted properly"
        user_check = requests.get(f"{USERS_URL}/{user_id}")
        assert user_check.status_code == 404, "❌ User was not deleted properly"
        report_lines.append("Cleanup verified: user and task deleted.")
        report_lines.append("✅ TEST PASSED")
    except Exception as e:
        report_lines.append(f"❌ TEST FAILED: {str(e)}")
    finally:
        generate_pdf_report('\n'.join(report_lines))

if __name__ == "__main__":
    integration_test()