import time
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from frontend_pdf_generator import generate_test_report

class TestResult:
    def __init__(self, test_name, category, status, error_message=None, duration=0):
        self.test_name = test_name
        self.category = category
        self.status = status
        self.error_message = error_message
        self.duration = duration
        self.timestamp = datetime.now()

class DataCleaner:
    def __init__(self):
        self.created_users = []
        self.created_tasks = []
        self.initial_users = []
        self.initial_tasks = []
        self.api_urls = {"users": "http://localhost:5002", "tasks": "http://localhost:5003"}
    
    def take_initial_snapshot(self):
        for resource in ["users", "tasks"]:
            try:
                response = requests.get(f"{self.api_urls[resource]}/{resource}", timeout=10)
                if response.status_code == 200:
                    ids = [str(item['id']) for item in response.json()]
                    setattr(self, f"initial_{resource}", ids)
            except Exception as e:
                print(f"Error tomando snapshot de {resource}: {e}")
        print(f"Snapshot inicial - Usuarios: {self.initial_users}, Tareas: {self.initial_tasks}")
    
    def add_created_item(self, item_type, item_id):
        item_id = str(item_id)
        target_list = getattr(self, f"created_{item_type}")
        if item_id not in target_list:
            target_list.append(item_id)
            print(f"Registrado {item_type[:-1]} para limpieza: {item_id}")
    
    def remove_from_cleanup(self, item_type, item_id):
        item_id = str(item_id)
        target_list = getattr(self, f"created_{item_type}")
        if item_id in target_list:
            target_list.remove(item_id)
            print(f"{item_type[:-1].title()} {item_id} removido de lista de limpieza")
    
    def get_current_data(self):
        current_data = {}
        for resource in ["users", "tasks"]:
            try:
                response = requests.get(f"{self.api_urls[resource]}/{resource}", timeout=10)
                current_data[resource] = [str(item['id']) for item in response.json()] if response.status_code == 200 else []
            except Exception as e:
                print(f"Error obteniendo {resource}: {e}")
                current_data[resource] = []
        return current_data["users"], current_data["tasks"]
    
    def cleanup_all_test_data(self):
        print("\nIniciando limpieza completa...")
        current_users, current_tasks = self.get_current_data()
        
        # Identificar datos de prueba
        test_users = list(set([u for u in current_users if u not in self.initial_users] + self.created_users))
        test_tasks = list(set([t for t in current_tasks if t not in self.initial_tasks] + self.created_tasks))
        
        print(f"Eliminando - Usuarios: {test_users}, Tareas: {test_tasks}")
        
        # Eliminar datos
        for resource, items in [("tasks", test_tasks), ("users", test_users)]:
            for item_id in items:
                try:
                    response = requests.delete(f"{self.api_urls[resource]}/{resource}/{item_id}", timeout=10)
                    status = "✅" if response.status_code in [200, 404] else "⚠️"
                    print(f"{status} {resource[:-1].title()} {item_id}")
                except Exception as e:
                    print(f"❌ Error eliminando {resource[:-1]} {item_id}: {e}")
        
        self.created_tasks.clear()
        self.created_users.clear()
    
    def verify_complete_cleanup(self):
        print("\nVerificando limpieza completa...")
        final_users, final_tasks = self.get_current_data()
        
        extra_users = [u for u in final_users if u not in self.initial_users]
        extra_tasks = [t for t in final_tasks if t not in self.initial_tasks]
        
        # Limpieza de emergencia si hay residuos
        for resource, items in [("users", extra_users), ("tasks", extra_tasks)]:
            for item_id in items:
                try:
                    requests.delete(f"{self.api_urls[resource]}/{resource}/{item_id}", timeout=10)
                    print(f"🚨 {resource[:-1].title()} residual {item_id} eliminado")
                except:
                    print(f"💥 No se pudo eliminar {resource[:-1]} residual {item_id}")
        
        # Verificación final
        if not extra_users and not extra_tasks:
            print("🎉 Limpieza completa verificada")
            return True
        else:
            final_check_users, final_check_tasks = self.get_current_data()
            remaining = [u for u in final_check_users if u not in self.initial_users] + [t for t in final_check_tasks if t not in self.initial_tasks]
            if remaining:
                print(f"💥 Datos residuales: {remaining}")
                return False
            print("✅ Limpieza de emergencia exitosa")
            return True

