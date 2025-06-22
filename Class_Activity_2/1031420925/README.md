
# Prueba de Integración – Actividad de Clase 2

> Juan Esteban Cárdenas Huertas  
> jucardenash@unal.edu.co

## Descripción general

Esta actividad tiene como objetivo complementar el ejercicio de pruebas de integración visto en clase. Para ello, se implementaron las siguientes mejoras en el sistema:

- Se añadió un endpoint que permite eliminar usuarios en el microservicio `Users_Service`.
- Se incorporó también la opción de borrar tareas desde el microservicio `Task_Service`.
- El frontend fue modificado para incluir interfaces donde se pueda eliminar tanto usuarios como tareas por su identificador.
- Se garantiza que los datos utilizados durante las pruebas sean eliminados posteriormente, tanto en backend como frontend.
- Al final de cada prueba, se genera un reporte en PDF con gráficas, almacenado en la carpeta `/Test/reports`, con nombres numerados secuencialmente.

## Requisitos previos

- Python versión 3.8 o superior
- pip (administrador de paquetes)
- Git instalado

## Puesta en marcha del entorno

### Clonación del repositorio

```bash
git clone https://github.com/SwEng2-2025i/MJ7h.git
```

Después, entrar en la carpeta correspondiente a esta actividad:

```bash
cd ./Class_Activity_2/1031420925
```

### Creación del entorno virtual

```bash
python -m venv venv
```

Activar el entorno:

```bash
venv/Scripts/activate
```

Luego cambiar el intérprete de Python en tu editor (por ejemplo, en VS Code: Ctrl + P → "Python: Select Interpreter" → escoger el del entorno virtual).

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

### Ejecución de los servicios

#### Microservicio de usuarios

```bash
cd Users_Service
python main.py
```

#### Microservicio de tareas

```bash
cd Task_Service
python main.py
```

#### Interfaz gráfica (Frontend)

```bash
cd Front-End
python main.py
```

### Acceso desde navegador

Una vez activos los servicios, la aplicación se puede usar desde el navegador en la dirección:  
`http://localhost:5000`

## Ejecución de pruebas de integración

Ubicarse primero en el directorio `Test`:

```bash
cd Test
```

Para ejecutar únicamente pruebas de los microservicios del backend:

```bash
python BackEnd-Test.py
```

Para pruebas que incluyan tanto backend como frontend (E2E):

```bash
python FrontEnd-Test.py
```

Tras ejecutar las pruebas, se generan automáticamente informes en PDF con visualizaciones, los cuales se almacenan en la carpeta `/Test/reports`.

## Detalles de implementación

### Cambios en Users_Service

Se agregó una ruta tipo `DELETE` que permite eliminar un usuario con base en su ID:  
`DELETE http://localhost:5001/users/<userid>`

### Cambios en Task_Service

De forma análoga, se incorporó una ruta para eliminar tareas:  
`DELETE http://localhost:5002/tasks/<taskid>`

### Modificaciones en el Frontend

La plantilla HTML se actualizó para agregar formularios que permiten eliminar usuarios y tareas ingresando su identificador. Se añadió el código necesario para comunicar estas acciones con los microservicios correspondientes.

### Ajustes en las pruebas

Los scripts de pruebas fueron ampliados para cubrir las nuevas funcionalidades de eliminación. Luego de crear usuarios y tareas durante los tests, estos se eliminan como parte del flujo de prueba para mantener una base de datos limpia.

### Generación de reportes

Se utilizó la biblioteca `reportlab` para crear los informes en PDF. Para las gráficas, se integraron `matplotlib` y `numpy`.  
Una clase personalizada en el archivo `report_generator.py` se encarga de gestionar la creación y guardado de estos reportes.

## Conclusión

El sistema funciona correctamente con las nuevas funcionalidades agregadas. Las pruebas de integración se ejecutan satisfactoriamente y los reportes permiten hacer seguimiento del estado de cada ejecución.
