# Desarrollado Por:
# Santiago Restrepo Rojas
# CC: 1021665025

---

# Modificaciones realizadas al sistema para cumplir con los requisitos de la Actividad de Clase 2. 

Las características implementadas incluyen la limpieza de datos después de la ejecución de las pruebas y la generación automática de reportes en PDF.

## Secciones de Código Añadidas y Modificadas

### 1. Limpieza de Datos

Para garantizar que los datos generados durante las pruebas no persistan en el sistema, se implementaron las siguientes modificaciones:

#### Backend (`Users_Service` y `Task_Service`)

- **Nuevos Endpoints `DELETE`**:
  - Se añadió un endpoint `DELETE /users/<id>` en `Users_Service/main.py` para eliminar usuarios.
  - Se añadió un endpoint `DELETE /tasks/<id>` en `Task_Service/main.py` para eliminar tareas.

- **Actualización de Pruebas de Backend (`Test/BackEnd-Test.py`)**:
  - Las pruebas de integración ahora utilizan un bloque `try...finally` para asegurar que, sin importar el resultado de la prueba, los usuarios y tareas creados sean eliminados.
  - Se añadieron funciones `delete_user` y `delete_task` que llaman a los nuevos endpoints `DELETE`.
  - Después de la eliminación, las pruebas verifican que los recursos ya no existan, asegurando una limpieza efectiva.

#### Frontend (`Test/FrontEnd-Test.py`)

- **Limpieza Post-Prueba**:
  - Al igual que en el backend, el script de pruebas de frontend ahora incluye un bloque `try...finally`.
  - Después de que las pruebas de Selenium concluyen, se realizan llamadas directas a los endpoints `DELETE` de los servicios de backend para eliminar el usuario y la tarea creados.
  - Esto se maneja utilizando la librería `requests` dentro del script de prueba de Selenium.
  - Se modifico la funcion `crear_tarea` para que devuelva el `task_id` y poder usarlo para la eliminacion.

### 2. Generación Automática de Reportes en PDF

Para cumplir con el requisito de generar reportes de prueba, se realizaron los siguientes cambios:

- **Captura de Logs**:
  - La salida estándar (`stdout`) se redirige durante la ejecución de la prueba para capturar todos los logs, como la creación de usuarios, tareas y los resultados de las aserciones.

- **Generación de PDF**:
  - Se utilizó la librería `fpdf2` (añadida a `requirements.txt`) para crear un reporte en PDF.
  - Se implementó una función `generate_pdf_report` que guarda los logs capturados en un archivo PDF.
  - Los reportes se nombran con un número secuencial (ej. `Reporte_Pruebas_1.pdf`, `Reporte_Pruebas_2.pdf`, etc.) para evitar sobrescribir los resultados anteriores.

## Conclusión

Las modificaciones realizadas aseguran que el entorno de pruebas sea limpio y que los resultados de las pruebas se almacenen de forma persistente y organizada, cumpliendo con todos los requisitos de la actividad. 