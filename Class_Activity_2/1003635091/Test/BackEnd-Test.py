import requests
import time
from datetime import datetime

try:
    from backend_pdf_generator import generate_backend_test_report
except ImportError:
    print("⚠️ Advertencia: No se encontró backend_pdf_generator.py")
    generate_backend_test_report = None

class TestResult:
    def __init__(self, test_name, category, status, error_message=None, duration=0):
        self.test_name = test_name
        self.category = category
        self.status = status
        self.error_message = error_message
        self.duration = duration
        self.timestamp = datetime.now()

class BackEndDataCleaner:
    def __init__(self):
        self.created_users = set()
        self.created_tasks = set()
        self.api_urls = {
            "users": "http://localhost:5002/users",
            "tasks": "http://localhost:5003/tasks"
        }
        self.initial_state = {"users": set(), "tasks": set()}
    
    def take_initial_snapshot(self):
        """Captura el estado inicial del sistema antes de las pruebas"""
        for resource in ["users", "tasks"]:
            try:
                response = requests.get(self.api_urls[resource], timeout=10)
                if response.status_code == 200:
                    ids = {str(item['id']) for item in response.json()}
                    self.initial_state[resource] = ids
                    print(f"Snapshot {resource}: {len(ids)} elementos")
            except Exception as e:
                print(f"Error tomando snapshot de {resource}: {e}")
                self.initial_state[resource] = set()
    
    def register_created_item(self, item_type, item_id):
        """Registra un elemento creado para limpieza posterior"""
        item_id = str(item_id)
        target_set = getattr(self, f"created_{item_type}")
        target_set.add(item_id)
    
    def unregister_item(self, item_type, item_id):
        """Desregistra un elemento que ya fue eliminado manualmente"""
        item_id = str(item_id)
        target_set = getattr(self, f"created_{item_type}")
        target_set.discard(item_id)
    
    def get_current_state(self):
        """Obtiene el estado actual del sistema"""
        current_state = {}
        for resource in ["users", "tasks"]:
            try:
                response = requests.get(self.api_urls[resource], timeout=10)
                current_state[resource] = {str(item['id']) for item in response.json()} if response.status_code == 200 else set()
            except:
                current_state[resource] = set()
        return current_state
    
    def cleanup_all_data(self):
        """Elimina TODOS los datos creados durante las pruebas"""
        print("\nIniciando limpieza completa de datos backend...")
        
        current_state = self.get_current_state()
        
        # Identificar todos los datos de prueba
        test_data = {}
        for resource in ["users", "tasks"]:
            new_items = current_state[resource] - self.initial_state[resource]
            tracked_items = getattr(self, f"created_{resource}")
            test_data[resource] = new_items | tracked_items
        
        print(f"Datos a eliminar - Usuarios: {len(test_data['users'])}, Tareas: {len(test_data['tasks'])}")
        
        # Eliminar tareas primero (integridad referencial)
        self._delete_items("tasks", test_data["tasks"])
        
        # Eliminar usuarios
        self._delete_items("users", test_data["users"])
        
        # Verificar limpieza completa
        self._verify_cleanup()
        
        # Limpiar registros internos
        self.created_users.clear()
        self.created_tasks.clear()
        print("✅ Limpieza backend completada")
    
    def _delete_items(self, resource, item_ids):
        """Elimina un conjunto de elementos de un tipo específico"""
        for item_id in item_ids:
            try:
                response = requests.delete(f"{self.api_urls[resource]}/{item_id}", timeout=10)
                if response.status_code in [200, 404]:
                    print(f"✅ {resource[:-1].title()} {item_id} eliminado")
                else:
                    print(f"⚠️ Error eliminando {resource[:-1]} {item_id}: {response.status_code}")
            except Exception as e:
                print(f"❌ Error eliminando {resource[:-1]} {item_id}: {e}")
    
    def _verify_cleanup(self):
        """Verifica que la limpieza fue exitosa"""
        final_state = self.get_current_state()
        
        for resource in ["users", "tasks"]:
            remaining_test_data = final_state[resource] - self.initial_state[resource]
            if remaining_test_data:
                print(f"⚠️ Datos residuales en {resource}: {remaining_test_data}")
                # Intento de limpieza de emergencia
                self._delete_items(resource, remaining_test_data)
            else:
                print(f"✅ {resource.title()} completamente limpio")

