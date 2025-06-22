import requests
from report_generator import generar_reporte_backend

def test_backend():
    print("🔧 Iniciando prueba de integración Backend...")

    # 1. Crear usuario
    user_data = {"name": "Usuario de prueba"}
    r = requests.post("http://localhost:5001/users", json=user_data)
    assert r.status_code == 201, "❌ Fallo al crear usuario"
    user = r.json()
    user_id = user["id"]
    print(f"✅ Usuario creado: {user}")

    # 2. Crear tarea
    task_data = {"title": "Tarea de prueba"}
    r = requests.post("http://localhost:5002/tasks", json=task_data)
    assert r.status_code == 201, "❌ Fallo al crear tarea"
    task = r.json()
    task_id = task["id"]
    print(f"✅ Tarea creada: {task}")

    # 3. Verificar existencia
    r = requests.get(f"http://localhost:5001/users/{user_id}")
    assert r.status_code == 200, "❌ Usuario no encontrado tras crearlo"

    r = requests.get(f"http://localhost:5002/tasks/{task_id}")
    assert r.status_code == 200, "❌ Tarea no encontrada tras crearla"

    # 4. Eliminar los datos (limpieza)
    r = requests.delete(f"http://localhost:5001/users/{user_id}")
    assert r.status_code == 200, "❌ Fallo al eliminar usuario"

    r = requests.delete(f"http://localhost:5002/tasks/{task_id}")
    assert r.status_code == 200, "❌ Fallo al eliminar tarea"

    # 5. Verificar eliminación
    r = requests.get(f"http://localhost:5001/users/{user_id}")
    assert r.status_code == 404, "❌ Usuario no fue eliminado correctamente"

    r = requests.get(f"http://localhost:5002/tasks/{task_id}")
    assert r.status_code == 404, "❌ Tarea no fue eliminada correctamente"

    print("✅ Limpieza de datos verificada")

    # 6. Generar reporte PDF
    generar_reporte_backend(user, task)
    print("📄 Reporte generado correctamente")

if __name__ == "__main__":
    test_backend()
