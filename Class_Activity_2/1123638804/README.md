# Integration Project - Brief Report

## Results Summary

This project now supports:
- **Automated data cleanup:** DELETE endpoints for users and tasks, allowing tests to remove only the data they created.
- **Automatic PDF report generation:** Each test run produces a sequentially numbered PDF report with the results, preserving all previous reports.

---

## Sections of Code Added

### Users Service (`Users_Service/main.py`)

**DELETE endpoint for users:**
```python
@service_a.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'User {user_id} deleted'}), 200
```

Purpose: Allows deletion of a user by ID for test cleanup.

Tasks Service (Task_Service/main.py)
DELETE endpoint for tasks:
```python
@service_b.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': f'Task {task_id} deleted'}), 200
```

Purpose: Allows deletion of a task by ID for test cleanup.

---

## Known Issues

- **PDF Report Formatting:** The PDF reports, while comprehensive, require further refinement for layout consistency.
- **API Response Time:** Under heavy load, some DELETE requests may experience slight delays.

## Libraries Installed
pip install fpdf
pip install flask flask_sqlalchemy flask_cors
pip install selenium
## PDF Report Generation Code Snippet

```python
from fpdf import FPDF
import os

def save_pdf_report(test_results, report_dir="reports"):
    os.makedirs(report_dir, exist_ok=True)
    existing = [f for f in os.listdir(report_dir) if f.startswith("report_") and f.endswith(".pdf")]
    nums = [int(f.split("_")[1].split(".")[0]) for f in existing if f.split("_")[1].split(".")[0].isdigit()]
    next_num = max(nums) + 1 if nums else 1
    filename = os.path.join(report_dir, f"report_{next_num}.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "FrontEnd Test Report", ln=True, align="C")
    pdf.ln(10)
    for line in test_results:
        pdf.multi_cell(0, 10, clean_text(line))
    pdf.output(filename)
    print(f"PDF report saved as {filename}")

def clean_text(text):
    return text.replace("✅", "[OK]").replace("❌", "[FAIL]")
```

# At the end of main(), after collecting test_results:
save_pdf_report(test_results)

## Conclusion

The integration project has successfully implemented the core features as outlined in the initial proposal. Further refinements and additional features are planned for future iterations.



