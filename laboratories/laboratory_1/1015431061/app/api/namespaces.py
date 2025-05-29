from flask_restx import Namespace

user_ns = Namespace('users', description='User operations')
notification_ns = Namespace('notifications', description='Notification operations')