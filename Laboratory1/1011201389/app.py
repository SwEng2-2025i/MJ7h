from flask import Flask
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# Enpoints definition

# Register users
@app.post('/users')
def register_user():
    pass

# Get users
@app.get('/users')
def get_users():
    pass

# Send a notification
@app.route('/notifications/send')
def send_notification():
    pass