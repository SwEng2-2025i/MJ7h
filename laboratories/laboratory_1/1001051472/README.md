**Autor:** Daniel Felipe Soracipa Torres

# Sistema de Notificaciones Multicanal (API REST)

## Explicación del sistema

Este proyecto implementa una API REST modular para un sistema de notificaciones donde los usuarios pueden registrarse con múltiples canales de comunicación (correo electrónico, SMS, consola). Al enviar una notificación, el sistema intenta primero el canal preferido del usuario. Si la entrega falla (simulada aleatoriamente), el sistema reintenta usando los canales de respaldo, siguiendo el orden especificado por el usuario.

La arquitectura sigue principios de clean architecture, separando adaptadores (manejadores HTTP), lógica de aplicación (casos de uso), lógica de dominio (entidades, canales de notificación, logger) e infraestructura (repositorio en memoria). Todos los datos se almacenan en memoria; no se requiere base de datos externa.

## Documentación de Endpoints

### Registrar un usuario
- **POST /users**
- **Descripción:** Registra un usuario con nombre, canal preferido y canales disponibles.
- **Ejemplo de cuerpo de solicitud:**
```json
{
  "name": "Juan",
  "preferred_channel": "email",
  "available_channels": ["email", "sms"]
}
```
- **Respuestas:**
  - 201 Created: `{ "message": "User registered successfully" }`
  - 400 Bad Request: `{ "error": "..." }`

### Listar todos los usuarios
- **GET /users**
- **Descripción:** Lista todos los usuarios registrados.
- **Ejemplo de respuesta:**
```json
[
  {
    "name": "Juan",
    "preferred_channel": "email",
    "available_channels": ["email", "sms"]
  }
]
```

### Enviar notificación
- **POST /notifications/send**
- **Descripción:** Envía una notificación a un usuario. El sistema intentará primero el canal preferido y luego los canales de respaldo si es necesario.
- **Ejemplo de cuerpo de solicitud:**
```json
{
  "user_name": "Juan",
  "message": "Tu cita es mañana.",
  "priority": "high"
}
```
- **Ejemplo de respuesta:**
  - Éxito: `{ "status": "delivered", "via": "Email" }`
  - Fallo: `{ "status": "failed" }`
  - Usuario no encontrado: `{ "status": "failed", "reason": "User not found" }`

## Justificación de patrones de diseño

### Chain of Responsibility (Cadena de Responsabilidad)
La lógica de entrega de notificaciones utiliza el patrón Chain of Responsibility. Cada canal de notificación (Email, SMS, Consola) es un manejador en la cadena. El sistema intenta enviar la notificación por el canal preferido; si falla (simulado aleatoriamente), pasa la solicitud al siguiente canal disponible, y así sucesivamente, hasta que la entrega sea exitosa o se agoten los canales.

### Singleton
El logger está implementado como un Singleton. Esto asegura que todas las partes del sistema utilicen la misma instancia de logger, centralizando la gestión de logs y evitando duplicados o inconsistencias.

## Documentación Swagger

La API está documentada usando Swagger/OpenAPI. Puedes acceder a la documentación interactiva (si tienes flasgger o flask-swagger-ui instalado) accediendo a:

```
http://127.0.0.1:5000/apidocs/
```

Desde ahí puedes probar los endpoints y ver los esquemas de entrada y salida.

## Instrucciones de instalación y pruebas

### Prerrequisitos
- Python 3.10+
- Flask
- (Opcional para Swagger): flasgger

### Instalación
1. Instala las dependencias:
   ```bash
   pip install Flask flasgger
   ```
2. Ejecuta la aplicación:
   ```bash
   python app.py
   ```

### Ejemplos de uso (curl)

#### Registrar un usuario
```bash
curl -X POST http://127.0.0.1:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Juan", "preferred_channel": "email", "available_channels": ["email", "sms"]}'
```

#### Listar usuarios
```bash
curl http://127.0.0.1:5000/users
```

#### Enviar notificación
```bash
curl -X POST http://127.0.0.1:5000/notifications/send \
  -H "Content-Type: application/json" \
  -d '{"user_name": "Juan", "message": "Tu cita es mañana.", "priority": "high"}'
```

### Pruebas con Postman
1. Importa los endpoints anteriores en Postman.
2. Usa los ejemplos de payload para probar el registro, listado y envío de notificaciones.

---

## Comentarios sobre el código

- El código está modularizado y bien comentado.
- Cada clase y método tiene una responsabilidad clara.
- El archivo `domain/notification_channels.py` contiene comentarios y nombres descriptivos para facilitar la comprensión del patrón Chain of Responsibility.
- El logger Singleton está documentado y su uso es evidente en los canales de notificación.
- Los endpoints están documentados y validados para entradas erróneas.

---


