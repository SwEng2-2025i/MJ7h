from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

# Simulamos una base de datos en memoria
users = []

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = {
        "id": str(uuid.uuid4()),
        "email": data.get("email"),
        "password": data.get("password")
    }
    users.append(new_user)
    return jsonify(new_user), 201

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), 200

@app.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users
    users = [u for u in users if u["id"] != user_id]
    return jsonify({"message": "Usuario eliminado"}), 200

if __name__ == "__main__":
    app.run(port=5001, debug=True)
