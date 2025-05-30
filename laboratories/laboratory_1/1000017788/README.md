# 🧪 Advanced Individual Lab: Multichannel Notification System (REST API)

**Developer:** David Alejandro Cifuentes Gonzalez 
**Date:** May 29, 2025  
 

## 📝 Context

In today's software architecture, building modular and scalable systems is essential. Design patterns play a key role in helping developers write cleaner, more maintainable, and extensible code.

This project implements a REST API for a notification system where users can register with multiple communication channels (e.g., email, SMS, console). When sending a notification, the system attempts to deliver it through the user's preferred channel first. If delivery fails (simulated randomly), the system attempts backup channels using a chain of responsibility.

The system implements **four design patterns**: Chain of Responsibility, Singleton, Strategy, and Factory patterns to create a robust, maintainable, and extensible notification system.

---

## 🎯 Objective

Develop a modular REST API to manage users and send notifications using **four advanced design patterns**: Chain of Responsibility, Singleton, Strategy, and Factory patterns.

---

## 🏗️ Architecture & Design Patterns

### 1. **Chain of Responsibility Pattern**
- **Purpose**: Handle notification delivery through different channels with fallback support
- **Implementation**: `patterns/chain_of_responsibility.py`
- **Components**:
  - `NotificationHandler`: Abstract base class
  - `EmailHandler`: Handles email notifications
  - `SMSHandler`: Handles SMS notifications  
  - `ConsoleHandler`: Handles console notifications (always succeeds as fallback)
  - `NotificationChain`: Manages the chain of handlers

### 2. **Singleton Pattern**
- **Purpose**: Ensure only one logger instance exists throughout the application
- **Implementation**: `patterns/singleton.py`
- **Components**:
  - `NotificationLogger`: Singleton logger that records all notification attempts

### 3. **Strategy Pattern**
- **Purpose**: Handle different notification priority processing strategies
- **Implementation**: `patterns/strategy.py`
- **Components**:
  - `HighPriorityStrategy`: Adds urgency indicators
  - `MediumPriorityStrategy`: Adds standard indicators
  - `LowPriorityStrategy`: Adds notice indicators
  - `NotificationStrategyContext`: Context for managing strategies

### 4. **Factory Pattern**
- **Purpose**: Create notification handlers based on channel type
- **Implementation**: `patterns/factory.py`
- **Components**:
  - `NotificationChannelFactory`: Creates appropriate handlers for each channel type

---

## 📁 Project Structure

```
├── app.py                          # Main Flask application with REST API endpoints
├── config.py                       # Application configuration
├── requirements.txt                # Python dependencies
├── test_api.py                     # API testing script
├── models/
│   ├── __init__.py
│   ├── user.py                     # User model
│   └── notification.py             # Notification model
├── patterns/
│   ├── __init__.py
│   ├── chain_of_responsibility.py  # Chain of Responsibility pattern
│   ├── singleton.py                # Singleton pattern
│   ├── strategy.py                 # Strategy pattern
│   └── factory.py                  # Factory pattern
└── tests/
    ├── __init__.py
    └── test_notification_system.py # Unit tests
```

---

## 🔁 Notification Logic

You will simulate delivery attempts via a **Chain of Responsibility**. For example:

1. A user has preferred channel = `email`, available = `[email, sms]`
2. Email channel is attempted (random failure simulated)
3. If it fails, the next channel (sms) is attempted

Use `random.choice([True, False])` to simulate failures.

---

## 🔧 REST API Endpoints

| Method | Endpoint              | Description                                      |
|--------|-----------------------|--------------------------------------------------|
| POST   | `/users`              | Register a user with name, preferred and available channels |
| GET    | `/users`              | List all users                                   |
| POST   | `/notifications/send` | Send a notification with message and priority    |

### Example Payloads

**POST /users**
```json
{
  "name": "Juan",
  "preferred_channel": "email",
  "available_channels": ["email", "sms"]
}
```

**POST /notifications/send**
```json
{
  "user_name": "Juan",
  "message": "Your appointment is tomorrow.",
  "priority": "high"
}
```


---

## 🚀 Setup and Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone or download the project**
   ```powershell
   cd "your patch"
   ```

2. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```powershell
   python app.py
   ```

4. **Access the API**
   - API Base URL: `http://localhost:5000`
   - Swagger Documentation: `http://localhost:5000/swagger/`

### Testing the API

**Option 1: Use the provided test script**
```powershell
python test_api.py
```

**Option 2: Run unit tests**
```powershell
python -m pytest tests/ -v
```

**Option 3: Manual testing with curl**
```powershell
# Register a user
curl -X POST http://localhost:5000/users -H "Content-Type: application/json" -d '{\"name\": \"Juan\", \"preferred_channel\": \"email\", \"available_channels\": [\"email\", \"sms\"]}'

# List users
curl -X GET http://localhost:5000/users

# Send notification
curl -X POST http://localhost:5000/notifications/send -H "Content-Type: application/json" -d '{\"user_name\": \"Juan\", \"message\": \"Test message\", \"priority\": \"high\"}'
```

---

## 📊 System Flow Diagram

```
User Registration → User Storage (In-Memory)
                          ↓
Notification Request → Strategy Pattern (Priority Processing)
                          ↓
                   Factory Pattern (Handler Creation)
                          ↓
              Chain of Responsibility (Channel Attempts)
                          ↓
                   Singleton Logger (Record Attempts)
                          ↓
                      Response to Client
```

