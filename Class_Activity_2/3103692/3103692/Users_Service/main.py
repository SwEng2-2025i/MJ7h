from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # 👈 Agregado

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


service_a = Flask(__name__)
CORS(service_a)  # 👈 Habilita CORS

service_a.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
service_a.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(service_a)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

@service_a.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data or not data['name'].strip():
        return jsonify({'error': 'El nombre es requerido'}), 400

    user = User(name=data['name'].strip())
    db.session.add(user)
    db.session.commit()
    print({'id': user.id, 'name': user.name})
    return jsonify({'id': user.id, 'name': user.name}), 201

@service_a.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({'id': user.id, 'name': user.name})
    return jsonify({'error': 'User not found'}), 404

@service_a.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name} for user in users])


# Código para borrar las rutas instance [

@service_a.route('/clean', methods=['POST'])
def clean_users():
    instance_folder = os.path.join(service_a.root_path, 'instance')
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
    with service_a.app_context():
        db.create_all()
    service_a.run(port=5001)
