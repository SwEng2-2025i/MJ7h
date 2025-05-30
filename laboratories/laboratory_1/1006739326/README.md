# 📬 Multichannel Notification System

**Autor:** Sergio Alejandro Nova Perez  
**ID:** 1006739326  
**Fecha de entrega:** 30 de mayo de 2025  

---

## 📝 Descripción general

Este sistema RESTful simula el envío de notificaciones multicanal (email, SMS, consola) utilizando patrones de diseño avanzados para garantizar modularidad, mantenibilidad y extensibilidad.

El objetivo principal es intentar el envío de una notificación usando el canal preferido del usuario. Si este falla (de forma simulada), se recurre a los canales alternativos mediante el patrón **Chain of Responsibility**.

El sistema utiliza almacenamiento en memoria (sin base de datos) y registra los intentos de notificación con un logger implementado como **Singleton**.

---

## 🧱 Estructura del Proyecto

app/
├── main.py
├── models/
│ └── init.py
├── patterns/
│ ├── channel_handler.py
│ └── factory.py
├── routes/
│ └── endpoints.py
├── services/
│ └── logger.py
requirements.txt
README.md
swagger.yaml


---

## 🧠 Patrones de diseño utilizados

### 🔗 Chain of Responsibility
Permite manejar el reintento de envío de notificaciones a través de una cadena de canales (email → sms → consola). Cada canal decide si manejar la notificación o pasarla al siguiente.

### 🏭 Factory
Se usa para construir dinámicamente la cadena de canales de notificación en el orden definido por el usuario.

### ♻️ Singleton (opcional recomendado)
Un logger que asegura que todos los intentos de envío se registren en una única instancia compartida.

---

## 🚀 Endpoints REST

### 📌 POST /users
Registra un nuevo usuario con canales de notificación.

#### 🧾 Request Body:
```json
{
  "name": "Juan",
  "preferred_channel": "email",
  "available_channels": ["email", "sms", "console"]
}


Respuesta
Formato json
{
  "message": "User registered successfully",
  "user": {
    "name": "Juan",
    "preferred_channel": "email",
    "available_channels": ["email", "sms", "console"]
  }
}

GET /users
Lista todos los usuarios registrados.
Respuesta
[
  {
    "name": "Juan",
    "preferred_channel": "email",
    "available_channels": ["email", "sms", "console"]
  }
]

POST /notifications/send

Envía una notificación a un usuario. Si el canal preferido falla, se reintenta con los demás canales disponibles.

Request body:
{
  "user_name":"Juan",
  "message": "Tu cita es mañana.",
  "priority": "high"
}

Respuesta exitosa:

{
  "message": "Notification delivered"
}

Respuesta si todos los canales fallan:

{
  "error": "All channels failed"
}

Instrucciones de ejecución

Requisitos

Python 3.12
Flask

Instalación y ejecución 


