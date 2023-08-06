from marshmallow import Schema, fields


class LoginSchema(Schema):
    email = fields.Str()
    password = fields.Str()
