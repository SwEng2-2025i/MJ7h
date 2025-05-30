from flask import jsonify, request
from model import usersModel
from services.notification_chain import NotificationChain
class NotificationsController:
    def __init__(self):
        self.user_model = usersModel.UsersModel()
    
    def sendNotification(self):
        try:
            notification_data = request.json
            user_name = notification_data.get('user_name')
            message = notification_data.get('message')
            priority = notification_data.get('priority')

            if not all([user_name,message,priority]):
                return jsonify({"error":"Missing values"}), 400
            
            notification_sender = NotificationChain()
            notification_sender.buildChain(user_name)
            success = notification_sender.sendNotification(notification_data)

            return jsonify({
                "user_name":user_name,
                "message":message,
                "priority":priority
            }),200
    

        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
                }), 500
            