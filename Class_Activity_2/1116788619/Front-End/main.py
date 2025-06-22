from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

USER_SERVICE_URL = "http://localhost:5001/users"
TASK_SERVICE_URL = "http://localhost:5002/tasks"

HTML = '''
<!DOCTYPE html>
<html>
<head><title>Frontend App</title></head>
<body>
    <h1>Gestión de Usuarios y Tareas</h1>

    <h2>Crear Usuario</h2>
    <form action="/crear_usuario" method="post">
        Nombre: <input type="text" name="name">
        <input type="submit" value="Crear">
    </form>

    <h2>Eliminar Usuario</h2>
    <form action="/eliminar_usuario" method="post">
        ID Usuario: <input type="text" name="user_id">
        <input type="submit" value="Eliminar">
    </form>

    <h2>Crear Tarea</h2>
    <form action="/crear_tarea" method="post">
        Título: <input type="text" name="title">
        <input type="submit" value="Crear">
    </form>

    <h2>Eliminar Tarea</h2>
    <form action="/eliminar_tarea" method="post">
        ID Tarea: <input type="text" name="task_id">
        <input type="submit" value="Eliminar">
    </form>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    name = request.form.get('name')
    response = requests.post(USER_SERVICE_URL, json={'name': name})
    if "python-requests" in request.headers.get("User-Agent", ""):
        return response.text
    return f"{response.text}<br><a href='/'>Volver</a>"

@app.route('/eliminar_usuario', methods=['POST'])
def eliminar_usuario():
    user_id = request.form.get('user_id')
    response = requests.delete(f"{USER_SERVICE_URL}/{user_id}")
    return f"Respuesta: {response.text}<br><a href='/'>Volver</a>"

@app.route('/crear_tarea', methods=['POST'])
def crear_tarea():
    title = request.form.get('title')
    response = requests.post(TASK_SERVICE_URL, json={'title': title})
    if "python-requests" in request.headers.get("User-Agent", ""):
        return response.text
    return f"{response.text}<br><a href='/'>Volver</a>"

@app.route('/eliminar_tarea', methods=['POST'])
def eliminar_tarea():
    task_id = request.form.get('task_id')
    response = requests.delete(f"{TASK_SERVICE_URL}/{task_id}")
    return f"Respuesta: {response.text}<br><a href='/'>Volver</a>"

if __name__ == '__main__':
    app.run(port=5000, debug=True)
