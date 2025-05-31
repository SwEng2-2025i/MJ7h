from flask_restful import Resource, reqparse
from core.repository import USERS, NOTIFICATIONS
from core.models import Notification
from core.patterns.chain import build_chain_for
from core.logger import EventLogger

# ------------------- parser ------------------------------------------------
_parser = reqparse.RequestParser()
_parser.add_argument("user_name", required=True, type=str)
_parser.add_argument("message", required=True, type=str)
_parser.add_argument(
    "priority",
    required=False,
    type=str,
    choices=("low", "normal", "high"),
    default="normal",
)


class NotificationSendResource(Resource):
    def post(self):
        """
        Send a notification
        ---
        tags: [Notifications]

        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required: [user_name, message]
              properties:
                user_name:
                  type: string
                  example: Juan
                message:
                  type: string
                  example: Your appointment is tomorrow.
                priority:
                  type: string
                  enum: [low, normal, high]
                  default: normal

        responses:
          200:
            description: Notification delivered via at least one channel
            schema:
              type: object
              properties:
                notification_id: {type: string, format: uuid}
                delivered:       {type: boolean}
            examples:
              application/json:
                notification_id: 02f7b9c8-dac6-436f-8c85-b36206be4d28
                delivered: true

          404:
            description: User not found

          500:
            description: Delivery failed on all channels
            schema:
              type: object
              properties:
                notification_id: {type: string, format: uuid}
                delivered:       {type: boolean}

        definitions:
          NotificationResult:
            type: object
            properties:
              notification_id:
                type: string
                format: uuid
              delivered:
                type: boolean
        """
        data = _parser.parse_args()
        user = USERS.get(data["user_name"])

        if not user:
            return {"error": "User not found"}, 404

        notif = Notification.create(user, data["message"])
        NOTIFICATIONS[notif.id] = notif

        chain = build_chain_for(user)
        logger = EventLogger()

        delivered = chain.handle(notif)

        logger.info(
            f"END  | notif={notif.id} | user={user.name} | "
            f"priority={data['priority']} | delivered={delivered}"
        )

        status = 200 if delivered else 500
        return {"notification_id": notif.id, "delivered": delivered}, status
