from flask import Blueprint , request 
from werkzeug.security import  generate_password_hash,check_password_hash
from app.extensions import db
from app.models.user_models import User
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from flasgger import swag_from
from app.docs.auth_docs import register_docs, login_docs

auth_bp = Blueprint('auth',__name__)

@auth_bp.route("/profile",methods=["GET"]) #protect route
@jwt_required()
def profile():
    user_id = int(get_jwt_identity())
    user = db.session.get(User,user_id)
    
    return {
        "user_id ":user.user_id,
        "name":user.name,
        "email":user.email,
        "role":user.role
    }

@auth_bp.route('/login',methods=["POST"])
@swag_from(login_docs)
def login():
    data = request.get_json()
    if not data :
        return{"message":"invalid input"},400
    
    login_credential = data.get("login_credential")
    password = data.get("password")
    if not login_credential or not password :
        return {"message":"invalid input"},400
    
    user = User.query.filter((User.name == login_credential) | (User.email == login_credential)).first() 
    if not user:
        return {"message":"wrong login credentials"},401
    
    if not check_password_hash(user.password,password):
        return {"message":"wrong login credentials"},401
    
    access_token = create_access_token(identity=str(user.user_id))#genrate jwt
    return {
        "message":"login successful",
        "user_id": user.user_id,
        "name" : user.name,
        "role":user.role,
        "access_token": access_token},200

@auth_bp.route("/register",methods = ["POST"])
@swag_from(register_docs)
def register():
    data = request.get_json()
    name = data.get("name")
    if not name :
        return {"message" : "name is required"}, 400 
    email = data.get("email")
    if not email or "@" not in email :
        return {"message" : "email required"}, 400 
    if User.query.filter_by(email=email).first() :
        return {"mesage" :"email already exists"},409 
    password = data.get("password")
    if not password or len(password) < 8:
        return {"message": "password length atleast 8"},400
        # or use flash message 
    password = generate_password_hash(password)
    
    user = User(name = name,email = email,password = password)
    db.session.add(user)
    db.session.commit()
    
    return {"user_id" : user.user_id,
            "name" : user.name ,
            "email" : user.email , 
            "role" : User.ROLE_MEMBER,
            "message" : "user created successfully"},201

@auth_bp.route("/users",methods=["GET"])
@jwt_required()
def users():
    current_user_id = int(get_jwt_identity())
    current_user = db.session.get(User,current_user_id)
    if User.ROLE_OWNER !=  current_user.role:
        return {"message":"forbidden"},403
    
    users = User.query.all()
    
    return [{"user_id":user.user_id,
             "name":user.name,
             "email":user.email,
             "role":user.role}for user in users],200

@auth_bp.route("/users/<int:user_id>/role",methods=["POST"])
@jwt_required()
def assign_role(user_id):
    current_user_id = int(get_jwt_identity())
    current_user = db.session.get(User,current_user_id)
    if current_user.role != User.ROLE_OWNER:
        return {"message":"forbidden"},403
    
    target_user = db.session.get(User,user_id)
    if not target_user:
        return {"message":"user not found"},404
    
    if current_user.user_id == target_user.user_id:
        return {"message":"can not change own role"},400
    
    data = request.get_json()
    if not data :
        return {"message":"invalid input"},400
    
    role = data.get('role')
    if role not in [ User.ROLE_MEMBER , User.ROLE_PROJECT_HEAD]:
        return {"message":"invalid role"},400
    
    if role == target_user.role:
        return {"message":"already assign"},400
    
    target_user.role = role
    db.session.commit()
    return {"user_id":target_user.user_id,
            "email":target_user.email,
            "name":target_user.name,
            "role":target_user.role},200