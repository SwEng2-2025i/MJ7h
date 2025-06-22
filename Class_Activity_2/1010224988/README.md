# Informe Breve del Proyecto de Automatización de Pruebas

## ✅ Resumen de Resultados

- Se implementaron correctamente pruebas de integración backend y pruebas frontend.
- Las pruebas generan reportes automáticos en formato PDF que indican los resultados, los IDs creados y la confirmación de eliminación de datos.

## 📌 Secciones de Código Agregadas

- `generate_pdf_report()`: generacion de reportes en archivo pdf (BackEnd-Test.py)
- `delete_tasks()`: Eliminacion de las tareas creadas durante la ejecucion del modulo de pruebas (BackEnd-Test.py) 
- `delete_users()`: Eliminacion de los usuarios creados durante la ejecucion del modulo de pruebas (BackEnd-Test.py)

- `generate_frontend_pdf_report()`: generacion de reportes en archivo pdf (FrontEnd-Test.py)
- `delete_tasks()`: Eliminacion de las tareas creadas durante la ejecucion del modulo de pruebas (FrontEnd-Test.py)
- `delete_users()`: Eliminacion de los usuarios creados durante la ejecucion del modulo de pruebas (FrontEnd-Test.py)

- Eliminación automática de los datos creados durante las pruebas
- Carpeta `test_reports/` donde se almacenan todos los reportes PDF generados tanto del frontend como del backend
