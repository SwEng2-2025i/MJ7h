# Actividad 2: Pruebas de Integración

## Cambios Implementados
1. **Limpieza de Datos**:
   - Se agregaron endpoints `DELETE` en Users-Service y Task-Service.
   - Las pruebas ahora eliminan datos creados y verifican su eliminación.

2. **Reportes en PDF**:
   - Se usó `FPDF` para generar informes con resultados.
   - Los reportes se guardan con nombres únicos (ej: `report_1.pdf`).

## Cómo Ejecutar
1. Iniciar servicios:
   ```bash
   python Users-Service/main.py
   python Task-Service/main.py
   python Front-End/main.py