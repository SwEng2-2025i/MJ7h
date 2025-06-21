import requests
import platform
from fpdf import FPDF
from datetime import datetime
import os
import sys

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("User created:", user_data)
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("Task created:", task_data)
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def cleanup(user_id, task_id):
    requests.delete(f"{USERS_URL}/{user_id}")
    requests.delete(f"{TASKS_URL}/{task_id}")
    print("Datos de prueba eliminados")

class PDFReport(FPDF):
    def __init__(self):
        super().__init__()
        self.set_font('Arial', '', 12)
        self.test_details = []
        self.report_title = "Reporte de Pruebas de Integracion"
    
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, self.report_title, 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}/{{nb}}', 0, 0, 'C')
    
    def add_test_section(self, title, content):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1)
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 6, content)
        self.ln(5)
    
    def add_test_table(self, headers, data):
        self.set_font('Arial', 'B', 10)
        col_widths = [40, 50, 30, 30]
        
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 10, header, 1, 0, 'C')
        self.ln()
        
        self.set_font('Arial', '', 10)
        for row in data:
            for i, item in enumerate(row):
                self.cell(col_widths[i], 6, str(item), 1, 0, 'C')
            self.ln()

def generate_pdf_report(test_data):
    try:
        pdf = PDFReport()
        pdf.alias_nb_pages()
        pdf.add_page()
        
        # Información general
        pdf.add_test_section("Informacion General", 
                           f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                           f"Resultado general: {'EXITO' if test_data['success'] else 'FALLO'}")
        
        # Detalles de ejecución
        execution_details = (
            f"Duracion total: {test_data['duration']:.2f} segundos\n"
            f"Servicios probados: Users-Service (5001), Task-Service (5002)\n"
            f"Total operaciones: {len(test_data['operations'])}"
        )
        pdf.add_test_section("Detalles de Ejecucion", execution_details)
        
        # Tabla de operaciones
        headers = ["Operacion", "Endpoint", "Datos", "Resultado"]
        data = []
        for op in test_data['operations']:
            data.append([
                op['operation'],
                op['endpoint'],
                str(op.get('request_data', '')),
                "PASS" if op['success'] else "FAIL"
            ])
        
        pdf.add_test_section("Detalle de Operaciones", "")
        pdf.add_test_table(headers, data)
        
        # Errores (si existen)
        if not test_data['success']:
            errors = "\n".join([f"- {e['operation']}: {e['error']}" 
                              for e in test_data['operations'] if not e['success']])
            pdf.add_test_section("Errores Detectados", errors)
        
        # Información del entorno
        env_info = (
            f"Python: {sys.version.split()[0]}\n"
            f"Sistema Operativo: {platform.system()} {platform.release()}\n"
            f"Directorio: {os.getcwd()}"
        )
        pdf.add_test_section("Entorno de Pruebas", env_info)
        
        # Guardar reporte con verificación
        report_number = len([f for f in os.listdir() if f.startswith("report_") and f.endswith(".pdf")]) + 1
        filename = f"report_{report_number}.pdf"
        full_path = os.path.abspath(filename)
        
        pdf.output(full_path)
        
        # Verificación de creación
        if os.path.exists(full_path):
            print(f"\n[SUCCESS] PDF generado correctamente en: {full_path}")
            return full_path
        else:
            print("\n[ERROR] El archivo PDF no se creó")
            return None
            
    except Exception as e:
        print(f"\n[ERROR] Fallo al generar PDF: {str(e)}")
        return None

def integration_test():
    # Prepara los datos para el reporte
    test_data = {
        'success': True,
        'operations': [],
        'start_time': datetime.now(),
        'duration': 0
    }

    try:
        # 1. Crear usuario
        print("\n[TEST] Creando usuario...")
        user_id = create_user("Camilo")
        test_data['operations'].append({
            'operation': 'Crear usuario',
            'endpoint': 'POST /users',
            'request_data': {'name': 'Camilo'},
            'success': True,
            'response_data': {'id': user_id}
        })

        # 2. Crear tarea
        print("[TEST] Creando tarea...")
        task_id = create_task(user_id, "Prepare presentation")
        test_data['operations'].append({
            'operation': 'Crear tarea',
            'endpoint': 'POST /tasks',
            'request_data': {'user_id': user_id, 'title': 'Prepare presentation'},
            'success': True,
            'response_data': {'id': task_id}
        })

        # 3. Verificar tareas
        print("[TEST] Verificando tareas...")
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        verification_passed = any(t["id"] == task_id for t in user_tasks)
        test_data['operations'].append({
            'operation': 'Verificar tareas',
            'endpoint': 'GET /tasks',
            'success': verification_passed,
            'response_data': {'tasks_found': len(user_tasks)}
        })

        if not verification_passed:
            raise AssertionError("La tarea no fue registrada correctamente")

        # 4. Limpieza
        print("[TEST] Limpiando datos de prueba...")
        cleanup(user_id, task_id)
        test_data['operations'].append({
            'operation': 'Limpieza de datos',
            'endpoint': 'DELETE /users/<id> y DELETE /tasks/<id>',
            'success': True
        })

        # Calcula duración
        test_data['duration'] = (datetime.now() - test_data['start_time']).total_seconds()
        
        # Verifica si todas las operaciones fueron exitosas
        test_data['success'] = all(op['success'] for op in test_data['operations'])

    except Exception as e:
        print(f"[TEST ERROR] {str(e)}")
        test_data['success'] = False
        if test_data['operations']:
            test_data['operations'][-1]['success'] = False
            test_data['operations'][-1]['error'] = str(e)
        else:
            test_data['error'] = str(e)
        
    finally:
        # Genera el reporte con todos los datos
        print("\n[TEST] Generando reporte PDF...")
        report_file = generate_pdf_report(test_data)

        if not test_data['success']:
            raise AssertionError("Algunas pruebas fallaron. Ver el reporte PDF para detalles.")
        else:
            print("[TEST] Todas las pruebas completadas exitosamente")

if __name__ == "__main__":
    print("Iniciando pruebas de integración...")
    integration_test()