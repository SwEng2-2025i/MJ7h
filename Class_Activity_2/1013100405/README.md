# 🧪 Class Activity 2: Integration Test

### Estudiante: Estephanie Pérez Mira

Este taller implementa pruebas automáticas con limpieza de datos y generación de reportes en PDF para un sistema compuesto por dos servicios: **Users Service** y **Tasks Service**, además de una interfaz web de frontend.

---

## 📦 Requisitos

A priori, se agregaron estas dependencias faltantes al archivo `requirements.txt`:

```
pip install flask_cors selenium reportlab
```

---

## 🧹 Cambios Implementados: Data clean up

### 1. Eliminación de Tareas Individuales

Se agregó al **Tasks Service** un endpoint para eliminar una tarea por su ID:

```python
@service_b.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Tarea no encontrada'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': f'Tarea {task_id} eliminada correctamente'}), 200
```

---

### 2. Validación antes de eliminar un usuario

El **Users Service** ahora se comunica con el **Tasks Service** para verificar si un usuario tiene tareas asociadas antes de permitir su eliminación:

Pasos realizados:
- Se creó un endpoint `DELETE /users/<user_id>`.
- Se hizo una consulta GET al servicio de tareas.
- Si el usuario tiene tareas, se rechaza la eliminación.
- Si no tiene tareas, se elimina exitosamente.
```python
@service_a.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    try:
        response = requests.get('http://localhost:5002/tasks')
        response.raise_for_status()
        tasks = response.json()
    except Exception as e:
        return jsonify({'error': f'No se pudo verificar las tareas: {str(e)}'}), 500

    user_tasks = [t for t in tasks if t["user_id"] == user_id]

    if user_tasks:
        return jsonify({'error': 'No se puede eliminar el usuario. Tiene tareas asociadas.'}), 400

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'Usuario {user_id} eliminado correctamente'}), 200
```

---
### 3. Limpieza de datos al final de la prueba de Integración Backend

Se agregaron funciones para eliminar la tarea y el usuario:

```python
def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()
```

Y se usaron al final de `integration_test()`:

```python
def integration_test():
    ...
    # 🔄 Limpieza de datos
    delete_task(task_id)
    delete_user(user_id)
```

---

### 4. Devolver el ID de la tarea creada en test Frontend

Se modificó la función `crear_tarea()` para retornar el ID:

```python
def crear_tarea(driver, wait, user_id):
    ...
    task_id = ''.join(filter(str.isdigit, task_result.text))
    return task_id
```

### 5. Limpieza de datos al final de test Frontend
Se modificó `main()` de esta manera:

```python
def main():
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    task_id = None
    user_id = None

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait)
        task_id = crear_tarea(driver, wait, user_id)
        ver_tareas(driver)
        time.sleep(2)
    finally:
        driver.quit()  # Siempre cierra el navegador

        # 🔄 Limpiar datos si fueron creados
        if task_id:
            try:
                response = requests.delete(f"http://localhost:5002/tasks/{task_id}")
                print(f"🗑️ Tarea {task_id} eliminada: {response.status_code}")
            except Exception as e:
                print(f"❌ Error al eliminar la tarea: {e}")

        if user_id:
            try:
                response = requests.delete(f"http://localhost:5001/users/{user_id}")
                print(f"🗑️ Usuario {user_id} eliminado: {response.status_code}")
            except Exception as e:
                print(f"❌ Error al eliminar el usuario: {e}")
```

---

## 📝 Cambios Implementados: Generación de Reportes PDF

### 🗂️ Ubicación de reportes

Todos los reportes se guardan secuencialmente en la carpeta:  
`Test/test_reports/`

---

### 1. Función general para crear reportes PDF

Función usada en frontend:

```python
def generar_reporte_pdf(contenido):
    carpeta = "test_reports"
    os.makedirs(carpeta, exist_ok=True)
    existentes = [f for f in os.listdir(carpeta) if f.startswith("reporte_test_") and f.endswith(".pdf")]
    numeros = [int(f.split("_")[-1].replace(".pdf", "")) for f in existentes]
    siguiente = max(numeros) + 1 if numeros else 1
    nombre_archivo = f"reporte_test_{siguiente:03}.pdf"
    ruta_completa = os.path.join(carpeta, nombre_archivo)

    c = canvas.Canvas(ruta_completa, pagesize=LETTER)
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, "Reporte de pruebas E2E - Frontend")
    c.drawString(50, 730, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, 710, f"Reporte N° {siguiente}")

    y = 690
    for linea in contenido.splitlines():
        c.drawString(50, y, linea)
        y -= 20
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = 750

    c.save()
    print(f"✅ Reporte generado: {ruta_completa}")
```

Función usada en backend:
```python
def generar_reporte_pdf(contenido):
    carpeta = "test_reports"
    os.makedirs(carpeta, exist_ok=True)
    existentes = [f for f in os.listdir(carpeta) if f.startswith("reporte_test_") and f.endswith(".pdf")]
    numeros = [int(f.split("_")[-1].replace(".pdf", "")) for f in existentes]
    siguiente = max(numeros) + 1 if numeros else 1
    nombre_archivo = f"reporte_test_{siguiente:03}.pdf"
    ruta_completa = os.path.join(carpeta, nombre_archivo)

    c = canvas.Canvas(ruta_completa, pagesize=LETTER)
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, "Reporte de pruebas de integración - Backend")
    c.drawString(50, 730, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, 710, f"Reporte N° {siguiente}")

    y = 690
    for linea in contenido.splitlines():
        c.drawString(50, y, linea)
        y -= 20
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = 750

    c.save()
    print(f"✅ Reporte generado: {ruta_completa}")
```
---

### 2. Generación del reporte en frontend

Dentro de `main()` al final:

```python
def main():
    ...
    contenido = f"""
Resultado de prueba automatizada:
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Estado: {estado}
Usuario ID: {user_id or 'N/A'}
Tarea ID: {task_id or 'N/A'}
Error (si ocurrió): {errores or 'Ninguno'}
"""
    generar_reporte_pdf(contenido)
```

---

### 3. Generación del reporte en backend

Al final de `integration_test()`:

```python
def integration_test():
    ...
    contenido = f"""
Resultado de prueba de integración:
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Estado: {estado}
Usuario ID: {user_id or 'N/A'}
Tarea ID: {task_id or 'N/A'}
Error (si ocurrió): {error or 'Ninguno'}
"""
    generar_reporte_pdf(contenido)
```
