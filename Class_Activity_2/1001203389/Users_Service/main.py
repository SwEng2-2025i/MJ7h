from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

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

# --- NUEVO: Endpoint para borrar un usuario ---
@service_a.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Opcional: Eliminar tareas asociadas a este usuario
    # import requests
    # requests.delete(f'http://localhost:5002/tasks/by_user/{user_id}')

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'User with id {user_id} deleted successfully'}), 200

if __name__ == '__main__':
    with service_a.app_context():
        db.create_all()
    service_a.run(port=5001)