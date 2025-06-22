# Aplicación de Tareas — Informe de Integración

### Estudiante: Nicolás Zuluaga Galindo

## Introducción

Las **pruebas de integración** resultan fundamentales en el desarrollo de software moderno, donde múltiples servicios deben comunicarse de forma correcta y segura. La alta interconexión entre APIs, bases de datos y la interfaz de usuario hace imprescindible validar el flujo completo de la aplicación, desde el front-end hasta el back-end, con el fin de garantizar que cualquier cambio no afecte la experiencia del usuario.

## Modificaciones al proyecto inicial

Con el objetivo de reforzar la calidad y la estabilidad del sistema, el proyecto original fue adaptado de la siguiente manera:

1. **Limpieza de datos tras las pruebas**: se añadieron operaciones que eliminan automáticamente los registros creados en las dos bases de datos (`users.db` y `tasks.db`) al finalizar cada ejecución de pruebas, asegurando un entorno limpio y reproducible.
2. **Pruebas de backend**: se definieron casos de integración en `Test/backend/test_backend_api.py` que:

   - Crean un usuario y una tarea mediante la API.
   - Verifican su creación y asociación.
   - Invocan los endpoints `DELETE` para eliminar los datos.
   - Validan que la limpieza se lleve a cabo correctamente.

3. **Pruebas E2E de frontend**: se implementaron pruebas end-to-end en `Test/e2e_frontend/test_frontend_e2e.py` utilizando **Selenium** para emular el comportamiento del usuario final:

   - Se automatiza un navegador para la creación de usuarios y tareas desde la UI.
   - Se comprueban los resultados tanto en la interfaz gráfica como a través de la API.
   - Se aplica la misma lógica de limpieza y verificación de datos.

## Nuevos endpoints para limpieza de datos

Para habilitar el borrado controlado de registros, se incorporaron en cada servicio los siguientes endpoints:

- **Task Service** (`Task_Service/main.py`):

  ```python
  @service_b.route('/tasks/<int:task_id>', methods=['DELETE'])
  def delete_task(task_id):
      # Elimina una tarea según su ID
  ```

- **User Service** (`Users_Service/main.py`):

  ```python
  @service_a.route('/users/<int:user_id>', methods=['DELETE'])
  def delete_user(user_id):
      # Elimina un usuario según su ID
  ```

Ambos endpoints se definen antes del arranque del servidor Flask, garantizando su disponibilidad en cada ejecución.

## Reportes automáticos

Se configuró un hook de pytest (`pytest_sessionfinish`) encargado de generar informes en formato PDF numerados de forma secuencial (`report_001.pdf`, `report_002.pdf`, ...) en la carpeta `reports/`. Cada informe contiene:

- Título con el nombre de la aplicación y número de informe.
- Fecha y resumen global de pruebas (total de casos, pasados y fallidos).
- Secciones separadas para **Backend** y **Frontend**, cada una con:

  - Descripción de los objetivos de las pruebas.
  - Tabla detallada de casos (número, características del test, resultado).
  - Calificación (score) de sección (porcentaje de éxito).

Este mecanismo facilita la difusión del estado de la aplicación ante stakeholders y personal interesado.

## Instalación y configuración

Para reproducir el entorno, se deben seguir estos pasos:

1. Clonar el repositorio:

   ```bash
   git clone <URL-del-proyecto>
   cd <directorio>
   ```

2. Crear y activar un entorno virtual:

   ```bash
   python -m venv env
   # Linux / macOS
   ```

env/bin/activate

# Windows

env\Scripts\activate

````
3. Instalar las dependencias:
```bash
pip install -r requirements.txt
````

Las librerías clave son:

- `pytest`
- `selenium`
- `requests`
- `reportlab`

## Ejecución de servicios

En diferentes terminales, iniciar los microservicios y la interfaz:

```bash
# Service de usuarios
cd Users_Service
python main.py

# Service de tareas
cd Task_Service
python main.py

# Front-End
cd Front-End
python main.py
```

## Ejecución de pruebas y consulta de resultados

Con los servicios en ejecución y desde la raíz del proyecto, lanzar:

```bash
pytest -q
```

- Las pruebas se ejecutarán en el orden **Backend → Frontend**.
- El informe en PDF se encontrará en `reports/report_XXX.pdf`.

Abrir el PDF para revisar el detalle de cada sección y el estado de las pruebas.

---

_Este documento describe las adaptaciones realizadas para asegurar la calidad del flujo de integración y la generación de informes automáticos._
