from db import db 

class UserModel(db.Model):
    __tablename__="users"
    
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    selectedUser = db.Column(db.Boolean, nullable=False)
    created_tasks = db.relationship("TaskModel", back_populates='creator')
    assigned_tasks = db.relationship("TaskModel", back_populates='assigned_users', secondary='assigntask')
    