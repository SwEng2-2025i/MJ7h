import os
import json
import time
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import requests

class TestReportGenerator:
    """Generador de reportes PDF para pruebas de integración"""
    
    def __init__(self, test_name):
        self.test_name = test_name
        self.test_results = []
        self.start_time = datetime.now()
        self.created_data = {
            'users': [],
            'tasks': []
        }
        
    def add_test_result(self, test_case, status, details="", execution_time=0):
        """Agrega un resultado de prueba al reporte"""
        self.test_results.append({
            'test_case': test_case,
            'status': status,
            'details': details,
            'execution_time': execution_time,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
    def track_created_user(self, user_id):
        """Registra un usuario creado durante las pruebas"""
        self.created_data['users'].append(user_id)
        
    def track_created_task(self, task_id):
        """Registra una tarea creada durante las pruebas"""
        self.created_data['tasks'].append(task_id)
        
    def cleanup_test_data(self):
        """Limpia todos los datos creados durante las pruebas"""
        cleanup_results = []
        
        # Limpiar tareas
        for task_id in self.created_data['tasks']:
            try:
                response = requests.delete(f"http://localhost:5002/tasks/{task_id}")
                if response.status_code == 200:
                    cleanup_results.append(f"✅ Tarea {task_id} eliminada correctamente")
                else:
                    cleanup_results.append(f"❌ Error eliminando tarea {task_id}: {response.text}")
            except Exception as e:
                cleanup_results.append(f"❌ Error eliminando tarea {task_id}: {str(e)}")
                
        # Limpiar usuarios
        for user_id in self.created_data['users']:
            try:
                response = requests.delete(f"http://localhost:5001/users/{user_id}")
                if response.status_code == 200:
                    cleanup_results.append(f"✅ Usuario {user_id} eliminado correctamente")
                else:
                    cleanup_results.append(f"❌ Error eliminando usuario {user_id}: {response.text}")
            except Exception as e:
                cleanup_results.append(f"❌ Error eliminando usuario {user_id}: {str(e)}")
                
        return cleanup_results
        
    def verify_data_cleanup(self):
        """Verifica que los datos hayan sido eliminados correctamente"""
        verification_results = []
        
        # Verificar que las tareas fueron eliminadas
        for task_id in self.created_data['tasks']:
            try:
                response = requests.get(f"http://localhost:5002/tasks")
                if response.status_code == 200:
                    tasks = response.json()
                    if not any(task['id'] == task_id for task in tasks):
                        verification_results.append(f"✅ Verificado: Tarea {task_id} no existe en el sistema")
                    else:
                        verification_results.append(f"❌ Error: Tarea {task_id} aún existe en el sistema")
                else:
                    verification_results.append(f"❌ Error verificando tarea {task_id}: {response.text}")
            except Exception as e:
                verification_results.append(f"❌ Error verificando tarea {task_id}: {str(e)}")
                
        # Verificar que los usuarios fueron eliminados
        for user_id in self.created_data['users']:
            try:
                response = requests.get(f"http://localhost:5001/users/{user_id}")
                if response.status_code == 404:
                    verification_results.append(f"✅ Verificado: Usuario {user_id} no existe en el sistema")
                else:
                    verification_results.append(f"❌ Error: Usuario {user_id} aún existe en el sistema")
            except Exception as e:
                verification_results.append(f"❌ Error verificando usuario {user_id}: {str(e)}")
                
        return verification_results
        
    def get_next_report_number(self):
        """Obtiene el siguiente número secuencial para el reporte"""
        reports_dir = "Test/reports"
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
            
        existing_reports = [f for f in os.listdir(reports_dir) if f.startswith("test_report_") and f.endswith(".pdf")]
        if not existing_reports:
            return 1
            
        numbers = []
        for report in existing_reports:
            try:
                num = int(report.replace("test_report_", "").replace(".pdf", ""))
                numbers.append(num)
            except ValueError:
                continue
                
        return max(numbers) + 1 if numbers else 1
        
    def generate_pdf_report(self, cleanup_results=None, verification_results=None):
        """Genera el reporte PDF con los resultados de las pruebas"""
        report_number = self.get_next_report_number()
        filename = f"Test/reports/test_report_{report_number:03d}.pdf"
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Centrado
        )
        story.append(Paragraph(f"Reporte de Pruebas de Integración #{report_number:03d}", title_style))
        story.append(Spacer(1, 12))
        
        # Información general
        info_data = [
            ['Nombre de la Prueba:', self.test_name],
            ['Fecha de Ejecución:', self.start_time.strftime("%Y-%m-%d %H:%M:%S")],
            ['Duración Total:', str(datetime.now() - self.start_time)],
            ['Total de Casos de Prueba:', str(len(self.test_results))]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Resultados de las pruebas
        story.append(Paragraph("Resultados de las Pruebas", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        if self.test_results:
            test_data = [['Caso de Prueba', 'Estado', 'Tiempo (s)', 'Detalles']]
            for result in self.test_results:
                status_symbol = "✅" if result['status'] == 'PASS' else "❌"
                test_data.append([
                    result['test_case'],
                    f"{status_symbol} {result['status']}",
                    f"{result['execution_time']:.2f}",
                    result['details'][:50] + "..." if len(result['details']) > 50 else result['details']
                ])
                
            test_table = Table(test_data, colWidths=[2*inch, 1*inch, 0.8*inch, 2.2*inch])
            test_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(test_table)
            story.append(Spacer(1, 20))
        
        # Datos creados durante las pruebas
        if self.created_data['users'] or self.created_data['tasks']:
            story.append(Paragraph("Datos Creados Durante las Pruebas", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            created_data = [['Tipo', 'IDs Creados']]
            if self.created_data['users']:
                created_data.append(['Usuarios', ', '.join(map(str, self.created_data['users']))])
            if self.created_data['tasks']:
                created_data.append(['Tareas', ', '.join(map(str, self.created_data['tasks']))])
                
            created_table = Table(created_data, colWidths=[1.5*inch, 4.5*inch])
            created_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(created_table)
            story.append(Spacer(1, 20))
        
        # Resultados de limpieza
        if cleanup_results:
            story.append(Paragraph("Resultados de Limpieza de Datos", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            for result in cleanup_results:
                story.append(Paragraph(result, styles['Normal']))
                story.append(Spacer(1, 6))
                
            story.append(Spacer(1, 12))
        
        # Resultados de verificación
        if verification_results:
            story.append(Paragraph("Verificación de Limpieza", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            for result in verification_results:
                story.append(Paragraph(result, styles['Normal']))
                story.append(Spacer(1, 6))
        
        # Construir PDF
        doc.build(story)
        
        print(f"📄 Reporte PDF generado: {filename}")
        return filename 