import requests
from Cleanup import cleanup_tasks, cleanup_users

USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    resp = requests.post(USERS_URL, json={"name": name}, timeout=5)
    resp.raise_for_status()
    return resp.json()["id"]

def create_task(user_id, description):
    resp = requests.post(
        TASKS_URL,
        json={"title": description, "user_id": user_id},
        timeout=5,
    )
    resp.raise_for_status()
    return resp.json()["id"]

def get_tasks():
    resp = requests.get(TASKS_URL, timeout=5)
    resp.raise_for_status()
    return resp.json()

def test_backend_api_limpieza_y_verificacion():
    # Aseguramos punto limpio al inicio
    cleanup_tasks()
    cleanup_users()

    # Crea usuario y tarea
    user_id = create_user("Camilo")
    task_id = create_task(user_id, "Prepare presentation")

    # Verifica que la tarea existe
    tasks = get_tasks()
    assert any(t["id"] == task_id and t["user_id"] == user_id for t in tasks), \
           "La tarea no se registró correctamente"

    # Ejecuta cleanup y vuelve a verificar
    cleanup_tasks()
    cleanup_users()

    tasks_after = get_tasks()
    assert not any(t["id"] == task_id for t in tasks_after), \
           "La tarea NO fue eliminada en el cleanup"

    user_status = requests.get(f"{USERS_URL}/{user_id}", timeout=5).status_code
    assert user_status == 404, "El usuario NO fue eliminado en el cleanup"
