import os

from flask_cors import CORS
import models

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST

from db import db

from resources.user import blp as UserBlueprint
from resources.task import blp as TaskBluePrint


def create_app(data_url=None): #data_url=None lets you pass a different database URL for testing
    app = Flask(__name__)
    
    CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})
    app.config["PROPAGATE_EXCEPTIONS"] = True #Allow Flask to show detailed errors/exceptions.
    app.config["API_TITLE"] = "Stores REST API" #This sets the title of your Swagger/OpenAPI documentation
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    
    app.config["SQLALCHEMY_DATABASE_URI"] = data_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app) #connect SQLAlchemy to Flask.
    api = Api(app) #enable Flask-Smorest routes and Swagger
    
    app.config["JWT_SECRET_KEY"] = "14350677282592166677008582084652283861"
    jwt = JWTManager(app)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header,jwt_payload):
        return jwt_payload['jti'] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header,jwt_payload):
        return(
            jsonify(
                {"description": "token has been revoked", "error":"token_revoked"}
            )
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "the token is not fresh",
                    "error": "fresh_token_required"
                }
            ), 401
        )
    
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if(identity == 1):
            return {"isAdmin": True}
        return {"isAdmin": False}
    
    @jwt.expired_token_loader
    def expired_toker_callback(jwt_header, jwt_payload):
        return(
            jsonify(
                {"message": "the token is expired", "error":"token_expired"}
            ), 
            401
        )
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed", "error":"invalid_token"}
            ),
            401
        )
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {"desciption": "request does not contain an access token", "error":"authorization_required"}
            ),
            401
        )

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(TaskBluePrint)
    
    with app.app_context():
        db.create_all()
        
    return app
