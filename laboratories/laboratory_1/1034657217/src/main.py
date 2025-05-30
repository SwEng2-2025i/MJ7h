from flask import Flask, jsonify, request
from routes.users import users_bp

app = Flask(__name__)

app.register_blueprint(users_bp)


if __name__=="__main__":
    app.run(debug=True)