create_task_docs = {
    "tags":["Task Management"],
    "summary":"create task",
    "description":"create a new task. only users with the Admin role can create tasks .",
    "security": [{
        "Bearer": []
    }],
    "parameters":[{
        "name":"body",
        "in":"body",
        "required": True,
        
        "schema":{
            "type":"object",
            
            "properties":{
                "title":{
                    "type":"string",
                    "description":"short title of the task.",
                    "example":"create a Enterprise Model"
                },
                "description":{
                    "type":"string",
                    "description":"for more details related to work ,it's optional.",
                    "example":"An Enterprise Model for CRUD operations"
                },
                "deadline":{
                    "type":"string",
                    "format":"date",
                    "description":"Deadline in YYYY-MM-DD format.",
                    "example":"2026-09-12"
                }
            },
            
            "required":["title","deadline"]
        }
    }],
    
    "responses":{
        201:{
            "description":"task created successfully",
            
            "examples":{
                "application/json":{
                    "message":"task created",
                    "task_id":1,
                    "title":"Enterprise model",
                    "description":"An Enterprise Model for CRUD operations",
                    "created_at":"2026-07-12T10:30:15",
                    "deadline":"2026-09-12",
                    "status":"task created",
                    "project_head_id":2
                }
            }
        },
        
        400:{
            "description":"Invalid Input"
        },
        
        403:{
            "description":"only Admin can create tasks."
        }
    }
}

assign_head_docs = {
    "tags": ["Task Management"],
    "summary": "Assigning project head",
    "description": "Assign a project head to an existing task. Only admin can perform this operation.",
    "security": [{
        "Bearer": []
    }],
    "parameters":[{
        "name": "task_id",
        "in": "path",
        "type": "integer",
        "required": True,
        "description": "task id on which head to be assigned.",
        "example": 15},
    {
        "name": "body",
        "in": "body",
        "required": True,     
        
        "schema": {
            "type": "object",
            
            "properties": {
                "project_head_id": {
                    "type": "integer",
                    "example": 10
                }
            },
            
            "required": ["project_head_id"]
        }
    }],
    
    "responses": {
        201: {
            "description": "head assigned successfull.",
            
            "exapmles": {
                "application/json":{
                    "message":"project head assigned successfull",
                    "assigned_by":1,
                    "assigned_to":10,
                    "task":15
                }
            }
        },
        
        400: {
            "description": "Invalid input or selected user is not a project head."
        },
        
        403: {
            "description": "only admin can assign head"
        },
        
        404: {
            "description": "task or project head not found"
        },
        
        409: {
            "description": "preassigned to same head"
        }
    }
}

assign_member_docs = {
    "tags": ["Task Management"],
    "summary": "Assign member",
    "description": "Assign a member to an existing task. Only admin and the assigned project head can perform this operation.",
    "security": [{
        "Bearer": []
    }],
    "parameters": [{
            "name": "task_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "Task id on which member needed to be assigned .",
            "example": 15
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            
            "schema":{
                "type": "object",
                
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "user id of the member to assign.",
                        "example":4
                    }
                },
                
                "required": ["user_id"]
            }
    }],
    
    "responses": {
        201: {
            "description":"Task assigned to member successfully.",
            "examples": {
               "application/json": {
                   "message": "task assigned successfully",
                   "assigned_by": 1,
                   "assigned_to": 4,
                   "task": 15
               } 
            }
        },
        
        400: {
            "description": "invalid input, project head not assigned , or selected user is not a member."
        },
        403: {
            "description": "only assigned project head or admin can assign member for related task."
        },
        404: {
            "description": "user not found or task does not exist."
        },
        409: {
            "description": "user already assigned"
        }
    }
}

get_tasks_docs = {
    "tags": ["Task Management"],
    "summary": "Get tasks",
    "description": "Returns tasks visible to the authenticated user based on their role. Administrators see all tasks, project heads see tasks assigned to them, and members see their assigned tasks.",
    "security": [{
        "Bearer": []
    }],
    "responses":{
        200: {
            "description": "Tasks data recive successfull",
            "examples": {
                "application/json": {
                    "task_id":1,
                    "created_by":2,
                    "title": "Swagger documentation",
                    "status": "completed",
                    "deadline": "2026-7-09",
                    "project_head_id": 3
                }
            }
        }
    }
}

