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