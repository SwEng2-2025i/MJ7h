import os
import sys
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

#Captura de los logs para incluirlos en el reporte
class TestLogger:
    """Captura logs de las pruebas para incluir en el reporte"""
    def __init__(self):
        self.logs = []
        self.original_stdout = sys.stdout
        
    def start_capture(self):
        sys.stdout = self
        
    def stop_capture(self):
        sys.stdout = self.original_stdout
        
    def write(self, text):
        self.logs.append(text)
        self.original_stdout.write(text)
        
    def flush(self):
        pass

class ReportGenerator:
    
    def __init__(self, test_type="Generic"):
        self.test_type = test_type
        self.start_time = datetime.now()
        
    def get_next_report_number(self, prefix="Reporte"):
        """Obtiene el siguiente número de reporte secuencial"""
        counter = 1
        while os.path.exists(f"{prefix}_{counter}.pdf"):
            counter += 1
        return counter
    
    def generate_consolidated_report(self, backend_logs, frontend_logs, 
                                   backend_status, frontend_status, 
                                   filename=None):
        
        if filename is None:
            report_number = self.get_next_report_number("Reporte_Consolidado")
            filename = f"Reporte_Consolidado_{report_number}.pdf"
            
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Título principal
        title_style = ParagraphStyle(
            'ConsolidatedTitle',
            parent=styles['Heading1'],
            fontSize=20,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=1
        )
        story.append(Paragraph("Reporte Consolidado de Pruebas", title_style))
        story.append(Spacer(1, 20))
        
        summary_data = [
            ['Fecha:', self.start_time.strftime("%Y-%m-%d %H:%M:%S")],
            ['Backend Status:', backend_status],
            ['Frontend Status:', frontend_status],
            ['Estado General:', self._get_overall_status(backend_status, frontend_status)]
        ]
        
        summary_table = Table(summary_data, colWidths=[120, 300])
        summary_table.setStyle(self._get_summary_table_style())
        
        story.append(Paragraph("Resumen Completo", styles['Heading2']))
        story.append(Spacer(1, 10))
        story.append(summary_table)
        story.append(Spacer(1, 30))
        
        # Sección Backend
        story.append(Paragraph("Pruebas Backend (Integración)", styles['Heading2']))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"Estado: {backend_status}", styles['Normal']))
        story.append(Spacer(1, 10))
        
        if backend_logs:
            for log_entry in backend_logs:
                if log_entry.strip():
                    story.append(Paragraph(log_entry.strip(), styles['Normal']))
                    story.append(Spacer(1, 4))
        
        story.append(Spacer(1, 20))
        
        # Sección Frontend
        story.append(Paragraph("Pruebas Frontend (End-to-End)", styles['Heading2']))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"Estado: {frontend_status}", styles['Normal']))
        story.append(Spacer(1, 10))
        
        if frontend_logs:
            for log_entry in frontend_logs:
                if log_entry.strip():
                    story.append(Paragraph(log_entry.strip(), styles['Normal']))
                    story.append(Spacer(1, 4))
        
        doc.build(story)
        print(f"Reporte consolidado generado: {filename}")
        return filename
    
    def generate_single_report(self, logs, test_status, test_type, filename=None):
        """Reporte individual"""

        if filename is None:
            report_number = self.get_next_report_number(f"Reporte_{test_type}")
            filename = f"Reporte_{test_type}_{report_number}.pdf"
            
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=1
        )
        story.append(Paragraph(f"Reporte de Pruebas {test_type}", title_style))
        story.append(Spacer(1, 20))
        
        # Información base
        info_data = [
            ['Fecha:', self.start_time.strftime("%Y-%m-%d %H:%M:%S")],
            ['Estado:', test_status],
            ['Tipo de Prueba:', test_type]
        ]
        
        info_table = Table(info_data, colWidths=[100, 300])
        info_table.setStyle(self._get_info_table_style())
        
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Logs de la prueba
        story.append(Paragraph("Logs de Ejecución:", styles['Heading2']))
        story.append(Spacer(1, 10))
        
        if logs:
            for log_entry in logs:
                if log_entry.strip():
                    story.append(Paragraph(log_entry.strip(), styles['Normal']))
                    story.append(Spacer(1, 6))
        
        doc.build(story)
        print(f"Reporte {test_type} generado: {filename}")
        return filename
    
    def _get_overall_status(self, backend_status, frontend_status):

        if "PASSED" in backend_status and "PASSED" in frontend_status:
            return "TODAS LAS PRUEBAS PASARON"
        elif "FAILED" in backend_status and "FAILED" in frontend_status:
            return "TODAS LAS PRUEBAS FALLARON"
        else:
            return "PRUEBAS MIXTAS - RESULTADOS COMBINADOS"
    
    def _get_summary_table_style(self):  # Config del pdf 
        """Estilo para la tabla de resumen"""
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
    
    def _get_info_table_style(self):
        """Estilo para la tabla de información"""
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

def create_logger():
    """Crea un logger para capturar logs de pruebas"""
    return TestLogger()

def generate_report(logs, test_status, test_type="Generic", filename=None):
    """Función para generar un reporte individual"""
    generator = ReportGenerator(test_type)
    return generator.generate_single_report(logs, test_status, test_type, filename)

def generate_consolidated_report(backend_logs, frontend_logs, 
                               backend_status, frontend_status, filename=None):
    """Función para generar un reporte consolidado"""
    generator = ReportGenerator()
    return generator.generate_consolidated_report(
        backend_logs, frontend_logs, backend_status, frontend_status, filename
    )
