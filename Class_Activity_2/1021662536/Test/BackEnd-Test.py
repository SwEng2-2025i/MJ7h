import requests
from report_generator import TestLogger, generate_report

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

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    if response.status_code == 200:
        print(f"✅ User {user_id} deleted successfully")
        return True
    else:
        print(f"❌ Failed to delete user {user_id}")
        return False

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    if response.status_code == 200:
        print(f"✅ Task {task_id} deleted successfully")
        return True
    else:
        print(f"❌ Failed to delete task {task_id}")
        return False

def verify_user_deleted(user_id):
    response = requests.get(f"{USERS_URL}/{user_id}")
    if response.status_code == 404:
        print(f"✅ Verified: User {user_id} no longer exists")
        return True
    else:
        print(f"❌ User {user_id} still exists")
        return False

def verify_task_deleted(task_id):
    response = requests.get(TASKS_URL)
    tasks = response.json()
    task_exists = any(t["id"] == task_id for t in tasks)
    if not task_exists:
        print(f"✅ Verified: Task {task_id} no longer exists")
        return True
    else:
        print(f"❌ Task {task_id} still exists")
        return False

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def integration_test():
    logger = TestLogger()
    user_id = None
    task_id = None
    test_status = "❌ FAILED"
    
    try:
        logger.start_capture()
        
        # Step 1: Create user
        user_id = create_user("Camilo")

        # Step 2: Create task for that user
        task_id = create_task(user_id, "Prepare presentation")

        # Step 3: Verify that the task is registered and associated with the user
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]

        assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
        print("✅ Test completed: task was successfully registered and linked to the user.")
        test_status = "✅ PASSED"
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        test_status = "❌ FAILED"
        
    finally:
        # Limpieza final

        if task_id:
            delete_task(task_id)
            verify_task_deleted(task_id)
            
        if user_id:
            delete_user(user_id)
            verify_user_deleted(user_id)
            
        print("Limpieza exitosa")
        logger.stop_capture()
        
        if __name__ == "__main__":
            generate_report(logger.logs, test_status, "Backend")


if __name__ == "__main__":
    integration_test()