import requests
import io
import sys
from pdf_report import generar_reporte_pdf

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

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()
    print(f"Task {task_id} deleted.")

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()
    print(f"User {user_id} deleted.")

def create_task_invalid_user(user_id):
    try:
        create_task(user_id, description="Task invalid")
    except requests.exceptions.HTTPError as e:
        print("Test failed as expected.", e)

def integration_test():
    log = io.StringIO()
    original_stdout = sys.stdout
    sys.stdout = log
    # Step 1: Create user
    user_id = create_user("Camilo")

    # Step 2: Create task for that user
    task_id = create_task(user_id, "Prepare presentation")

    # Step 3: Verify that the task is registered and associated with the user
    tasks = get_tasks()
    user_tasks = [t for t in tasks if t["user_id"] == user_id]

    assert any(t["id"] == task_id for t in user_tasks), "The task was not correctly registered"
    print("Test passed: task was successfully registered and linked to the user")

    delete_task(task_id)
    delete_user(user_id)
    # Step 4: Verify that the task and user were deleted
    tasks = get_tasks()
    assert not any(t["id"] == task_id for t in tasks), "The task was not deleted"
    assert not any(t["user_id"] == user_id for t in tasks), "The user was not deleted"
    print("Test passed: task and its user were successfully deleted.")

    # Step 5: Verify that the API correctly rejects the creation of a task with a non-existent user ID
    try:
        create_task_invalid_user(user_id) 
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 404, "The API did not return a 404 error for a non-existent user ID"

    print("Test passed: the API correctly rejected the creation of a task with a non-existent user ID.")
    print("Integration test completed successfully.")

    sys.stdout = original_stdout  # Restaurar salida
    generar_reporte_pdf(log.getvalue())
    log.close()



if __name__ == "__main__":
    integration_test()