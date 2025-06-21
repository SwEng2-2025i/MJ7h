Cambio 1 implementado:
En requirements.txt agregué la librerías faltantes:
pip install flask_cors selenium


Para hacer primera parte del taller, se hicieron nuevos metodos HTML para los servicios.

Primero se implemento el metodo de eliminar una tarea individual, dentro de task service:
@service_b.route('/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Tarea no encontrada'}), 404

        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': f'Tarea {task_id} eliminada correctamente'}), 200

Luego se hizo un metodo en users tasks con este detalle:
Para que el servicio de usuarios (service_a) verifique si el usuario tiene tareas asociadas en el tasks service antes de eliminarlo, debes:

    Agregar una ruta DELETE para /users/<int:user_id>.

    Hacer una solicitud GET al tasks service para consultar las tareas del usuario.

    Si tiene tareas asociadas, rechazar la eliminación con un error.

    Si no tiene tareas, proceder a eliminar al usuario.


Luego efectuamos los data clean up en el test de backend haciendo lo siguiente:
primero, agregar los metodos para la eliminacion de una tarea y un user:
def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()
    print(f"🗑️ Task {task_id} deleted")

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()
    print(f"🗑️ User {user_id} deleted")

luego, agregar estas lineal al final de la funcion integration test:
 #🔄 Step 4: Data clean up
    delete_task(task_id)
    delete_user(user_id)

Lo siguiente fue efectuar los cleanup para el test de frontend, haciendo lo siguiente:
Modificar crear_tarea() para devolver task_id, quedando algo así:
def crear_tarea(driver, wait, user_id):
    ...
    assert "Tarea creada con ID" in task_result.text
    task_id = ''.join(filter(str.isdigit, task_result.text))
    return task_id