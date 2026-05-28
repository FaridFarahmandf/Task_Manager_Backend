from marshmallow import fields, Schema

from schemas.userschema import PlainUserSchema

class PlainTaskSchema(Schema): 
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    status = fields.Str(required=True)
    priority = fields.Str(required=True)
    
class TaskSchema(PlainTaskSchema):
    creator_id = fields.Int(required=True, load_only=True)
    creator = fields.Nested(PlainUserSchema(), dump_only=True)
    assigned_users = fields.List(fields.Nested(PlainUserSchema(),required=True, dump_only=True))
    assigned_user_ids = fields.List(
        fields.Int(),
        load_only=True
    ) #When creating a task, do you want to assign users at the same time?
