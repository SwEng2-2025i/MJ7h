# **Actividad de Clase 2 – Pruebas de Integración con Limpieza y Reportes PDF**


## 🧪 Descripción general

Esta actividad extiende el ejemplo de pruebas de integración trabajado en clase, implementando:

1. Limpieza de los datos creados durante la ejecución de las pruebas (sin afectar otros datos).
2. Generación automática de reportes PDF con los resultados de cada ejecución.
3. Inclusión de pruebas fallidas de forma controlada para validar el reporte.

---

## 🧱 Estructura del sistema

- `Users_Service/main.py`: Servicio Flask que gestiona usuarios.
- `Task_Service/main.py`: Servicio Flask que gestiona tareas asociadas a usuarios.
- `Front-End/main.py`: Servicio Flask que ofrece la interfaz gráfica.
- `Test/BackEnd-Test.py`: Test de integración de backend.
- `Test/Frontend_Test.py`: Test de extremo a extremo del frontend con Selenium.
- `reports/`: Almacena los reportes PDF generados por los tests.

---

## ✅ Cambios realizados

### 🔧 Backend (servicios)

#### `Users_Service/main.py`
- Se agregó un endpoint `DELETE /users/<id>` para permitir la eliminación de usuarios creados durante pruebas.

#### `Task_Service/main.py`
- Se agregó un endpoint `DELETE /tasks/<id>` para permitir la eliminación de tareas creadas durante pruebas.

### 🧪 Tests

#### `Test/BackEnd-Test.py`
- Se añadió limpieza automática de la tarea y usuario creados durante el test.
- Se validó que los datos fueran correctamente eliminados.
- Se implementó la generación de un PDF automático con numeración (`backend_report_#.pdf`).
- Se añadió intencionalmente un test fallido (verificación de cantidad de tareas) para comprobar la aparición de errores en el reporte.

#### `Test/Frontend_Test.py`
- Se utilizó Selenium para automatizar la creación de usuario, tarea y consulta desde la interfaz web.
- Se limpió automáticamente el usuario y tarea creados desde el backend.
- Se verificó que los datos hubieran sido eliminados correctamente.
- Se generó un PDF de resultados numerado (`frontend_report_#.pdf`).
- Se incluyó intencionalmente una aserción fallida para simular un error controlado.

---

## 📂 Archivos modificados o añadidos

| Archivo              | Modificación                                                |
|----------------------|-------------------------------------------------------------|
| `Users_Service/main.py`       | Agregado endpoint DELETE `/users/<id>`                      |
| `Task_Service/main.py`       | Agregado endpoint DELETE `/tasks/<id>`                      |
| `Test/BackEnd-Test.py`| Limpieza, verificación, PDF y test fallido                  |
| `Test/Frontend_Test.py`   | Limpieza, verificación, PDF y test fallido                  |
| `reports/`           | Carpeta creada automáticamente para almacenar los reportes  |
| `README.md`          | Este archivo                                                 |

---
## **Inicio Rápido**

### 1. 📦 Instalar dependencias

`pip install flask flask_sqlalchemy flask_cors requests fpdf selenium`

### 2. 🚀 Ejecutar los servicios

```
# Terminal 1 - Users_Service (puerto 5001)
python main.py

# Terminal 2 -Task_Service (puerto 5002)
python main.py

# Terminal 3 - Front-End (puerto 5000)
python main.py
```
### 3. 🧪 Ejecutar pruebas

### **Test de backend:** 

`BackEnd-Test.py`

### **Test de frontend**

`FrontEnd-Test.py`


### 4. 📄 Ver resultados

```
reports/backend_report_1.pdf
reports/frontend_report_1.pdf
```