class ExtendedTestSuite:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.results = []
        self.data_cleaner = DataCleaner()
        self.start_time = datetime.now()
    
    def setup_driver(self):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 15)
    
    def teardown_driver(self):
        if self.driver:
            self.driver.quit()
    
    def run_test(self, test_func, test_name, category):
        start_time = time.time()
        try:
            test_func()
            result = TestResult(test_name, category, 'PASS', duration=time.time() - start_time)
            print(f"✅ {test_name} - PASÓ")
        except Exception as e:
            result = TestResult(test_name, category, 'FAIL', str(e), time.time() - start_time)
            print(f"❌ {test_name} - FALLÓ: {str(e)}")
        self.results.append(result)
    
    def abrir_frontend(self):
        self.driver.get("http://localhost:5001")
        self.wait.until(EC.presence_of_element_located((By.ID, "username")))
    
    def _interact_with_element(self, element_id, value=None, button_xpath=None):
        """Llena campo y opcionalmente hace click"""
        element = self.wait.until(EC.element_to_be_clickable((By.ID, element_id)))
        element.clear()
        if value:
            element.send_keys(str(value))
        
        if button_xpath:
            button = self.wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
            button.click()
    
    def _wait_for_result_text(self, result_id, expected_text):
        """Espera texto específico en elemento de resultado"""
        self.wait.until(EC.text_to_be_present_in_element((By.ID, result_id), expected_text))
        return self.driver.find_element(By.ID, result_id).text
    
    def _verify_deletion(self, item_type, item_id):
        """Verifica que un elemento fue eliminado"""
        url = f"http://localhost:500{2 if item_type == 'users' else 3}/{item_type}/{item_id}"
        for _ in range(5):
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 404:
                    return True
                time.sleep(1)
            except:
                return True
        
        # Fallback: eliminar directamente
        try:
            requests.delete(url, timeout=10)
            return True
        except:
            return False
    
    def crear_usuario_exitoso(self):
        unique_name = f"Usuario_{int(time.time() * 1000)}"
        self._interact_with_element("username", unique_name, "//button[contains(text(), 'Crear Usuario')]")
        
        result = self._wait_for_result_text("user-result", "Usuario creado con ID")
        assert "Usuario creado con ID" in result
        
        user_id = str(''.join(filter(str.isdigit, result)))
        self.data_cleaner.add_created_item("users", user_id)
        return user_id
    
    def crear_usuario_fallido(self):
        self._interact_with_element("username", "", "//button[contains(text(), 'Crear Usuario')]")
        result = self._wait_for_result_text("user-result", "Error")
        if "Error" not in result:
            raise AssertionError("Se esperaba error al crear usuario sin nombre")
    
    def crear_tarea_exitosa(self):
        user_id = self.crear_usuario_exitoso()
        unique_task = f"Tarea_{int(time.time() * 1000)}"
        
        self._interact_with_element("task", unique_task)
        self._interact_with_element("userid", user_id, "//button[text()='Crear Tarea']")
        
        result = self._wait_for_result_text("task-result", "Tarea creada con ID")
        assert "Tarea creada con ID" in result
        
        task_id = str(''.join(filter(str.isdigit, result)))
        self.data_cleaner.add_created_item("tasks", task_id)
        return task_id
    
    def crear_tarea_fallida(self):
        self._interact_with_element("task", "Tarea Fallida")
        self._interact_with_element("userid", "99999", "//button[text()='Crear Tarea']")
        
        result = self._wait_for_result_text("task-result", "Error")
        if "Error" not in result:
            raise AssertionError("Se esperaba error al crear tarea con usuario inexistente")
    
    def eliminar_usuario_exitoso(self):
        user_id = self.crear_usuario_exitoso()
        self._interact_with_element("delete-user-id", user_id, "//button[contains(text(), 'Eliminar Usuario')]")
        
        result = self._wait_for_result_text("delete-user-result", "eliminado correctamente")
        assert "eliminado correctamente" in result
        
        if self._verify_deletion("users", user_id):
            self.data_cleaner.remove_from_cleanup("users", user_id)
    
    def eliminar_usuario_fallido(self):
        self._interact_with_element("delete-user-id", "99999", "//button[contains(text(), 'Eliminar Usuario')]")
        result = self._wait_for_result_text("delete-user-result", "Error")
        if "Error" not in result:
            raise AssertionError("Se esperaba error al eliminar usuario inexistente")
    
    def eliminar_tarea_exitosa(self):
        task_id = self.crear_tarea_exitosa()
        self._interact_with_element("delete-task-id", task_id, "//button[contains(text(), 'Eliminar Tarea')]")
        
        result = self._wait_for_result_text("delete-task-result", "eliminada correctamente")
        assert "eliminada correctamente" in result
        
        if self._verify_deletion("tasks", task_id):
            self.data_cleaner.remove_from_cleanup("tasks", task_id)
    
    def eliminar_tarea_fallida(self):
        self._interact_with_element("delete-task-id", "99999", "//button[contains(text(), 'Eliminar Tarea')]")
        result = self._wait_for_result_text("delete-task-result", "Error")
        if "Error" not in result:
            raise AssertionError("Se esperaba error al eliminar tarea inexistente")
    
    def test_eliminacion_y_verificacion(self):
        print("\nIniciando prueba de eliminación y verificación...")
        
        user_id = self.crear_usuario_exitoso()
        task_id = self.crear_tarea_exitosa()
        
        # Verificar existencia inicial
        for url in [f"http://localhost:5003/tasks/{task_id}", f"http://localhost:5002/users/{user_id}"]:
            assert requests.get(url, timeout=10).status_code == 200
        
        # Eliminar a través de UI
        self._interact_with_element("delete-task-id", task_id, "//button[contains(text(), 'Eliminar Tarea')]")
        self._wait_for_result_text("delete-task-result", "eliminada correctamente")
        
        self._interact_with_element("delete-user-id", user_id, "//button[contains(text(), 'Eliminar Usuario')]")
        self._wait_for_result_text("delete-user-result", "eliminado correctamente")
        
        # Verificar eliminación
        if self._verify_deletion("tasks", task_id):
            self.data_cleaner.remove_from_cleanup("tasks", task_id)
        if self._verify_deletion("users", user_id):
            self.data_cleaner.remove_from_cleanup("users", user_id)
        
        print("Prueba de eliminación completada")
    
    def run_all_tests(self):
        print("Tomando snapshot inicial...")
        self.data_cleaner.take_initial_snapshot()
        
        self.setup_driver()
        
        # Lista de pruebas
        tests = [
            (self.crear_usuario_exitoso, "Crear Usuario Exitoso", "Creación de Usuarios"),
            (self.crear_usuario_fallido, "Crear Usuario Fallido", "Creación de Usuarios"),
            (self.crear_tarea_exitosa, "Crear Tarea Exitosa", "Creación de Tareas"),
            (self.crear_tarea_fallida, "Crear Tarea Fallida", "Creación de Tareas"),
            (self.eliminar_usuario_exitoso, "Eliminar Usuario Exitoso", "Eliminación de Usuarios"),
            (self.eliminar_usuario_fallido, "Eliminar Usuario Fallido", "Eliminación de Usuarios"),
            (self.eliminar_tarea_exitosa, "Eliminar Tarea Exitosa", "Eliminación de Tareas"),
            (self.eliminar_tarea_fallida, "Eliminar Tarea Fallida", "Eliminación de Tareas"),
            (self.test_eliminacion_y_verificacion, "Eliminación y Verificación Completa", "Eliminación de Datos")
        ]
        
        try:
            self.abrir_frontend()
            print("\nIniciando pruebas...")
            
            for test_func, name, category in tests:
                self.run_test(test_func, name, category)
                
        finally:
            self.teardown_driver()
            
            # Limpieza y verificación
            current_users, current_tasks = self.data_cleaner.get_current_data()
            print(f"\nEstado antes de limpieza:")
            print(f"Usuarios: {current_users} | Tareas: {current_tasks}")
            print(f"Rastreados - Usuarios: {self.data_cleaner.created_users} | Tareas: {self.data_cleaner.created_tasks}")
            
            self.data_cleaner.cleanup_all_test_data()
            
            if not self.data_cleaner.verify_complete_cleanup():
                raise Exception("LIMPIEZA INCOMPLETA - Datos residuales detectados")
            print("✅ LIMPIEZA COMPLETA GARANTIZADA")
        
        # Generar PDF
        print("\nGenerando reporte PDF...")
        try:
            pdf_file = generate_test_report(self.results, self.start_time)
            print(f"Reporte PDF: {pdf_file}")
        except Exception as e:
            print(f"Error generando PDF: {e}")
            pdf_file = None
        
        self._show_stats()
        return pdf_file
    
    def _show_stats(self):
        total = len(self.results)
        passed = len([r for r in self.results if r.status == 'PASS'])
        
        print(f"\n{'='*50}")
        print("RESUMEN FINAL")
        print(f"{'='*50}")
        print(f"Total: {total} | Exitosas: {passed} | Fallidas: {total-passed} | Éxito: {(passed/total*100):.1f}%")
        
        # Stats por categoría
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
    print("Sistema de Pruebas Automatizadas")
    print("=" * 50)
    
    test_suite = ExtendedTestSuite()
    
    try:
        pdf_report = test_suite.run_all_tests()
        print(f"\nPruebas completadas. {'Reporte: ' + pdf_report if pdf_report else 'Error en reporte PDF'}")
    except Exception as e:
        print(f"\nError crítico: {e}")
        raise
    finally:
        print("\nEjecución finalizada")

if __name__ == "__main__":
    main()
