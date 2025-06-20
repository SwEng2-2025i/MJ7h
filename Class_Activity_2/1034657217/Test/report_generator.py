import os
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

class TestReportGenerator:
    def __init__(self, reports_dir="reports"):
        self.reports_dir = reports_dir
        os.makedirs(reports_dir, exist_ok=True)
    
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
        """Genera el reporte PDF"""
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
        
        # Información general
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
        
        # Resultados detallados
        story.append(Paragraph("Test Results Details", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        for i, result in enumerate(test_results, 1):
            # Status con color
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
        print(f"✅ Report generated: {filepath}")
        return filepath