from flask import Blueprint, request, jsonify
from controllers.user_controller import UserController

users_bp = Blueprint('users',__name__,url_prefix='/users')
user_controller = UserController()

@users_bp.route('/', methods=['GET'])
def get_users():
    return user_controller.get_all_users()

@users_bp.route('/',methods=['POST'])
def register_user():
    return user_controller.register_user()