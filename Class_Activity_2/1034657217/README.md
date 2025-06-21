# Práctica Integration Test (class activity 2)

> Martin Moreno Jara mamorenoj@unal.edu.co

## Descripción de la actividad

En esta actividad se completa el ejemplo presentado en clase sobre test de
integración, añadiendo las siguientes características:

- Endpoint para eliminar usuarios en el servicio `Users_Service`.
- Endpoint para eliminar tareas en el servicio `Task_Service`.
- Actualización del frontend para incluir secciones para eliminar usuario y
  servicio por id.
- Eliminación de los datos creados durante las pruebas, tanto de backend como de
  frontend.
- Generación de reportes en formato pdf con gráficas en la carpeta
  `/Test/reports` con numeración sucesiva.

## Requisitos

- Python 3.8+
- pip (gestor de paquetes de Python)
- Git

## Setup

### Clonar repositorio

```bash
git clone https://github.com/SwEng2-2025i/MJ7h.git
```

Luego ubicarse en el directorio de esta actividad.

```bash
cd ./Class_Activity_2/1034657217
```

### Crear entorno virtual

```bash
python -m venv venv
```

```bash
venv/Scripts/activate
```

Cambiar intérprete de Python (crtl + P, luego select python interpreter y
escoger la ruta del entorno virtual).

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Inciar servicios

#### Servicio de usuarios

Ubicarse en el directorio `Users_Service`.

```bash
cd Users_Service
```

ejectuar main.py

```bash
python main.py
```

#### Servicio de tareas

Ubicarse en el directorio `Task_Service`.

```bash
cd Task_Service
```

ejectuar main.py

```bash
python main.py
```

#### Frontend

Ubicarse en el directorio `Front-End`.

```bash
cd Front-End
```

ejectuar main.py

```bash
python main.py
```

### Probar en el navegador

El proyecto se puede probar desde el frontend, en la url `localhost:5000`

### Pruebas de integración

Para ejecutar las pruebas de integración de los servicios del backend y el
frontend, primero ubicarse en el directorio `Test`.

```bash
cd Test
```

Se pueden ejecutar pruebas de integración entre los servicios del backen, o
incluyendo el frontend. Para cada tipo de prueba, se ejecuta su respectivo
archivo.

Para pruebas de integración del backend

```bash
python BackEnd-Test.py
```

Para pruebas E2E del backend y el frontend

```bash
python FrontEnd-Test.py
```

Después de ejecutar cada tipo de prueba, se genera su respectivo informe en el
directorio de`/Test/reports`.

## Cambios y adiciones en el código

### cambios en Users_Service

Se agregó un endpoint para la eliminicación de un usuario según su id.
`DELETE localhost:5001/users/<userid>`

### cambios en Task_Service

Se agregó un endpoint para la eliminicación de una tarea según su id.
`DELETE localhost:5002/tasks/<taskid>`

### cambios en Front-End

Se actualizó la plantilla html para incluir secciones para la eliminación de
tareas y usuarios. Asimismo, se actualizó la parte del script para que se
conecté con los servicios y haya funcionalidad.

### Actualización de los tests

Para ambos casos se agregaron funciones para probar las nuevas funcionalidades
de eliminar tarea y usuario y se aplicaron en el flujo de las pruebas para ser
ejecutadas después de hacer la creación. Se hace para probar la funcionalidad y
no alterar la base de datos con las pruebas.

### Reportes

Se utilizó la libreria `reportlab` para generar los reportes en pdf, junto con
otras dependencias para generar gráficas (`matplotlib`, `numpy`).

Se creo una clase para crear los reportes en `report_generator.py` y esta se
utiliza en el flujo de las pruebas de integración para luego guardar el reporte
en la carpeta `/Test/reports`

## Resultados

La aplicación es funcional y pasa los test de integración. También se puede ver
la trazabilidad de los mismos en los reportes.
