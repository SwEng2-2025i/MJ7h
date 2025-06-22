import requests
import json
from report_generator import generar_reporte_frontend

def test_frontend():
    print("🔧 Iniciando prueba E2E Frontend + Backend...")

    # 1. Crear usuario a través del frontend
    response = requests.post("http://localhost:5000/crear_usuario", data={"name": "Usuario E2E"})
    assert response.status_code == 200
    user_id = extraer_id_desde_respuesta(response.text)
    assert user_id is not None, "❌ No se pudo extraer el ID del usuario"
    print(f"✅ Usuario creado por frontend con ID: {user_id}")

    # 2. Crear tarea a través del frontend
    response = requests.post("http://localhost:5000/crear_tarea", data={"title": "Tarea E2E"})
    assert response.status_code == 200
    task_id = extraer_id_desde_respuesta(response.text)
    assert task_id is not None, "❌ No se pudo extraer el ID de la tarea"
    print(f"✅ Tarea creada por frontend con ID: {task_id}")

    # 3. Verificar datos por backend
    r1 = requests.get(f"http://localhost:5001/users/{user_id}")
    r2 = requests.get(f"http://localhost:5002/tasks/{task_id}")
    assert r1.status_code == 200, "❌ Usuario no encontrado en backend"
    assert r2.status_code == 200, "❌ Tarea no encontrada en backend"

    # 4. Eliminar los datos (limpieza)
    requests.delete(f"http://localhost:5001/users/{user_id}")
    requests.delete(f"http://localhost:5002/tasks/{task_id}")

    # 5. Confirmar eliminación
    r1 = requests.get(f"http://localhost:5001/users/{user_id}")
    r2 = requests.get(f"http://localhost:5002/tasks/{task_id}")
    assert r1.status_code == 404, "❌ Usuario no fue eliminado correctamente"
    assert r2.status_code == 404, "❌ Tarea no fue eliminada correctamente"
    
    print("✅ Limpieza E2E verificada")

    # 6. Generar reporte
    generar_reporte_frontend(user_id, task_id)
    print("📄 Reporte E2E generado correctamente")

def extraer_id_desde_respuesta(texto_html):
    try:
        json_obj = json.loads(texto_html)
        return json_obj.get("id")
    except Exception:
        return None

if __name__ == "__main__":
    test_frontend()
