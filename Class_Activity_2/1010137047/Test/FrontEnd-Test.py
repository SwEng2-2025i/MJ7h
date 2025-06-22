import requests
from test_report_gen import generate_pdf_report

FRONT_URL = "http://localhost:5000"
USER_API = "http://localhost:5001"
TASK_API = "http://localhost:5002"

def run_frontend_test():
    results = []
    email = "frontend@test.com"
    password = "abc123"
    title = "Tarea Frontend"

    # Simula el registro de usuario desde frontend
    try:
        form = {"email": email, "password": password}
        r = requests.post(f"{FRONT_URL}/", data=form)
        results.append("Usuario creado desde Front-End")
    except Exception as e:
        results.append(f"Error creando usuario desde frontend: {e}")

    # Simula la creación de tarea desde frontend
    try:
        form = {"title": title}
        r = requests.post(f"{FRONT_URL}/", data=form)
        results.append("Tarea creada desde Front-End")
    except Exception as e:
        results.append(f"Error creando tarea desde frontend: {e}")

    # Limpieza
    try:
        users = requests.get(f"{USER_API}/users").json()
        user = next((u for u in users if u["email"] == email), None)
        if user:
            requests.delete(f"{USER_API}/users/{user['id']}")
            results.append("Usuario limpiado correctamente")
        else:
            results.append("Usuario no encontrado para limpiar")
    except Exception as e:
        results.append(f"Error eliminando usuario: {e}")

    try:
        tasks = requests.get(f"{TASK_API}/tasks").json()
        task = next((t for t in tasks if t["title"] == title), None)
        if task:
            requests.delete(f"{TASK_API}/tasks/{task['id']}")
            results.append("Tarea limpiada correctamente")
        else:
            results.append("Tarea no encontrada para limpiar")
    except Exception as e:
        results.append(f"Error eliminando tarea: {e}")

    generate_pdf_report("\n".join(results))

if __name__ == "__main__":
    run_frontend_test()
