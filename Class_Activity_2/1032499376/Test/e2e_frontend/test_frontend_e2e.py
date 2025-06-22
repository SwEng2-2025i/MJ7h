import time
import requests
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Cleanup import cleanup_tasks, cleanup_users

# Endpoints para verificación directa
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"


def abrir_frontend(driver):
    driver.get("http://localhost:5000")
    time.sleep(2)


def crear_usuario(driver, wait) -> int:
    driver.find_element(By.ID, "username").send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()

    # ESPERA a que aparezca el texto esperado
    wait.until(
        EC.text_to_be_present_in_element((By.ID, "user-result"), "Usuario creado con ID")
    )
    result = driver.find_element(By.ID, "user-result").text
    assert "Usuario creado con ID" in result, "❌ No se creó el usuario"
    return int(''.join(filter(str.isdigit, result)))


def crear_tarea(driver, wait, user_id) -> int:
    driver.find_element(By.ID, "task").send_keys("Terminar laboratorio")
    time.sleep(1)
    driver.find_element(By.ID, "userid").send_keys(str(user_id))
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[text()='Crear Tarea']").click()

    # ESPERA a que aparezca el texto de confirmación
    wait.until(
        EC.text_to_be_present_in_element((By.ID, "task-result"), "Tarea creada con ID")
    )
    text = driver.find_element(By.ID, "task-result").text
    assert "Tarea creada con ID" in text, "❌ No se creó la tarea"
    return int(''.join(filter(str.isdigit, text)))


def ver_tareas(driver):
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)
    tasks_text = driver.find_element(By.ID, "tasks").text
    assert "Terminar laboratorio" in tasks_text, "❌ La tarea no aparece en la lista"


@pytest.mark.usefixtures("clean_db")
def test_frontend_e2e_flow(driver):
    """
    1) Cleanup automático (con clean_db) y pre-cleanup manual.
    2) Crea usuario y tarea vía UI.
    3) Verifica interfaz y API.
    4) Cleanup manual y verificación final.
    """
    cleanup_tasks()
    cleanup_users()

    wait = WebDriverWait(driver, 10)
    abrir_frontend(driver)

    user_id = crear_usuario(driver, wait)
    task_id = crear_tarea(driver, wait, user_id)
    ver_tareas(driver)

    # Verificación backend antes de cleanup
    tasks = requests.get(TASKS_URL, timeout=5).json()
    assert any(t["id"] == task_id and t["user_id"] == user_id for t in tasks), \
           "La tarea no se registró correctamente en el backend"

    # Post-cleanup manual y verificación
    cleanup_tasks()
    cleanup_users()

    tasks_after = requests.get(TASKS_URL, timeout=5).json()
    assert not any(t["id"] == task_id for t in tasks_after), \
           "Sigue habiendo tareas después del cleanup"

    status = requests.get(f"{USERS_URL}/{user_id}", timeout=5).status_code
    assert status == 404, "Sigue habiendo usuario después del cleanup"
