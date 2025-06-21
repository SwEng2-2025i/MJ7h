import requests
import pytest # Importar pytest

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

# --- FUNCIONES AUXILIARES DE API (con borrado) ---

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    return response.json()

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={"title": description, "user_id": user_id})
    response.raise_for_status()
    return response.json()

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    return response.json()

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()
    print(f"✅ User {user_id} deleted.")
    return response.json()

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()
    print(f"✅ Task {task_id} deleted.")
    return response.json()

# --- PRUEBAS DE INTEGRACIÓN ---

def test_integration_successful_with_cleanup():
    """
    Prueba de integración que crea un usuario y una tarea, verifica la creación,
    y luego limpia los datos creados (borra el usuario y la tarea).
    """
    user_data = None
    task_data = None
    
    try:
        # Step 1: Create user
        user_data = create_user("Camilo-Test")
        user_id = user_data["id"]
        print("✅ User created:", user_data)

        # Step 2: Create task for that user
        task_data = create_task(user_id, "Prepare presentation for test")
        task_id = task_data["id"]
        print("✅ Task created:", task_data)

        # Step 3: Verify that the task is registered and associated with the user
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]

        assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
        print("✅ Verification complete: task was successfully registered.")

    finally:
        # Step 4: Cleanup (this will run even if assertions fail)
        print("\n--- Starting Cleanup ---")
        if task_data:
            delete_task(task_data["id"])
        if user_data:
            delete_user(user_data["id"])
        print("--- Cleanup Finished ---")


# El bloque if __name__ == "__main__": no es necesario con pytest,
# pero se puede dejar para ejecución manual si se desea.
if __name__ == "__main__":
    # Para ejecutar con pytest, simplemente corre `pytest` en la terminal.
    # Esta llamada es para ejecución manual del script.
    try:
        test_integration_successful_with_cleanup()
        test_failing_example()
    except AssertionError as e:
        print(e)