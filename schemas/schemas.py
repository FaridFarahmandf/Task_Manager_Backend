from marshmallow import fields, Schema


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    name = fields.Str(required=True)
    role = fields.Str(required=True)
    country= fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    email = fields.Str(required=True)
    selectedUser = fields.Bool()
    


class PlainTaskSchema(Schema): 
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    status = fields.Str(required=True)
    priority = fields.Str(required=True)
    
class TaskSchema(PlainTaskSchema):
    creator_id = fields.Int(dump_only=True)
    creator = fields.Nested(PlainUserSchema(), dump_only=True)
    assigned_users = fields.List(fields.Nested(PlainUserSchema(),required=True, dump_only=True))
    assigned_user_ids = fields.List(
        fields.Int(),
        load_only=True
    ) #When creating a task, do you want to assign users at the same time?

class UserSchema(PlainUserSchema):
    created_tasks = fields.List(fields.Nested(PlainTaskSchema()), dump_only=True)
    assigned_tasks = fields.List(fields.Nested(PlainTaskSchema()), dump_only=True)
    
class UserResponseSchema(UserSchema):
    users = fields.List(fields.Nested(UserSchema()), dump_only=True)
    selectedUsers = fields.List(fields.Nested(UserSchema()), dump_only=True)
    
class UserUpdatedSchema(Schema): 
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    name = fields.Str(required=True)
    role = fields.Str(required=True)
    country= fields.Str(required=True)
    email = fields.Str(required=True)
    selectedUser = fields.Bool()
    
    
class UserUpdatedListSchema(Schema):
    user = fields.Nested(UserUpdatedSchema())
    selectedUsers = fields.List(fields.Nested(UserSchema()), dump_only=True)
    
    
        

class LoginUserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    email = fields.Str(required=True)