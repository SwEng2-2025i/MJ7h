Multichannel Notification System (REST API)

This project implements a modular REST API for a multichannel notification system using Flask. It allows users to register with multiple communication channels (e.g., email, SMS, console) and send notifications. The system prioritizes the user's preferred channel and, if delivery fails, attempts fallback channels using a Chain of Responsibility design pattern. A Singleton pattern is used for centralized logging of all notification attempts.
🎯 Objective

To develop a modular and scalable REST API for managing users and sending notifications, demonstrating the application of at least two advanced design patterns (Chain of Responsibility and Singleton).
🔁 Notification Logic

When a notification is sent:

    The system first attempts to deliver it through the user's preferred_channel.

    If delivery fails (simulated randomly using random.choice([True, False])), the system attempts the next available channel in the user's available_channels list, following the Chain of Responsibility.

    This process continues until the notification is successfully delivered or all available channels have been attempted and failed.

    Every attempt and its outcome (success/failure) are recorded by a centralized logger.

🔧 REST API Endpoints

The API exposes the following endpoints:
1. POST /users

Registers a new user with their communication preferences.

    Description: Creates a new user entry in the system's in-memory database.

    Method: POST

    URL: /users

    Request Body (JSON):

    {
      "name": "Juan",
      "preferred_channel": "email",
      "available_channels": ["email", "sms"]
    }

        name (string, required): Unique name for the user.

        preferred_channel (string, required): The user's primary channel for notifications. Must be one of ["email", "sms", "console"].

        available_channels (array of strings, required): A list of all channels the user can receive notifications through. Each element must be one of ["email", "sms", "console"].

    Responses:

        201 Created: User registered successfully.

        {
          "message": "User registered successfully",
          "user": {
            "name": "Juan",
            "preferred_channel": "email",
            "available_channels": ["email", "sms"]
          }
        }

        400 Bad Request: Missing required fields or invalid channel names.

        409 Conflict: User with the given name already exists.

2. GET /users

Lists all registered users.

    Description: Retrieves a list of all users currently registered in the system.

    Method: GET

    URL: /users

    Responses:

        200 OK: A list of user objects.

        [
          {
            "name": "Juan",
            "preferred_channel": "email",
            "available_channels": ["email", "sms"]
          },
          {
            "name": "Maria",
            "preferred_channel": "sms",
            "available_channels": ["sms", "email", "console"]
          }
        ]

3. POST /notifications/send

Sends a notification to a specified user.

    Description: Initiates the notification delivery process for a user, attempting channels based on preference and availability.

    Method: POST

    URL: /notifications/send

    Request Body (JSON):

    {
      "user_name": "Juan",
      "message": "Your appointment is tomorrow.",
      "priority": "high"
    }

        user_name (string, required): The name of the recipient user.

        message (string, required): The content of the notification message.

        priority (string, required): The priority of the notification. Can be "high", "medium", or "low".

    Responses:

        200 OK: Notification process initiated. Check logs for delivery status.

        {
          "message": "Notification process initiated. Check logs for delivery status."
        }

        400 Bad Request: Missing required fields.

        404 Not Found: The specified user_name does not exist.

        500 Internal Server Error: Notification delivery failed for all available channels or no valid channels configured for the user.

📄 Class/Module Diagram

+-----------------+       +-----------------------+       +---------------------+
|    app.py       |       |       models.py       |       |     logger.py       |
|-----------------|       |-----------------------|       |---------------------|
| - Flask app     |------>| - User class          |<------| - Logger (Singleton)|
| - API Endpoints |       | - Notification class  |       | - log()             |
| - users_db      |       +-----------------------+       | - get_logs()        |
| - Class         |                                       +---------------------+
|   Notification  |       +-----------------------+
+-----------------+       |     channels.py       |
        |                 |-----------------------|
        |                 | - NotificationChannel |<-----+
        |                 |   (Abstract)          |      |
        |                 | - EmailChannel        |      |
        |                 | - SMSChannel          |      |
        |                 | - ConsoleChannel      |      |
        |                 +-----------------------+      |
        |                                                |
        +----------------->+-----------------------+     |
                         |     handlers.py       |     |
                         |-----------------------|     |
                         | - ChannelChainBuilder |----->+
                         | - build_chain()       |
                         +-----------------------+


