# 🧪 Advanced Individual Lab: Multichannel Notification System (REST API)

## 📝 Context

In today's software architecture, building modular and scalable systems is essential. Design patterns play a key role in helping developers write cleaner, more maintainable, and extensible code.

In this individual lab, you will implement a REST API for a notification system where users can register with multiple communication channels (e.g., email, SMS, console). When sending a notification, the system should first attempt to deliver it through the user's preferred channel. If delivery fails (simulated randomly), the system should attempt backup channels using a chain of responsibility.

The lab requires the use of at least two design patterns (chain of responsibility and one additional pattern of your choice). You will simulate notification logic, model system behavior, and structure the solution into clean, reusable components.

---

## 🎯 Objective

Develop a modular REST API to manage users and send notifications using **at least two advanced design patterns**, in addition to detailed design patterns.

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

## ✅ Requirements

- Use Flask for REST API
- Apply at least two design patterns
- Simulate channel failures and retry using fallback
- Logger must record every notification attempt (optional Singleton)
- No database required (in-memory data structures allowed)
- Code must be modular, clean, and well-documented

---

## 📄 Deliverable

- Complete source code in organized structure
- A `README.md` that includes:
  - README.md with the full name.
  - System explanation and endpoint documentation
  - Class/module diagram
  - Design pattern justifications
  - Setup and testing instructions (e.g., curl/Postman examples)
- Documentation using Swagger should be included
- Well-commented code

---



## Submission Format- 
It must be delivered **via a pull request to the main branch of the repository**, which must be merged before the delivery date. In the folder laboratories/laboratory_1, create an X folder (where X = your identity document number), which must include the deliverable.


## ⏱️ Delivery date -> MAY 30, 2025 -> 23:59 GTM-5
