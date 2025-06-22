## Estructura del Proyecto

Este proyecto está organizado en servicios independientes, cada uno en su carpeta correspondiente. También incluye los scripts de pruebas y los reportes generados.

## Estructura
```bash
1010137047/
├── Front-End/
│ ├── main.py # Interfaz web en Flask
│ └── templates/
│ └── index.html # Formulario HTML
├── Users_Service/
│ └── main.py # Servicio API para gestión de usuarios
├── Task_Service/
│ └── main.py # Servicio API para gestión de tareas
├── Test/
│ ├── BackEnd-Test.py # Prueba de integración de servicios backend
│ ├── FrontEnd-Test.py # Prueba simulando interacción desde frontend
│ └── test_report_generator.py # Script para generar reporte PDF automático
├── Test_Reports/ # Carpeta de reportes generados
├── requirements.txt # Librerías necesarias
└── README.md # Documentación del proyecto
```
## Cómo ejecutar

A continuación se describen los pasos para ejecutar correctamente el sistema y correr las pruebas de integración.

### 1. Instalar dependencias

Desde la carpeta raíz `1010137047/`, ejecuta:

```bash
pip install -r requirements.txt
```
### 2. Iniciar los servicios

* Terminal 1 – Servicio de usuarios
python Users_Service/main.py

* Terminal 2 – Servicio de tareas
python Task_Service/main.py

* Terminal 3 – Front-End web
python Front-End/main.py

Confirmar que los puertos estén escuchando:

Usuarios: http://localhost:5001
Tareas: http://localhost:5002
Interfaz web: http://localhost:5000

### 3. Ejecutar las pruebas

* Terminal 4 – Prueba de backend
python Test/BackEnd-Test.py

* Terminal 5 – Prueba de frontend
python Test/FrontEnd-Test.py

### 4. Verificar los reportes generados

Al finalizar cada prueba, se generará un reporte PDF numerado automáticamente dentro de la carpeta Test_Reports/.




