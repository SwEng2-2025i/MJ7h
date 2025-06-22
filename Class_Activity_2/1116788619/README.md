
# Práctica Integration Test (class activity 2)

> Wullfredo Javier Barco Godoy - wbarco@unal.edu.co  
> Ingeniería de Software II - Universidad Nacional de Colombia

## Descripción de la actividad

En esta actividad se amplió el ejemplo de prueba de integración revisado en clase, implementando las siguientes funcionalidades:

- Endpoint para eliminar usuarios en el servicio `Users_Service`.
- Endpoint para eliminar tareas en el servicio `Task_Service`.
- Interfaz web (frontend) para crear y eliminar usuarios y tareas.
- Limpieza automática de datos creados por las pruebas (tanto en backend como frontend).
- Generación de reportes automáticos en PDF en cada ejecución de prueba.

## Estructura del proyecto

```
1116788619/
├── Front-End/
│   └── main.py
├── Task_Service/
│   └── main.py
├── Users_Service/
│   └── main.py
├── Test/
│   ├── BackEnd-Test.py
│   ├── FrontEnd-Test.py
│   ├── report_generator.py
│   └── reports/
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.8+
- pip

## Instalación

Crear y activar entorno virtual:

```bash
python -m venv venv
venv/Scripts/activate     # En Windows
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

### Iniciar servicios

Ejecutar cada servicio en terminales diferentes:

```bash
# Servicio de usuarios
cd Users_Service
python main.py
```

```bash
# Servicio de tareas
cd Task_Service
python main.py
```

```bash
# Frontend
cd Front-End
python main.py
```

### Acceder al frontend

Visitar `http://localhost:5000` en el navegador para usar la interfaz de usuario.

### Ejecutar pruebas de integración

```bash
cd Test
python BackEnd-Test.py
python FrontEnd-Test.py
```

Cada prueba genera un archivo PDF con los resultados en la carpeta `Test/reports/`.

## Cambios implementados

### `Users_Service/main.py`

- Se agregó `POST /users` y `DELETE /users/<user_id>` para gestión de usuarios en memoria.

### `Task_Service/main.py`

- Se agregó `POST /tasks` y `DELETE /tasks/<task_id>` para gestión de tareas en memoria.

### `Front-End/main.py`

- Interfaz HTML con formularios para crear y eliminar usuarios y tareas.
- Conecta con los microservicios mediante `requests`.

### `Test/BackEnd-Test.py`

- Pruebas de creación y eliminación directa por API REST.
- Verificación y limpieza de datos.
- Generación de reporte PDF con gráfica y resumen.

### `Test/FrontEnd-Test.py`

- Pruebas E2E completas desde el frontend.
- Validación de operaciones y limpieza vía backend.
- Generación de segundo reporte PDF.

### `report_generator.py`

- Crea archivos PDF secuenciales (`report_1.pdf`, `report_2.pdf`, ...).
- Incluye fecha, resumen textual y gráfica con `matplotlib`.

## Resultados

- Las pruebas automáticas se ejecutan correctamente.
- Los reportes PDF generados demuestran la trazabilidad y limpieza de datos.
- La interfaz web permite probar manualmente las funciones implementadas.
