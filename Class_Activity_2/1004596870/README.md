# 🔧 Sistema de Pruebas de Integración Mejorado

Este proyecto implementa un sistema de pruebas de integración para una aplicación web con frontend y backend separados, incluyendo características avanzadas de limpieza de datos y generación de reportes.

## 🚀 Características Implementadas

### ✅ Funcionalidades Originales
- **Servicio de Usuarios**: API REST para gestión de usuarios (puerto 5001)
- **Servicio de Tareas**: API REST para gestión de tareas (puerto 5002)
- **Frontend**: Interfaz web para interactuar con los servicios (puerto 5000)
- **Pruebas de Integración**: Verificación de la comunicación entre servicios

### 🆕 Nuevas Funcionalidades

#### 1. 🧹 Limpieza Automática de Datos
- **Seguimiento automático**: Todos los datos creados durante las pruebas son registrados
- **Eliminación post-prueba**: Los datos de prueba se eliminan automáticamente al finalizar
- **Verificación de limpieza**: El sistema verifica que los datos se hayan eliminado correctamente
- **Endpoints de eliminación**: Nuevos endpoints DELETE en ambos servicios

#### 2. 📄 Generación de Reportes PDF
- **Numeración secuencial**: Cada reporte tiene un número único que no sobrescribe los anteriores
- **Información detallada**: Incluye fecha, tipo de prueba, resultados y resumen
- **Formato profesional**: Diseño limpio y fácil de leer con estadísticas

#### 3. 🤖 Manejo Automático de WebDrivers
- **webdriver-manager**: Descarga y configura automáticamente ChromeDriver
- **Configuración optimizada**: Opciones de Chrome para mejor rendimiento
- **Manejo de errores**: Gestión robusta de errores en las pruebas de frontend

## 📁 Estructura del Proyecto

```
Example 5 - Integration Test/
├── Front-End/
│   └── main.py                 # Servidor frontend
├── Users_Service/
│   ├── main.py                 # Servicio de usuarios (puerto 5001)
│   │  └── [NUEVO] Endpoint DELETE /users/<id>
│   └── instance/
│       └── users.db           # Base de datos de usuarios
├── Task_Service/
│   ├── main.py                 # Servicio de tareas (puerto 5002)
│   │  └── [NUEVO] Endpoint DELETE /tasks/<id>
│   └── instance/
│       └── tasks.db           # Base de datos de tareas
├── Test/
│   ├── BackEnd-Test.py         # Pruebas de backend con limpieza y PDF
│   └── FrontEnd-Test.py        # Pruebas de frontend con limpieza y PDF
├── reports/                    # Directorio para reportes PDF
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Este archivo
```

## 🛠️ Instalación y Configuración

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Verificar Instalación
```bash
python -c "import flask, selenium, reportlab; print('✅ Todas las dependencias instaladas')"
```

## 🧪 Ejecución de Pruebas

### Pruebas de Backend
```bash
python Test/BackEnd-Test.py
```

**Características incluidas:**
- ✅ Creación de usuarios y tareas
- ✅ Verificación de integración
- ✅ Limpieza automática de datos
- ✅ Generación de reporte PDF

### Pruebas de Frontend
```bash
python Test/FrontEnd-Test.py
```

**Características incluidas:**
- ✅ Pruebas automatizadas con Selenium
- ✅ Interacción con interfaz web
- ✅ Limpieza automática de datos
- ✅ Generación de reporte PDF

### Ejecutar Servicios Manualmente

1. **Iniciar servicio de usuarios**:
   ```bash
   python Users_Service/main.py
   ```

2. **Iniciar servicio de tareas**:
   ```bash
   python Task_Service/main.py
   ```

3. **Iniciar frontend**:
   ```bash
   python Front-End/main.py
   ```

## 📊 Reportes Generados

### Ubicación de Reportes
Los reportes PDF se guardan en el directorio `reports/` con el formato:
```
reporte_001_20250121_143022.pdf
reporte_002_20250121_143045.pdf
...
```

### Contenido de los Reportes
- **Información del reporte**: Fecha, número secuencial, tipo de prueba
- **Resultados detallados**: Estado de cada prueba individual
- **Resumen estadístico**: Total de pruebas, éxitos, fallos, tasa de éxito
- **Formato profesional**: Diseño limpio y fácil de leer

## 🔍 Verificación de Limpieza

El sistema verifica automáticamente que:
- ✅ Los usuarios creados durante las pruebas han sido eliminados
- ✅ Las tareas creadas durante las pruebas han sido eliminadas
- ✅ No quedan datos residuales en las bases de datos

## 🚨 Manejo de Errores

### Errores Comunes y Soluciones

1. **Puerto en uso**:
   ```bash
   # Verificar puertos en uso
   netstat -ano | findstr :5000
   netstat -ano | findstr :5001
   netstat -ano | findstr :5002
   ```

2. **ChromeDriver no encontrado**:
   - El sistema usa `webdriver-manager` que descarga automáticamente ChromeDriver
   - Si hay problemas, verificar conexión a internet

3. **Base de datos bloqueada**:
   - Detener todos los servicios
   - Eliminar archivos `.db` si es necesario
   - Reiniciar servicios

## 📈 Mejoras Implementadas

### Antes vs Después

| Aspecto | Versión Original | Versión Mejorada |
|---------|------------------|------------------|
| Limpieza de datos | ❌ Manual | ✅ Automática |
| Reportes | ❌ Solo consola | ✅ PDF profesional |
| WebDriver | ❌ Manual | ✅ Automático |
| Verificación | ❌ Básica | ✅ Completa |
| Numeración | ❌ No aplica | ✅ Secuencial |

## 🔧 Código Autocontenido

Cada archivo de prueba (`BackEnd-Test.py` y `FrontEnd-Test.py`) incluye:
- **Limpieza de datos**: Funciones integradas para eliminar datos de prueba
- **Generación de PDF**: Funciones integradas para crear reportes
- **Verificación**: Funciones integradas para verificar la limpieza
- **Manejo de errores**: Gestión robusta de excepciones

No se requieren archivos utilitarios externos - todo está autocontenido en cada archivo de prueba.

## 📝 Licencia

Este proyecto es parte del curso de Ingeniería de Software II.

---

**Desarrollado con ❤️ para demostrar las mejores prácticas en pruebas de integración** 