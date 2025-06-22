import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
from reportlab.pdfgen import canvas
import io
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from datetime import datetime

# Importaciones adicionales para reportes avanzados
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


@dataclass
class TestResult:
    """Clase para representar el resultado de una prueba individual"""
    name: str
    status: str  # 'PASSED', 'FAILED', 'SKIPPED'
    duration: float
    message: str = ""
    details: str = ""


@dataclass
class ReportData:
    """Clase para encapsular todos los datos del reporte"""
    title: str = "Reporte de Pruebas Automatizadas"
    project_name: str = "Frontend test"
    version: str = "1.0.0"
    environment: str = "TE:"
    test_results: List[TestResult] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    execution_time: datetime = field(default_factory=datetime.now)


class PDFReportGenerator:
    """Generador avanzado de reportes PDF para pruebas automatizadas"""
    
    def __init__(self, output_dir: str = "TestReports"):
        self.output_dir = output_dir
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Configurar estilos personalizados para el reporte"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkgreen,
            fontName='Helvetica-Bold'
        ))
        
    def _generate_filename(self) -> str:
        """Generar nombre de archivo secuencial"""
        os.makedirs(self.output_dir, exist_ok=True)
        
        existing_files = [
            f for f in os.listdir(self.output_dir) 
            if f.startswith("report_") and f.endswith(".pdf")
        ]
        
        numbers = []
        for filename in existing_files:
            try:
                num_str = filename.split("_")[1].split(".")[0]
                if num_str.isdigit():
                    numbers.append(int(num_str))
            except (IndexError, ValueError):
                continue
        
        new_number = max(numbers, default=0) + 1
        filename = f"report_{new_number:03d}.pdf"
        
        return os.path.join(self.output_dir, filename)
    
    def _create_header_footer_canvas(self, canvas_obj, doc):
        """Crear encabezado y pie de página personalizados"""
        canvas_obj.saveState()
        
        # Encabezado
        canvas_obj.setFont('Helvetica-Bold', 10)
        canvas_obj.setFillColor(colors.darkblue)
        canvas_obj.drawString(2*cm, A4[1] - 1.5*cm, "🧪 Reporte de Pruebas Automatizadas")
        
        # Línea del encabezado
        canvas_obj.setStrokeColor(colors.lightgrey)
        canvas_obj.setLineWidth(0.5)
        canvas_obj.line(2*cm, A4[1] - 1.8*cm, A4[0] - 2*cm, A4[1] - 1.8*cm)
        
        # Pie de página
        canvas_obj.setFont('Helvetica', 8)
        canvas_obj.setFillColor(colors.grey)
        canvas_obj.drawString(2*cm, 1.5*cm, f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        canvas_obj.drawRightString(A4[0] - 2*cm, 1.5*cm, f"Página {doc.page}")
        
        # Línea del pie de página
        canvas_obj.line(2*cm, 1.8*cm, A4[0] - 2*cm, 1.8*cm)
        
        canvas_obj.restoreState()
    
    def _build_summary_section(self, report_data: ReportData) -> List:
        """Construir la sección de resumen"""
        story = []
        
        story.append(Paragraph("📊 Resumen Ejecutivo", self.styles['CustomHeading']))
        
        total_tests = len(report_data.test_results)
        passed = sum(1 for test in report_data.test_results if test.status == 'PASSED')
        failed = sum(1 for test in report_data.test_results if test.status == 'FAILED')
        skipped = sum(1 for test in report_data.test_results if test.status == 'SKIPPED')
        success_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        total_duration = sum(test.duration for test in report_data.test_results)
        
        summary_data = [
            ['Métrica', 'Valor'],
            ['Total de Pruebas', str(total_tests)],
            ['✅ Exitosas', str(passed)],
            ['❌ Fallidas', str(failed)],
            ['⏭️ Omitidas', str(skipped)],
            ['Tasa de Éxito', f"{success_rate:.1f}%"],
            ['Tiempo Total', f"{total_duration:.2f}s"],
            ['Proyecto', report_data.project_name],
            ['Versión', report_data.version],
            ['Entorno', report_data.environment]
        ]
        
        summary_table = Table(summary_data, colWidths=[4*cm, 4*cm])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        return story
    
    def _build_results_section(self, report_data: ReportData) -> List:
        """Construir la sección de resultados detallados"""
        story = []
        
        story.append(Paragraph("🔍 Resultados Detallados", self.styles['CustomHeading']))
        
        if not report_data.test_results:
            story.append(Paragraph("No hay resultados de pruebas disponibles.", self.styles['Normal']))
            return story
        
        results_data = [['Prueba', 'Estado', 'Duración (s)', 'Mensaje']]
        
        for test in report_data.test_results:
            if test.status == 'PASSED':
                status_paragraph = Paragraph(f"<font color='green'><b>✅ {test.status}</b></font>", self.styles['Normal'])
            elif test.status == 'FAILED':
                status_paragraph = Paragraph(f"<font color='red'><b>❌ {test.status}</b></font>", self.styles['Normal'])
            else:
                status_paragraph = Paragraph(f"<font color='orange'><b>⏭️ {test.status}</b></font>", self.styles['Normal'])
            
            message_text = test.message[:80] + "..." if len(test.message) > 80 else test.message
            message_paragraph = Paragraph(message_text, self.styles['Normal'])
            
            results_data.append([
                Paragraph(test.name, self.styles['Normal']),
                status_paragraph,
                f"{test.duration:.2f}",
                message_paragraph
            ])
        
        results_table = Table(results_data, colWidths=[5.5*cm, 2.5*cm, 2*cm, 6.5*cm])
        results_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(results_table)
        story.append(Spacer(1, 20))
        
        return story
    
    def _build_failed_tests_section(self, report_data: ReportData) -> List:
        """Construir sección de pruebas fallidas con detalles"""
        story = []
        
        failed_tests = [test for test in report_data.test_results if test.status == 'FAILED']
        
        if not failed_tests:
            return story
        
        story.append(Paragraph("🚨 Análisis de Fallas", self.styles['CustomHeading']))
        
        for i, test in enumerate(failed_tests, 1):
            story.append(Paragraph(f"<b>{i}. {test.name}</b>", self.styles['Normal']))
            
            if test.message:
                story.append(Paragraph(f"<b>Error:</b> {test.message}", self.styles['Normal']))
            
            if test.details:
                story.append(Paragraph(f"<b>Detalles:</b>", self.styles['Normal']))
                story.append(Paragraph(f"<font name='Courier' size='8'>{test.details}</font>", self.styles['Normal']))
            
            story.append(Spacer(1, 10))
        
        return story
    
    def generate_report(self, report_data: ReportData) -> str:
        """Generar el reporte PDF completo"""
        filename = self._generate_filename()
        
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2.5*cm,
            bottomMargin=2.5*cm
        )
        
        story = []
        
        story.append(Paragraph(f"🧪 {report_data.title}", self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        story.append(Paragraph(f"<b>Proyecto:</b> {report_data.project_name}", self.styles['Normal']))
        story.append(Paragraph(f"<b>Versión:</b> {report_data.version}", self.styles['Normal']))
        story.append(Paragraph(f"<b>Entorno:</b> {report_data.environment}", self.styles['Normal']))
        story.append(Paragraph(f"<b>Fecha de Ejecución:</b> {report_data.execution_time.strftime('%Y-%m-%d %H:%M:%S')}", self.styles['Normal']))
        story.append(Spacer(1, 30))
        
        story.extend(self._build_summary_section(report_data))
        story.extend(self._build_results_section(report_data))
        story.extend(self._build_failed_tests_section(report_data))
        
        doc.build(story, onFirstPage=self._create_header_footer_canvas, 
                 onLaterPages=self._create_header_footer_canvas)
        
        print(f"📄 Reporte PDF generado exitosamente: {filename}")
        return filename


# Variables globales para capturar resultados
test_results = []
report_generator = PDFReportGenerator()


def add_test_result(name: str, status: str, duration: float, message: str = "", details: str = ""):
    """Agregar resultado de prueba"""
    global test_results
    test_results.append(TestResult(
        name=name,
        status=status,
        duration=duration,
        message=message,
        details=details
    ))


def generar_reporte_pdf(contenido):
    """Función original mejorada que ahora usa el sistema avanzado"""
    global test_results, report_generator
    
    # Crear datos del reporte
    report_data = ReportData(
        title="Reporte de Pruebas Automatizadas",
        project_name="Frontend Test",
        version="1.0.0",
        environment="TE: localhost",
        test_results=test_results,
        execution_time=datetime.now()
    )
    
    # Generar reporte avanzado
    report_generator.generate_report(report_data)
    
    # También mantener el reporte de texto simple si se desea
    carpeta = "TestReports"
    os.makedirs(carpeta, exist_ok=True)
    
    existentes = [f for f in os.listdir(carpeta) if f.startswith("report_text_") and f.endswith(".txt")]
    numeros = [int(f.split("_")[2].split(".")[0]) for f in existentes if f.split("_")[2].split(".")[0].isdigit()]
    nuevo_num = max(numeros, default=0) + 1
    nombre_archivo = f"report_text_{nuevo_num:03d}.txt"
    ruta = os.path.join(carpeta, nombre_archivo)
    
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(f"🧪 Resultado de Pruebas Automatizadas\n")
        f.write(f"Fecha y hora de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n")
        f.write(contenido)
    
    print(f"📄 Reporte de texto generado: {ruta}")