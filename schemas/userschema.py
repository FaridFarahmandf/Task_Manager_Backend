from marshmallow import fields, Schema

from schemas.taskschema import PlainTaskSchema


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    name = fields.Str(required=True)
    role = fields.Str(required=True)
    country= fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    email = fields.Str(required=True)
    
class UserSchema(PlainUserSchema):
    created_tasks = fields.List(fields.Nested(PlainTaskSchema()), dump_only=True)
    assigned_tasks = fields.List(fields.Nested(PlainTaskSchema()), dump_only=True)
    