class BackEndTestSuite:
    def __init__(self):
        self.api_urls = {
            "users": "http://localhost:5002/users",
            "tasks": "http://localhost:5003/tasks"
        }
        self.results = []
        self.data_cleaner = BackEndDataCleaner()
        self.start_time = datetime.now()
    
    def run_test(self, test_func, test_name, category):
        """Ejecuta un test individual con manejo de errores"""
        start_time = time.time()
        try:
            test_func()
            result = TestResult(test_name, category, 'PASS', duration=time.time() - start_time)
            print(f"✅ {test_name}")
        except Exception as e:
            result = TestResult(test_name, category, 'FAIL', str(e), time.time() - start_time)
            print(f"❌ {test_name}: {str(e)}")
        
        self.results.append(result)
    
    def _make_request(self, method, url, **kwargs):
        """Wrapper para peticiones HTTP con timeout consistente"""
        kwargs.setdefault('timeout', 10)
        return requests.request(method, url, **kwargs)
    
    def _create_user_direct(self, name="Usuario Test"):
        """Crea un usuario directamente sin usar otros métodos de test"""
        response = self._make_request('POST', self.api_urls["users"], json={"name": name})
        if response.status_code == 201:
            user_data = response.json()
            self.data_cleaner.register_created_item("users", user_data["id"])
            return user_data["id"]
        return None
    
    def _create_task_direct(self, user_id, title="Tarea Test"):
        """Crea una tarea directamente sin usar otros métodos de test"""
        response = self._make_request('POST', self.api_urls["tasks"], json={"title": title, "user_id": user_id})
        if response.status_code == 201:
            task_data = response.json()
            self.data_cleaner.register_created_item("tasks", task_data["id"])
            return task_data["id"]
        return None
    
    # Tests de Usuarios
    def test_create_user_success(self):
        """Test creación exitosa de usuario"""
        response = self._make_request('POST', self.api_urls["users"], json={"name": "Usuario Test"})
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        
        user_data = response.json()
        assert "id" in user_data and user_data["name"] == "Usuario Test"
        
        self.data_cleaner.register_created_item("users", user_data["id"])
        return user_data["id"]
    
    def test_create_user_empty_name(self):
        """Test creación de usuario con nombre vacío"""
        response = self._make_request('POST', self.api_urls["users"], json={"name": ""})
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    
    def test_create_user_no_name(self):
        """Test creación de usuario sin campo name"""
        response = self._make_request('POST', self.api_urls["users"], json={})
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    
    def test_get_user_success(self):
        """Test obtener usuario existente"""
        user_id = self._create_user_direct()
        assert user_id is not None, "Failed to create user for test"
        
        response = self._make_request('GET', f"{self.api_urls['users']}/{user_id}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        user_data = response.json()
        assert user_data["id"] == user_id, "User ID mismatch"
    
    def test_get_user_not_found(self):
        """Test obtener usuario inexistente"""
        response = self._make_request('GET', f"{self.api_urls['users']}/99999")
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    
    def test_get_all_users(self):
        """Test obtener lista de usuarios"""
        response = self._make_request('GET', self.api_urls["users"])
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert isinstance(response.json(), list), "Response should be a list"
    
    def test_delete_user_success(self):
        """Test eliminación exitosa de usuario"""
        user_id = self._create_user_direct()
        assert user_id is not None, "Failed to create user for test"
        
        response = self._make_request('DELETE', f"{self.api_urls['users']}/{user_id}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Verificar eliminación
        get_response = self._make_request('GET', f"{self.api_urls['users']}/{user_id}")
        assert get_response.status_code == 404, "User should be deleted"
        
        # Desregistrar ya que fue eliminado manualmente
        self.data_cleaner.unregister_item("users", user_id)
    
    def test_delete_user_not_found(self):
        """Test eliminación de usuario inexistente"""
        response = self._make_request('DELETE', f"{self.api_urls['users']}/99999")
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    
    # Tests de Tareas
    def test_create_task_success(self):
        """Test creación exitosa de tarea"""
        user_id = self._create_user_direct()
        assert user_id is not None, "Failed to create user for test"
        
        response = self._make_request('POST', self.api_urls["tasks"], json={"title": "Tarea Test", "user_id": user_id})
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        
        task_data = response.json()
        assert "id" in task_data and task_data["title"] == "Tarea Test" and task_data["user_id"] == user_id
        
        self.data_cleaner.register_created_item("tasks", task_data["id"])
        return task_data["id"]
    
    def test_create_task_invalid_user(self):
        """Test creación de tarea con usuario inexistente"""
        response = self._make_request('POST', self.api_urls["tasks"], json={"title": "Tarea Test", "user_id": 99999})
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    
    def test_create_task_empty_title(self):
        """Test creación de tarea con título vacío"""
        user_id = self._create_user_direct()
        assert user_id is not None, "Failed to create user for test"
        
        response = self._make_request('POST', self.api_urls["tasks"], json={"title": "", "user_id": user_id})
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    
    def test_create_task_missing_fields(self):
        """Test creación de tarea con campos faltantes"""
        response = self._make_request('POST', self.api_urls["tasks"], json={})
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    
    def test_get_task_success(self):
        """Test obtener tarea existente"""
        user_id = self._create_user_direct()
        task_id = self._create_task_direct(user_id)
        assert task_id is not None, "Failed to create task for test"
        
        response = self._make_request('GET', f"{self.api_urls['tasks']}/{task_id}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        task_data = response.json()
        assert task_data["id"] == task_id, "Task ID mismatch"
    
    def test_get_task_not_found(self):
        """Test obtener tarea inexistente"""
        response = self._make_request('GET', f"{self.api_urls['tasks']}/99999")
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    
    def test_get_all_tasks(self):
        """Test obtener lista de tareas"""
        response = self._make_request('GET', self.api_urls["tasks"])
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert isinstance(response.json(), list), "Response should be a list"
    
    def test_delete_task_success(self):
        """Test eliminación exitosa de tarea"""
        user_id = self._create_user_direct()
        task_id = self._create_task_direct(user_id)
        assert task_id is not None, "Failed to create task for test"
        
        response = self._make_request('DELETE', f"{self.api_urls['tasks']}/{task_id}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Verificar eliminación
        get_response = self._make_request('GET', f"{self.api_urls['tasks']}/{task_id}")
        assert get_response.status_code == 404, "Task should be deleted"
        
        # Desregistrar ya que fue eliminada manualmente
        self.data_cleaner.unregister_item("tasks", task_id)
    
    def test_delete_task_not_found(self):
        """Test eliminación de tarea inexistente"""
        response = self._make_request('DELETE', f"{self.api_urls['tasks']}/99999")
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    
    # Tests de Integración
    def test_user_task_integration(self):
        """Test integración usuario-tarea completa"""
        # Crear usuario específico para esta prueba
        user_id = self._create_user_direct("Usuario Integración")
        assert user_id is not None, "Failed to create user"
        
        # Crear tarea específicamente para ese usuario
        task_id = self._create_task_direct(user_id, "Tarea Integración")
        assert task_id is not None, "Failed to create task"
        
        # Verificar vinculación
        response = self._make_request('GET', self.api_urls["tasks"])
        assert response.status_code == 200
        
        tasks = response.json()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        assert any(t["id"] == task_id for t in user_tasks), f"Task {task_id} not linked to user {user_id}"
    
    def test_delete_user_cascade(self):
        """Test eliminación en cascada: usuario elimina sus tareas"""
        user_id = self._create_user_direct("Usuario Cascada")
        task_id = self._create_task_direct(user_id, "Tarea Cascada")
        
        # Eliminar usuario
        delete_response = self._make_request('DELETE', f"{self.api_urls['users']}/{user_id}")
        assert delete_response.status_code == 200
        
        # Verificar que la tarea también fue eliminada
        task_check = self._make_request('GET', f"{self.api_urls['tasks']}/{task_id}")
        assert task_check.status_code == 404, "Task should be deleted when user is deleted"
        
        # Desregistrar ambos elementos
        self.data_cleaner.unregister_item("users", user_id)
        self.data_cleaner.unregister_item("tasks", task_id)
    
    def test_multiple_tasks_per_user(self):
        """Test múltiples tareas por usuario"""
        user_id = self._create_user_direct("Usuario Múltiples")
        
        # Crear 3 tareas para el mismo usuario
        task_ids = []
        for i in range(3):
            task_id = self._create_task_direct(user_id, f"Tarea {i+1}")
            assert task_id is not None, f"Failed to create task {i+1}"
            task_ids.append(task_id)
        
        # Verificar que todas están asociadas al usuario
        response = self._make_request('GET', self.api_urls["tasks"])
        tasks = response.json()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        
        assert len(user_tasks) >= 3, f"Expected at least 3 tasks, found {len(user_tasks)}"
        for task_id in task_ids:
            assert any(t["id"] == task_id for t in user_tasks), f"Task {task_id} not found"
    
    def run_all_tests(self):
        """Ejecuta toda la suite de tests backend"""
        print("Tomando snapshot inicial del backend...")
        self.data_cleaner.take_initial_snapshot()
        
        # Definición de todos los tests
        test_suite = [
            # Tests API Usuarios
            (self.test_create_user_success, "Crear Usuario Exitoso", "API Usuarios"),
            (self.test_create_user_empty_name, "Crear Usuario Nombre Vacío", "API Usuarios"),
            (self.test_create_user_no_name, "Crear Usuario Sin Nombre", "API Usuarios"),
            (self.test_get_user_success, "Obtener Usuario Exitoso", "API Usuarios"),
            (self.test_get_user_not_found, "Obtener Usuario Inexistente", "API Usuarios"),
            (self.test_get_all_users, "Obtener Todos los Usuarios", "API Usuarios"),
            (self.test_delete_user_success, "Eliminar Usuario Exitoso", "API Usuarios"),
            (self.test_delete_user_not_found, "Eliminar Usuario Inexistente", "API Usuarios"),
            
            # Tests API Tareas
            (self.test_create_task_success, "Crear Tarea Exitosa", "API Tareas"),
            (self.test_create_task_invalid_user, "Crear Tarea Usuario Inválido", "API Tareas"),
            (self.test_create_task_empty_title, "Crear Tarea Título Vacío", "API Tareas"),
            (self.test_create_task_missing_fields, "Crear Tarea Campos Faltantes", "API Tareas"),
            (self.test_get_task_success, "Obtener Tarea Exitosa", "API Tareas"),
            (self.test_get_task_not_found, "Obtener Tarea Inexistente", "API Tareas"),
            (self.test_get_all_tasks, "Obtener Todas las Tareas", "API Tareas"),
            (self.test_delete_task_success, "Eliminar Tarea Exitosa", "API Tareas"),
            (self.test_delete_task_not_found, "Eliminar Tarea Inexistente", "API Tareas"),
            
            # Tests Integración
            (self.test_user_task_integration, "Integración Usuario-Tarea", "Integración Backend"),
            (self.test_delete_user_cascade, "Eliminación en Cascada", "Integración Backend"),
            (self.test_multiple_tasks_per_user, "Múltiples Tareas por Usuario", "Integración Backend")
        ]
        
        try:
            print(f"\nEjecutando {len(test_suite)} tests backend...")
            
            for test_func, name, category in test_suite:
                self.run_test(test_func, name, category)
        
        finally:
            # Limpieza garantizada
            self.data_cleaner.cleanup_all_data()
        
        # Generar reporte y mostrar estadísticas
        pdf_file = self._generate_pdf_report()
        self._show_stats()
        
        return self.results, pdf_file
    
    def _generate_pdf_report(self):
        """Genera el reporte PDF automáticamente"""
        print("\nGenerando reporte PDF backend...")
        try:
            if generate_backend_test_report:
                pdf_file = generate_backend_test_report(self.results, self.start_time)
                return pdf_file
            else:
                print("⚠️ No se pudo generar PDF - falta backend_pdf_generator.py")
                return None
        except Exception as e:
            print(f"❌ Error generando PDF: {e}")
            return None
    
    def _show_stats(self):
        """Muestra estadísticas finales en consola"""
        total = len(self.results)
        passed = len([r for r in self.results if r.status == 'PASS'])
        
        print(f"\n{'='*50}")
        print("RESUMEN TESTS BACKEND")
        print(f"{'='*50}")
        print(f"Total: {total} | Exitosos: {passed} | Fallidos: {total-passed} | Éxito: {(passed/total*100):.1f}%")
        
        # Estadísticas por categoría
        categories = {}
        for result in self.results:
            cat = result.category
            if cat not in categories:
                categories[cat] = {'passed': 0, 'failed': 0}
            categories[cat]['passed' if result.status == 'PASS' else 'failed'] += 1
        
        print("\nPor categoría:")
        for cat, data in categories.items():
            total_cat = data['passed'] + data['failed']
            rate = (data['passed'] / total_cat * 100) if total_cat > 0 else 0
            print(f"  {cat}: {data['passed']}/{total_cat} ({rate:.1f}%)")

def main():
    print("Sistema de Pruebas Backend")
    print("=" * 50)
    
    suite = BackEndTestSuite()
    
    try:
        results, pdf_file = suite.run_all_tests()
        # ✅ LÍNEA AÑADIDA - Mostrar nombre del archivo PDF generado
        if pdf_file:
            print(f"\n🎯 Pruebas backend completadas. Reporte: {pdf_file}")
        else:
            print(f"\n🎯 Pruebas backend completadas. Error generando reporte PDF.")
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        raise
    finally:
        print("\n🏁 Ejecución finalizada")

if __name__ == "__main__":
    main()
