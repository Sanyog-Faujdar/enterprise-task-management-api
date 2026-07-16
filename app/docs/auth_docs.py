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

