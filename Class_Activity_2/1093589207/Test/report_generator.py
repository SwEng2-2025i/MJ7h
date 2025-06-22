import os
from fpdf import FPDF
import datetime

def generate_pdf_report(test_name, results):
    # Find the next sequential report number
    report_num = 1
    while os.path.exists(f"{test_name}_report_{report_num}.pdf"):
        report_num += 1
    
    report_filename = f"{test_name}_report_{report_num}.pdf"

    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Test Report: {test_name}", ln=True, align='C')
    
    # Date
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 10, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    pdf.ln(10)

    # Results
    pdf.set_font("Arial", '', 11)
    for line in results:
        if line.startswith("✅"):
            pdf.set_text_color(0, 128, 0)  # Green
        elif line.startswith("❌"):
            pdf.set_text_color(255, 0, 0)  # Red
        else:
            pdf.set_text_color(0, 0, 0)  # Black
        
        pdf.multi_cell(0, 8, txt=line)
    
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)

    pdf.output(report_filename)
    print(f"✅ Report generated: {report_filename}")