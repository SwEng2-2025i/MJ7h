from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os
import requests

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(names):

    users_data = []

    for name in names:
        response = requests.post(USERS_URL, json={"name": name})
        response.raise_for_status()

        user_data = response.json()
        users_data.append(user_data["id"])
        
        print("✅ User created:", users_data[len(users_data)-1], user_data["name"])

    return users_data

def create_task(users_id, description):

    i = 1

    tasks_data = []

    for id in users_id:

        response = requests.post(TASKS_URL, json={
                "title": description + " " + str(i),
                "user_id": id
        })
        response.raise_for_status()
        task_data = response.json()
        tasks_data.append(task_data["id"])
        
        print("✅ Task created:", tasks_data[len(tasks_data)-1])
        i += 1

    return tasks_data

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def delete_users(user_ids):
    for id in user_ids:
        response = requests.delete(f"{USERS_URL}/{id}")
        if response.status_code == 200:
            print(f"🗑️ User {id} deleted")
        else:
            print(f"⚠️ Failed to delete user {id}: {response.status_code} - {response.text}")

def delete_tasks(task_ids):
    for id in task_ids:
        response = requests.delete(f"{TASKS_URL}/{id}")
        if response.status_code == 200:
            print(f"🗑️ Task {id} deleted")
        else:
            print(f"⚠️ Failed to delete task {id}: {response.status_code} - {response.text}")

def generate_pdf_report(user_ids, task_ids, test_result="Success", error_details=None, start_time=None, end_time=None):
    reports_dir = "test_reports"
    os.makedirs(reports_dir, exist_ok=True)

    # Secuencia de archivos
    existing_reports = [f for f in os.listdir(reports_dir) if f.startswith("test_report_") and f.endswith(".pdf")]
    next_number = 1
    if existing_reports:
        numbers = [int(f.split("_")[2].split(".")[0]) for f in existing_reports if f.split("_")[2].split(".")[0].isdigit()]
        next_number = max(numbers) + 1 if numbers else 1

    report_name = f"test_report_{next_number:03}.pdf"
    report_path = os.path.join(reports_dir, report_name)

    # Calcular duración
    duration = (end_time - start_time).total_seconds() if start_time and end_time else None
    formatted_start = start_time.strftime("%Y-%m-%d %H:%M:%S") if start_time else "N/A"
    formatted_end = end_time.strftime("%Y-%m-%d %H:%M:%S") if end_time else "N/A"

    # PDF
    c = canvas.Canvas(report_path, pagesize=letter)
    c.setFont("Helvetica", 12)

    c.drawString(50, 770, f"🧪 Test Report #{next_number}")
    c.drawString(50, 750, f"Date: {formatted_start}")
    c.drawString(50, 735, f"End: {formatted_end}")
    if duration:
        c.drawString(50, 720, f"Duration: {duration:.2f} seconds")
    c.drawString(50, 700, f"Result: {test_result}")

    y = 680
    c.drawString(50, y, f"Users created: {len(user_ids)}")
    for uid in user_ids:
        y -= 20
        c.drawString(70, y, f"- User ID: {uid}")

    y -= 30
    c.drawString(50, y, f"Tasks created: {len(task_ids)}")
    for tid in task_ids:
        y -= 20
        c.drawString(70, y, f"- Task ID: {tid}")

    y -= 30
    if test_result == "Failure" and error_details:
        c.drawString(50, y, "❌ Error details:")
        for line in error_details.splitlines():
            y -= 20
            c.drawString(70, y, f"{line}")

    y -= 40
    c.drawString(50, y, "✅ Cleanup: All users and tasks deleted after test.")
    c.save()

    print(f"📄 Report saved as {report_path}")



def integration_test():

    start_time = datetime.now()

    names = ["Ana", "Juan", "Camilo", " David", "Victoria", "Luz", "Miguel Alex "]

    # Step 1: Create user
    user_id = create_user(names)

    # Step 2: Create task for that user
    task_id = create_task(user_id, "Prepare presentation")

    result = "Success"
    error_details = None

    try:
        # Step 3: Verify that the task is registered and associated with the user
        tasks = get_tasks()
    
        user_tasks = [t for t in tasks if t["user_id"] in user_id]

        assert any(t["id"] in task_id and t["user_id"] in user_id for t in tasks), "❌ The task was not correctly registered"
        print("✅ Test completed: task was successfully registered and linked to the user.")
    except Exception as e:
        result = "Failure"
        error_details = str(e)
        print(error_details)

    delete_tasks(task_id)
    delete_users(user_id)

    end_time = datetime.now()

    generate_pdf_report(
        user_ids=user_id,
        task_ids=task_id,
        test_result=result,
        error_details=error_details,
        start_time=start_time,
        end_time=end_time
    )

if __name__ == "__main__":
    integration_test()