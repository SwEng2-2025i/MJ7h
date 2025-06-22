# Class Activity 2 - Integration Testing  
**Estudiante:** Sergio Alejandro Nova Pérez  
**ID:** 1006739326

## Descripción

Este repositorio contiene la solución para la Actividad 2 de integración de sistemas, la cual consistió en extender un ejemplo de pruebas de integración para cumplir los siguientes objetivos:

- **Limpieza de datos:** Los datos generados por las pruebas se eliminan automáticamente al finalizar cada test, y se verifica que hayan sido correctamente eliminados.  
- **Generación automática de reporte PDF:** Al finalizar cada ejecución de prueba (tanto BackEnd como FrontEnd), se genera un archivo PDF secuencial con el resultado de los tests. Todos los reportes se conservan.

---

## Estructura de la Carpeta

Class_Activity_2/
└── 1006739326/
├── Example5-IntegrationTest/
│ ├── Front-End/
│ │ └── main.py
│ ├── Task_Service/
│ │ └── main.py
│ ├── Users_Service/
│ │ └── main.py
│ ├── Test/
│ │ ├── BackEnd-Test.py
│ │ ├── FrontEnd-Test.py
│ │ └── report.py
│ └── requirements.txt
└── README.md


---

## Archivos Principales

- **BackEnd-Test.py:** Prueba de integración que verifica la creación, consulta y limpieza de usuarios y tareas desde la API.
- **FrontEnd-Test.py:** Prueba E2E utilizando Selenium, que crea un usuario y tarea desde el Front-End, y luego elimina los datos creados.
- **report.py:** Módulo para generación automática de reportes en PDF.
- **requirements.txt:** Lista de dependencias necesarias.
- **main.py (Front-End, Task_Service, Users_Service):** Código de los microservicios.

---

## Mejoras y Cambios Realizados

- Se agregó lógica de **limpieza automática** (eliminación de usuario/tarea creados por la prueba).
- Se verifica tras la eliminación que los datos ya no existan (respuestas 404).
- Se implementó la **generación de PDF** para cada test, guardando cada reporte con un número secuencial para evitar sobreescritura.
- Se actualizaron los scripts para ser fácilmente ejecutables en entorno local.

---

## Instrucciones de Ejecución

1. **Instalar dependencias**
    ```bash
    pip install -r requirements.txt
    ```

2. **Levantar los tres microservicios** en terminales separadas:
    ```bash
    # Terminal 1
    cd Example5-IntegrationTest/Users_Service
    python main.py

    # Terminal 2
    cd Example5-IntegrationTest/Task_Service
    python main.py

    # Terminal 3 (Front-End)
    cd Example5-IntegrationTest/Front-End
    python main.py
    ```

3. **Ejecutar pruebas**

    - **BackEnd:**
      ```bash
      cd Example5-IntegrationTest/Test
      python BackEnd-Test.py
      ```

    - **FrontEnd:**  
      Asegúrate de tener [chromedriver](https://chromedriver.chromium.org/downloads) instalado y en tu PATH.
      ```bash
      cd Example5-IntegrationTest/Test
      python FrontEnd-Test.py
      ```

---

## Resultados

- Se generan archivos PDF dentro de la carpeta `reports/` mostrando el resultado y validación de cada test.
- Los datos generados por las pruebas se eliminan y se verifica su ausencia correctamente.



## Observaciones

- El código se adaptó solo con los cambios necesarios para cumplir los requisitos, manteniendo la estructura original del ejemplo.
- Para pruebas E2E, asegúrate de tener una versión compatible de `chromedriver` y Google Chrome.

---

## Secciones de código modificadas o agregadas

- Lógica de limpieza y verificación (`BackEnd-Test.py`, `FrontEnd-Test.py`)
- Generación de PDF (`report.py`)
- Actualización de `requirements.txt` para incluir dependencias de reportlab y selenium

---

**Fecha de entrega:** 21 de junio

---

