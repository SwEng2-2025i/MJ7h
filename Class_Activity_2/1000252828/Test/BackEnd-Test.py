import requests
import sys
import os

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reporting.pdf_generator import generate_pdf_report

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name, logs):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    logs.append(f"✅ User created: {user_data}")
    return user_data["id"]

def create_task(user_id, description, logs):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    logs.append(f"✅ Task created: {task_data}")
    return task_data["id"]

def get_tasks(logs):
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def delete_user(user_id, logs):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()
    logs.append(f"✅ User {user_id} deleted.")

def delete_task(task_id, logs):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()
    logs.append(f"✅ Task {task_id} deleted.")

def verify_user_deleted(user_id, logs):
    response = requests.get(f"{USERS_URL}/{user_id}")
    assert response.status_code == 404, f"❌ User {user_id} was not deleted."
    logs.append(f"✅ User {user_id} verified as deleted.")

def verify_task_deleted(task_id, logs):
    response = requests.get(f"{TASKS_URL}/{task_id}")
    assert response.status_code == 404, f"❌ Task {task_id} was not deleted."
    logs.append(f"✅ Task {task_id} verified as deleted.")


def integration_test(logs):
    # Step 1: Create user
    user_id = create_user("Camilo", logs)

    # Step 2: Create task for that user
    task_id = create_task(user_id, "Prepare presentation", logs)

    # Step 3: Verify that the task is registered and associated with the user
    tasks = get_tasks(logs)
    user_tasks = [t for t in tasks if t["user_id"] == user_id]

    assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
    logs.append("✅ Test completed: task was successfully registered and linked to the user.")

    # Step 4: Cleanup data
    logs.append("\n🧹 Starting data cleanup...")
    delete_task(task_id, logs)
    delete_user(user_id, logs)

    # Step 5: Verify cleanup
    logs.append("\n🔬 Verifying data cleanup...")
    verify_task_deleted(task_id, logs)
    verify_user_deleted(user_id, logs)
    logs.append("\n✅ Cleanup verified. Test finished.")


if __name__ == "__main__":
    logs = []
    try:
        integration_test(logs)
    finally:
        for line in logs:
            print(line)
        generate_pdf_report("BackEnd_Test", logs)