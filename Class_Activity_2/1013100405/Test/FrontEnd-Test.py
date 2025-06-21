import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

def abrir_frontend(driver):
    driver.get("http://localhost:5000")
    time.sleep(2)

def crear_usuario(driver, wait):
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    print("Resultado usuario:", user_result)
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))
    return user_id

def crear_tarea(driver, wait, user_id):
    task_input = driver.find_element(By.ID, "task")
    task_input.send_keys("Terminar laboratorio")
    time.sleep(1)

    userid_input = driver.find_element(By.ID, "userid")
    userid_input.send_keys(user_id)
    userid_input.send_keys('\t')
    time.sleep(1)

    crear_tarea_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']"))
    )
    crear_tarea_btn.click()
    time.sleep(2)

    wait.until(
        EC.text_to_be_present_in_element((By.ID, "task-result"), "Tarea creada con ID")
    )
    task_result = driver.find_element(By.ID, "task-result")
    print("Texto en task_result:", task_result.text)
    assert "Tarea creada con ID" in task_result.text
    task_id = ''.join(filter(str.isdigit, task_result.text))
    return task_id

def ver_tareas(driver):
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

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

def main():
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    task_id = None
    user_id = None
    estado = "✅ Exitoso"
    errores = ""

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait)
        task_id = crear_tarea(driver, wait, user_id)
        ver_tareas(driver)
        time.sleep(2)

    except Exception as e:
        estado = "❌ Fallido"
        errores = str(e)
        print("Error durante la prueba:", errores)

    finally:
        driver.quit()

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

        # 📝 Generar reporte PDF
        contenido = f"""
Resultado de prueba automatizada:
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Estado: {estado}
Usuario ID: {user_id or 'N/A'}
Tarea ID: {task_id or 'N/A'}
Error (si ocurrió): {errores or 'Ninguno'}
"""
        generar_reporte_pdf(contenido)

if __name__ == "__main__":
    main()
