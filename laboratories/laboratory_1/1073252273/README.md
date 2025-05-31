📬 Notification API – Flask
Una API REST modular para registrar usuarios y enviar notificaciones mediante canales como email o SMS, con manejo de fallos y reintentos mediante patrón Chain of Responsibility.

🚀 Características:
-API REST con Flask
-Registro y listado de usuarios
-Envío de notificaciones con canales de fallback
-Simulación de fallos en canales (random.choice)
-Uso de patrones de diseño:
    ✅ Chain of Responsibility (envío con fallback)
    ✅ Factory Pattern (instanciación de canales)
    ✅ Singleton Pattern (logger opcional)
-Almacenamiento en memoria (sin base de datos)
-Código modular y limpio

📦 Requisitos:
-Python 3.8+
-Flask

▶️ Ejecución
Desde la raíz del proyecto:
python app.py

Servidor disponible en:
http://localhost:5000


🔌 Endpoints:
📍 POST /users
Registrar un nuevo usuario.

📍 GET /users
Lista todos los usuarios registrados.

📍 POST /notifications/send
Envía una notificación al usuario especificado. Intenta el canal preferido primero, y luego los alternativos si falla.

JSON Payload (Todo se uso mediante Postman):
Registrar usuarios:
{
  "name": "Juan",
  "preferred_channel": "email",
  "available_channels": ["email", "sms"]
}

Envio de notificacion:
{
  "user_name": "Juan",
  "message": "Your appointment is tomorrow.",
  "priority": "high"
}

🔄 Lógica de envío (Chain of Responsibility):
-Se intenta enviar la notificación por el canal preferido.
-Si falla (simulado con random.choice([True, False])), se intenta el siguiente canal disponible.
-Todos los intentos se registran con el logger.
-Si todos fallan, se retorna un error 500.

🧰 Patrones de Diseño Usados:
-Factory Pattern: Instancia canales (email, sms)
-Chain of Responsibility: Mecanismo de fallback al enviar notificaciones

Presentado por: Yerall Felipe Rojas Cardenas.

