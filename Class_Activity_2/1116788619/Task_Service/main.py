from flask import Flask, request, jsonify

app = Flask(__name__)

# Almacenamiento en memoria
tareas = {}
contador_tareas = 1

@app.route('/tasks', methods=['POST'])
def crear_tarea():
    global contador_tareas
    datos = request.get_json()
    if 'title' not in datos:
        return jsonify({'error': 'Falta el título de la tarea'}), 400
    
    task_id = str(contador_tareas)
    tareas[task_id] = {
        'id': task_id,
        'title': datos['title']
    }
    contador_tareas += 1
    return jsonify(tareas[task_id]), 201

@app.route('/tasks/<task_id>', methods=['DELETE'])
def eliminar_tarea(task_id):
    if task_id in tareas:
        del tareas[task_id]
        return jsonify({'message': f'Tarea {task_id} eliminada'}), 200
    else:
        return jsonify({'error': 'Tarea no encontrada'}), 404

@app.route('/tasks/<task_id>', methods=['GET'])
def obtener_tarea(task_id):
    if task_id in tareas:
        return jsonify(tareas[task_id]), 200
    else:
        return jsonify({'error': 'Tarea no encontrada'}), 404

@app.route('/tasks', methods=['GET'])
def listar_tareas():
    return jsonify(list(tareas.values())), 200

if __name__ == '__main__':
    app.run(port=5002, debug=True)
