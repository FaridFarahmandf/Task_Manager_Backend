from db import db 

class TaskModel(db.Model): 
    __tablename__ = "tasks"
    
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    status= db.Column(db.String, nullable=False)
    priority = db.Column(db.String, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    creator = db.relationship("UserModel", back_populates='created_tasks')
    assigned_users = db.relationship("UserModel", back_populates='assigned_tasks', secondary='assigntask' )