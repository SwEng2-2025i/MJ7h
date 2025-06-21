from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests  # ✅ Importación agregada

service_a = Flask(__name__)
CORS(service_a)

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
    return jsonify({'error': 'Usuario no encontrado'}), 404

@service_a.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name} for user in users])

# ✅ ENDPOINT FALTANTE - Eliminar usuario
@service_a.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    # Eliminar tareas asociadas primero
    try:
        response = requests.delete(f'http://localhost:5003/tasks/user/{user_id}')
        if response.status_code != 200:
            return jsonify({'error': 'Error eliminando tareas del usuario'}), 500
    except Exception as e:
        return jsonify({'error': f'Error de conexión: {str(e)}'}), 500

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'Usuario {user_id} eliminado correctamente'}), 200

if __name__ == '__main__':
    with service_a.app_context():
        db.create_all()
    service_a.run(port=5002)
