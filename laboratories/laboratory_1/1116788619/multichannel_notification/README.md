Sistema de Notificaciones Multicanal (REST API)

Descripción
Este proyecto es un sistema básico de notificaciones multicanal construido con Flask. Permite registrar usuarios con canales de notificación preferidos (email, sms) y enviar mensajes que intentan llegar primero por el canal preferido, con fallback automático a otros canales disponibles.

El sistema registra usuarios con canales disponibles y preferidos. Al enviar una notificación, se intenta el canal preferido y si falla, se hace fallback automático al siguiente canal disponible, todo registrado con un logger singleton y validado con Marshmallow.

---

Estructura del proyecto

multichannel_notification/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── handlers/
│   │   └── handler.py
│   ├── utils/
│   │   └── logger.py
│   ├── schemas/
│   │   ├── user_schema.py
│   │   └── notification_schema.py
├── tests/
│   └── test_api.py
├── run.py
├── requirements.txt
├── README.md
├── swagger_multichannel_notification.yaml
├── multichannel_notification_postman_collection.json

---

Endpoints

Método | Ruta                  | Descripción
-------|-----------------------|-------------------------------
POST   | /users                | Registrar usuario
GET    | /users                | Listar usuarios
POST   | /notifications/send   | Enviar notificación
GET    | /logs                 | Ver logs de intentos de envío

---

Patrones de diseño utilizados

- Chain of Responsibility:  
  Para gestionar el intento de envío por canales con fallback automático, mejorando la flexibilidad y extensibilidad.

- Singleton (Logger):  
  Para registrar de forma centralizada y consistente todos los intentos de envío en una sola instancia.

- Blueprint (Flask):  
  Para organizar las rutas y controladores modularmente, facilitando el mantenimiento y escalabilidad.

---

Validación y manejo de errores

- Validación de entradas con marshmallow para asegurar integridad y tipos correctos.  
- Manejo global de errores HTTP y excepciones inesperadas, con respuestas JSON claras y uniformes.  
- Mensajes de error adecuados en caso de campos faltantes, usuario no encontrado, o errores internos.

---

Cómo ejecutar el proyecto

1. Clonar o descargar el repositorio.  
2. Crear y activar un entorno virtual:

   python -m venv venv
   source venv/bin/activate   # En Windows: venv\Scripts\activate

3. Instalar dependencias:

   pip install -r requirements.txt
   pip install pytest

4. Ejecutar la aplicación:

   python run.py

5. Usar Postman o curl para probar los endpoints.

---

Ejemplos de uso con curl

Registrar usuario:

curl -X POST http://127.0.0.1:5000/users -H "Content-Type: application/json" -d "{\"name\": \"Juan\", \"preferred_channel\": \"email\", \"available_channels\": [\"email\", \"sms\"]}"

Enviar notificación:

curl -X POST http://127.0.0.1:5000/notifications/send -H "Content-Type: application/json" -d "{\"user_name\": \"Juan\", \"message\": \"Tu cita es mañana\", \"priority\": \"alta\"}"

Obtener logs:

curl http://127.0.0.1:5000/logs

---

Pruebas unitarias

- Se incluyen pruebas unitarias básicas con pytest para validar:  
  - Registro de usuarios  
  - Envío de notificaciones  
  - Respuesta a usuarios no registrados  
  - Visualización de logs  
  - Validaciones de entradas

Para ejecutar pruebas:

   pytest

---

Documentación

- Se incluye archivo swagger_multichannel_notification.yaml para documentación OpenAPI.  
- Puede importarse en Postman o abrirse con Swagger Editor.

---

Mejoras futuras

- Implementar persistencia con base de datos para usuarios y logs.  
- Añadir autenticación y autorización para endpoints sensibles.  
- Mejorar el sistema de logging con niveles y almacenamiento en archivos.  
- Crear un frontend para interacción amigable con el usuario.  
- Añadir pruebas automatizadas más exhaustivas y de integración.

---

Autor

Wullfredo Javier Barco Godoy

---

Notas

- Actualmente la persistencia es en memoria; al reiniciar el servidor se pierden usuarios y logs.  
- La persistencia en base de datos puede implementarse como mejora futura.
