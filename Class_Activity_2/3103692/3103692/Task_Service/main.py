from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests

# importaciones para el borrado de instance [
from flask import Flask, jsonify
import os, shutil

app = Flask(__name__, instance_relative_config=True)

# ]


# importaciones para la creación del reporte en PDF [
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
from flask import send_file

# ]



service_b = Flask(__name__)
CORS(service_b)

service_b.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
service_b.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(service_b)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

@service_b.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or not data.get('title') or not data.get('user_id'):
        return jsonify({'error': 'Datos inválidos'}), 400
    try:
        user_check = requests.get(f'http://localhost:5001/users/{data["user_id"]}')
    except Exception as e:
        return jsonify({'error': f'Error de conexión al verificar usuario: {str(e)}'}), 500

    if user_check.status_code != 200:
        return jsonify({'error': 'ID de usuario inválido'}), 400

    task = Task(title=data['title'], user_id=data['user_id'])
    db.session.add(task)
    db.session.commit()
    return jsonify({'id': task.id, 'title': task.title, 'user_id': task.user_id}), 201

@service_b.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': t.id, 'title': t.title, 'user_id': t.user_id} for t in tasks])


# Código para borrar las rutas instance [

@service_b.route('/clean', methods=['POST'])
def clean_tasks():
    instance_folder = os.path.join(service_b.root_path, 'instance')
    if os.path.exists(instance_folder):
        shutil.rmtree(instance_folder)
    os.makedirs(instance_folder, exist_ok=True)
    return jsonify(status='ok')

#]


# Código para generar el reporte en formato PDF [
@app.route('/report', methods=['GET'])
def generate_report():
    # Aquí obtén las estadísticas reales (puedes leer logs o guardarlas en BD)
    total = 100
    passed = 85
    failed = total - passed

    # --- 1) Generar la gráfica ---
    fig, ax = plt.subplots()
    ax.pie([passed, failed], labels=['OK', 'FALLÓ'], autopct='%1.1f%%')
    ax.set_title('Resultados de pruebas E2E')
    buf = io.BytesIO()
    plt.savefig(buf, format='PNG')
    plt.close(fig)
    buf.seek(0)

    # --- 2) Crear PDF y embedir la imagen ---
    pdf_path = os.path.join(app.root_path, 'reports', 'test_report.pdf')
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, height - 50, "Informe de Pruebas de Integración")
    # Inserta la imagen de la gráfica
    c.drawImage(buf, 40, height/2 - 100, width=400, preserveAspectRatio=True)
    c.showPage()
    c.save()

    # --- 3) Devolver la ruta o el propio PDF para descarga ---
    return send_file(pdf_path, as_attachment=True)

#]


if __name__ == '__main__':
    with service_b.app_context():
        db.create_all()
    service_b.run(port=5002)
