# Multichannel Notification System (REST API)

## Descripción
Sistema de notificaciones multicanal que utiliza Chain of Responsibility para manejar los fallos en los canales de notificación y Singleton para el logger.

## Patrones de diseño utilizados
1. **Chain of Responsibility**: Para manejar los diferentes canales de notificación y su orden de fallback.
2. **Singleton**: Para el logger que registra todos los intentos de notificación.

## Endpoints

### Users
- `POST /users`: Registrar un nuevo usuario
- `GET /users`: Listar todos los usuarios

### Notifications
- `POST /notifications/send`: Enviar una notificación

## Ejemplos de uso

### Registrar un usuario
```bash
curl -X POST http://localhost:5500/users \
-H "Content-Type: application/json" \
-d '{
  "name": "Juan",
  "preferred_channel": "email",
  "available_channels": ["email", "sms"]
}'