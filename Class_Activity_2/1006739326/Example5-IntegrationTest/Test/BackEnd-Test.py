import sys, os
# Añadimos la carpeta raíz (Example5-IntegrationTest) al path para poder importar report.py
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

import requests
from report import generate_report

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


# --- Data cleanup helpers ---
def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()
    print(f"🗑️  Task {task_id} deleted")

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()
    print(f"🗑️  User {user_id} deleted")



def integration_test():
    # Step 1: Create user
    user_id = create_user("Camilo")

    # Step 2: Create task for that user
    task_id = create_task(user_id, "Prepare presentation")

    # Step 3: Verify that the task is registered and associated with the user
    tasks = get_tasks()
    user_tasks = [t for t in tasks if t["user_id"] == user_id]

    assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
    print("✅ Test completed: task was successfully registered and linked to the user.")


    # Step 4: Cleanup created data
    delete_task(task_id)
    delete_user(user_id)

    # Step 5: Verify data has been deleted
    tasks_after = get_tasks()
    assert not any(t["id"] == task_id for t in tasks_after), \
        "❌ Task was not deleted"
    resp = requests.get(f"{USERS_URL}/{user_id}")
    assert resp.status_code == 404, "❌ User was not deleted"
    print("✅ Cleanup verified: task and user removed")
    # Step 6: Generate PDF report
    summary = (
        f"User ID: {user_id}\n"
        f"Task ID: {task_id}\n"
        "All integration steps passed and cleanup verified."
    )
    pdf_path = generate_report("BackEnd Integration", summary)
    print(f"📄 Report generated at {pdf_path}")

if __name__ == "__main__":
    integration_test()