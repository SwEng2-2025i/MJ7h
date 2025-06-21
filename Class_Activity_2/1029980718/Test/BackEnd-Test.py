import requests
import time
from test_utils import TestReportGenerator

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

class BackEndIntegrationTest:
    def __init__(self):
        self.report_generator = TestReportGenerator("BackEnd Integration Test")
        
    def create_user(self, name):
        """Crea un usuario y registra su ID para limpieza posterior"""
        start_time = time.time()
        try:
            response = requests.post(USERS_URL, json={"name": name})
            response.raise_for_status()
            user_data = response.json()
            user_id = user_data["id"]
            
            # Registrar el usuario creado para limpieza posterior
            self.report_generator.track_created_user(user_id)
            
            execution_time = time.time() - start_time
            self.report_generator.add_test_result(
                "Crear Usuario", 
                "PASS", 
                f"Usuario '{name}' creado con ID {user_id}",
                execution_time
            )
            
            print(f"✅ Usuario creado: {user_data}")
            return user_id
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.report_generator.add_test_result(
                "Crear Usuario", 
                "FAIL", 
                f"Error creando usuario: {str(e)}",
                execution_time
            )
            raise e

    def create_task(self, user_id, description):
        """Crea una tarea y registra su ID para limpieza posterior"""
        start_time = time.time()
        try:
            response = requests.post(TASKS_URL, json={
                "title": description,
                "user_id": user_id
            })
            response.raise_for_status()
            task_data = response.json()
            task_id = task_data["id"]
            
            # Registrar la tarea creada para limpieza posterior
            self.report_generator.track_created_task(task_id)
            
            execution_time = time.time() - start_time
            self.report_generator.add_test_result(
                "Crear Tarea", 
                "PASS", 
                f"Tarea '{description}' creada con ID {task_id} para usuario {user_id}",
                execution_time
            )
            
            print(f"✅ Tarea creada: {task_data}")
            return task_id
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.report_generator.add_test_result(
                "Crear Tarea", 
                "FAIL", 
                f"Error creando tarea: {str(e)}",
                execution_time
            )
            raise e

    def get_tasks(self):
        """Obtiene todas las tareas del sistema"""
        start_time = time.time()
        try:
            response = requests.get(TASKS_URL)
            response.raise_for_status()
            tasks = response.json()
            
            execution_time = time.time() - start_time
            self.report_generator.add_test_result(
                "Obtener Tareas", 
                "PASS", 
                f"Se obtuvieron {len(tasks)} tareas del sistema",
                execution_time
            )
            
            return tasks
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.report_generator.add_test_result(
                "Obtener Tareas", 
                "FAIL", 
                f"Error obteniendo tareas: {str(e)}",
                execution_time
            )
            raise e

    def verify_task_association(self, user_id, task_id):
        """Verifica que la tarea esté correctamente asociada al usuario"""
        start_time = time.time()
        try:
            tasks = self.get_tasks()
            user_tasks = [t for t in tasks if t["user_id"] == user_id]
            task_found = any(t["id"] == task_id for t in user_tasks)
            
            execution_time = time.time() - start_time
            
            if task_found:
                self.report_generator.add_test_result(
                    "Verificar Asociación Tarea-Usuario", 
                    "PASS", 
                    f"Tarea {task_id} correctamente asociada al usuario {user_id}",
                    execution_time
                )
                print("✅ Verificación exitosa: tarea correctamente registrada y vinculada al usuario.")
                return True
            else:
                self.report_generator.add_test_result(
                    "Verificar Asociación Tarea-Usuario", 
                    "FAIL", 
                    f"Tarea {task_id} NO encontrada para el usuario {user_id}",
                    execution_time
                )
                print("❌ Error: la tarea no fue correctamente registrada")
                return False
                
        except Exception as e:
            execution_time = time.time() - start_time
            self.report_generator.add_test_result(
                "Verificar Asociación Tarea-Usuario", 
                "FAIL", 
                f"Error verificando asociación: {str(e)}",
                execution_time
            )
            raise e

    def run_integration_test(self):
        """Ejecuta la prueba de integración completa"""
        print("🚀 Iniciando prueba de integración del BackEnd...")
        
        try:
            # Paso 1: Crear usuario
            user_id = self.create_user("Camilo")

            # Paso 2: Crear tarea para ese usuario
            task_id = self.create_task(user_id, "Preparar presentación")

            # Paso 3: Verificar que la tarea está registrada y asociada con el usuario
            verification_success = self.verify_task_association(user_id, task_id)
            
            if not verification_success:
                raise AssertionError("La verificación de asociación tarea-usuario falló")

            print("✅ Prueba de integración completada exitosamente")
            
        except Exception as e:
            print(f"❌ Error en la prueba de integración: {str(e)}")
            raise e
        finally:
            # Paso 4: Limpieza de datos
            print("\n🧹 Iniciando limpieza de datos...")
            cleanup_results = self.report_generator.cleanup_test_data()
            
            for result in cleanup_results:
                print(result)
            
            # Paso 5: Verificar limpieza
            print("\n🔍 Verificando limpieza de datos...")
            verification_results = self.report_generator.verify_data_cleanup()
            
            for result in verification_results:
                print(result)
            
            # Paso 6: Generar reporte PDF
            print("\n📄 Generando reporte PDF...")
            report_file = self.report_generator.generate_pdf_report(
                cleanup_results, 
                verification_results
            )
            
            print(f"✅ Prueba completada. Reporte generado: {report_file}")

def main():
    """Función principal para ejecutar las pruebas"""
    test = BackEndIntegrationTest()
    test.run_integration_test()

if __name__ == "__main__":
    main()