import requests
from test_report_gen import generate_pdf_report

# Endpoints base
USER_API = "http://localhost:5001"
TASK_API = "http://localhost:5002"

# Variables de test
test_email = "test@example.com"
test_password = "test123"
task_title = "Tarea de prueba"

def run_backend_test():
    results = []
    created_user_id = None
    created_task_id = None

    # === TEST USUARIO ===
    try:
        user_data = {"email": test_email, "password": test_password}
        r = requests.post(f"{USER_API}/users", json=user_data)
        r.raise_for_status()
        created_user_id = r.json().get("id")
        results.append("Usuario creado exitosamente")
    except Exception as e:
        results.append(f"Error al crear usuario: {e}")

    # === TEST TAREA ===
    try:
        task_data = {"title": task_title}
        r = requests.post(f"{TASK_API}/tasks", json=task_data)
        r.raise_for_status()
        created_task_id = r.json().get("id")
        results.append("Tarea creada exitosamente")
    except Exception as e:
        results.append(f"Error al crear tarea: {e}")

    # === DELETE USUARIO ===
    if created_user_id:
        try:
            r = requests.delete(f"{USER_API}/users/{created_user_id}")
            if r.status_code == 200:
                results.append("Usuario eliminado correctamente")
            else:
                results.append("Falló la eliminación del usuario")
        except Exception as e:
            results.append(f"Error al eliminar usuario: {e}")

    # === DELETE TAREA ===
    if created_task_id:
        try:
            r = requests.delete(f"{TASK_API}/tasks/{created_task_id}")
            if r.status_code == 200:
                results.append("Tarea eliminada correctamente")
            else:
                results.append("Falló la eliminación de la tarea")
        except Exception as e:
            results.append(f"Error al eliminar tarea: {e}")

    # === VERIFICACIÓN DE LIMPIEZA ===
    try:
        users = requests.get(f"{USER_API}/users").json()
        user_exists = any(u.get("email") == test_email for u in users)
        if not user_exists:
            results.append("Usuario efectivamente eliminado")
        else:
            results.append("Usuario aún existe")

        tasks = requests.get(f"{TASK_API}/tasks").json()
        task_exists = any(t.get("title") == task_title for t in tasks)
        if not task_exists:
            results.append("Tarea efectivamente eliminada")
        else:
            results.append("Tarea aún existe")

    except Exception as e:
        results.append(f"Error al verificar limpieza: {e}")

    # === GENERAR REPORTE PDF ===
    generate_pdf_report("\n".join(results))

if __name__ == "__main__":
    run_backend_test()
