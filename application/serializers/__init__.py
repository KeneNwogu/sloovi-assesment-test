from application import ma, mongo
from marshmallow import fields


class TemplatesSerializer(ma.Schema):
    class Meta:
        fields = ("template_name", "subject",  "body")


class UserSerializer(ma.Schema):
    email = fields.Email(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    password = fields.String(required=True)
