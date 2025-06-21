Pruebas de Integración y Reporte Automático
Este proyecto incluye pruebas de integración automatizadas para los servicios de usuarios y tareas. 

Las pruebas realizan lo siguiente:

.Crean un usuario y una tarea usando los endpoints de los microservicios.

.Eliminan los datos creados durante la prueba.

.Verifican que los datos hayan sido correctamente eliminados del sistema.

.Generan automáticamente un reporte en PDF con los resultados de la prueba.

.Cada reporte PDF tiene un número secuencial y se guarda en la carpeta reports sin sobrescribir reportes anteriores.

¿Cómo ejecutar las pruebas?

-Asegúrate de que los servicios Users_Service (puerto 5001) y Task_Service (puerto 5002) estén corriendo.

-Ve a la carpeta Test y ejecuta
  python integration_test.py
  
-El resultado de la prueba se guardará en un archivo PDF dentro de la carpeta reports.
