# backend_pdf_generator.py
import os
from datetime import datetime
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

class BackendPDFReporter:
    def __init__(self, results, start_time):
        self.results = results
        self.start_time = start_time
    
    def _get_next_filename(self, base_name="BackEnd Tests Report"):
        """Genera el siguiente nombre de archivo disponible"""
        counter = 1
        
        filename = f"{base_name}.pdf"
        if not os.path.exists(filename):
            return filename
        
        while True:
            filename = f"{base_name} ({counter}).pdf"
            if not os.path.exists(filename):
                return filename
            counter += 1
    
    def get_statistics(self):
        total = len(self.results)
        passed = len([r for r in self.results if r.status == 'PASS'])
        failed = total - passed
        
        categories = {}
        for result in self.results:
            if result.category not in categories:
                categories[result.category] = {'passed': 0, 'failed': 0}
            if result.status == 'PASS':
                categories[result.category]['passed'] += 1
            else:
                categories[result.category]['failed'] += 1
        
        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'pass_rate': (passed / total * 100) if total > 0 else 0,
            'categories': categories
        }
    
    def generate_charts(self):
        stats = self.get_statistics()
        
        plt.figure(figsize=(12, 8))
        
        # Gráfica de pastel general
        plt.subplot(2, 2, 1)
        labels = ['Exitosas', 'Fallidas']
        sizes = [stats['passed'], stats['failed']]
        colors_pie = ['#4CAF50', '#F44336']
        explode = (0.1, 0)
        
        plt.pie(sizes, explode=explode, labels=labels, colors=colors_pie, 
                autopct='%1.1f%%', shadow=True, startangle=90)
        plt.title('Resultados Generales Backend')
        
        # Gráfica de barras por categoría
        plt.subplot(2, 2, 2)
        categories = list(stats['categories'].keys())
        passed_counts = [stats['categories'][cat]['passed'] for cat in categories]
        failed_counts = [stats['categories'][cat]['failed'] for cat in categories]
        
        x = range(len(categories))
        width = 0.35
        
        plt.bar([i - width/2 for i in x], passed_counts, width, label='Exitosas', color='#4CAF50')
        plt.bar([i + width/2 for i in x], failed_counts, width, label='Fallidas', color='#F44336')
        
        plt.xlabel('Categorías')
        plt.ylabel('Número de Pruebas')
        plt.title('Resultados por Categoría Backend')
        plt.xticks(x, categories, rotation=45)
        plt.legend()
        
        # Gráfica de línea temporal
        plt.subplot(2, 1, 2)
        times = [r.timestamp for r in self.results]
        cumulative_passed = []
        cumulative_failed = []
        
        passed_count = 0
        failed_count = 0
        
        for result in self.results:
            if result.status == 'PASS':
                passed_count += 1
            else:
                failed_count += 1
            cumulative_passed.append(passed_count)
            cumulative_failed.append(failed_count)
        
        plt.plot(times, cumulative_passed, 'g-', label='Acumuladas Exitosas', marker='o')
        plt.plot(times, cumulative_failed, 'r-', label='Acumuladas Fallidas', marker='x')
        plt.xlabel('Tiempo')
        plt.ylabel('Número de Pruebas')
        plt.title('Progreso de Pruebas Backend')
        plt.legend()
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        chart_path = 'backend_test_results_chart.png'
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return chart_path
    
    def generate_pdf_report(self):
        chart_path = self.generate_charts()
        stats = self.get_statistics()
        
        pdf_filename = self._get_next_filename()
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1
        )
        story.append(Paragraph("Reporte de Pruebas Backend", title_style))
        story.append(Spacer(1, 12))
        
        story.append(Paragraph("Resumen Ejecutivo", styles['Heading2']))
        summary_data = [
            ['Métrica', 'Valor'],
            ['Total de Pruebas', str(stats['total'])],
            ['Pruebas Exitosas', str(stats['passed'])],
            ['Pruebas Fallidas', str(stats['failed'])],
            ['Tasa de Éxito', f"{stats['pass_rate']:.1f}%"],
            ['Duración Total', str(datetime.now() - self.start_time)]
        ]
        
        summary_table = Table(summary_data)
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)  # ✅ Corregido: agregado paréntesis de cierre
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 12))
        
        if os.path.exists(chart_path):
            story.append(Paragraph("Análisis Visual", styles['Heading2']))
            story.append(Image(chart_path, width=7*inch, height=5.6*inch))
        story.append(Spacer(1, 12))
        
        story.append(Paragraph("Resultados por Categoría", styles['Heading2']))
        for category, data in stats['categories'].items():
            total_cat = data['passed'] + data['failed']
            success_rate = (data['passed'] / total_cat * 100) if total_cat > 0 else 0
            
            story.append(Paragraph(f"<b>{category}</b>", styles['Heading3']))
            cat_data = [
                ['Métrica', 'Valor'],
                ['Pruebas Exitosas', str(data['passed'])],
                ['Pruebas Fallidas', str(data['failed'])],
                ['Tasa de Éxito', f"{success_rate:.1f}%"]
            ]
            
            cat_table = Table(cat_data)
            cat_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(cat_table)
            story.append(Spacer(1, 12))
        
        failed_tests = [r for r in self.results if r.status == 'FAIL']
        if failed_tests:
            story.append(Paragraph("Detalles de Pruebas Fallidas", styles['Heading2']))
            for test in failed_tests:
                story.append(Paragraph(f"<b>{test.test_name}</b> ({test.category})", styles['Heading4']))
                story.append(Paragraph(f"Error: {test.error_message}", styles['Normal']))
                story.append(Spacer(1, 6))
        
        doc.build(story)
        
        if os.path.exists(chart_path):
            os.remove(chart_path)
        
        return pdf_filename

def generate_backend_test_report(results, start_time):
    reporter = BackendPDFReporter(results, start_time)
    return reporter.generate_pdf_report()
