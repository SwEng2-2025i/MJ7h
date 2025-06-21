import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    opts = Options()
    # opts.add_argument("--headless")
    drv = webdriver.Chrome(options=opts)
    yield drv
    drv.quit()

def abrir_frontend(driver):
    driver.get("http://localhost:5000")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

def test_crear_y_borrar_usuario_y_tarea(driver):
    wait = WebDriverWait(driver, 10)
    user = "UsuarioPrueba"
    task = "TareaPrueba"
    abrir_frontend(driver)

    # Crear usuario
    driver.find_element(By.ID, "username").send_keys(user)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "user-result"), "Usuario creado con ID"))
    uid = ''.join(filter(str.isdigit, driver.find_element(By.ID, "user-result").text))

    # Crear tarea
    driver.find_element(By.ID, "task").send_keys(task)
    driver.find_element(By.ID, "userid").send_keys(uid)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']"))).click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "task-result"), "Tarea creada con ID"))

    # Verificar lista contiene la tarea
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(1)
    assert task in driver.find_element(By.ID, "tasks").text

    # Borrar tarea
    xpath_btn = f"//li[contains(., '{task}')]//button[text()='Borrar']"
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath_btn))).click()
    time.sleep(1)
    assert task not in driver.find_element(By.ID, "tasks").text

    # Borrar usuario
    driver.find_element(By.ID, "delete-userid").send_keys(uid)
    driver.find_element(By.XPATH, "//button[text()='Borrar Usuario']").click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "delete-user-result"), "deleted successfully"))

def test_force_failure():
    """Test diseñado para fallar siempre, como ejemplo."""
    assert False, "❌ Esta es una falla intencional para generar un informe."
