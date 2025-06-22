# Práctica: Integration Test (Class Activity 2)

## Descripción
Esta práctica consiste en la implementación y prueba de integración de un sistema distribuido en Python, compuesto por varios servicios independientes que interactúan entre sí. El sistema está diseñado para simular una arquitectura de microservicios y poner en práctica conceptos de integración y pruebas automatizadas.

### Características principales
- Arquitectura modular basada en microservicios.
- Servicios independientes para gestión de usuarios y tareas.
- Interfaz Front-End para interacción con el usuario.
- Comunicación entre servicios mediante peticiones HTTP.
- Pruebas automatizadas de integración para validar la interacción entre componentes.
- Generación de reportes de pruebas.
- Fácil despliegue y ejecución de cada servicio por separado.

## Estructura del Proyecto
- `Front-End/`: Interfaz principal del sistema.
- `Task_Service/`: Servicio encargado de la gestión de tareas.
- `Users_Service/`: Servicio encargado de la gestión de usuarios.
- `Test/`: Pruebas automatizadas para los servicios y reportes generados.
- `requirements.txt`: Dependencias necesarias para ejecutar el proyecto.

## Instalación
1. Clona este repositorio.
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución del Proyecto
Asegúrate de estar en la carpeta `1003864575` antes de ejecutar los servicios. Abre tres terminales diferentes y ejecuta en cada una:

```powershell
# Terminal 1
python .\Front-End\main.py

# Terminal 2
python .\Task_Service\main.py

# Terminal 3
python .\Users_Service\main.py
```

Cada servicio mostrará en consola un mensaje indicando que está corriendo y el puerto en el que escucha (por ejemplo, `Running on http://127.0.0.1:5000/`).

## Ejecución de Pruebas de Integración
Con los servicios en ejecución, abre una nueva terminal, navega a la carpeta `Test` y ejecuta:

```powershell
cd .\Test
python .\BackEnd-Test.py
python .\FrontEnd-Test.py
```

Los reportes de pruebas se guardarán en la carpeta `reports/` o `Test_Reports/` según la configuración.

Si tienes problemas de puertos ocupados, asegúrate de cerrar instancias previas de los servicios antes de volver a ejecutarlos.

## Autores
- [David Andres Alarcon Vargas "daalarconv@unal.edu.co" 1003864575]
Realmenten no pude hacerlo correr y verificar sus ejecuciones por tener desincronzadas mis extenciones en el computador de la casa pq viaje (lo siento)