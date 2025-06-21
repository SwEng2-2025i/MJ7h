import os
import glob
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors


class TestReportGenerator:
    def __init__(self, reports_dir="Test_Reports"):
        self.reports_dir = reports_dir
        os.makedirs(reports_dir, exist_ok=True)
    
    def get_next_report_number(self):
        """Generate sequential report number"""
        existing_reports = glob.glob(os.path.join(self.reports_dir, "test_report_*.pdf"))
        if not existing_reports:
            return 1
        
        numbers = []
        for report in existing_reports:
            try:
                # Extract number from filename like "test_report_001.pdf"
                filename = os.path.basename(report)
                number_str = filename.split('_')[2].split('.')[0]
                numbers.append(int(number_str))
            except (IndexError, ValueError):
                continue
        
        return max(numbers) + 1 if numbers else 1
    
    def generate_report(self, test_name, test_results, created_data, cleanup_results):
        """Generate PDF report with test results"""
        report_number = self.get_next_report_number()
        filename = f"test_report_{report_number:03d}.pdf"
        filepath = os.path.join(self.reports_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        story.append(Paragraph(f"Test Report #{report_number:03d}", title_style))
        story.append(Spacer(1, 12))
        
        # Test Information
        story.append(Paragraph(f"<b>Test Name:</b> {test_name}", styles['Normal']))
        story.append(Paragraph(f"<b>Execution Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Test Results
        story.append(Paragraph("<b>Test Results:</b>", styles['Heading2']))
        for result in test_results:
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            story.append(Paragraph(f"{status} - {result['description']}", styles['Normal']))
            if 'details' in result:
                story.append(Paragraph(f"    Details: {result['details']}", styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Created Data
        if created_data:
            story.append(Paragraph("<b>Data Created During Test:</b>", styles['Heading2']))
            
            # Users table
            if 'users' in created_data and created_data['users']:
                story.append(Paragraph("Users:", styles['Heading3']))
                user_data = [['ID', 'Name']]
                user_data.extend([[str(user['id']), user['name']] for user in created_data['users']])
                
                user_table = Table(user_data)
                user_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(user_table)
                story.append(Spacer(1, 12))
            
            # Tasks table
            if 'tasks' in created_data and created_data['tasks']:
                story.append(Paragraph("Tasks:", styles['Heading3']))
                task_data = [['ID', 'Title', 'User ID']]
                task_data.extend([[str(task['id']), task['title'], str(task['user_id'])] for task in created_data['tasks']])
                
                task_table = Table(task_data)
                task_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(task_table)
                story.append(Spacer(1, 12))
        
        # Cleanup Results
        story.append(Paragraph("<b>Data Cleanup Results:</b>", styles['Heading2']))
        for cleanup in cleanup_results:
            status = "✅ SUCCESS" if cleanup['success'] else "❌ FAILED"
            story.append(Paragraph(f"{status} - {cleanup['description']}", styles['Normal']))
            if 'details' in cleanup:
                story.append(Paragraph(f"    Details: {cleanup['details']}", styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        print(f"📄 Report generated: {filepath}")
        return filepath
