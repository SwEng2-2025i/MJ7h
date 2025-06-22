import requests
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

class BackendIntegrationTest:
    def __init__(self):
        self.created_users = []
        self.created_tasks = []
        self.test_results = {}
        self.ensure_reports_directory()
    
    def ensure_reports_directory(self):
        """Asegura que el directorio de reportes existe"""
        if not os.path.exists("reports"):
            os.makedirs("reports")
    
    def get_next_report_number(self):
        """Obtiene el siguiente número de reporte basado en los archivos existentes"""
        existing_reports = [f for f in os.listdir("reports") if f.endswith('.pdf')]
        if not existing_reports:
            return 1
        
        numbers = []
        for report in existing_reports:
            try:
                number = int(report.split('_')[1].split('.')[0])
                numbers.append(number)
            except (IndexError, ValueError):
                continue
        
        return max(numbers) + 1 if numbers else 1
    
    def generate_pdf_report(self, test_results, test_type="Backend Integration"):
        """Genera un reporte PDF con los resultados de las pruebas"""
        report_number = self.get_next_report_number()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_{report_number:03d}_{timestamp}.pdf"
        filepath = os.path.join("reports", filename)
        
        # Crear el documento PDF
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Título del reporte
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1
        )
        title = Paragraph(f"Reporte de Pruebas {test_type} - #{report_number:03d}", title_style)
        story.append(title)
        
        # Información del reporte
        info_data = [
            ["Fecha de ejecución:", datetime.now().strftime("%d/%m/%Y %H:%M:%S")],
            ["Tipo de prueba:", test_type],
            ["Número de reporte:", f"#{report_number:03d}"],
            ["Archivo:", filename]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Resultados de las pruebas
        results_title = Paragraph("Resultados de las Pruebas", styles['Heading2'])
        story.append(results_title)
        story.append(Spacer(1, 12))
        
        # Tabla de resultados
        if test_results:
            results_data = [["Prueba", "Estado", "Detalles"]]
            for test_name, result in test_results.items():
                status = "✅ PASÓ" if result.get('success', False) else "❌ FALLÓ"
                details = result.get('details', '')
                results_data.append([test_name, status, details])
            
            results_table = Table(results_data, colWidths=[2*inch, 1*inch, 3*inch])
            results_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(results_table)
        
        story.append(Spacer(1, 20))
        
        # Resumen
        summary_title = Paragraph("Resumen", styles['Heading2'])
        story.append(summary_title)
        story.append(Spacer(1, 12))
        
        if test_results:
            total_tests = len(test_results)
            passed_tests = sum(1 for result in test_results.values() if result.get('success', False))
            failed_tests = total_tests - passed_tests
            
            summary_data = [
                ["Total de pruebas:", str(total_tests)],
                ["Pruebas exitosas:", str(passed_tests)],
                ["Pruebas fallidas:", str(failed_tests)],
                ["Tasa de éxito:", f"{(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "0%"]
            ]
            
            summary_table = Table(summary_data, colWidths=[2*inch, 1*inch])
            summary_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(summary_table)
        
        # Construir el PDF
        doc.build(story)
        print(f"✅ Reporte PDF generado: {filepath}")
        return filepath
    
    def track_user_creation(self, user_id):
        """Registra un usuario creado durante las pruebas"""
        self.created_users.append(user_id)
        print(f"📝 Usuario registrado para limpieza: ID {user_id}")
    
    def track_task_creation(self, task_id):
        """Registra una tarea creada durante las pruebas"""
        self.created_tasks.append(task_id)
        print(f"📝 Tarea registrada para limpieza: ID {task_id}")
    
    def cleanup_test_data(self):
        """Limpia todos los datos creados durante las pruebas"""
        print("\n🧹 Iniciando limpieza de datos de prueba...")
        
        # Limpiar tareas primero (por las restricciones de clave foránea)
        for task_id in self.created_tasks:
            try:
                response = requests.delete(f"{TASKS_URL}/{task_id}")
                if response.status_code == 200:
                    print(f"✅ Tarea eliminada: ID {task_id}")
                else:
                    print(f"⚠️ No se pudo eliminar tarea ID {task_id}: {response.status_code}")
            except Exception as e:
                print(f"❌ Error eliminando tarea ID {task_id}: {str(e)}")
        
        # Limpiar usuarios
        for user_id in self.created_users:
            try:
                response = requests.delete(f"{USERS_URL}/{user_id}")
                if response.status_code == 200:
                    print(f"✅ Usuario eliminado: ID {user_id}")
                else:
                    print(f"⚠️ No se pudo eliminar usuario ID {user_id}: {response.status_code}")
            except Exception as e:
                print(f"❌ Error eliminando usuario ID {user_id}: {str(e)}")
        
        # Verificar que la limpieza fue exitosa
        self.verify_cleanup()
        
        # Limpiar las listas de seguimiento
        self.created_users.clear()
        self.created_tasks.clear()
        print("✅ Limpieza de datos completada\n")
    
    def verify_cleanup(self):
        """Verifica que los datos de prueba han sido eliminados correctamente"""
        print("🔍 Verificando limpieza de datos...")
        
        # Verificar que los usuarios no existen
        for user_id in self.created_users:
            try:
                response = requests.get(f"{USERS_URL}/{user_id}")
                if response.status_code == 404:
                    print(f"✅ Usuario ID {user_id} eliminado correctamente")
                else:
                    print(f"❌ Usuario ID {user_id} aún existe")
            except Exception as e:
                print(f"⚠️ Error verificando usuario ID {user_id}: {str(e)}")
        
        # Verificar que las tareas no existen
        for task_id in self.created_tasks:
            try:
                response = requests.get(f"{TASKS_URL}/{task_id}")
                if response.status_code == 404:
                    print(f"✅ Tarea ID {task_id} eliminada correctamente")
                else:
                    print(f"❌ Tarea ID {task_id} aún existe")
            except Exception as e:
                print(f"⚠️ Error verificando tarea ID {task_id}: {str(e)}")
        
        print("✅ Verificación de limpieza completada")
    
    def create_user(self, name):
        response = requests.post(USERS_URL, json={"name": name})
        response.raise_for_status()
        user_data = response.json()
        print("✅ User created:", user_data)
        
        # Registrar para limpieza
        self.track_user_creation(user_data["id"])
        return user_data["id"]

    def create_task(self, user_id, description):
        response = requests.post(TASKS_URL, json={
            "title": description,
            "user_id": user_id
        })
        response.raise_for_status()
        task_data = response.json()
        print("✅ Task created:", task_data)
        
        # Registrar para limpieza
        self.track_task_creation(task_data["id"])
        return task_data["id"]

    def get_tasks(self):
        response = requests.get(TASKS_URL)
        response.raise_for_status()
        tasks = response.json()
        return tasks

    def test_user_creation(self):
        """Prueba la creación de usuarios"""
        try:
            user_id = self.create_user("TestUser_Backend")
            self.test_results["Creación de Usuario"] = {
                "success": True,
                "details": f"Usuario creado con ID {user_id}"
            }
            return user_id
        except Exception as e:
            self.test_results["Creación de Usuario"] = {
                "success": False,
                "details": f"Error: {str(e)}"
            }
            raise

    def test_task_creation(self, user_id):
        """Prueba la creación de tareas"""
        try:
            task_id = self.create_task(user_id, "TestTask_Backend")
            self.test_results["Creación de Tarea"] = {
                "success": True,
                "details": f"Tarea creada con ID {task_id} para usuario {user_id}"
            }
            return task_id
        except Exception as e:
            self.test_results["Creación de Tarea"] = {
                "success": False,
                "details": f"Error: {str(e)}"
            }
            raise

    def test_task_verification(self, user_id, task_id):
        """Prueba que la tarea se registró correctamente y está asociada al usuario"""
        try:
            tasks = self.get_tasks()
            user_tasks = [t for t in tasks if t["user_id"] == user_id]
            
            task_found = any(t["id"] == task_id for t in user_tasks)
            if task_found:
                self.test_results["Verificación de Tarea"] = {
                    "success": True,
                    "details": f"Tarea {task_id} encontrada y asociada al usuario {user_id}"
                }
            else:
                self.test_results["Verificación de Tarea"] = {
                    "success": False,
                    "details": f"Tarea {task_id} no encontrada para el usuario {user_id}"
                }
                raise AssertionError("La tarea no fue correctamente registrada")
        except Exception as e:
            self.test_results["Verificación de Tarea"] = {
                "success": False,
                "details": f"Error: {str(e)}"
            }
            raise

    def run_integration_test(self):
        """Ejecuta la prueba de integración completa"""
        print("🚀 Iniciando pruebas de integración de Backend...")
        
        try:
            # Step 1: Create user
            user_id = self.test_user_creation()

            # Step 2: Create task for that user
            task_id = self.test_task_creation(user_id)

            # Step 3: Verify that the task is registered and associated with the user
            self.test_task_verification(user_id, task_id)

            print("✅ Todas las pruebas de backend completadas exitosamente")
            
        except Exception as e:
            print(f"❌ Error en las pruebas de backend: {str(e)}")
        
        finally:
            # Limpiar datos de prueba
            self.cleanup_test_data()
            
            # Generar reporte PDF
            pdf_path = self.generate_pdf_report(self.test_results, "Backend Integration")
            print(f"📄 Reporte PDF generado: {pdf_path}")

def integration_test():
    """Función principal para ejecutar las pruebas"""
    test_runner = BackendIntegrationTest()
    test_runner.run_integration_test()

if __name__ == "__main__":
    integration_test()