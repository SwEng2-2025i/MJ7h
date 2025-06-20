import requests

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    try:
        response = requests.post(USERS_URL, json={"name": name})
        if response.status_code == 201:
            user_data = response.json()
            print("✅ User created:", user_data)
            return user_data["id"]
        else:
            print(f"❌ Failed to create user: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception while creating user: {e}")
    return None

def create_task(user_id, description):
    try:
        response = requests.post(TASKS_URL, json={
            "title": description,
            "user_id": user_id
        })
        if response.status_code == 201:
            task_data = response.json()
            print("✅ Task created:", task_data)
            return task_data["id"]
        else:
            print(f"❌ Failed to create task: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception while creating task: {e}")
    return None

def get_tasks():
    try:
        response = requests.get(TASKS_URL)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to fetch tasks: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception while fetching tasks: {e}")
    return []

def delete_user(user_id):
    try:
        response = requests.delete(f"{USERS_URL}/{user_id}")
        if response.status_code == 200:
            print(f"✅ User with ID {user_id} deleted successfully.")
        else:
            print(f"❌ Failed to delete user {user_id}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception while deleting user {user_id}: {e}")

def delete_task(task_id):
    try:
        response = requests.delete(f"{TASKS_URL}/{task_id}")
        if response.status_code == 200:
            print(f"✅ Task with ID {task_id} deleted successfully.")
        else:
            print(f"❌ Failed to delete task {task_id}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception while deleting task {task_id}: {e}")

def integration_test():
    print("🚀 Starting integration test...")

    user_id = create_user("Camilo")
    if user_id is None:
        print("🛑 Aborting test: user creation failed.")
        return

    task_id = create_task(user_id, "Prepare presentation")
    if task_id is None:
        print("🛑 Aborting test: task creation failed.")
        delete_user(user_id)
        return

    tasks = get_tasks()
    user_tasks = [t for t in tasks if t["user_id"] == user_id]
    if any(t["id"] == task_id for t in user_tasks):
        print("✅ Task correctly registered")
    else:
        print("❌ Task was not correctly registered")

    delete_task(task_id)
    delete_user(user_id)

    tasks_after = get_tasks()
    if all(t["id"] != task_id for t in tasks_after):
        print("✅ Cleanup verified: task and user deleted")
    else:
        print("❌ Task was not properly deleted")

if __name__ == "__main__":
    integration_test()
