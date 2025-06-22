Funcionalidades recientes incorporadas
Con base en la evolución del proyecto y el uso práctico en escenarios de pruebas y ejecución, se han agregado dos nuevas funcionalidades clave para facilitar la gestión del estado del sistema y la generación de reportes visuales:

1. 🧹 Limpieza automática del sistema (borrar información de prueba)
Ahora el sistema permite eliminar automáticamente la información residual generada durante el uso del sistema o durante pruebas. Esta acción antes se hacía de forma manual eliminando las carpetas instance/.

Se ha implementado un nuevo endpoint (POST /clean) en el backend que elimina las carpetas instance/ de cada microservicio relevante.

En el frontend se ha añadido un botón accesible desde la interfaz que ejecuta esta limpieza con un solo clic, previa confirmación del usuario.

Esto permite dejar el sistema en un estado limpio sin intervención manual en el servidor ni en los archivos del proyecto.

🔐 Nota: esta funcionalidad puede ser protegida con autenticación o roles si se requiere en producción.

2. 📊 Generación de informe PDF con gráficas de resultados de pruebas
Para facilitar el seguimiento de las pruebas del sistema a usuarios no técnicos, se añadió una funcionalidad que permite:

Generar un informe en formato PDF que contiene una gráfica tipo torta (pie chart) o de barras, mostrando el número total de pruebas realizadas, cuántas fueron exitosas y cuántas fallaron.

Este informe se genera al visitar el endpoint GET /report y se guarda de forma permanente en el directorio reports/ del sistema.

Desde la interfaz, el usuario puede hacer clic en un botón que abre o descarga el archivo PDF generado.

📦 Librerías utilizadas: matplotlib, reportlab y flask.send_file.

✅ Resumen de nuevas rutas añadidas
Método	Ruta	Descripción
POST	/clean	Elimina carpetas instance/ para reiniciar el sistema a un estado limpio
GET	/report	Genera un informe en PDF con gráficas sobre resultados de pruebas realizadas

💡 Consideraciones
Asegúrate de que el backend tiene permisos de escritura sobre el directorio donde se generará el PDF.

Para ambientes productivos, se recomienda proteger estas rutas con mecanismos de autenticación o panel de administración.

Estas funcionalidades se integran manteniendo la modularidad y el enfoque por microservicios del sistema original.