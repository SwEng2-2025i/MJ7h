
# Notification Delivery System

  

## Author

- Estephanie Pérez Mira - eperezmi@unal.edu.co

  

## System Overview

  

This project implements a notification delivery system that allows sending messages to users via various channels (e.g., email, WhatsApp). It also keeps a history of all sent notifications, using In Memory storage.

  

## Features

  

- Keeps a repository of users.

- Send notifications to a user via their available channels.

- Log every sent notification with metadata for auditability.

  

## Endpoints
Their description can be found at greater detail at the [Swagger Documentation](http://localhost:5000/apidocs/#/Users/post_users), when running the flask application.
  

###  `POST /notifications/send`

  

**Description**: Send a notification to a specific user.

  

**Request Body**:

```json

{

"user_name":  "john_doe",

"message":  "Your order #123 has been shipped!",

"priority":  "High"

}

```

  

**Response**:

```json

{

"status":  "Notification processed",

"successfully_sent":  true

}

```

  

###  `GET /notifications/logger`

  

**Description**: Retrieve the list of previously sent notifications.

  

**Response**:

```json

{

"logs":  [

{

"timestamp":  "2025-05-30 18:31:02.276949",

"username":  "Juan",

"channel":  "whatsapp",

"message":  "Your appointment is tomorrow.",

"priority":  "medium",

"successful":  false

}

]

}

```


## Design Patterns Used
### Chain of Responsibility Patterns
In this proyect, the Chain of Responsibility pattern is employed to establish a flexible and extensible sequence of processing steps, within two primary contexts:
- **HTTP Request Body Validation**: This application of the pattern ensures that incoming HTTP request bodies adhere to predefined structural and data requirements. Each handler in the chain is responsible for validating a specific parameter or condition. If a parameter is invalid or missing, the chain terminates, and an appropriate error is returned. The two instances of classes implemented are described below:
	- **User Creation (`POST /users`)**: this chain validates the request body submitted for creating a new user profile, ensuring the presence of mandatory user attributes:
		```
		data  =  request.json
		
		user_body_handler  =  NewUsernameGivenHandler(ValidatePreferredChannelHandler(ValidateAvailableChannelsHandler(SuccessHandler())))
		
		result  =  user_body_handler.handle(data)
		```
	- **Notification Request (`POST /notifications/send`)**: This chain validates the request body for sending notifications, verifying that all necessary attributes for constructing a notification object are present:
		```
		data  =  request.json
		
		notification_body_handler  =  UsernameGivenHandler(MessageGivenHandler(PriorityGivenHandler(SuccessHandler())))

		result  =  notification_body_handler.handle(data)
		```
- **Notification Channel Delivery Logic**: Beyond validation, the Chain of Responsibility pattern is also utilized to implement the sequential logic for attempting notification delivery across various communication channels. This ensures that the preferred channel is attempted first, with subsequent fallback to other available channels if the initial attempt is unsuccessful. This design encapsulates complex retry and fallback mechanisms, making the primary notification sending logic cleaner.
	- **Notification Channel Handling (`POST /notifications/send`)**: This chain receives both the notification body `data` and the `User` object, allowing handlers within the chain to access the user's preferred and available channels through dependency injection:
		```
		notification_channels_handler  =  TryPreferredChannel(TryOtherChannels())

		successful  =  notification_channels_handler.handle(user,  data)
		```
### Strategy Pattern
The Strategy pattern comes with the great feature of defining a family of algorithms, each encapsulated into a separate class, and making them interchangeable depending of the context being called.
In this project, the Strategy pattern plays a crucial role within the **Notification Channel Delivery Chain of Responsibility**, facilitating the dynamic selection of the appropriate communication method (e.g., email, SMS, WhatsApp) based on the user's preferences and available channels.
- **Excerpt from Notification Channel Handlers:** Both TryPreferredChannel and TryOtherChannels handlers, dynamically instantiate and utilize the **appropriate strategy** based on the channel selected:
	```
	class TryPreferredChannel(Handler):
    def handle(self, user:User,data):
        # Send notification
        channel = user.preferred_channel
        strategy_cls = current_app.config["STRATEGY_MAP"].get(channel)
        strategy = NotificationContext(strategy_cls())
        successful = strategy.send(user, data.get("message"), data.get("priority")) # Log is saved inside this method

        if successful:
            return successful
        else:
            return super().handle(user, data)
     ```
	```
	class TryOtherChannels(Handler):
	    def handle(self, user:User,data):
	        successful = False
	        for channel in user.available_channels:
	            if channel != user.preferred_channel:
	                strategy_cls = current_app.config["STRATEGY_MAP"].get(channel)
	                strategy = NotificationContext(strategy_cls())
	                successful = strategy.send(user, data.get("message"), data.get("priority")) # Log is saved inside this method
	                if successful:
	                    break
	        
	        return successful
	```

## Setup Instructions

  

1.  **Clone the repository**:

```bash

git  clone  https://github.com/SwEng2-2025i/MJ7h.git

cd  Laboratory1/1013100405/Lab1/

```

  

2.  **Install dependencies**:

```bash

pip  install  Flask, Flasgger

```

  

3.  **Run the Flask app**:

```bash

python  main.py

```

  

## Testing with CURL
### Create a New User
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    	"username": "Juan",
    	"preferred_channel": "whatsapp",
    	"available_channels": ["email", "sms"
,"whatsapp","instagram"]
  }'
```
Expected output:
```bash
{
  "available_channels": [
	"email",
	"sms",
	"whatsapp",
	"instagram"
  ],
  "preferred_channel": "whatsapp",
  "username": "Juan"
}
```
### Retrieve All Users
```bash
curl http://localhost:5000/users \
```
Expected output:
```bash
[
  {
	"available_channels": [
  	"email",
  	"sms",
  	"whatsapp",
  	"instagram"
	],
	"preferred_channel": "whatsapp",
	"username": "Juan"
  }
]
```
### Send a Notification

```bash

curl -X POST http://localhost:5000/notifications/send \
  -H "Content-Type: application/json" \
  -d '{
	"user_name": "Juan",
	"message": "Your appointment is tomorrow.",
	"priority": "high"
  }'
```
Expected output ("successful" status will vary):
```bash
{
  "status": "Notification processed",   	 
  "successfully_sent": true
}
```
  

### Retrieve Notification Logs

```bash

curl http://localhost:5000/notifications/logger

```
Expected output (successful, timestamp and number of attempted sendings will vary):
```bash
{
  "logs": [
	{
  	"channel": "whatsapp",
  	"message": "Your appointment is tomorrow.",
  	"priority": "medium",
  	"successful": false,
  	"timestamp": "2025-05-30 18:31:02.276949",
  	"username": "Juan"
	},
	{
  	"channel": "email",
  	"message": "Your appointment is tomorrow.",
  	"priority": "medium",
  	"successful": true,
  	"timestamp": "2025-05-30 18:31:02.276985",
  	"username": "Juan"
	}
  ]
}
```
