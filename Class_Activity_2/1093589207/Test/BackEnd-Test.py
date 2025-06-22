import requests
from report_generator import generate_pdf_report

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

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()
    print(f"✅ User {user_id} deleted.")

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()
    print(f"✅ Task {task_id} deleted.")

def verify_user_deleted(user_id):
    response = requests.get(f"{USERS_URL}/{user_id}")
    assert response.status_code == 404, "❌ User was not deleted."
    print("✅ User deletion verified.")

def verify_task_deleted(task_id):
    response = requests.get(f"{TASKS_URL}/{task_id}")
    assert response.status_code == 404, "❌ Task was not deleted."
    print("✅ Task deletion verified.")

def integration_test():
    user_id = None
    task_id = None
    results = []
    
    try:
        results.append("--- Starting Backend Integration Test ---")
        
        # Step 1: Create user
        user_id = create_user("Camilo")
        results.append(f"✅ User created with ID: {user_id}")

        # Step 2: Create task for that user
        task_id = create_task(user_id, "Prepare presentation")
        results.append(f"✅ Task created with ID: {task_id}")

        # Step 3: Verify that the task is registered
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
        results.append("✅ Verification complete: Task was successfully registered and linked to the user.")

    except Exception as e:
        results.append(f"❌ TEST FAILED: {e}")
    finally:
        # Cleanup
        results.append("\n--- Starting Cleanup ---")
        try:
            if task_id:
                delete_task(task_id)
                results.append(f"✅ Task {task_id} deleted.")
                verify_task_deleted(task_id)
                results.append("✅ Task deletion verified.")
            if user_id:
                delete_user(user_id)
                results.append(f"✅ User {user_id} deleted.")
                verify_user_deleted(user_id)
                results.append("✅ User deletion verified.")
            results.append("--- Cleanup Successful ---")
        except Exception as e:
            results.append(f"❌ CLEANUP FAILED: {e}")

        generate_pdf_report("Backend_Integration_Test", results)

if __name__ == "__main__":
    integration_test()