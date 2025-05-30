from flask import jsonify, request
from model import usersModel

class NotificationsController:
    def __init__(self):
        self.user_model = usersModel.UsersModel()
    
    def sendNotification(self):
        try:
            return jsonify({
                "user_name":"martin",
                "message":"notification",
                "priority":"high"
            }), 200
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
                }), 500
            