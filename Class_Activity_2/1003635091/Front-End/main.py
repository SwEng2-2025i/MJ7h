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
      width: 100%;
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
    button.delete {
      background: #f44336;
    }
    button.delete:hover {
      background: #d32f2f;
    }
    button:hover {
      background: #45a049;
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
      margin-bottom: 6px;
      padding: 5px;
      background: #f9f9f9;
      border-radius: 3px;
      border-left: 3px solid #4CAF50;
    }
    .user-item {
      border-left-color: #2196F3;
    }
    .task-item {
      border-left-color: #FF9800;
    }
    .id-badge {
      background: #e0e0e0;
      padding: 2px 6px;
      border-radius: 10px;
      font-size: 12px;
      font-weight: bold;
      color: #666;
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

  <!-- Nueva sección para mostrar usuarios -->
  <div class="card">
    <h2>👥 Usuarios</h2>
    <button onclick='verUsuarios()'>Actualizar lista de usuarios</button>
    <ul id='users'></ul>
  </div>

  <div class="card">
    <h2>📋 Tareas</h2>
    <button onclick='verTareas()'>Actualizar lista de tareas</button>
    <ul id='tasks'></ul>
  </div>
  
  <!-- Sección para eliminar datos -->
  <div class="card">
    <h2>🗑️ Eliminar Datos</h2>
    
    <label>ID de Usuario a Eliminar:</label>
    <input id='delete-user-id' placeholder='Ej: 1'>
    <button class="delete" onclick='eliminarUsuario()'>Eliminar Usuario</button>
    <div id="delete-user-result" class="result"></div>
    
    <label>ID de Tarea a Eliminar:</label>
    <input id='delete-task-id' placeholder='Ej: 1'>
    <button class="delete" onclick='eliminarTarea()'>Eliminar Tarea</button>
    <div id="delete-task-result" class="result"></div>
  </div>

<script>
function crearUsuario() {
  const name = document.getElementById('username').value;
  fetch('http://localhost:5002/users', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({name})
  }).then(r => r.json()).then(data => {
    const result = document.getElementById('user-result');
    if (data.id) {
      result.textContent = `✅ Usuario creado con ID ${data.id}`;
      result.className = 'result';
      // Actualizar lista de usuarios automáticamente
      verUsuarios();
    } else {
      result.textContent = `❌ Error: ${data.error}`;
      result.className = 'error';
    }
  });
}

function crearTarea() {
  const title = document.getElementById('task').value;
  const user_id = document.getElementById('userid').value;
  fetch('http://localhost:5003/tasks', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({title, user_id})
  }).then(r => r.json()).then(data => {
    const result = document.getElementById('task-result');
    if (data.id) {
      result.textContent = `✅ Tarea creada con ID ${data.id}`;
      result.className = 'result';
      // Actualizar lista de tareas automáticamente
      verTareas();
    } else {
      result.textContent = `❌ Error: ${data.error}`;
      result.className = 'error';
    }
  });
}

function verUsuarios() {
  fetch('http://localhost:5002/users')
    .then(r => r.json())
    .then(data => {
      let ul = document.getElementById('users');
      ul.innerHTML = '';
      if (data.length === 0) {
        let li = document.createElement('li');
        li.innerText = 'No hay usuarios registrados';
        li.style.fontStyle = 'italic';
        li.style.color = '#666';
        ul.appendChild(li);
      } else {
        data.forEach(u => {
          let li = document.createElement('li');
          li.className = 'user-item';
          li.innerHTML = `<span class="id-badge">ID: ${u.id}</span> ${u.name}`;
          ul.appendChild(li);
        });
      }
    })
    .catch(error => {
      console.error('Error al cargar usuarios:', error);
      let ul = document.getElementById('users');
      ul.innerHTML = '<li style="color: red;">Error al cargar usuarios</li>';
    });
}

function verTareas() {
  fetch('http://localhost:5003/tasks')
    .then(r => r.json())
    .then(data => {
      let ul = document.getElementById('tasks');
      ul.innerHTML = '';
      if (data.length === 0) {
        let li = document.createElement('li');
        li.innerText = 'No hay tareas registradas';
        li.style.fontStyle = 'italic';
        li.style.color = '#666';
        ul.appendChild(li);
      } else {
        data.forEach(t => {
          let li = document.createElement('li');
          li.className = 'task-item';
          li.innerHTML = `<span class="id-badge">ID: ${t.id}</span> ${t.title} <em>(Usuario ID: ${t.user_id})</em>`;
          ul.appendChild(li);
        });
      }
    })
    .catch(error => {
      console.error('Error al cargar tareas:', error);
      let ul = document.getElementById('tasks');
      ul.innerHTML = '<li style="color: red;">Error al cargar tareas</li>';
    });
}

function eliminarUsuario() {
  const userId = document.getElementById('delete-user-id').value;
  fetch(`http://localhost:5002/users/${userId}`, {
    method: 'DELETE'
  }).then(r => {
    if (r.status === 200) return r.json();
    return r.json().then(error => { throw error; });
  }).then(data => {
    const result = document.getElementById('delete-user-result');
    result.textContent = `✅ ${data.message}`;
    result.className = 'result';
    // Actualizar listas automáticamente
    verUsuarios();
    verTareas();
  }).catch(error => {
    const result = document.getElementById('delete-user-result');
    result.textContent = `❌ Error: ${error.error || 'Error desconocido'}`;
    result.className = 'error';
  });
}

function eliminarTarea() {
  const taskId = document.getElementById('delete-task-id').value;
  fetch(`http://localhost:5003/tasks/${taskId}`, {
    method: 'DELETE'
  }).then(r => {
    if (r.status === 200) return r.json();
    return r.json().then(error => { throw error; });
  }).then(data => {
    const result = document.getElementById('delete-task-result');
    result.textContent = `✅ ${data.message}`;
    result.className = 'result';
    // Actualizar lista de tareas automáticamente
    verTareas();
  }).catch(error => {
    const result = document.getElementById('delete-task-result');
    result.textContent = `❌ Error: ${error.error || 'Error desconocido'}`;
    result.className = 'error';
  });
}

// Cargar datos iniciales al cargar la página
window.onload = function() {
  verUsuarios();
  verTareas();
};
</script>
</body>
</html>
'''

@frontend.route('/')
def index():
    return render_template_string(HTML)

if __name__ == '__main__':
    frontend.run(port=5001)
