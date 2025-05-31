from flask_restful import Resource, reqparse
from core.models import User, ChannelType
from core.repository import USERS

# ---------- parser de argumentos ------------------------------------------
_parser = reqparse.RequestParser()
_parser.add_argument("name", required=True, type=str)
_parser.add_argument("preferred_channel", required=True, type=str)
_parser.add_argument(
    "available_channels", required=True, type=list, location="json"
)


class UserResource(Resource):
    # ---------------------- POST /users ------------------------------------
    def post(self):
        """
        Register a new user
        ---
        tags: [Users]

        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required: [name, preferred_channel, available_channels]
              properties:
                name:
                  type: string
                  example: Juan
                preferred_channel:
                  type: string
                  enum: [email, sms, console]
                  example: email
                available_channels:
                  type: array
                  items:
                    type: string
                    enum: [email, sms, console]
                  example: ["email", "sms"]

        responses:
          201:
            description: User created
            schema:
              $ref: '#/definitions/User'
          400:
            description: User already exists

        definitions:
          User:
            type: object
            properties:
              id:
                type: string
                format: uuid
                example: 57464933-b41a-4492-91df-9cb427b9dfa9
              name:
                type: string
                example: Juan
              preferred_channel:
                type: string
                enum: [email, sms, console]
                example: email
              available_channels:
                type: array
                items:
                  type: string
                  enum: [email, sms, console]
                example: ["email", "sms"]
        """
        data = _parser.parse_args()
        name = data["name"]

        if name in USERS:
            return {"error": "User already exists"}, 400

        preferred = ChannelType[data["preferred_channel"].upper()]

        # filtra duplicados y el propio preferido
        backups = []
        for c in data["available_channels"]:
            ct = ChannelType[c.upper()]
            if ct != preferred and ct not in backups:
                backups.append(ct)

        user = User.create(name, preferred, backups)
        USERS[name] = user
        return {"id": user.id, "name": user.name}, 201

    # ---------------------- GET /users -------------------------------------
    def get(self):
        """
        List all users
        ---
        tags: [Users]
        responses:
          200:
            description: Array of users
            schema:
              type: array
              items:
                $ref: '#/definitions/User'
        """
        return [
            {
                "id": u.id,
                "name": u.name,
                "preferred_channel": u.preferred_channel.name.lower(),
                "available_channels": [c.name.lower() for c in u.backup_channels],
            }
            for u in USERS.values()
        ], 200
