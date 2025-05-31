from flask import Flask, request, jsonify
from models.user_store import UserStore
from channels.builder import builds_chain
from extra.logger import logger
import random

app = Flask(__name__)
user_store = UserStore()
# tes primero
@app.route('/users', methods=['GET'])
def list_users():
    users = user_store.list_users()
    return jsonify({'users': users}), 200