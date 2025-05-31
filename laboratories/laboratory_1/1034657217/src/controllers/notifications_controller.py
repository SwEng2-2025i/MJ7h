from flask import jsonify, request
from model import usersModel
from services.notification_service import NotificationService
class NotificationsController:
    def __init__(self):
        self.user_model = usersModel.UsersModel()
        self.notification_service = NotificationService()
    
    def sendNotification(self):
        try:
            notification_data = request.json
            user_name = notification_data.get('user_name')
            message = notification_data.get('message')
            priority = notification_data.get('priority')
            # verificar que estén todos los campos
            if not all([user_name,message,priority]):
                return jsonify({"error":"Missing values"}), 400
            #usa la cadena de responsabilidad
            notification_success = self.notification_service.sendNotification(notification_data)

            return jsonify({
                "success":notification_success
            }),200
    

        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
                }), 500
            