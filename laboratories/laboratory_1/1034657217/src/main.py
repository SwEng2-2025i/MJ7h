from flask import Flask, jsonify, request
from flask_restx import Api
from routes.users import users_bp
from routes.notifications import notifications_bp
from utils.logger import Logger
from model.usersModel import UsersModel

logger =Logger()
logger.startLog()
UsersModel()
app = Flask(__name__)
api = Api(app,title="Laboratory 1 Martin Moreno", version="1.0",doc='/docs')


if __name__=="__main__":
    app.register_blueprint(users_bp)
    app.register_blueprint(notifications_bp)
    app.run(debug=True)