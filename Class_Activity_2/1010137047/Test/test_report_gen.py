from fpdf import FPDF
import os
from datetime import datetime

def generate_pdf_report(test_results):
    os.makedirs("Test_Reports", exist_ok=True)
    existing = [f for f in os.listdir("Test_Reports") if f.endswith(".pdf")]
    num = len(existing) + 1
    filename = f"Test_Reports/test_report_{str(num).zfill(3)}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Test Report #{num}", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Generated: {datetime.now()}", ln=True, align="L")
    pdf.ln(10)
    for line in test_results.split("\n"):
        pdf.multi_cell(0, 10, txt=line)
    
    pdf.output(filename)
    print(f"PDF generated: {filename}")

