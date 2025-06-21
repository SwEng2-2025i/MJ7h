from flask import Flask, render_template_string

frontend = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Laboratorio de Integración</title>
    <style>
        * { box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #f0f2f5; margin: 0; padding: 40px; display: flex; flex-direction: column; align-items: center; }
        h1 { margin-bottom: 30px; color: #333; }
        .card { background: white; border-radius: 10px; padding: 20px 30px; margin-bottom: 30px; width: 100%; max-width: 500px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        label { font-weight: bold; display: block; margin-top: 15px; }
        input { width: 100%; padding: 10px; margin-top: 5px; border-radius: 5px; border: 1px solid #ccc; }
        button { width: 100%; margin-top: 20px; padding: 10px; color: white; font-size: 16px; border: none; border-radius: 5px; cursor: pointer; transition: background 0.3s; }
        button.create-btn { background: #4CAF50; }
        button.create-btn:hover { background: #45a049; }
        button.delete-btn { background: #f44336; margin-top: 5px; } /* NUEVO */
        button.delete-btn:hover { background: #da190b; } /* NUEVO */
        .result { margin-top: 10px; color: green; font-weight: bold; }
        .error { margin-top: 10px; color: red; font-weight: bold; }
        ul { padding-left: 0; margin-top: 10px; list-style: none; } /* MODIFICADO */
        li { margin-bottom: 10px; background: #fafafa; padding: 10px; border-radius: 5px; display: flex; justify-content: space-between; align-items: center; } /* MODIFICADO */
    </style>
</head>
<body>
    <h1>🔧 Laboratorio de Integración</h1>

    <div class="card">
        <h2>👤 Crear Usuario</h2>
        <label>Nombre:</label>
        <input id='username' placeholder='Ej: Ana'>
        <button class="create-btn" onclick='crearUsuario()'>Crear Usuario</button>
        <div id="user-result" class="result"></div>
    </div>

    <div class="card">
        <h2>🗑️ Borrar Usuario</h2>
        <label>ID de Usuario a Borrar:</label>
        <input id='delete-userid' placeholder='Ej: 1'>
        <button class="delete-btn" onclick='borrarUsuario()'>Borrar Usuario</button>
        <div id="delete-user-result" class="result"></div>
    </div>

    <div class="card">
        <h2>📝 Crear Tarea</h2>
        <label>ID de Usuario:</label>
        <input id='userid' placeholder='Ej: 1'>
        <label>Título de la tarea:</label>
        <input id='task' placeholder='Ej: Terminar laboratorio'>
        <button class="create-btn" onclick='crearTarea()'>Crear Tarea</button>
        <div id="task-result" class="result"></div>
    </div>

    <div class="card">
        <h2>📋 Tareas</h2>
        <button class="create-btn" onclick='verTareas()'>Actualizar lista de tareas</button>
        <ul id='tasks'></ul>
    </div>

<script>
function crearUsuario() {
    const name = document.getElementById('username').value;
    fetch('http://localhost:5001/users', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name})
    }).then(r => r.json()).then(data => {
        const result = document.getElementById('user-result');
        if (data.id) {
            result.textContent = `✅ Usuario creado con ID ${data.id}`;
            result.className = 'result';
        } else {
            result.textContent = `❌ Error: ${data.error}`;
            result.className = 'error';
        }
    });
}

// --- NUEVO: Función para borrar usuario ---
function borrarUsuario() {
    const userId = document.getElementById('delete-userid').value;
    if (!userId) {
        alert('Por favor, ingresa un ID de usuario.');
        return;
    }
    fetch(`http://localhost:5001/users/${userId}`, {
        method: 'DELETE'
    }).then(r => r.json().then(data => ({status: r.status, body: data})))
      .then(res => {
        const result = document.getElementById('delete-user-result');
        if (res.status === 200) {
            result.textContent = `✅ ${res.body.message}`;
            result.className = 'result';
            verTareas(); // Actualizar la lista de tareas
        } else {
            result.textContent = `❌ Error: ${res.body.error}`;
            result.className = 'error';
        }
    });
}


function crearTarea() {
    const title = document.getElementById('task').value;
    const user_id = document.getElementById('userid').value;
    fetch('http://localhost:5002/tasks', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({title, user_id})
    }).then(r => r.json()).then(data => {
        const result = document.getElementById('task-result');
        if (data.id) {
            result.textContent = `✅ Tarea creada con ID ${data.id}`;
            result.className = 'result';
            verTareas(); // Actualizar la lista automáticamente
        } else {
            result.textContent = `❌ Error: ${data.error}`;
            result.className = 'error';
        }
    });
}

// --- NUEVO: Función para borrar tarea ---
function borrarTarea(taskId) {
    fetch(`http://localhost:5002/tasks/${taskId}`, {
        method: 'DELETE'
    }).then(r => {
        if(r.ok) {
            verTareas(); // Si se borra, refresca la lista
        } else {
            alert('Error al borrar la tarea');
        }
    });
}

function verTareas() {
    fetch('http://localhost:5002/tasks')
        .then(r => r.json())
        .then(data => {
            let ul = document.getElementById('tasks');
            ul.innerHTML = '';
            data.forEach(t => {
                let li = document.createElement('li');
                // MODIFICADO: Añadir botón de borrado a cada tarea
                li.innerHTML = `
                    <span>${t.title} (Usuario ID: ${t.user_id})</span>
                    <button class="delete-btn" onclick="borrarTarea(${t.id})">Borrar</button>
                `;
                ul.appendChild(li);
            });
        });
}

// Cargar tareas al iniciar
window.onload = verTareas;
</script>
</body>
</html>
'''

@frontend.route('/')
def index():
    return render_template_string(HTML)

if __name__ == '__main__':
    frontend.run(port=5000)