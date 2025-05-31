from flask import Flask
from flask_restx import Api

app = Flask(__name__)
api = Api(app, version='1.0', title='Multichannel Notification System API',
    description='A REST API for a notification system using Chain of Responsibility and Singleton patterns.')

if __name__ == '__main__':
    app.run(debug=True) 