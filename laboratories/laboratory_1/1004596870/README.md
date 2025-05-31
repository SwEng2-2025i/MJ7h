# 🧪 Advanced Individual Lab: Multichannel Notification System (REST API)

## 👤 Author
**ID:** 1004596870

---

## 🧩 System Overview

This REST API simulates a multichannel notification system. Users can register with a preferred and a list of available communication channels. Notifications are sent starting from the preferred channel. If delivery fails, the system retries other channels following a **Chain of Responsibility**.

---

## ⚙️ Technologies

- Python 3.10+
- Flask
- Random (for simulating delivery failures)

---

## 🧱 Architecture & Design Patterns

### 1. **Chain of Responsibility**
Used to define a sequence of channels to attempt when sending notifications. Each channel tries to send the message and passes it along the chain if it fails.

### 2. **Singleton**
The Logger class is implemented using the Singleton pattern to ensure a single logging instance across the system.

### ✅ Optional: Factory Method
A `ChannelFactory` creates channel instances based on a string identifier, promoting loose coupling and scalability.

---

## 🧪 Endpoints

| Method | Endpoint              | Description                                      |
|--------|-----------------------|--------------------------------------------------|
| POST   | `/users`              | Register a user with name, preferred and available channels |
| GET    | `/users`              | List all users                                   |
| POST   | `/notifications/send` | Send a notification with message and priority    |

### 📥 Example Payloads

**POST /users**
```json
{
  "name": "Manuel",
  "preferred_channel": "email",
  "available_channels": ["email", "sms", "console"]
}
```

**POST /notifications/send**
```json
{
  "user_name": "Manuel",
  "message": "Your appointment is tomorrow.",
  "priority": "high"
}
```

---

## 🧪 Testing

### Run API:
```bash
cd laboratories/laboratory_1/1004596870/app
python app.py
```

### Test with `curl`:
```bash
curl -X POST http://127.0.0.1:5000/users \
     -H "Content-Type: application/json" \
     -d '{"name": "Manuel", "preferred_channel": "email", "available_channels": ["email", "sms"]}'

curl http://127.0.0.1:5000/users

curl -X POST http://127.0.0.1:5000/notifications/send \
     -H "Content-Type: application/json" \
     -d '{"user_name": "Manuel", "message": "Hello!", "priority": "high"}'
```

---

## 🧮 Class Diagram (Simplified UML)

```
+-------------------+       +-----------------+
|      User         |       |   Notification  |
+-------------------+       +-----------------+
| - name            |       | - message       |
| - preferred       |       | - priority      |
| - available       |       +-----------------+
+-------------------+

         |
         v
+-----------------------+         +----------------------+
|   NotificationService |<--------|     ChannelFactory    |
+-----------------------+         +----------------------+
| - chain               |         | +create_channel()     |
| +send()               |         +----------------------+
+-----------------------+

         |
         v
+---------------------+
|     BaseChannel     |<-----------------------------+
+---------------------+                              |
| +handle()           |                              |
| +set_next()         |                              |
+---------------------+                              |
     /     |     \                                    |
    /      |      \                                   |
Email  Console  SMS Channel----------------------------+

          ^
          |
     +----------------+
     |     Logger     | (Singleton)
     +----------------+
     | +log()         |
     +----------------+
```

---

## 🗃️ Folder Structure

```
laboratories/
└── laboratory_1/
    └── 1004596870/
        └── app/
            ├── app.py
            ├── models/
            │   └── user.py
            ├── services/
            │   └── notification_service.py
            ├── channels/
            │   ├── base_channel.py
            │   ├── email_channel.py
            │   ├── sms_channel.py
            │   ├── console_channel.py
            │   └── channel_factory.py
            └── utils/
                └── logger.py
```

---

## 📦 Installation

```bash
pip install flask
```

---

