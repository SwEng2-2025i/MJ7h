"""
Cleanup.py

Script para eliminar todos los registros de usuarios y tareas
vía los endpoints REST de User_Service y Task_Service.
"""
import requests

# URLs de los servicios
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"


def cleanup_tasks():
    """
    Obtiene todas las tareas y las elimina una por una.
    """
    try:
        resp = requests.get(TASKS_URL, timeout=5)
        resp.raise_for_status()
    except Exception as e:
        print(f"Error al obtener tareas: {e}")
        return

    tasks = resp.json()
    if not tasks:
        print("No hay tareas para eliminar.")
        return

    for t in tasks:
        task_id = t.get("id")
        try:
            del_resp = requests.delete(f"{TASKS_URL}/{task_id}", timeout=5)
            if del_resp.status_code == 200:
                print(f"✅ Tarea eliminada: {task_id}")
            else:
                print(f"⚠️ Falló al eliminar tarea {task_id}: {del_resp.status_code}")
        except Exception as e:
            print(f"Error al eliminar tarea {task_id}: {e}")


def cleanup_users():
    """
    Obtiene todos los usuarios y los elimina uno por uno.
    """
    try:
        resp = requests.get(USERS_URL, timeout=5)
        resp.raise_for_status()
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return

    users = resp.json()
    if not users:
        print("No hay usuarios para eliminar.")
        return

    for u in users:
        user_id = u.get("id")
        try:
            del_resp = requests.delete(f"{USERS_URL}/{user_id}", timeout=5)
            if del_resp.status_code == 200:
                print(f"✅ Usuario eliminado: {user_id}")
            else:
                print(f"⚠️ Falló al eliminar usuario {user_id}: {del_resp.status_code}")
        except Exception as e:
            print(f"Error al eliminar usuario {user_id}: {e}")


if __name__ == "__main__":
    print("🔄 Iniciando limpieza de datos...")
    
    cleanup_tasks()
    
    cleanup_users()
    print("🎉 Limpieza completada.")
