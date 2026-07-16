get_logs_docs = {
    "tags": ["Activity"],
    "summary": "Get activity logs",
    "description": "Retrieve activity logs with optional filtering by task, user, action, date range, and pagination. Returned data is automatically restricted based on the authenticated user's role.",
    "security": [{
        "Bearer": []
    }],
    "parameters":[{
        "name": "page",
        "in": "query",
        "type": "integer",
        "description": "Page number used for paginated results. Defaults to 1 if not provided.",
        "example": 1
    },{
        "name":"per_page",
        "in": "query",
        "type":"integer",
        "description": "number of logs per page(maximum 100)",
        "example": 20
    },{    
        "name":"from_date",
        "in":"query",
        "type":"string",
        "format":"date",
        "description":"Return logs created on or after this date.",
        "example":"2026-07-01"
    },{
        "name":"to_date",
        "in":"query",
        "type":"string",
        "format":"date",
        "description":"Return logs created on or before this date.",
        "example":"2026-07-31"
    },{
        "name":"task_id",
        "in":"query",
        "type":"integer",
        "description":"Filter logs by task ID.",
        "example":15
    },{
        "name":"user_id",
        "in":"query",
        "type":"integer",
        "description":"Filter logs by user ID.",
        "example":4
    },{
        "name": "action",
        "in": "query",
        "type": "string",
        "description": "Filter logs by activity type.",
        "example": "TASK_CREATED"
    }],
    
    "responses": {
        200: {
            "description":"Returns a paginated list of activity logs matching the supplied filters.",
            "examples": {
                "application/json":{
                    "page": 1,
                    "per_page": 20,
                    "total": 32,
                    "pages": 2,
                    "has_next": True,
                    "has_prev": False,
                    "logs": [
                        {
                            "log_id": 1,
                            "task_id": 10,
                            "user_id": 5,
                            "action": "TASK_CREATED",
                            "details": "Task 'Build API' created",
                            "created_at": "2026-07-03T15:25:41"
                        }
                    ]
                }
            }
        }
    }
}
