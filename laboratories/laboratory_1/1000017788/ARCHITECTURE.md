# 🏗️ Class/Module Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    MULTICHANNEL NOTIFICATION SYSTEM             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Flask API     │────│   Controllers    │────│   Models        │
│   (app.py)      │    │   (Endpoints)    │    │   (Data)        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                       │
         │                        │                       │
         ▼                        ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DESIGN PATTERNS LAYER                      │
├─────────────────┬─────────────────┬─────────────────┬──────────┤
│ Chain of Resp.  │   Singleton     │   Strategy      │ Factory  │
│ (Notifications) │   (Logger)      │ (Priorities)    │(Handlers)│
└─────────────────┴─────────────────┴─────────────────┴──────────┘
```

## Detailed Class Relationships

### 1. Models Layer
```
User
├── id: str
├── name: str
├── preferred_channel: str
├── available_channels: List[str]
├── created_at: datetime
└── to_dict() → dict

Notification
├── id: str
├── user_name: str
├── message: str
├── priority: str
├── created_at: datetime
├── delivered: bool
├── delivery_channel: Optional[str]
├── attempts: int
├── mark_delivered(channel: str)
├── add_attempt()
└── to_dict() → dict
```

### 2. Chain of Responsibility Pattern
```
NotificationHandler (Abstract)
├── _next_handler: Optional[NotificationHandler]
├── set_next(handler) → NotificationHandler
└── handle(notification, user) → bool (Abstract)
    │
    ├── EmailHandler
    │   └── handle() → bool (Random success/failure)
    │
    ├── SMSHandler
    │   └── handle() → bool (Random success/failure)
    │
    └── ConsoleHandler
        └── handle() → bool (Always succeeds)

NotificationChain
├── first_handler: Optional[NotificationHandler]
├── last_handler: Optional[NotificationHandler]
├── add_handler(handler)
└── handle(notification, user) → bool
```

### 3. Singleton Pattern
```
NotificationLogger (Singleton)
├── _instance: NotificationLogger (Class variable)
├── _initialized: bool (Class variable)
├── logs: List[str]
├── logger: logging.Logger
├── log(message: str)
├── get_logs() → List[str]
└── clear_logs()
```

### 4. Strategy Pattern
```
NotificationStrategy (Abstract)
└── process(notification) → Notification (Abstract)
    │
    ├── HighPriorityStrategy
    │   └── process() → "🚨 URGENT: {message}"
    │
    ├── MediumPriorityStrategy
    │   └── process() → "ℹ️ INFO: {message}"
    │
    └── LowPriorityStrategy
        └── process() → "📝 NOTICE: {message}"

NotificationStrategyContext
├── _strategy: NotificationStrategy
├── set_strategy(strategy)
└── process_notification(notification) → Notification
```

### 5. Factory Pattern
```
NotificationChannelFactory
├── _handlers: Dict[str, Type[NotificationHandler]]
├── create_handler(channel: str) → NotificationHandler
├── get_available_channels() → list
└── register_handler(channel, handler_class)
```

## Data Flow Diagram

```
HTTP Request
    │
    ▼
┌─────────────────┐
│ Flask Endpoint  │ (POST /users, GET /users, POST /notifications/send)
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Input Validation│ (Validate JSON, check required fields)
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Model Creation  │ (User/Notification objects)
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Strategy Pattern│ (Process priority: High/Medium/Low)
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Factory Pattern │ (Create appropriate handlers)
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Chain of Resp.  │ (Attempt delivery through channels)
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Singleton Logger│ (Log all attempts and results)
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ HTTP Response   │ (JSON with status and details)
└─────────────────┘
```

## Pattern Interaction Example

```
1. User sends POST /notifications/send
2. API validates input and creates Notification object
3. Strategy Pattern processes message based on priority:
   - High: "🚨 URGENT: {message}"
   - Medium: "ℹ️ INFO: {message}" 
   - Low: "📝 NOTICE: {message}"
4. Factory Pattern creates handlers for user's channels
5. Chain of Responsibility attempts delivery:
   - Try preferred channel first
   - If fails, try next available channel
   - Continue until success or all channels exhausted
6. Singleton Logger records every attempt
7. Return success/failure status to client
```

## System Benefits

### Modularity
- Each pattern handles a specific concern
- Easy to add new channels, priorities, or strategies
- Clean separation of responsibilities

### Extensibility
- New notification channels: Add handler + register in factory
- New priority levels: Create new strategy class
- New logging destinations: Extend singleton logger
- New validation rules: Modify endpoint logic

### Maintainability
- Single responsibility principle followed
- Clear pattern implementations
- Comprehensive logging for debugging
- Well-documented code with type hints

### Reliability
- Automatic fallback through chain of responsibility
- Always-successful console handler as final fallback
- Comprehensive error handling and validation
- Singleton ensures consistent logging
