import requests
import os
from reportlab.pdfgen import canvas

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

# Directorio para reportes
REPORT_DIR = 'test_reports'
os.makedirs(REPORT_DIR, exist_ok=True)

def get_next_report_number():
    existing = [f for f in os.listdir(REPORT_DIR) if f.startswith('report_') and f.endswith('.pdf')]
    nums = [int(f.split('_')[1].split('.')[0]) for f in existing]
    return max(nums) + 1 if nums else 1


def generate_pdf_report(passed: bool, details: str):
    num = get_next_report_number()
    filepath = os.path.join(REPORT_DIR, f'report_{num}.pdf')
    c = canvas.Canvas(filepath)
    c.drawString(50, 800, f'Test Report #{num}')
    c.drawString(50, 780, f'Passed: {passed}')
    text = c.beginText(50, 750)
    for line in details.splitlines():
        text.textLine(line)
    c.drawText(text)
    c.save()
    print(f'✅ PDF report generated: {filepath}')


def create_user(name):
    r = requests.post(USERS_URL, json={"name": name}); r.raise_for_status(); return r.json()["id"]

def create_task(user_id, description):
    r = requests.post(TASKS_URL, json={"title": description, "user_id": user_id}); r.raise_for_status(); return r.json()["id"]


def delete_task(task_id):
    return requests.delete(f"{TASKS_URL}/{task_id}")

def delete_user(user_id):
    return requests.delete(f"{USERS_URL}/{user_id}")


def get_tasks():
    return requests.get(TASKS_URL).json()


def integration_test():
    details = []
    try:
        # Crear usuario y tarea
        user_id = create_user("Camilo")
        task_id = create_task(user_id, "Prepare presentation")
        details.append(f"Created user {user_id} and task {task_id}")

        # Verificar registro
        tasks = get_tasks()
        assert any(t["id"] == task_id and t["user_id"] == user_id for t in tasks), "Task not linked"
        details.append("✅ Task correctly registered and linked")

        # Limpieza: borrar tarea
        r_task_del = delete_task(task_id)
        assert r_task_del.status_code == 200, "Failed to delete task"
        # Verificar eliminación en backend
        tasks_after = get_tasks()
        assert not any(t["id"] == task_id for t in tasks_after), "Task not deleted"
        details.append("✅ Task deleted successfully and verified")

        # Limpieza: borrar usuario
        r_user_del = delete_user(user_id)
        assert r_user_del.status_code == 200, "Failed to delete user"
        # Verificar eliminación usuario
        r_user_get = requests.get(f"{USERS_URL}/{user_id}")
        assert r_user_get.status_code == 404, "User not deleted"
        details.append("✅ User deleted successfully and verified")

        generate_pdf_report(True, "\n".join(details))
        print("✅ All backend test steps passed.")
    except AssertionError as e:
        details.append(f"❌ AssertionError: {str(e)}")
        generate_pdf_report(False, "\n".join(details))
        raise


if __name__ == "__main__":
    integration_test()