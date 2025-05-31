from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    name = fields.Str(required=True)
    preferred_channel = fields.Str(required=True, validate=validate.OneOf(["email", "sms"]))
    available_channels = fields.List(fields.Str(validate=validate.OneOf(["email", "sms"])), required=True)