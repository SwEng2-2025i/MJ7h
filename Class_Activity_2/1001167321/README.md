# 🧪 Proyecto de Integración: Frontend + Servicios REST

Este proyecto integra un sistema distribuido compuesto por:

- **Frontend** en el puerto `5000`.
- **Microservicio de Usuarios** en el puerto `5001`.
- **Microservicio de Tareas** en el puerto `5002`.

## ✅ Reporte de Pruebas

Las pruebas automatizadas fueron ejecutadas exitosamente. A continuación, un resumen:

- **Pruebas correctas:**
  - Creación de usuario (`Ana`) → pasó.
  - Creación de tarea asignada al usuario → pasó.
  - Verificación de visualización de tarea → pasó.
  - Eliminación de tarea → pasó.
  - Eliminación de usuario → pasó.

- **Prueba negativa:**
  - Se intentó crear una tarea con un ID de usuario inválido.
  - El sistema respondió correctamente con error.
  - Esta prueba fue diseñada para **fallar a propósito** y verificar manejo de errores.

- **Reporte PDF:**  
  Se genera automáticamente un archivo `reporte.pdf` al finalizar las pruebas con los resultados detallados.

## 🚀 Nuevas Funcionalidades Implementadas

Se han añadido capacidades de eliminación tanto para usuarios como para tareas en los microservicios, y estas operaciones son accesibles desde el frontend.

### ⚙️ Servicios (`Users_Service/` y `Task_Service/`)

* **Capacidad de Eliminación:**
    * **`Users_Service`**: Ahora incluye un endpoint `DELETE /users/<int:user_id>` que permite borrar usuarios de la base de datos.
    * **`Task_Service`**: Se añadió un endpoint `DELETE /tasks/<int:task_id>` para eliminar tareas específicas de la base de datos.

### 🌐 Frontend (`Front-End/`)

* **Interfaz de Usuario para Eliminación:**
    * Se han incorporado **nuevas secciones intuitivas con campos de entrada y botones** para "Eliminar Usuario" y "Eliminar Tarea".
    * La lógica JavaScript subyacente (`eliminarUsuario()` y `eliminarTarea()`) gestiona las solicitudes `DELETE` a los servicios de backend y muestra los mensajes de confirmación o error directamente en la interfaz.

---

## 🧪 Pruebas Automatizadas

Se ha reforzado la suite de pruebas con la adición de funcionalidades de limpieza automática y un sistema de reporte PDF.

### 🛠️ Tests de Integración (`Test/`)

#### 🛠️ BackEnd Test (`BackEnd-Test.py`)

Este script valida la interacción directa entre los microservicios.

* **Limpieza Automática:**
    * Se crearon funciones `delete_task(task_id)` y `delete_user(user_id)` para eliminar programáticamente los datos creados durante cada ejecución de prueba.
* **Test de Falla Explícita (`create_task_invalid_user(user_id)`):**
    * Se añadió un test que intenta crear una tarea asignándola a un `user_id` que se sabe que **no existe**.
    * El test verifica que el `task_service` responda con el esperado error **`400 Bad Request`**, confirmando el correcto manejo de entradas inválidas.

### 🚀 FrontEnd Test (`FrontEnd-Test.py`)

Este script simula las interacciones del usuario directamente en el frontend.

* **Funcionalidad de Limpieza vía Frontend:**
    * Se implementaron las funciones `eliminar_tarea(driver, task_id)` y `eliminar_usuario(driver, task_id)`. Estas simulan los clics y entradas del usuario en la interfaz para activar la eliminación, y verifican que los mensajes de éxito sean mostrados.
    * Se añadió una aserción para confirmar que una tarea eliminada ya no aparece en la lista después de actualizarla.
* **Test de Falla (`crear_tarea_con_usuario_invalido(driver, wait, user_id)`):**
    * Esta prueba simula el intento de crear una tarea en el frontend usando un `ID de usuario inexistente`.
    * Verifica que la interfaz muestre el **mensaje de error correcto** y que el elemento de resultado tenga la clase CSS designada para errores.

### 2. 📄 Generación automática de reporte PDF

Archivo: `pdf_report.py`

```python
def generar_reporte_pdf(texto):
    ...
```

- Se usa `fpdf.FPDF()` para generar un archivo `reporte.pdf`.
- Guarda los resultados impresos en consola usando `io.StringIO()`.

En `FrontEnd-Test.py` y en `BackEnd-Test.py`, se añadió la funcionalidad y luego de cada ejecución de los scripts se ve reflejado el reporte pertienente.

---

## 📂 Estructura de Reportes

Todos los reportes PDF se guardan en la carpeta **`reportes/`**. Los nombres de los archivos siguen el formato: `reporte_<sequential number>.pdf`, asegurando la trazabilidad y la no sobrescritura.

---

## ▶️ Cómo ejecutar los tests

Instala las dependencias necesarias indicadas en el archivo `requirements.txt`:

```bash
pip install flask flask_sqlalchemy requests flask_cors selenium fpdf2
```

### Inicia los servicios

Abre una terminal para cada servicio y ejecuta:

```bash
cd Users_Service
python main.py
```

```bash
cd Task_Service
python main.py
```

```bash
cd Front-End
python main.py
```

### Ejecuta los tests desde la carpeta `Test`:

```bash
cd Test
python BackEnd-Test.py
python FrontEnd-Test.py
```

## 📄 Autor y licencia

Desarrollado por Tatiana Acelas