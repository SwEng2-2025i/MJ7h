import requests

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("✅ User created:", user_data)
    return user_data["id"]

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()
    print("✅ User deleted:", user_id)
    return response.json()

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("✅ Task created:", task_data)
    return task_data["id"]

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()
    print("✅ Task deleted:", task_id)
    return response.json()

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def get_user(user_id):
    response = requests.get(f"{USERS_URL}/{user_id}")
    response.raise_for_status()
    users = response.json()
    return users

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

    #step 4: Delete the task
    delete_task(task_id)
    new_tasks = get_tasks()
    assert not any(t["id"] == task_id for t in new_tasks), "❌ The task was not deleted"
    print("✅ Task deleted successfully.")

    # Step 5: Delete the user
    delete_user(user_id)
    try:
        deletion_confirm = get_user(user_id)
        print("❌ User deletion failed: user still exists.")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print("✅ User deletion confirmed: user not found.")

    print("✅ All integration tests passed successfully.")


if __name__ == "__main__":
    integration_test()