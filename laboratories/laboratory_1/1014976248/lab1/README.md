# Multichannel Notification System API

## Luis Felipe Tolosa Sierra

**Multichannel Notification System with Design Patterns in Flask**

---

## System Explanation

This is a modular and extensible REST API developed using Flask and Flask-RESTx. It allows registering users and sending notifications through multiple channels (email, SMS, console, and push). The system is built using key software design patterns to ensure clean architecture and maintainability.

### Key Features

- Register users with preferred and available notification channels.
- Send notifications using a priority fallback mechanism.
- Each attempt is logged by a Singleton logger.
- Swagger documentation included.
- Easily extensible with new channels or logic.

### Used Design Patterns

- **Singleton** for centralized logging.
- **Strategy** for different notification sending mechanisms.
- **Chain of Responsibility** for fallback among channels.
- **Factory** for instantiating strategies dynamically.

---

## Class/Module Diagram (Overview)

| Folder/File                        | Classes / Functions                                  | Responsibility                                      |
| ---------------------------------- | ---------------------------------------------------- | --------------------------------------------------- |
| `logger/notification_logger.py`    | `NotificationLogger`                                 | Singleton logger for notification history           |
| `strategies/`                      | `NotificationStrategy`, `Email...`, `SMS...`, etc.   | Defines and implements sending logic per channel    |
| `handlers/`                        | `NotificationHandler`, `ConcreteNotificationHandler` | Implements fallback chain for sending notifications |
| `factories/`                       | `NotificationStrategyFactory`                        | Factory for creating strategy instances             |
| `models/user.py`                   | `User`, `UserManager`                                | Manages user data and operations                    |
| `services/notification_service.py` | `NotificationService`                                | Coordinates notification sending logic              |
| `api/`                             | Flask Resources (`UsersResource`, etc.)              | REST endpoints for user and notification management |
| `extensions.py`                    | `api`                                                | Flask-RESTx API instance                            |
| `app.py`                           | -                                                    | Application bootstrap and endpoint registration     |

---

## Design Pattern Justifications

| Pattern                     | Justification                                                                                                                  |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **Singleton**               | Ensures a single instance of the `NotificationLogger`, which centralizes log management and avoids fragmented histories.       |
| **Strategy**                | Each channel (email, sms, console, push) implements a common interface, allowing them to be swapped or extended independently. |
| **Chain of Responsibility** | Enables failover behavior across multiple channels. If one channel fails, the next is automatically tried.                     |
| **Factory**                 | Simplifies the creation of channel strategies based on user input or configuration, reducing tight coupling.                   |

---

## Endpoint Documentation

All endpoints are exposed via a REST API and documented with Swagger at `/swagger/`.

---

### 1. **Register User**

- **URL:** `/users`
- **Method:** `POST`
- **Description:** Registers a new user with their preferred and available notification channels.
- **Example JSON Body:**

```json
{
  "name": "juan",
  "preferred_channel": "email",
  "available_channels": ["email", "sms", "console"]
}
```

- **Responses:**
  - `201 Created`: User successfully registered.
  - `400 Bad Request`: Invalid fields or user already exists.

---

### 2. **List Users**

- **URL:** `/users`
- **Method:** `GET`
- **Description:** Retrieves a list of all registered users.

- **Example Successful Response:**

```json
{
  "users": [
    {
      "name": "juan",
      "preferred_channel": "email",
      "available_channels": ["email", "sms", "console"],
      "created_at": "2025-05-29T12:00:00"
    }
  ],
  "total": 1
}
```

---

### 3. **Send Notification**

- **URL:** `/notifications/send`
- **Method:** `POST`
- **Description:** Sends a notification to a user through their channel chain.
- **Example JSON Body:**

```json
{
  "user_name": "juan",
  "message": "Test message",
  "priority": "high"
}
```

- **Responses:**
  - `200 OK`: Notification successfully sent through one of the channels.
  - `202 Accepted`: Request processed but delivery failed.
  - `404 Not Found`: User not found.
  - `400 Bad Request`: Invalid data.

---

### 4. **Notification History**

- **URL:** `/notifications/history`
- **Method:** `GET`
- **Description:** Returns the history of all notification attempts (successful or failed).

- **Example Response:**

```json
{
  "history": [
    {
      "timestamp": "2025-05-29T12:10:00",
      "user_name": "juan",
      "channel": "email",
      "message": "Test message",
      "success": true,
      "priority": "high"
    }
  ],
  "total": 1
}
```

---

### 5. **List Available Channels**

- **URL:** `/channels`
- **Method:** `GET`
- **Description:** Returns the list of supported notification channels.

- **Example Response:**

```json
{
  "channels": ["email", "sms", "console", "push"],
  "total": 4
}
```

---

### 6. **Health Check**

- **URL:** `/health`
- **Method:** `GET`
- **Description:** Checks if the service is up and running.

- **Example Response:**

```json
{
  "status": "healthy",
  "timestamp": "2025-05-29T12:15:00",
  "service": "Multichannel Notification System"
}
```

---

## Testing Instructions

### Using `curl`

#### Register User

```bash
curl -X POST http://localhost:5000/users -H "Content-Type: application/json" -d '{"name": "juan", "preferred_channel": "email", "available_channels": ["email", "sms", "console"]}'
```

#### Send Notification

```bash
curl -X POST http://localhost:5000/notifications/send -H "Content-Type: application/json" -d '{"user_name": "juan", "message": "Hola Juan", "priority": "high"}'
```

#### View History

```bash
curl http://localhost:5000/notifications/history
```

### Using Postman

1. Open Postman and create a new Collection.
2. Add a `POST /users` request with JSON body.
3. Add a `POST /notifications/send` request.
4. Add a `GET /notifications/history` request.
5. Optionally test `/channels` and `/health`.

---

## Swagger Instructions

Once the app is running, open a browser and go to:

```
http://localhost:5000/swagger/
```

You will see the interactive documentation where you can test each endpoint directly.

---