💡 Design Pattern Justifications
1. Chain of Responsibility Pattern

    Application: Used for handling notification delivery across multiple channels.

    Justification: This pattern is ideal for scenarios where a request (sending a notification) can be handled by one of several handlers (notification channels), and the decision of which handler to use depends on runtime conditions (channel success/failure).

        Decoupling: The sender of the notification (the app.py endpoint) is decoupled from the specific logic of each channel and their fallback order. It simply passes the notification to the head of the chain.

        Flexibility: The order and types of channels in the chain can be dynamically configured based on user preferences (preferred_channel, available_channels), without modifying the core sending logic. New channels can be added easily without impacting existing ones.

        Fallback Mechanism: It naturally supports the required fallback mechanism, where if one channel fails, the request is automatically passed to the next in line.

2. Singleton Pattern

    Application: Used for the Logger class.

    Justification: This pattern ensures that a class has only one instance and provides a global point of access to that instance.

        Centralized Logging: A single logger instance ensures that all notification attempts, successes, and failures across the entire application are recorded in one consistent place, preventing dispersed log management.

        Resource Management: For resources that should only have one instance (like a global configuration manager or, in this case, a log file handler if persistence were added), Singleton prevents multiple instances from conflicting or consuming unnecessary resources.

        Global Access: It provides a well-known, single point of access to the logging functionality from any part of the application.

🚀 Setup and Testing Instructions
Prerequisites

    Python 3.8+

    pip (Python package installer)

Installation

    Clone the repository (if applicable, otherwise save the files):

    # Assuming you have the files in a directory named 'notification_system'
    # cd notification_system

    Install required Python packages:

    pip install Flask Flask-RESTX

Running the Application

    Navigate to the project directory:

    cd /path/to/your/notification_system

    Run the Flask application:

    python app.py

    The application will start on http://127.0.0.1:5000/ (or http://localhost:5000/).

Testing the API

You can use curl from your terminal or a tool like Postman/Insomnia to test the endpoints.
1. Register a User (POST /users)

curl -X POST \
  http://127.0.0.1:5000/users/ \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Alice",
    "preferred_channel": "email",
    "available_channels": ["email", "sms", "console"]
  }'
```bash
curl -X POST \
  http://127.0.0.1:5000/users/ \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Bob",
    "preferred_channel": "sms",
    "available_channels": ["sms", "email"]
  }'

2. List All Users (GET /users)

curl -X GET \
  http://127.0.0.1:5000/users/

3. Send a Notification (POST /notifications/send)

To Alice (preferred: email, fallback: sms, console):

curl -X POST \
  http://127.0.0.1:5000/notifications/send \
  -H 'Content-Type: application/json' \
  -d '{
    "user_name": "Alice",
    "message": "Your meeting is at 10 AM",
    "priority": "high"
  }'

Observe the console output for log messages indicating delivery attempts and success/failure for each channel.

To Bob (preferred: sms, fallback: email):

curl -X POST \
  http://127.0.0.1:5000/notifications/send \
  -H 'Content-Type: application/json' \
  -d '{
    "user_name": "Bob",
    "message": "Your package has shipped!",
    "priority": "medium"
  }'

Again, check the console for detailed delivery logs.
📚 Documentation using Swagger

The API is self-documented using Swagger UI, which can be accessed at:

    Swagger UI: http://127.0.0.1:5000/apidocs/

This interface provides a visual way to explore the endpoints, understand their parameters, and even make test requests directly from the browser.