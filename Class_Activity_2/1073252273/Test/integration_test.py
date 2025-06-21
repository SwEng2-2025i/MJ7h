import requests
import os
from fpdf import FPDF
from datetime import datetime

# Configuración de endpoints
USERS_URL = 'http://localhost:5001/users'
TASKS_URL = 'http://localhost:5002/tasks'

REPORTS_DIR = 'reports'

# Utilidad para generar nombre secuencial de PDF
def get_next_report_filename():
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)
    existing = [f for f in os.listdir(REPORTS_DIR) if f.startswith('reporte_') and f.endswith('.pdf')]
    nums = [int(f.split('_')[1].split('.')[0]) for f in existing if f.split('_')[1].split('.')[0].isdigit()]
    next_num = max(nums) + 1 if nums else 1
    return os.path.join(REPORTS_DIR, f'reporte_{next_num}.pdf')

# Clase para el PDF
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Reporte de Pruebas de Integracion', 0, 1, 'C')
        self.ln(10)

    def add_result(self, text):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, text)
        self.ln(2)

def test_create_and_cleanup():
    results = []
    # 1. Crear usuario
    user_resp = requests.post(USERS_URL, json={'name': 'TestUser'})
    assert user_resp.status_code == 201, 'No se pudo crear usuario'
    user_id = user_resp.json()['id']
    results.append(f'Usuario creado: ID={user_id}')

    # 2. Crear tarea
    task_resp = requests.post(TASKS_URL, json={'title': 'TestTask', 'user_id': user_id})
    assert task_resp.status_code == 201, 'No se pudo crear tarea'
    task_id = task_resp.json()['id']
    results.append(f'Tarea creada: ID={task_id}')

    # 3. Verificar existencia
    tasks = requests.get(TASKS_URL).json()
    assert any(t['id'] == task_id for t in tasks), 'La tarea no existe tras crearla'
    results.append('Tarea verificada en el sistema')

    # 4. Eliminar tarea
    del_task = requests.delete(f'{TASKS_URL}/{task_id}')
    assert del_task.status_code == 200, 'No se pudo eliminar tarea'
    results.append('Tarea eliminada')

    # 5. Eliminar usuario
    del_user = requests.delete(f'{USERS_URL}/{user_id}')
    assert del_user.status_code == 200, 'No se pudo eliminar usuario'
    results.append('Usuario eliminado')

    # 6. Verificar limpieza
    tasks = requests.get(TASKS_URL).json()
    assert not any(t['id'] == task_id for t in tasks), 'La tarea no fue eliminada'
    results.append('Verificacion: tarea eliminada correctamente')
    users = requests.get(USERS_URL).json()
    assert not any(u['id'] == user_id for u in users), 'El usuario no fue eliminado'
    results.append('Verificacion: usuario eliminado correctamente')

    return results

def main():
    pdf = PDFReport()
    pdf.add_page()
    pdf.add_result(f'Fecha y hora: {datetime.now()}')
    try:
        results = test_create_and_cleanup()
        for r in results:
            pdf.add_result(r)
        pdf.add_result('\nTodas las pruebas pasaron correctamente.')
    except AssertionError as e:
        pdf.add_result('Error: ' + str(e))
    filename = get_next_report_filename()
    pdf.output(filename)
    print(f'Reporte generado: {filename}')

if __name__ == '__main__':
    main()
