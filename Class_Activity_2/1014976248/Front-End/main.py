from flask import Flask, render_template_string

frontend = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Laboratorio de Integración</title>
  <style>
    * {
      box-sizing: border-box;
    }
    body {
      font-family: 'Segoe UI', sans-serif;
      background: #f0f2f5;
      margin: 0;
      padding: 40px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    h1 {
      margin-bottom: 30px;
      color: #333;
    }
    .card {
      background: white;
      border-radius: 10px;
      padding: 20px 30px;
      margin-bottom: 30px;
      width: 100%;
      max-width: 500px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    label {
      font-weight: bold;
      display: block;
      margin-top: 15px;
    }
    input {
      width: 100%;
      padding: 10px;
      margin-top: 5px;
      border-radius: 5px;
      border: 1px solid #ccc;
    }
    button {
      margin-top: 20px;
      padding: 10px;
      background: #4CAF50;
      color: white;
      font-size: 16px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      transition: background 0.3s;
    }
    button:hover {
      background: #45a049;
    }
    .btn-eliminar {
      margin-left: 10px;
      background: #d9534f;
      padding: 6px 10px;
      font-size: 14px;
      color: white;
      border: none;
      border-radius: 5px;
    }
    .btn-eliminar:hover {
      background: #c9302c;
    }
    .result {
      margin-top: 10px;
      color: green;
      font-weight: bold;
    }
    .error {
      margin-top: 10px;
      color: red;
      font-weight: bold;
    }
    ul {
      padding-left: 20px;
      margin-top: 10px;
    }
    li {
      margin-bottom: 10px;
    }
  </style>
</head>
<body>
  <h1>🔧 Laboratorio de Integración</h1>

  <div class="card">
    <h2>👤 Crear Usuario</h2>
    <label>Nombre:</label>
    <input id='username' placeholder='Ej: Ana'>
    <button onclick='crearUsuario()'>Crear Usuario</button>
    <div id="user-result" class="result"></div>
  </div>

  <div class="card">
    <h2>📝 Crear Tarea</h2>
    <label>ID de Usuario:</label>
    <input id='userid' placeholder='Ej: 1'>
    <label>Título de la tarea:</label>
    <input id='task' placeholder='Ej: Terminar laboratorio'>
    <button onclick='crearTarea()'>Crear Tarea</button>
    <div id="task-result" class="result"></div>
  </div>

  <div class="card">
    <h2>📋 Tareas</h2>
    <button onclick='verTareas()'>Actualizar lista de tareas</button>
    <ul id='tasks'></ul>
    <div id="task-delete-result" class="result"></div>
  </div>

  <div class="card">
    <h2>🗑️ Eliminar Usuario</h2>
    <label>ID del Usuario a eliminar:</label>
    <input id='delete-user-id' placeholder='Ej: 1'>
    <button class="btn-eliminar" onclick='eliminarUsuario()'>Eliminar Usuario</button>
    <div id="delete-user-result" class="result"></div>
  </div>


<script>
let lastUserId = null;

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
      lastUserId = data.id;
      document.getElementById('userid').value = data.id;
      document.getElementById('delete-user-id').value = data.id;
      document.getElementById('username').value = '';

      // ✅ Solo inicia el flujo automático una vez
      if (!flujoAutomaticoEjecutado) {
        flujoAutomaticoEjecutado = true;
        setTimeout(() => crearTarea(), 500);
      }
    } else {
      result.textContent = `❌ Error: ${data.error}`;
      result.className = 'error';
    }
  });
}

function crearTarea() {
  const title = document.getElementById('task').value || "Tarea automática";
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
      document.getElementById('task').value = '';
      verTareas();

      // Eliminar tarea automáticamente
      setTimeout(() => {
        const botones = document.querySelectorAll("button.btn-eliminar");
        for (const btn of botones) {
          if (btn.onclick && btn.onclick.toString().includes(`${data.id}`)) {
            btn.click();
            break;
          }
        }
      }, 1000);

      // Eliminar usuario automáticamente
      setTimeout(() => {
        const btnEliminarUsuario = document.querySelector("button[onclick='eliminarUsuario()']");
        if (btnEliminarUsuario) {
          btnEliminarUsuario.click();
        }
      }, 2000);
    } else {
      result.textContent = `❌ Error: ${data.error}`;
      result.className = 'error';
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
        li.innerHTML = `${t.title} (Usuario ID: ${t.user_id})
          <button class="btn-eliminar" onclick="eliminarTarea(${t.id})">Eliminar</button>`;
        ul.appendChild(li);
      });
    });
}

function eliminarTarea(id) {
  fetch(`http://localhost:5002/tasks/${id}`, {
    method: 'DELETE'
  })
  .then(response => {
    if (response.ok) {
      document.getElementById('task-delete-result').textContent = `✅ Tarea ${id} eliminada`;
      document.getElementById('task-delete-result').className = 'result';
      verTareas();
    } else {
      document.getElementById('task-delete-result').textContent = `❌ Error al eliminar tarea ${id}`;
      document.getElementById('task-delete-result').className = 'error';
    }
  });
}

function eliminarUsuario() {
  const userId = document.getElementById('delete-user-id').value;
  fetch(`http://localhost:5001/users/${userId}`, {
    method: 'DELETE'
  })
  .then(response => {
    if (response.ok) {
      document.getElementById('delete-user-result').textContent = `✅ Usuario ${userId} eliminado`;
      document.getElementById('delete-user-result').className = 'result';

      // 🧹 Limpia campos relacionados
      document.getElementById('userid').value = '';
      document.getElementById('delete-user-id').value = '';
      document.getElementById('task').value = '';

      // 🧼 Limpia resultados anteriores (opcional)
      document.getElementById('task-result').textContent = '';
      document.getElementById('task-delete-result').textContent = '';

      verTareas();
    } else {
      return response.json().then(err => {
        document.getElementById('delete-user-result').textContent = `❌ ${err.error}`;
        document.getElementById('delete-user-result').className = 'error';
      });
    }
  })
  .catch(error => {
    document.getElementById('delete-user-result').textContent = `❌ Error de red`;
    document.getElementById('delete-user-result').className = 'error';
  });
}

</script>
</body>
</html>
'''


@frontend.route('/')
def index():
    return render_template_string(HTML)

if __name__ == '__main__':
    frontend.run(port=5000)
