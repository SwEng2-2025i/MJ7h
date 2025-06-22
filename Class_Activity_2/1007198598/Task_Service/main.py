from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests

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

@service_b.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task by ID"""
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    try:
        db.session.delete(task)
        db.session.commit()
        print(f"Task {task_id} deleted successfully")
        return jsonify({'message': f'Task {task_id} deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting task {task_id}: {str(e)}")
        return jsonify({'error': f'Error deleting task: {str(e)}'}), 500

if __name__ == '__main__':
    with service_b.app_context():
        db.create_all()
    service_b.run(port=5002)