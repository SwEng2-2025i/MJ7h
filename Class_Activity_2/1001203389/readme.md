````markdown
# Cambios Realizados

## Front-End (`Front-End/main.py`)
- **Estilos y estructura HTML/CSS**  
  - Se introdujeron clases `create-btn` y `delete-btn` para diferenciar botones de creación y borrado.  
  - Lista de tareas sin viñetas (`list-style: none`) y diseño flex para cada ítem (padding, fondo y botón de borrado alineado).  
- **Nueva funcionalidad JavaScript**  
  - `borrarUsuario()`: llama a `DELETE /users/{id}` y muestra mensaje de éxito o error.  
  - `borrarTarea(id)`: llama a `DELETE /tasks/{id}` tras pulsar el botón “Borrar” en cada ítem.  
  - Auto-refresh de la lista de tareas tras crear o borrar (`verTareas()`), y carga inicial al `window.onload`.

---

## Task_Service (`Task_Service/main.py`)
- **Nuevo endpoint**  
  ```http
  DELETE /tasks/<int:task_id>
````

* Elimina la tarea especificada y devuelve `{ "message": "Task with id X deleted successfully" }` o `404` si no existe.

---

## Users\_Service (`Users_Service/main.py`)

* **Nuevo endpoint**

  ```http
  DELETE /users/<int:user_id>
  ```

  * Elimina el usuario indicado y devuelve `{ "message": "User with id X deleted successfully" }` o `404` si no existe.
  * Se dejó comentada opción para eliminar tareas asociadas al usuario en cascada.

---

## Pruebas (`test/`)

* **`test_backend.py`**

  * Se añadieron funciones `delete_user()` y `delete_task()` para limpieza automática (cleanup) tras cada test.
* **`test_frontend.py`**

  * Integración de Selenium con Pytest para:

    * Creación y borrado de usuario y tarea desde la UI.
    * Asersión de que la tarea desaparece tras el borrado.
* **`FrontEnd-Test.py`**

  * Script standalone E2E adaptado al nuevo flujo: crea usuario, crea tarea, verifica y finaliza.
* **`test_force_failure`**

  * Test intencional que falla para generar ejemplos de reporte de errores.

