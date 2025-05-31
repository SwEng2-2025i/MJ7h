# Multichannel Notification System

**Full Name:** [Keynes Stephens Watson]

## System Explanation
This REST API allows you to register users with multiple notification channels (email, sms, console) and send notifications using a chain of responsibility. If the preferred channel fails, fallback channels are attempted. All notification attempts are logged using a Singleton logger.

### Endpoints
- `POST /users` — Register a user
- `GET /users` — List all users
- `POST /notifications/send` — Send a notification to a user
- `GET /logs` — Get notification logs
- `GET /swagger` — Swagger/OpenAPI documentation

## Class/Module Diagram
The Diagram is in the folder with name DiagramClass.png

## Design Pattern Justifications
- **Chain of Responsibility:** Used for notification delivery attempts across multiple channels.
- **Singleton:** Used for the logger to ensure a single, global log instance.

## Setup & Testing Instructions
1. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
2. Run the server:
   ```powershell
   python app.py
   ```
3. Test endpoints (examples):
   - Register user(POST/users):
     ```powershell
     curl.exe -X POST http://localhost:5000/users -H "Content-Type: application/json" -d "{\"name\":\"Juan\",\"preferred_channel\":\"email\",\"available_channels\":[\"email\",\"sms\"]}"
     ```
     -Respond:
     {
        "message": "User registered",
        "user": {
              "available_channels": [
              "email",
              "sms"
             ],
             "name": "Juan",
             "preferred_channel": "email"
        }
      }
     
   - Send notification(POST/notifications/send):
     ```powershell
     curl.exe -X POST http://localhost:5000/notifications/send -H "Content-Type: application/json" -d "{\"user_name\":\"Juan\",\"message\":\"Your appointment is tomorrow.\",\"priority\":\"high\"}"
     ```
     -Respond:
     {
       "delivered": true
      }
   - Get logs:
     ```powershell
     curl.exe http://localhost:5000/logs
     ```
     -Respond:
     [
       "Attempting EMAIL to Juan: 'Your appointment is tomorrow.' - Failed",
       "Attempting SMS to Juan: 'Your appointment is tomorrow.' - Success",
       "Attempting EMAIL to Juan: 'Your appointment is tomorrow.' - Success"
      ]

   - Get user(Get/user)
      ```powershell
      curl.exe http://localhost:5000/users
      ```
    -Respond:
      [
       {
        "available_channels": [
            "email",
            "sms"
        ],
        "name": "Juan",
        "preferred_channel": "email"
       }
      ]
   - View Swagger:
     Open http://localhost:5000/swagger in your browser.

## Documentation
- See `swagger.yaml` for full OpenAPI documentation.
- Code is well-commented for clarity.
