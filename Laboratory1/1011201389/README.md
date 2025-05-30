# Laboratory 1
Samuel Josué Vargas Castro

The system consists in sending notifications to users through an endpoint. The system has three main endpoints. POST /users create a user with the fields name, preferred_channel and available_channels; GET /users obtain all users and POST /notifications/send, sends a notification through the petition body, with the user_name, the message and the priority.

The system receives the data from the api built with Flask and stores the users in a runtime database.
Every incoming data is validated using chains of handlers for the different attributes of the data, to be then stored in the local models.
For the notification, the systems receives the data through the endpoint, search the destiny user and sends both objects to a notification service. The notification service stores the available handlers for the different channels in the system and builts a chain of responsibility with the desired channels of the user, beginning with the preferred channel. It also allows to write a succesful or unsuccesful response in a global aplication logger. Once there, the system tries to send in the first handler and if its succesful, returns the notification sent, but if it's unsuccessful, it pass the operation to next handler. Either way, every try is registered in the logger. Once every channel fails, the system sents an error response and logs that every channel failed.

# Diagram

# Design Patterns

In the system, there were various implemented designed patterns to ensure a better code.
- Factory Method: In the models' classes, there was defined a from_dict method that receives a dictionary and builds the object without accessing publicly to the constructor, enabling a better creation of objects and reducing the code repetition.
- Chain of Responsibility: This pattern was used for two main reasons, first, the data incoming in the responses should be in a specific format, and the builiding of chains of validations ensure that the different parameters are in the correct form and also is open in the future to change the rules of validation easily. On the other hand, it was used for the management of the available and preferred channels of the user, in this way, if a notification try fails, another handler assumes the responsibility.
- Singleton: This pattern was used to ensure  an unique access to a logger instance, allowing an unified view to register the information concerning the notificications attempts.

# Setup and configuration

First, clone the repository
On the main folder of the system laboratories/laboratory_1/1011201389/ there's a requirements.txt file, use the command <insert the command> to install the dependencies on the file, or also run the following command pip install flask flasgger
Once running, you can create a user by doing a POST petition to the http://127.0.0.1:5001/users with the fields name, preferred_channel, available_channels. <Show the curl command>
You can get a list of all users by doing a GET petition to the http://127.0.0.1:5001/users.
You can send a notification to a user by doing a POST petition to the the http://127.0.0.1:5001/notification/send with the fields user_name, message and priority.
Finally, you can see all the documentation of the api in http://127.0.0.1:5001/apidocs/
