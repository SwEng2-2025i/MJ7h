from marshmallow import Schema, fields, validate

class NotificationSchema(Schema):
    user_name = fields.Str(required=True)
    message = fields.Str(required=True)
    priority = fields.Str(required=True, validate=validate.OneOf(["alta", "media", "baja"]))
