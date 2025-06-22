# 📝 Informe de Pruebas de Integración - Jhoan Sebastian Franco Ruiz

## Resultados de las Pruebas

- **Creación de usuarios:** Los usuarios se crearon correctamente mediante las pruebas de front-end y back-end.
- **Creación de tareas:** Las tareas se asignaron correctamente a los usuarios y se almacenaron de forma persistente.
- **Listado de tareas:** El listado reflejó correctamente las tareas creadas.
- **Eliminación:** Tanto usuarios como tareas se eliminaron correctamente, reflejándose los cambios en la interfaz y el backend.
- **Registro en PDF:** Los resultados y logs de las pruebas se generaron y almacenaron en archivos PDF para trazabilidad.

**TEST 1**
![](/MJ7h/Class_Activity_2/1118528726/imagenes/BK-T1.png)
**TEST 2**
![](/MJ7h/Class_Activity_2/1118528726/imagenes/BK-T2.png)

**TEST 3**
![](/MJ7h/Class_Activity_2/1118528726/imagenes/FE-T3.png)

**TEST 4**
![](/MJ7h/Class_Activity_2/1118528726/imagenes/FE-T4.png)

## Secciones de Código Agregadas

Las siguientes secciones fueron agregadas 
1. Se modifico los archivos de **test**; Tanto las pruebas de *FrontEnd* como *BackEnd* para los borrados y para la generación de PDF.
2. Se creo otro servicio en la carpeta **pdf** con la libreria *ReportLab*
3. Se agrego un return de id en los endpoints de **task** 
4. Se modifico y agrego en la carpeta de **Front-End** unas funciones para el borrado y un unos div con botones de borrado en Frontend. 

## Intalación de dependencias
Instalar las librerias del archivo **requirements.txt**
```sh
   pip install -r requirements.txt
   ```

## Cómo Ejecutar las Pruebas

1. Inicie todos los servicios backend (`Users_Service`, `Task_Service`, `PDF`) y el front-end.
2. Ejecute la prueba de integración del backend:
   ```sh
   python BackEnd-Test.py
   ```
3. Ejecute la prueba de integración del frontend (requiere Chrome y Selenium):
   ```sh
   python FrontEnd-Test.py
   ```
4. Revise los reportes PDF generados en el directorio `PDF_TEST`.


