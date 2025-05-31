from flask import Flask, request, jsonify
from models.user_store import UserStore
from channels.builder import build_chain
from extra.logger import logger
import random

app = Flask(__name__)
user_store = UserStore()
# obtener usuarios
@app.route('/users', methods=['GET'])
def list_users():
    users = user_store.list_users()
    return jsonify({'users': users}), 200

# api de users para registrar un usuario
@app.route('/users', methods=['POST'])
def register_user():
    data = request.get_json()
    name = data.get('name')
    preferred = data.get('preferred_channel')
    available = data.get('available_channels', [])

    if not name or not preferred or not available:
        return jsonify({'error': 'Falta nombre, canal preferido o canales disponibles'}), 400

    if preferred not in available:
        return jsonify({'error': 'El canal preferido debe estar en la lista de disponibles'}), 400

    success = user_store.add_user(name, preferred, available)
    if not success:
        return jsonify({'error': 'Usuario ya existe'}), 400

    return jsonify({'message': f'Usuario {name} registrado.'}), 201