get_task_docs = {
    "tags": ["Task Management"],
    "summary": "get task by id",
    "description": "Returns detailed information about a specific task if the authenticated user has permission to view it.",
    "security": [{
        "Bearer": []
    }],
    "parameters": [{
        "name": "task_id",
        "in": "path",
        "type": "integer",
        "required": True, 
        "descriprition": "Unique id of the  task.",
        "example": 15       
    }],
    "responses": {
        200: {
            "description": "Task data recive successfull",
            "examples": {
                "application/json": {
                    "task_id": 1,
                    "title": "swagger documentation",
                    "description": "well mannered design documentation of REST API.",
                    "status": "created",
                    "created_by": 2,
                    "project_head_id": 3,
                    "created_at": "2026-03-03T10:15:30",
                    "deadline": "2023-07-05"
                }
            }
        },
        403: {
            "description": "user does not have permission to view this task."
        },
        404: {
            "description": "Task not found"
        }
    }
}

task_modification_docs = {
    "tags": ["Task Management"],
    "summary": "Update task",
    "description": """  Updates an existing task.
                        Permissions:
                        - Admin: title, description and deadline
                        - Project Head: status, description and deadline
                        - Member: status only. """,
    "security": [{
        "Bearer": []
    }],
    "parameters": [{
        "name": "task_id",
        "in": "path",
        "type": "integer",
        "required": True,
        "description": "Unique id of the task.",
        "example": 15
    },
    {
        "name": "body",
        "in": "body",
        "required": True,
        "schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
            "description": {"type": "string"},
            "deadline": {
                "type": "string",
                "format": "date"
            },
            "status": {
                "type": "string",
                "enum": [
                    "TASK_CREATED",
                    "ASSIGNED",
                    "IN_PROGRESS",
                    "COMPLETED"
                ]
            }
            }
        }     
    }],
    "responses":{
        200:{
            "description": "updated successfully",
            "examples":{
                "application/json":{
                    "task_id":15,
                    "title":"create a Enterprise Model",
                    "description":"An Enterprise Model for CRUD operations",
                    "status":"TASK CREATED",
                    "deadline":"2026-09-12",
                    "updated_by":5,
                    "created_by":6
                }
            }
        },
        400:{
            "description":"invalid input or unsupproted task status."
        },
        403:{
            "description":"User does not have permission to update this task.",
        },
        404:{
            "description":"task not found"
        }
    }
}

delete_task_docs = {
    "tags":["Task Management"],
    "summary":"Delete task",
    "description":"Moves a task to the recycle bin using soft delete. Only administrators can perform this operation.",
    "security": [{
        "Bearer": []
    }],
    "parameters":[{
        "name":"task_id",
        "in":"path",
        "type":"integer",
        "required":True,
        "description":"Unique id of the task.",
        "example":15
    }],
    "responses":{
        200:{
            "description":"Task successfully moved to the recycle bin.",
            "examples":{
                "application/json":{
                    "message":"Task moved to recycle bin.",
                    "task_id":15
                }
            }
        },
        403:{
            "description":"User does not have permission to delete the task."
        },
        404:{
            "description":"Task not found."
        },
        409:{
            "description":"Task aurleady deleted."
        }
    }
}

restore_task_docs = {
    "tags":["Task Management"],
    "summary":"Restore task",
    "description":"Restores a soft-deleted task from the recycle bin. Only administrators can perform this operation.",
    "security": [{
        "Bearer": []
    }],
    "parameters":[{
        "name": "task_id",
        "in": "path",
        "type": "integer",
        "required": True,
        "description": "Unique id of the task.",
        "example": 15
    }],
    "responses":{
        200:{
            "description":"Restore successfull from recycle bin.",
            "examples":{
                "application/json":{
                    "message":"task restored from recycle bin",
                    "task_id":15
                }
            }
        },
         403:{
            "description":"User does not have permission to restore the task."
        },
        404:{
            "description":"Task not found."
        },
        409:{
            "description":"Task is aurleady active."
        }
    }
}
