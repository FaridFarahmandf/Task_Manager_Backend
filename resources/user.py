from operator import or_


from flask.views import MethodView
from flask_smorest import Blueprint,abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, get_jwt_identity, jwt_required

from blocklist import BLOCKLIST
from db import db

from models.user import UserModel
from schemas.schemas import UserSchema
from schemas.schemas import LoginUserSchema

blp = Blueprint("users", __name__, description="Operations on users")

@blp.route("/login")
class LoginUser(MethodView):
    @blp.arguments(LoginUserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first();
        
        if user and pbkdf2_sha256.verify(user_data["password"], user.password): 
            access_token = create_access_token(identity=str(user.id), fresh=True)
            refresh_token = create_refresh_token(identity=str(user.id))
            return {"access_token":access_token, "refresh_token":refresh_token}
        
        abort(401,message="Invalid Credential")
        
        
    
@blp.route("/register")
class RegisterUser(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201,UserSchema)
    def post(self,user_data):
        
        current_user = UserModel.query.filter(
            or_(
                UserModel.username == user_data["username"], 
                UserModel.email == user_data["email"])
            ).first()
        
        if current_user:
            abort(409, message="User already existed")
        
        new_user = UserModel(
            username=user_data["username"],
            name = user_data["name"],
            country = user_data["country"],
            role = user_data["role"],
            email = user_data["email"],
            password = pbkdf2_sha256.hash(user_data["password"]),
        )
        
        try: 
            db.session.add(new_user)
            db.session.commit()
        except:
            abort(400, message="Cannot register a user")
        
        return new_user

    @blp.route("/refresh")
    class UserRefreshToken(MethodView):
        @jwt_required(refresh=True)
        def post(self):
            current_user = get_jwt_identity()
            new_token = create_access_token(identity=current_user, fresh=False)
            jti = get_jwt()["jti"]
            BLOCKLIST.add(jti)
            return {"access_token": new_token}
    
    @blp.route("/logout")
    class LogoutUser(MethodView):
        @jwt_required()
        def post(self):
            jti = get_jwt()["jti"]
            BLOCKLIST.add(jti)
            return {"message": "User successfully log out."}
    
        
    @blp.route("/user/<string:user_id>")
    class UserInfo(MethodView):
        @blp.response(200, UserSchema)
        def get(self, user_id):
            user = UserModel.query.get_or_404(user_id)
            return user
        
        def delete(self, user_id):
            user = UserModel.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()
            
            return {"message":"user deleted successfully"}

    @blp.route("/users")
    class Users(MethodView):
        @blp.response(200, UserSchema(many=True))
        def get(self):
            print("helloo")
            users = UserModel.query.all()
            return users