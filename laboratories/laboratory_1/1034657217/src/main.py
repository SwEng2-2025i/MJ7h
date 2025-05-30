from flask import Flask, jsonify, request
from routes.users import users_bp
from routes.notifications import notifications_bp

app = Flask(__name__)


if __name__=="__main__":
    app.register_blueprint(users_bp)
    app.register_blueprint(notifications_bp)
    app.run(debug=True)