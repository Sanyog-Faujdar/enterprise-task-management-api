from flask import Blueprint , request 
from werkzeug.security import  generate_password_hash,check_password_hash
from app.extensions import db
from app.models.user_models import User
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity

auth_bp = Blueprint('auth',__name__)

@auth_bp.route("/profile",methods=["GET"]) #protect route
@jwt_required()
def profile():
    user_id = int(get_jwt_identity())
    user = db.session.get(User,user_id)
    
    return {
        "user_id ":user.user_id,
        "name":user.name,
        "email":user.email
    }

@auth_bp.route('/login',methods=["POST"])
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
        "access_token": access_token},200

@auth_bp.route("/register",methods = ["POST"])
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
            "message" : "user created successfully"},201