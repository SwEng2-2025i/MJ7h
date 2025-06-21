# Class Activity 2 - Integration Test Extension

## Breve explicación de los cambios

Se extendió el sistema de pruebas de integración para cumplir con los siguientes objetivos:

- **Limpieza automática de datos:**  
  Todos los datos creados durante la ejecución de los tests (usuarios y tareas) son eliminados al finalizar cada prueba. Además, se verifica que los datos hayan sido correctamente eliminados.
- **Generación automática de reportes PDF:**  
  Los resultados de cada ejecución de los tests se guardan automáticamente en un archivo PDF secuencial dentro de la carpeta `reports/`. Cada reporte tiene un número único y no sobrescribe los anteriores.

## Archivos modificados

- `Test/BackEnd-Test.py`:  
  Se agregaron la limpieza de datos, la verificación de eliminación y la generación de reportes PDF.
- `Test/FrontEnd-Test.py`:  
  Se agregaron la limpieza de datos, la verificación de eliminación y la generación de reportes PDF.
- `Users_Service/main.py`:  
  Se agregó el endpoint DELETE para usuarios.
- `Task_Service/main.py`:  
  Se agregó el endpoint DELETE para tareas.

## Cómo ejecutar los tests

1. **Instala las dependencias necesarias usando el archivo `requirements.txt`:**
   ```sh
   pip install -r requirements.txt
   ```
   (Asegúrate también de tener [ChromeDriver](https://chromedriver.chromium.org/downloads) si usas Selenium.)

2. **Inicia los servicios:**
   - Abre una terminal para cada servicio y ejecuta:
     ```sh
     cd Users_Service
     python main.py
     ```
     ```sh
     cd Task_Service
     python main.py
     ```
     ```sh
     cd Front-End
     python main.py
     ```

3. **Ejecuta los tests desde la carpeta `Test`:**
   ```sh
   cd Test
   python BackEnd-Test.py
   python FrontEnd-Test.py
   ```

## Dónde encontrar los reportes PDF

- Los reportes PDF se generan automáticamente en la carpeta `Test/reports/`.
- Cada vez que ejecutes un test, se creará un nuevo archivo PDF con los resultados, por ejemplo: `report_1.pdf`, `report_2.pdf`, etc.

---

**Autor:**  
*Juan Camilo López Bustos