from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort

from db import db

from models.task import TaskModel
from models.user import UserModel
from schemas.schemas import TaskSchema


blp = Blueprint("tasks", __name__, "Operations on tasks")

@blp.route("/task/<int:user_id>")
class CreatingTask(MethodView):
    @blp.arguments(TaskSchema)
    @blp.response(201, TaskSchema)
    @jwt_required()
    def post(self, task_data, user_id): 
        enteredTitle = task_data["title"]
        enteredDescription = task_data["description"]
        enteredStatus = task_data["status"]
        enteredPriority = task_data["priority"]
        
        newTask = TaskModel(
            title = enteredTitle,
            description = enteredDescription,
            status = enteredStatus,
            priority = enteredPriority,
            creator_id = user_id,
        )
        assigned_user_ids = task_data.get("assigned_user_ids", [])
        
        if assigned_user_ids:
            assigned_users = UserModel.query.filter(
                UserModel.id.in_(assigned_user_ids)
            ).all()

            newTask.assigned_users = assigned_users
            
        try: 
            db.session.add(newTask)
            db.session.commit()
            
            return newTask
        except:
            abort(400, message="cannot create a new task.")
            
            
@blp.route("/task")
class AllTask(MethodView): 
    @blp.response(200, TaskSchema(many=True))
    @jwt_required()
    def get(self):
        return TaskModel.query.all()
    
    

@blp.route("/task/<string:task_id>")
class Task(MethodView):
    @blp.response(200,TaskSchema)
    @jwt_required()
    def get(self, task_id):
        task =  TaskModel.query.get_or_404(task_id)
        return task