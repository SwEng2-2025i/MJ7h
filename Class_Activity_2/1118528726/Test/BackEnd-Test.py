import requests

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PDF.creation_PDF import generar_pdf

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("✅ User created:", user_data)
    return (user_data["id"] , ("(good) User created:", str(user_data)))

def delete_user(user_id):
    url = f"{USERS_URL}/{user_id}"
    response = requests.delete(url)
    response.raise_for_status()
    message = response.json()
    print("✅ User deleted: ", message)
    return ("(good) User deleted: ", str(message))


def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("✅ Task created:", task_data)
    return (task_data["id"] , ("(good) Task created:", str(task_data)))

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    print(tasks)
    dic = tasks
    string = str(dic).replace('{', '').replace('}', '\n')
    return (tasks,("(good) Tasks retrieved:", string))

#
def delete_task(id_task):
    url = f"{TASKS_URL}/{id_task}"
    response = requests.delete(url)
    response.raise_for_status()
    message = response.json()
    print("✅ task deleted: ", message)
    return ("(good) Task deleted: ", str(message))


def integration_test():
    array = [] 
    # Step 1: Create user
    user_id, message = create_user("Camilo")
    array.append(message)

    # Step 2: Create task for that user
    task_id, message= create_task(user_id, "Prepare presentation")
    array.append(message)

    # Step 3: Verify that the task is registered and associated with the user
    tasks, message = get_tasks()
    array.append(message)

    user_tasks = [t for t in tasks if t["user_id"] == user_id]

    assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"

    #Step 4: Delete the task and the user 
    message = delete_task(task_id)
    array.append(message)

    message = delete_user(user_id)
    array.append(message)

    print("✅ Test completed: task was successfully registered and linked to the user.")
    
    generar_pdf("BackEnd-Test", array)


def integration_test_witherror(nameUser, nameTask):
    array = [] 

    # Step 1: Create user
    try:
        user_id, message = create_user(nameUser)
        array.append(message)
        # Step 2: Create task
        try:
            task_id, message= create_task(user_id, nameTask)
            array.append(message)
            
            # step 3: verify task   
            tasks, message = get_tasks()
            array.append(message)

            user_tasks = [t for t in tasks if t["user_id"] == user_id]

            assert any(t["id"] == task_id for t in user_tasks), array.append("❌ The task was not correctly registered")

            #Step 4: Delete the task and the user 
            try:
                message = delete_task(task_id)
                array.append(message)

                message = delete_user(user_id)
                array.append(message)
                print("✅ Test completed: task was successfully registered and linked to the user.")
            
            except requests.exceptions.HTTPError as e:
                array.append(("(bad) Error creating user:", f"{e.response.json()}"))
        except requests.exceptions.HTTPError as e:
            array.append(("(bad) Error creating user:" ,f"{e.response.json()}"))
    except requests.exceptions.HTTPError as e:
        array.append(("(bad) Error creating user:", f"{e.response.json()}"))

    generar_pdf("BackEnd-Test", array)


# Main 
if __name__ == "__main__":
    # integration_test()
    integration_test_witherror("Camilo", "Prepare presentation")
    integration_test_witherror("", "Prepare presentation")