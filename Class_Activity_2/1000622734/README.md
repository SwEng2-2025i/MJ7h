# Class Activity 2

Realizado por Fabián Alejandro Torres Ramos, `fatorresra@unal.edu.co`, en base al ejemplo de tests de integración que se encuentra en [este link](https://github.com/SwEng2-2025i/SwEng2_2025i_Examples/tree/main/Example%205%20-%20Integration%20Test).

## Funcionalidades implementadas

### Limpieza de datos

Se agregó un endpoint a los servicios de usuarios y tareas para permitir la eliminación de algún usuario/tarea en base al ID, junto a campos en el frontend para realizar estas peticiones. En el frontend también se incluye una sección para ver la lista de usuarios y se muestra la ID de cada tarea en la lista de tareas.

Se agregaron funciones en ambos tipos de tests para eliminar los datos de prueba ingresados, y los mensajes de éxito/error respectivos.

### Generación de reportes en PDF

Se usa un búfer para guardar las impresiones de consola y mediante la librería `fPDF` esto se exporta a un archivo PDF que se guarda en la carpeta `./Test/results/` con nombre secuencial. Por las limitaciones de esta librería los emojis no se codifican correctamente, pero se mantienen todos los mensajes de los tests.