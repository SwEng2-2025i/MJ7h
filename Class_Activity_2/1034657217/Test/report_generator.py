import os
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from matplotlib import pyplot as plt
import numpy as np
from io import BytesIO
from reportlab.platypus import Image

class TestReportGenerator:
    def __init__(self, reports_dir="reports"):
        self.reports_dir = reports_dir
        os.makedirs(reports_dir, exist_ok=True)
    
    def create_test_results_chart(self, test_results):
        """Crea gráfica de barras de resultados"""
        passed = sum(1 for r in test_results if r['status'] == 'PASS')
        failed = sum(1 for r in test_results if r['status'] == 'FAIL')
        
        # Configurar la gráfica
        fig, ax = plt.subplots(figsize=(8, 6))
        categories = ['Passed', 'Failed']
        values = [passed, failed]
        colors = ['#4CAF50', '#f44336']
        
        bars = ax.bar(categories, values, color=colors)
        ax.set_ylabel('Number of Tests')
        ax.set_title('Test Results Summary')
        
        # Agregar valores encima de las barras
        for bar, value in zip(bars, values):
            if value > 0:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                       str(value), ha='center', va='bottom', fontweight='bold')
        
        # Guardar en memoria
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        return img_buffer

    def create_duration_chart(self, test_results):
        """Crea gráfica de duración de tests"""
        test_names = [r['name'][:20] + '...' if len(r['name']) > 20 else r['name'] 
                     for r in test_results]
        durations = [r.get('duration', 0) for r in test_results]
        colors = ['#4CAF50' if r['status'] == 'PASS' else '#f44336' for r in test_results]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(test_names, durations, color=colors)
        ax.set_xlabel('Duration (seconds)')
        ax.set_title('Test Execution Times')
        
        # Agregar valores al final de las barras
        for i, (bar, duration) in enumerate(zip(bars, durations)):
            if duration > 0:
                ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                       f'{duration}s', ha='left', va='center')
        
        plt.tight_layout()
        
        # Guardar en memoria
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        return img_buffer

    def create_pie_chart(self, test_results):
        """Crea gráfica circular de resultados"""
        passed = sum(1 for r in test_results if r['status'] == 'PASS')
        failed = sum(1 for r in test_results if r['status'] == 'FAIL')
        
        if passed == 0 and failed == 0:
            return None
            
        fig, ax = plt.subplots(figsize=(8, 8))
        
        sizes = []
        labels = []
        colors = []
        
        if passed > 0:
            sizes.append(passed)
            labels.append(f'Passed ({passed})')
            colors.append('#4CAF50')
            
        if failed > 0:
            sizes.append(failed)
            labels.append(f'Failed ({failed})')
            colors.append('#f44336')
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                         startangle=90, textprops={'fontsize': 12})
        
        ax.set_title('Test Results Distribution', fontsize=16, fontweight='bold')
        
        # Guardar en memoria
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        return img_buffer
    
    def get_next_report_number(self):
        """Obtiene el siguiente número secuencial"""
        existing_files = [f for f in os.listdir(self.reports_dir) if f.startswith("test_report_")]
        if not existing_files:
            return 1
        
        numbers = []
        for file in existing_files:
            try:
                num = int(file.split("_")[2].split(".")[0])
                numbers.append(num)
            except:
                continue
        
        return max(numbers) + 1 if numbers else 1
    
    def generate_report(self, test_results, test_type="Integration"):
        """Genera el reporte PDF con gráficas"""
        report_num = self.get_next_report_number()
        filename = f"test_report_{report_num:03d}.pdf"
        filepath = os.path.join(self.reports_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            textColor=colors.darkblue
        )
        story.append(Paragraph(f"Test Report #{report_num:03d}", title_style))
        story.append(Spacer(1, 12))
        
        # Información general (mismo código anterior)
        info_data = [
            ["Test Type:", test_type],
            ["Date:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ["Total Tests:", str(len(test_results))],
            ["Passed:", str(sum(1 for r in test_results if r['status'] == 'PASS'))],
            ["Failed:", str(sum(1 for r in test_results if r['status'] == 'FAIL'))],
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
        
        # SECCIÓN DE GRÁFICAS
        story.append(Paragraph("Visual Analysis", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        # Gráfica circular
        pie_chart = self.create_pie_chart(test_results)
        if pie_chart:
            story.append(Paragraph("Test Results Distribution", styles['Heading3']))
            story.append(Image(pie_chart, width=5*inch, height=5*inch))
            story.append(Spacer(1, 20))
        
        # Gráfica de barras
        bar_chart = self.create_test_results_chart(test_results)
        story.append(Paragraph("Test Results Summary", styles['Heading3']))
        story.append(Image(bar_chart, width=6*inch, height=4*inch))
        story.append(Spacer(1, 20))
        
        # Gráfica de duración
        if any(r.get('duration', 0) > 0 for r in test_results):
            duration_chart = self.create_duration_chart(test_results)
            story.append(Paragraph("Test Execution Times", styles['Heading3']))
            story.append(Image(duration_chart, width=7*inch, height=4*inch))
            story.append(Spacer(1, 20))
        
        # Resultados detallados (mismo código anterior)
        story.append(Paragraph("Test Results Details", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        for i, result in enumerate(test_results, 1):
            status_color = colors.green if result['status'] == 'PASS' else colors.red
            status_text = f"<font color='{status_color.hexval()}'>{result['status']}</font>"
            
            test_data = [
                [f"Test {i}:", result['name']],
                ["Status:", Paragraph(status_text, styles['Normal'])],
                ["Duration:", f"{result.get('duration', 'N/A')} seconds"],
                ["Details:", result.get('details', 'No details available')]
            ]
            
            if result['status'] == 'FAIL' and 'error' in result:
                test_data.append(["Error:", result['error']])
            
            test_table = Table(test_data, colWidths=[1.5*inch, 4*inch])
            test_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            
            story.append(test_table)
            story.append(Spacer(1, 10))
        
        doc.build(story)
        print(f"✅ Report with charts generated: {filepath}")
        return filepath