---

## 🔧 API Endpoints Documentation

### Base URL: `http://localhost:5000`

### 1. User Management

#### **POST /users** - Register a new user
**Request Body:**
```json
{
  "name": "Juan",
  "preferred_channel": "email",
  "available_channels": ["email", "sms"]
}
```

**Response (201 Created):**
```json
{
  "id": "uuid-string",
  "name": "Juan",
  "preferred_channel": "email",
  "available_channels": ["email", "sms"],
  "created_at": "2025-05-29T10:30:00"
}
```

#### **GET /users** - List all users
**Response (200 OK):**
```json
[
  {
    "id": "uuid-string",
    "name": "Juan",
    "preferred_channel": "email",
    "available_channels": ["email", "sms"],
    "created_at": "2025-05-29T10:30:00"
  }
]
```

### 2. Notification Management

#### **POST /notifications/send** - Send a notification
**Request Body:**
```json
{
  "user_name": "Juan",
  "message": "Your appointment is tomorrow.",
  "priority": "high"
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Notification processed",
  "notification_id": "uuid-string",
  "attempts": 2,
  "delivered": true
}
```

---

## 🔄 Notification Flow Example

1. **User Registration:**
   - User "Juan" registers with preferred channel "email" and available channels ["email", "sms"]

2. **Notification Request:**
   - High priority notification sent to "Juan"
   - Strategy Pattern processes message: "🚨 URGENT: Your appointment is tomorrow."

3. **Handler Creation:**
   - Factory Pattern creates EmailHandler and SMSHandler

4. **Chain Processing:**
   - EmailHandler attempts delivery (simulated random failure)
   - If email fails, SMSHandler attempts delivery
   - ConsoleHandler serves as final fallback (always succeeds)

5. **Logging:**
   - Singleton Logger records all attempts and outcomes

---

## 🧪 Testing Examples

### Postman Collection

**1. Register Users:**
```json
POST http://localhost:5000/users
{
  "name": "Maria",
  "preferred_channel": "sms",
  "available_channels": ["sms", "console"]
}
```

**2. Send High Priority Notification:**
```json
POST http://localhost:5000/notifications/send
{
  "user_name": "Maria",
  "message": "Emergency system alert",
  "priority": "high"
}
```

**3. Send Low Priority Notification:**
```json
POST http://localhost:5000/notifications/send
{
  "user_name": "Maria",
  "message": "Weekly newsletter available",
  "priority": "low"
}
```

---

## 🎨 Design Pattern Justifications

### **Chain of Responsibility**
- **Why:** Allows flexible handling of notification delivery with automatic fallback to alternative channels
- **Benefit:** Easy to add new notification channels without modifying existing code
- **Implementation:** Each handler attempts delivery and passes to next handler on failure

### **Singleton**
- **Why:** Ensures consistent logging across the entire application with a single point of access
- **Benefit:** Prevents multiple logger instances and maintains centralized log management
- **Implementation:** Thread-safe singleton with lazy initialization

### **Strategy**
- **Why:** Enables different processing strategies based on notification priority
- **Benefit:** Easy to add new priority levels and modify processing logic independently
- **Implementation:** Context class manages different priority strategies

### **Factory**
- **Why:** Centralizes creation of notification handlers and abstracts instantiation logic
- **Benefit:** Easy to add new channel types and modify handler creation logic
- **Implementation:** Maps channel types to handler classes with extensible registration

---

## 📈 System Features

### ✅ Implemented Features
- [x] REST API with Flask and Swagger documentation
- [x] User registration and management
- [x] Multi-channel notification delivery
- [x] Random failure simulation
- [x] Chain of responsibility for fallback channels
- [x] Priority-based message processing
- [x] Comprehensive logging system
- [x] Unit tests with good coverage
- [x] Modular, clean architecture

### 🔮 Possible Enhancements
- [ ] Database persistence (SQLite/PostgreSQL)
- [ ] Real notification delivery (SMTP, SMS APIs)
- [ ] Authentication and authorization
- [ ] Notification scheduling
- [ ] Delivery status tracking
- [ ] Rate limiting and throttling
- [ ] Metrics and monitoring

---

## 🐛 Troubleshooting

### Common Issues

**1. Module Import Errors**
```powershell
# Ensure you're in the project directory
cd "your path"
# Set Python path if needed
$env:PYTHONPATH = "."
python app.py
```

**2. Port Already in Use**
```
Error: Address already in use
```
- Change port in `app.py`: `app.run(port=5001)`
- Or kill process using port 5000

**3. Missing Dependencies**
```powershell
pip install -r requirements.txt --upgrade
```

---

## 📝 Development Notes

### Code Quality Standards
- All functions have docstrings
- Type hints used throughout
- Comprehensive error handling
- Consistent naming conventions
- Modular architecture with separation of concerns

### Testing Strategy
- Unit tests for all design patterns
- Integration tests for API endpoints
- Failure simulation testing
- Edge case validation

---

## 👤 Author

**Developer:** David Alejandro Cifuentes Gonzalez
**Student ID:** 1000017788
**Date:** May 29, 2025  


---


**⏱️ Delivery Date:** May 30, 2025 - 23:59 GMT-5
