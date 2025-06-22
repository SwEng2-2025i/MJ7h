import requests
import os
import io
import sys
import traceback
from datetime import datetime
from dataclasses import dataclass
from typing import List
from t_back import PDFReportGenerator, ReportData, TestResult

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"


class TestLogger:
    """Clase para capturar y registrar resultados de pruebas"""
    
    def __init__(self):
        self.test_results = []
        self.logs = []
        self.current_test = None
        self.start_time = None
    
    def start_test(self, test_name: str):
        """Iniciar un nuevo test"""
        self.current_test = test_name
        self.start_time = datetime.now()
        self.log(f"🚀 Iniciando: {test_name}")
    
    def end_test(self, status: str, message: str = "", details: str = ""):
        """Finalizar el test actual"""
        if self.current_test and self.start_time:
            duration = (datetime.now() - self.start_time).total_seconds()
            result = TestResult(
                name=self.current_test,
                status=status,
                duration=duration,
                message=message,
                details=details
            )
            self.test_results.append(result)
            
            status_icon = "✅" if status == "PASSED" else "❌" if status == "FAILED" else "⏭️"
            self.log(f"{status_icon} {self.current_test}: {status} ({duration:.2f}s)")
            if message:
                self.log(f"   📝 {message}")
        
        self.current_test = None
        self.start_time = None
    
    def log(self, message: str):
        """Registrar un mensaje"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        print(log_entry)  # También imprimir en consola
    
    def log_error(self, error: Exception):
        """Registrar un error con detalles completos"""
        error_details = traceback.format_exc()
        self.log(f"❌ Error: {str(error)}")
        return error_details


# Instancia global del logger
test_logger = TestLogger()


def create_user(name):
    """Crear un usuario y registrar el resultado"""
    test_logger.start_test("Crear Usuario")
    try:
        response = requests.post(USERS_URL, json={"name": name})
        response.raise_for_status()
        user_data = response.json()
        test_logger.log(f"✅ Usuario creado: {user_data}")
        test_logger.end_test("PASSED", f"Usuario '{name}' creado con ID {user_data['id']}")
        return user_data["id"]
    except Exception as e:
        error_details = test_logger.log_error(e)
        test_logger.end_test("FAILED", f"Error al crear usuario: {str(e)}", error_details)
        raise


def create_task(user_id, description):
    """Crear una tarea y registrar el resultado"""
    test_logger.start_test("Crear Tarea")
    try:
        response = requests.post(TASKS_URL, json={
            "title": description,
            "user_id": user_id
        })
        response.raise_for_status()
        task_data = response.json()
        test_logger.log(f"✅ Tarea creada: {task_data}")
        test_logger.end_test("PASSED", f"Tarea '{description}' creada con ID {task_data['id']}")
        return task_data["id"]
    except Exception as e:
        error_details = test_logger.log_error(e)
        test_logger.end_test("FAILED", f"Error al crear tarea: {str(e)}", error_details)
        raise


def get_tasks():
    """Obtener todas las tareas"""
    test_logger.start_test("Obtener Tareas")
    try:
        response = requests.get(TASKS_URL)
        response.raise_for_status()
        tasks = response.json()
        test_logger.log(f"📋 Tareas obtenidas: {len(tasks)} tareas encontradas")
        test_logger.end_test("PASSED", f"Obtenidas {len(tasks)} tareas exitosamente")
        return tasks
    except Exception as e:
        error_details = test_logger.log_error(e)
        test_logger.end_test("FAILED", f"Error al obtener tareas: {str(e)}", error_details)
        raise


def delete_user(user_id):
    """Eliminar un usuario y registrar el resultado"""
    test_logger.start_test("Eliminar Usuario")
    try:
        response = requests.delete(f"{USERS_URL}/{user_id}")
        if response.status_code != 200:
            error_msg = f"Error al eliminar usuario: {response.text}"
            test_logger.end_test("FAILED", error_msg)
            test_logger.log(f"❌ {error_msg}")
        else:
            test_logger.log(f"🧹 Usuario {user_id} eliminado")
            test_logger.end_test("PASSED", f"Usuario {user_id} eliminado correctamente")
    except Exception as e:
        error_details = test_logger.log_error(e)
        test_logger.end_test("FAILED", f"Excepción al eliminar usuario: {str(e)}", error_details)


def delete_task(task_id):
    """Eliminar una tarea y registrar el resultado"""
    test_logger.start_test("Eliminar Tarea")
    try:
        response = requests.delete(f"{TASKS_URL}/{task_id}")
        if response.status_code != 200:
            error_msg = f"Error al eliminar tarea: {response.text}"
            test_logger.end_test("FAILED", error_msg)
            test_logger.log(f"❌ {error_msg}")
        else:
            test_logger.log(f"🧹 Tarea {task_id} eliminada")
            test_logger.end_test("PASSED", f"Tarea {task_id} eliminada correctamente")
    except Exception as e:
        error_details = test_logger.log_error(e)
        test_logger.end_test("FAILED", f"Excepción al eliminar tarea: {str(e)}", error_details)


def verify_deletion(user_id, task_id):
    """Verificar que los elementos fueron eliminados correctamente"""
    test_logger.start_test("Verificar Eliminación de Usuario")
    try:
        user_response = requests.get(f"{USERS_URL}/{user_id}")
        if user_response.status_code == 404:
            test_logger.end_test("PASSED", "Usuario eliminado correctamente - 404 recibido")
        else:
            test_logger.end_test("FAILED", f"Usuario aún existe - Status: {user_response.status_code}")
            return
    except Exception as e:
        error_details = test_logger.log_error(e)
        test_logger.end_test("FAILED", f"Error verificando eliminación de usuario: {str(e)}", error_details)
        return
    
    test_logger.start_test("Verificar Eliminación de Tarea")
    try:
        tasks = get_tasks()
        task_exists = any(t["id"] == task_id for t in tasks)
        if not task_exists:
            test_logger.end_test("PASSED", "Tarea eliminada correctamente - No encontrada en lista")
        else:
            test_logger.end_test("FAILED", "Tarea aún existe en la lista")
    except Exception as e:
        error_details = test_logger.log_error(e)
        test_logger.end_test("FAILED", f"Error verificando eliminación de tarea: {str(e)}", error_details)


def verify_task_creation(user_id, task_id):
    """Verificar que la tarea fue creada correctamente"""
    test_logger.start_test("Verificar Creación de Tarea")
    try:
        tasks = get_tasks()
        task_found = any(t["id"] == task_id and t["user_id"] == user_id for t in tasks)
        if task_found:
            test_logger.end_test("PASSED", "Tarea registrada correctamente en el sistema")
        else:
            test_logger.end_test("FAILED", "Tarea no encontrada en el sistema")
    except Exception as e:
        error_details = test_logger.log_error(e)
        test_logger.end_test("FAILED", f"Error verificando creación de tarea: {str(e)}", error_details)


def integration_test():
    """Ejecutar el test de integración completo"""
    test_logger.log("🧪 Iniciando Test de Integración Completo")
    test_logger.log("=" * 50)
    
    user_id = None
    task_id = None
    
    try:
        # Fase 1: Creación de datos
        test_logger.log("📝 Fase 1: Creación de datos")
        user_id = create_user("Camilo")
        task_id = create_task(user_id, "Prepare presentation")
        
        # Fase 2: Verificación de creación
        test_logger.log("🔍 Fase 2: Verificación de creación")
        verify_task_creation(user_id, task_id)
        
        # Fase 3: Eliminación de datos
        test_logger.log("🧹 Fase 3: Eliminación de datos")
        delete_task(task_id)
        delete_user(user_id)
        
        # Fase 4: Verificación de eliminación
        test_logger.log("✅ Fase 4: Verificación de eliminación")
        verify_deletion(user_id, task_id)
        
        test_logger.log("🎉 Test de integración completado")
        
    except Exception as e:
        test_logger.log(f"💥 Test de integración falló: {str(e)}")
        test_logger.log("🔧 Intentando limpiar recursos...")
        
        # Intentar limpiar recursos en caso de error
        if task_id:
            try:
                delete_task(task_id)
            except:
                pass
        
        if user_id:
            try:
                delete_user(user_id)
            except:
                pass


def generate_comprehensive_report():
    """Generar un reporte comprehensivo con todos los datos capturados"""
    
    # Crear datos del reporte
    report_data = ReportData(
        title="Reporte de Test de Integración - API Users/Tasks",
        project_name="Backend test",
        version="1.0.0",
        environment="Local Development",
        test_results=test_logger.test_results,
        execution_time=datetime.now()
    )
    
    # Generar reporte usando la clase avanzada
    generator = PDFReportGenerator()
    filename = generator.generate_report(report_data)
    
    # También generar un archivo de log
    log_filename = filename.replace('.pdf', '_logs.txt')
    with open(log_filename, 'w', encoding='utf-8') as f:
        f.write("LOGS DETALLADOS DEL TEST DE INTEGRACIÓN\n")
        f.write("=" * 50 + "\n\n")
        for log_entry in test_logger.logs:
            f.write(log_entry + "\n")
    
    print(f"📊 Reporte PDF generado: {filename}")
    print(f"📄 Logs detallados: {log_filename}")
    
    return filename


if __name__ == "__main__":
    print("🚀 Iniciando Test de Integración con Reporte Avanzado")
    print("=" * 60)
    
    try:
        # Ejecutar tests
        integration_test()
        
        # Generar reporte
        print("\n" + "=" * 60)
        print("📊 Generando reporte...")
        generate_comprehensive_report()
        
        # Mostrar resumen
        print("\n📈 RESUMEN DE EJECUCIÓN:")
        total_tests = len(test_logger.test_results)
        passed = sum(1 for test in test_logger.test_results if test.status == 'PASSED')
        failed = sum(1 for test in test_logger.test_results if test.status == 'FAILED')
        
        print(f"   Total de pruebas: {total_tests}")
        print(f"   ✅ Exitosas: {passed}")
        print(f"   ❌ Fallidas: {failed}")
        print(f"   📊 Tasa de éxito: {(passed/total_tests*100):.1f}%" if total_tests > 0 else "   📊 No hay datos")
        
    except Exception as e:
        print(f"💥 Error crítico en la ejecución: {e}")
        print("🔧 Generando reporte de error...")
        
        # Agregar el error crítico como un test fallido
        test_logger.start_test("Ejecución General del Test")
        test_logger.end_test("FAILED", f"Error crítico: {str(e)}", traceback.format_exc())
        
        # Generar reporte incluso con error
        generate_comprehensive_report()
    
    print("\n🏁 Proceso completado")