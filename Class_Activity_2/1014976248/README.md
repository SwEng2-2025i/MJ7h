# 🧪 Laboratorio de Integración – Sistema de Microservicios con Reportes Automatizados

## ✅ Resumen del Proyecto

Este sistema implementa una arquitectura de microservicios en Flask compuesta por tres componentes principales: `User_Service`, `Task_Service` y `Front-End`, con pruebas automatizadas para BackEnd y FrontEnd. Además, genera reportes PDF de los resultados de prueba sin sobrescribir los anteriores.

---

## 📦 Estructura del Sistema

```
.
├── Front-End/
│   └── main.py                # Interfaz web HTML y lógica de interacción (creación, eliminación, verificación)
├── Task_Service/
│   └── main.py                # CRUD para tareas (con validación vía User_Service)
├── Users_Service/
│   └── main.py                # CRUD para usuarios
├── Test/
│   ├── BackEnd-Test.py        # Pruebas de integración backend (requests)
│   ├── FrontEnd-Test.py       # Pruebas E2E usando Selenium
│   ├── t_back.py              # Utilidad para generar PDF del backend
│   ├── t_front.py             # Utilidad para generar PDF del frontend
├── TestReports/
│   └── report_001.pdf, ...    # Reportes PDF generados automáticamente
```

---

## ⚙️ Funcionalidades Agregadas

### 1. **Lógica de eliminación automática de datos de prueba**

- `BackEnd-Test.py`: Se eliminan los datos creados tras la ejecución y se verifica su eliminación.
- `FrontEnd-Test.py`: Automatización de clicks para borrar tareas y usuarios desde la interfaz.

### 2. **Mensajes de verificación visual**

- Se muestran mensajes en pantalla luego de crear/eliminar entidades en `main.py` del Front-End.

### 3. **Botones de eliminación integrados**

- Añadido botón rojo de eliminación para tareas y usuarios (`main.py`, plantilla HTML).

### 4. **Generación automática de reportes PDF**

- `t_back.py` y `t_front.py`: Generadores de reportes PDF estilizados y numerados.
- Reportes se almacenan en `TestReports/` sin sobrescribir anteriores.

---

## 🧪 Pruebas Realizadas

### Backend (archivo: `BackEnd-Test.py`)

- Crear Usuario
- Crear Tarea
- Verificar creación
- Eliminar Usuario y Tarea
- Verificar eliminación
- Generación de PDF

### Frontend (archivo: `FrontEnd-Test.py`)

- Carga de página
- Creación de usuario y tarea vía Selenium
- Confirmación visual de acciones
- Verificación DOM
- Eliminación automática desde interfaz
- Verificación de backend en caso de doble limpieza
- Generación de PDF y .txt

---

## 📄 Archivos Clave Añadidos o Modificados

| Archivo                 | Cambio / Propósito                                 |
| ----------------------- | -------------------------------------------------- |
| `Front-End/main.py`     | Interfaz visual + lógica de creación y eliminación |
| `Users_Service/main.py` | Endpoint DELETE añadido y verificación GET         |
| `Task_Service/main.py`  | Validación cruzada con User_Service                |
| `BackEnd-Test.py`       | Limpieza + verificación + logging estructurado     |
| `FrontEnd-Test.py`      | Pruebas E2E Selenium + verificación + PDF          |
| `t_back.py`             | Reporte estilizado (resumen, tabla, errores)       |
| `t_front.py`            | Igual a t_back pero para pruebas de interfaz       |

---

## 🧾 Ejecución

```bash
# 1. Ejecutar servicios
python Users_Service/main.py
python Task_Service/main.py
python Front-End/main.py

# 2. Ejecutar pruebas de integración
python Test/BackEnd-Test.py
python Test/FrontEnd-Test.py

# 3. Ver reportes en carpeta TestReports/
```

---

## 🎯 Conclusión

Se logró construir un entorno completo de integración entre microservicios Flask con pruebas automatizadas, verificación visual e informes PDF estéticos y secuenciales.
