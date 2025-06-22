import requests

USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def run():
    """Intenta crear una tarea con un user_id inexistente (debe fallar)."""
    # 9999 es un ID que no existe
    resp = requests.post(TASKS_URL, json={"title": "Tarea fantasma", "user_id": 9999})
    assert resp.status_code == 201, "El servicio NO debería permitir user_id inválido"
