from flask import Blueprint, jsonify
from controllers.notifications_controller import NotificationsController

notifications_bp = Blueprint("notifications",__name__,url_prefix='/notifications')
notifications_controller = NotificationsController()

@notifications_bp.route('/send',methods=['POST'])
def send_notification():
    return notifications_controller.sendNotification()