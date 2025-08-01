import os
from fpdf import FPDF
from datetime import datetime

REPORT_DIR = 'reports'

def get_next_report_filename(base_name):
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)
    
    i = 1
    while True:
        filename = os.path.join(REPORT_DIR, f"{base_name}_{i}.pdf")
        if not os.path.exists(filename):
            return filename
        i += 1

def generate_pdf_report(test_name, logs):
    filename = get_next_report_filename(test_name)
    
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f'Test Report: {test_name}', 0, 1, 'C')
    pdf.cell(0, 10, f'Execution Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=10)
    
    for line in logs:
        cleaned_line = line.replace('\n', ' ').replace('\r', '').strip()
        cleaned_line = cleaned_line.encode('latin-1', 'ignore').decode('latin-1')
        
        if cleaned_line:
            pdf.cell(0, 5, txt=cleaned_line, ln=1)

    pdf.output(filename)
    print(f"\n📄 PDF report generated: {filename}") 