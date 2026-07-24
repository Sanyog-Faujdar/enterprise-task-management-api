register_docs = {
    "tags": ["Authentication"],
    "summary": "register a new user",
    "description": "creates a new user account in the system .",
    
    "parameters": [{
        "name": "body",
        "in": "body",
        "required": True,
        
        "schema": {
            "type": "object",
            
            "properties": {
                "name": {
                    "type": "string",
                    "exapmle": "rahul"
                },
                
                "email": {
                    "type": "string",
                    "example": "rahul@gmail.com"
                },
                
                "password": {
                    "type": "string",
                    "exapmle": "passwoed122"
                }
            },
            
            "required": ["name","email","password"]
        }
    }],
    
    "responses": {
        201:{
            "description": "user registered successfully",
            "examples": {
                "application/json":{
                    "message": "user registerd successfully",
                    "user_id": 1,
                    "name": "raahul",
                    "email": "rahul@gmail.com"
                }
            }
        },
        
        400: {
        "description": "Invalid input"  
        },
        
        409: {
            "description": "Email already exists"
        }
    }
}

login_docs = {
    "tags": ["Authentication"],
    "summary": "Login user",
    "description": "Authenticate a registered user using either a username or an email address  and return a jwt access token .",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            
            "schema": {
                "type": "object",
                
                "properties": {
                    "login_credential": {
                        "type": "string",
                        "description": "enter either your username or email address",
                        "example": "rahul@example.com"
                    },
                    
                    "password": {
                        "type": "string",
                        "description": "user password",
                        "example": "password1234"
                    }
                },
                
                "required": ["login_credential","password"]
            }
        }
    ],
    
    "responses": {
        200: {
            "description": "Login sucessfull",
            "examples": {
                "application/json": {
                    "message": "login successfull",
                    "user_id": 1,
                    "name": "rahul",
                    "role": "member",
                    "access_token": "eyjhbgc..."
                }
            }
        },
        
        400: {
            "description": "invalid input"
        },
        
        401: {
          "description": "invalid email or password"  
        }
    }
}

profile_docs ={
    "tags":["Authentication"],
    "summary":"User profile",
    "description":"Authorized user can see and access the needed information related to it.",
    "security": [{
        "Bearer": []
    }],
    "responses":{
        200:{
            "description":"Authorized user information.",
            "examples":{
                "application/json":{
                    "user_id ":1,
                    "name":"owner",
                    "email":"singh@example.com",
                    "role":"owner"
                }
            }
        }
    }
}

users_docs = {
    "tags":["Authentication"],
    "summary":"Get users",
    "description":"If Authorized user is owner her/him can see the persons user id under his/her influence.",
    "security":[{
        "Bearer":[]
    }],
    "responses":{
        200:{
            "description":"User under his/her influence.",
            "examples":{
                "application/json":{
                
                    "user_id":2,
                    "name":"sanyog",
                    "email":"ss@example.com",
                    "role":"member"
                
                }
            }
        }
    }
}

assign_role_docs = {
    "tags":["Authentication"],
    "summary":"Changing job role.",
    "description":"Owner may change the role of it's influnced users.",
    "security":[{
        "Bearer":[]
    }],
    "parameters":[{
        "name":"user_id",
        "in":"path",
        "type":"integer",
        "required":True,
        "description":"user_id whose job role is owner want to change.",
        "example":5
    },{
        "name":"body",
        "in":"body",
        "required":True,
        "schema":{
            "type":"object",
            "properties":{
                "role":{
                    "type":"string",
                    "description":"job role owner want to see the specific user.",
                    "example":"member"
                }
            }
        }
    }],
    "responses":{
        200:{
            "description":"job role changed successfully",
            "examples":{
                "application/json":{
                    "user_id":5,
                    "email":"sin@example.com",
                    "name":"sanyog",
                    "role":"member"
                }
            }
        },
        400:{
            "description":"can not change own role or invalid role or input or already assigned."
        },
        403:{
            "description":"forbidden"
        },
        404:{
            "description":"user not found"
        }
    }
}