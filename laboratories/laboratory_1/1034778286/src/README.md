# Multichannel Notification System

**Author**: Juan David Ardila Diaz  
**Date**: May 30, 2025  
**Lab**: Advanced Individual Lab – REST API Design with Design Patterns  

---

## Description

This project is a multichannel notification system built with Flask. It allows users to register with a preferred communication channel (e.g., email, SMS, console), and sends notifications through the preferred channel. If that channel fails (simulated randomly), fallback channels are used via the **Chain of Responsibility** pattern.

---

## Design Patterns Used

### 1. Chain of Responsibility
Used to attempt message delivery across available channels in a fallback sequence. If the preferred channel fails, the next one is tried until the message is delivered or all fail.

- Implemented via individual handler classes like `EmailHandler`, `SMSHandler`, `ConsoleHandler`, each with a `set_next()` method and a `handle()` method.
- The chain is built dynamically based on the user’s available channels and order of preference.

### 2. Factory Pattern
Used to instantiate the appropriate handler object for a communication channel, improving modularity and maintainability.

- Implemented via `FactoryHandler.createHandler(channel: str)`.

### 3. Singleton (Logger)
An optional singleton logger is implemented to ensure centralized logging of all notification attempts.

- Logging is used across all handlers and use cases to record success and failure of notifications.

---

## REST API Endpoints

### `POST /users`
Registers a new user.

#### Request Body
```json
{
  "name": "Juan",
  "preferred_channel": "email",
  "available_channels": ["email", "sms"]
}
```

#### Response
```json
{
  "message": "User Juan created successfully",
  "user_data": {
    "name": "Juan",
    "preferred_channel": "email",
    "available_channels": ["email", "sms"]
  }
}
```

### `POST /notifications/send`
Registers and sends a new notification.

#### Request Body
```json
{
  "user_name": "Juan",
  "message": "Your appointment is tomorrow.",
  "priority": "high"
}
```

#### Response
```json
{
  "message": "Notification sent successfully",
  "notification_data": {
    "user": "Juan",
    "message": "Your appointment is tomorrow.",
    "priority": "high"
  },
  "channel_used": "sms"
}
```
---
## Setup Instructions
### Prerequisites
- Python 3.9+
- pip

### Installation

Clone the repository:

```
git clone https://github.com/yourusername/yourrepo.git
cd laboratories/laboratory_1/<your-ID>
```

Create and activate virtual environment:

```
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```
Install dependencies:

```
pip install -r requirements.txt

```
Run the app:

```
python main.py
```

## Testing Instructions
Using curl
Create a user

```
curl -X POST http://localhost:5000/users -H "Content-Type: application/json" -d '{
  "name": "Juan",
  "preferred_channel": "email",
  "available_channels": ["email", "sms"]
}'
```

Send a notification
```
curl -X POST http://localhost:5000/notifications/send -H "Content-Type: application/json" -d '{
  "user_name": "Juan",
  "message": "Your appointment is tomorrow.",
  "priority": "high"
}'
```
---
## Project Structure
```css
.
├── main.py
├── requirements.txt
├── README.md
├── src
│   ├── handlers
│   │   ├── handler.py
│   │   ├── email_handler.py
│   │   ├── sms_handler.py
│   │   ├── console_handler.py
│   │   ├── handler_factory.py
│   │   └── createChain.py
│   ├── models
│   │   ├── user.py
│   │   ├── notification.py
│   │   └── memory.py
│   ├── routes
│   │   └── http_handler.py
│   ├── use_cases
│   │   └── use_case.py
│   └── utils
│       └── logger.py
```