import requests
from reports.generate_report import generate_pdf_report

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    try:
        response = requests.post(USERS_URL, json={"name": name})
        if response.status_code == 201:
            user_data = response.json()
            print("[OK] User created:", user_data)
            return user_data["id"]
        else:
            print(f"[ERROR] Failed to create user: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERROR] Exception while creating user: {e}")
    return None

def create_task(user_id, description):
    try:
        response = requests.post(TASKS_URL, json={
            "title": description,
            "user_id": user_id
        })
        if response.status_code == 201:
            task_data = response.json()
            print("[OK] Task created:", task_data)
            return task_data["id"]
        else:
            print(f"[ERROR] Failed to create task: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERROR] Exception while creating task: {e}")
    return None

def get_tasks():
    try:
        response = requests.get(TASKS_URL)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[ERROR] Failed to fetch tasks: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Exception while fetching tasks: {e}")
    return []

def delete_user(user_id):
    try:
        response = requests.delete(f"{USERS_URL}/{user_id}")
        if response.status_code == 200:
            print(f"[OK] User with ID {user_id} deleted successfully.")
        else:
            print(f"[ERROR] Failed to delete user {user_id}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERROR] Exception while deleting user {user_id}: {e}")

def delete_task(task_id):
    try:
        response = requests.delete(f"{TASKS_URL}/{task_id}")
        if response.status_code == 200:
            print(f"[OK] Task with ID {task_id} deleted successfully.")
        else:
            print(f"[ERROR] Failed to delete task {task_id}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERROR] Exception while deleting task {task_id}: {e}")

def integration_test():
    test_log = ""
    user_id = None
    task_id = None

    try:
        test_log += "[INFO] Starting integration test...\n"
        user_id = create_user("Camilo")
        if user_id:
            test_log += f"[OK] User created: ID {user_id}\n"
            task_id = create_task(user_id, "Prepare presentation")
            if task_id:
                test_log += f"[OK] Task created: ID {task_id}\n"
                tasks = get_tasks()
                if any(t["id"] == task_id for t in tasks):
                    test_log += "[OK] Task successfully found in task list\n"
                else:
                    test_log += "[ERROR] Task not found in task list\n"
            else:
                test_log += "[ERROR] Task creation failed\n"
        else:
            test_log += "[ERROR] User creation failed\n"
    except Exception as e:
        test_log += f"[ERROR] Exception during test execution: {e}\n"
    finally:
        if task_id:
            delete_task(task_id)
            test_log += f"[CLEANUP] Task {task_id} deleted\n"
        if user_id:
            delete_user(user_id)
            test_log += f"[CLEANUP] User {user_id} deleted\n"

        generate_pdf_report(test_log)

if __name__ == "__main__":
    integration_test()
