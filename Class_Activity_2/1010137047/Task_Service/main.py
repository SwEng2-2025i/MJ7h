from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

# Simulamos base de datos en memoria
tasks = []

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    new_task = {
        "id": str(uuid.uuid4()),
        "title": data.get("title"),
        "done": False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route("/tasks", methods=["GET"])
def list_tasks():
    return jsonify(tasks), 200

@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Tarea eliminada"}), 200

if __name__ == "__main__":
    app.run(port=5002, debug=True)
