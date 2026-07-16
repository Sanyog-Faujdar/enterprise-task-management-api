get_dashboard_docs = {
    "tags":["Dashboard"],
    "summary":"Get dashboard",
    "description": '''
                    Returns dashboard statistics based on the authenticated user's role.
                        - Admin receives system-wide statistics.
                        - Project Head receives statistics for managed tasks and team members.
                        - Member receives  statistics for their assign tasks.''',
    "security": [{
        "Bearer": []
    }],
    "responses":{
        200:{
            "description":"Returns dashboard statistics based on the authenticated user's role.",
            "examples":{
                "application/json":{
                    "Admin Dashboard":{
                        "summary":"Dashboard returned for an administrator",
                        "value":{
                            "users":{
                                "total": 7,
                                "admins": 1,
                                "project_heads": 2,
                                "members": 4
                            },
                            "tasks":{
                                "total": 6,
                                "active": 6,
                                "deleted": 0,
                                "created": 7,
                                "assigned": 1,
                                "in_progress": 0,
                                "under_review": 2,
                                "completed": 1,
                                "closed": 1,
                                "overdue": 2
                            },
                            "activity":{
                            "logs_today":100
                            }
                        }
                    },
                    "Project Head Dashboard":{
                        "summary":"Dashboard returned for a project head",
                        "value":{
                            "users":{
                                "members":4
                            },
                            "tasks":{
                                "total_tasks":5,
                                "completed": 2,
                                "in_progress":2,
                                "under_review":1,
                                "overdue":0,
                                "assigned":5
                            },
                            "activity":{
                                "logs_today":140
                            }
                        }
                    },
                    "Member Dashboard":{
                        "summary":"dashboard returned for a member",
                        "value":{
                            "tasks":{
                                "total":2,
                                "completed":0,
                                "in_progress":2,
                                "overdue":0
                            },
                            "activity":{
                                "logs_today":100
                            }
                        }
                    }
                }
            }
        },
        403: {
            "description": "Unauthorized access."
        }
    }
}
