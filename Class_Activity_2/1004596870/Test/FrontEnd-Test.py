import time
import requests
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

class FrontendIntegrationTest:
    def __init__(self):
        self.created_users = []
        self.created_tasks = []
        self.test_results = {}
        self.created_user_id = None
        self.created_task_id = None
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
    
    def generate_pdf_report(self, test_results, test_type="Frontend Integration"):
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
                response = requests.delete(f"http://localhost:5002/tasks/{task_id}")
                if response.status_code == 200:
                    print(f"✅ Tarea eliminada: ID {task_id}")
                else:
                    print(f"⚠️ No se pudo eliminar tarea ID {task_id}: {response.status_code}")
            except Exception as e:
                print(f"❌ Error eliminando tarea ID {task_id}: {str(e)}")
        
        # Limpiar usuarios
        for user_id in self.created_users:
            try:
                response = requests.delete(f"http://localhost:5001/users/{user_id}")
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
                response = requests.get(f"http://localhost:5001/users/{user_id}")
                if response.status_code == 404:
                    print(f"✅ Usuario ID {user_id} eliminado correctamente")
                else:
                    print(f"❌ Usuario ID {user_id} aún existe")
            except Exception as e:
                print(f"⚠️ Error verificando usuario ID {user_id}: {str(e)}")
        
        # Verificar que las tareas no existen
        for task_id in self.created_tasks:
            try:
                response = requests.get(f"http://localhost:5002/tasks/{task_id}")
                if response.status_code == 404:
                    print(f"✅ Tarea ID {task_id} eliminada correctamente")
                else:
                    print(f"❌ Tarea ID {task_id} aún existe")
            except Exception as e:
                print(f"⚠️ Error verificando tarea ID {task_id}: {str(e)}")
        
        print("✅ Verificación de limpieza completada")
    
    def setup_driver(self):
        """Configura el driver de Edge con webdriver-manager"""
        from selenium.webdriver.edge.options import Options as EdgeOptions
        from selenium.webdriver.edge.service import Service as EdgeService
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        options = EdgeOptions()
        # options.add_argument('--headless')  # Comentado para mostrar la ventana
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
        return driver

    def abrir_frontend(self, driver):
        """Abre la aplicación frontend en el navegador"""
        try:
            driver.get("http://localhost:5000")
            time.sleep(2)  # Dar tiempo a que la página cargue
            self.test_results["Apertura del Frontend"] = {
                "success": True,
                "details": "Frontend cargado correctamente en http://localhost:5000"
            }
        except Exception as e:
            self.test_results["Apertura del Frontend"] = {
                "success": False,
                "details": f"Error: {str(e)}"
            }
            raise

    def crear_usuario(self, driver, wait):
        """Llena el formulario de creación de usuario y lo envía"""
        try:
            username_input = driver.find_element(By.ID, "username")
            username_input.send_keys("TestUser_Frontend")
            time.sleep(1)
            
            driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
            time.sleep(2)

            user_result = driver.find_element(By.ID, "user-result").text
            print("Resultado usuario:", user_result)
            
            if "Usuario creado con ID" in user_result:
                user_id = ''.join(filter(str.isdigit, user_result))
                self.created_user_id = int(user_id)
                
                # Registrar para limpieza
                self.track_user_creation(self.created_user_id)
                
                self.test_results["Creación de Usuario (Frontend)"] = {
                    "success": True,
                    "details": f"Usuario creado con ID {user_id}"
                }
                return user_id
            else:
                raise AssertionError(f"Error en creación de usuario: {user_result}")
                
        except Exception as e:
            self.test_results["Creación de Usuario (Frontend)"] = {
                "success": False,
                "details": f"Error: {str(e)}"
            }
            raise

    def crear_tarea(self, driver, wait, user_id):
        """Llena el formulario de creación de tarea y lo envía"""
        try:
            task_input = driver.find_element(By.ID, "task")
            task_input.send_keys("TestTask_Frontend")
            time.sleep(1)

            userid_input = driver.find_element(By.ID, "userid")
            userid_input.send_keys(user_id)
            userid_input.send_keys('\t')  # Forzar focus out del input
            time.sleep(1)

            crear_tarea_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']"))
            )
            crear_tarea_btn.click()
            time.sleep(2)

            wait.until(
                EC.text_to_be_present_in_element((By.ID, "task-result"), "Tarea creada con ID")
            )
            task_result = driver.find_element(By.ID, "task-result")
            print("Texto en task_result:", task_result.text)
            
            if "Tarea creada con ID" in task_result.text:
                task_id = ''.join(filter(str.isdigit, task_result.text))
                self.created_task_id = int(task_id)
                
                # Registrar para limpieza
                self.track_task_creation(self.created_task_id)
                
                self.test_results["Creación de Tarea (Frontend)"] = {
                    "success": True,
                    "details": f"Tarea creada con ID {task_id} para usuario {user_id}"
                }
            else:
                raise AssertionError(f"Error en creación de tarea: {task_result.text}")
                
        except Exception as e:
            self.test_results["Creación de Tarea (Frontend)"] = {
                "success": False,
                "details": f"Error: {str(e)}"
            }
            raise

    def ver_tareas(self, driver):
        """Hace clic en el botón para actualizar la lista de tareas y verifica que aparezca la nueva tarea"""
        try:
            driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
            time.sleep(2)

            tasks = driver.find_element(By.ID, "tasks").text
            print("Tareas:", tasks)
            
            if "TestTask_Frontend" in tasks:
                self.test_results["Verificación de Lista de Tareas"] = {
                    "success": True,
                    "details": "Tarea encontrada en la lista de tareas del frontend"
                }
            else:
                raise AssertionError("La tarea no aparece en la lista")
                
        except Exception as e:
            self.test_results["Verificación de Lista de Tareas"] = {
                "success": False,
                "details": f"Error: {str(e)}"
            }
            raise

    def run_integration_test(self):
        """Ejecuta la prueba de integración completa del frontend"""
        print("🚀 Iniciando pruebas de integración de Frontend...")
        driver = None
        
        try:
            driver = self.setup_driver()
            wait = WebDriverWait(driver, 10)
            
            self.abrir_frontend(driver)
            user_id = self.crear_usuario(driver, wait)
            self.crear_tarea(driver, wait, user_id)
            self.ver_tareas(driver)
            
            time.sleep(3)  # Delay final para observar resultados
            print("✅ Todas las pruebas de frontend completadas exitosamente")
            
        except Exception as e:
            print(f"❌ Error en las pruebas de frontend: {str(e)}")
        
        finally:
            if driver:
                driver.quit()  # Siempre cerrar el navegador al final
            
            # Limpiar datos de prueba
            self.cleanup_test_data()
            
            # Generar reporte PDF
            pdf_path = self.generate_pdf_report(self.test_results, "Frontend Integration")
            print(f"📄 Reporte PDF generado: {pdf_path}")

def main():
    """Función principal para ejecutar las pruebas"""
    test_runner = FrontendIntegrationTest()
    test_runner.run_integration_test()

if __name__ == "__main__":
    main()
