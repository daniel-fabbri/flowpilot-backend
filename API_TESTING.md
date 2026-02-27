# API Testing Guide

This document provides example API calls for testing the FlowPilot Backend.

## Prerequisites

1. Ensure the API is running:
   ```bash
   uvicorn app.main:app --reload
   ```

2. The API will be available at `http://localhost:8000`

3. Interactive documentation is available at:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## Example API Calls

### Health Check

```bash
curl http://localhost:8000/health
```

### Projects

**Create a project:**
```bash
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -d '{
    "scope": {
      "project_title": "My First Project",
      "project_description": "This is a test project"
    },
    "status": "active"
  }'
```

**List all projects:**
```bash
curl http://localhost:8000/api/v1/projects
```

**Get a specific project:**
```bash
curl http://localhost:8000/api/v1/projects/1
```

**Update a project:**
```bash
curl -X PUT http://localhost:8000/api/v1/projects/1 \
  -H "Content-Type: application/json" \
  -d '{
    "scope": {
      "project_title": "Updated Project Title",
      "project_description": "Updated description"
    },
    "status": "active"
  }'
```

**Delete a project (soft delete):**
```bash
curl -X DELETE http://localhost:8000/api/v1/projects/1
```

### Todos

**Create a todo:**
```bash
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "scope": {
      "project_title": "My Todo",
      "project_description": "Description",
      "tasks": [
        {
          "title": "Task 1",
          "description": "First task",
          "owner": "user@example.com",
          "duedate": "2024-12-31",
          "createdAt": "2024-01-01"
        }
      ]
    },
    "status": "open"
  }'
```

**List all todos:**
```bash
curl http://localhost:8000/api/v1/todos
```

**Get todos for a specific project:**
```bash
curl http://localhost:8000/api/v1/projects/1/todos
```

**Get a specific todo:**
```bash
curl http://localhost:8000/api/v1/todos/1
```

**Update a todo:**
```bash
curl -X PUT http://localhost:8000/api/v1/todos/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress"
  }'
```

**Delete a todo:**
```bash
curl -X DELETE http://localhost:8000/api/v1/todos/1
```

### Status Reports

**Create a status report:**
```bash
curl -X POST http://localhost:8000/api/v1/status-reports \
  -H "Content-Type: application/json" \
  -d '{
    "todo_id": 1,
    "scope": {
      "title": "Weekly Status Report",
      "description": "Progress update for this week",
      "owners": ["user1@example.com", "user2@example.com"],
      "createdAt": "2024-01-15"
    },
    "status": "draft"
  }'
```

**List all status reports:**
```bash
curl http://localhost:8000/api/v1/status-reports
```

**Get status reports for a specific todo:**
```bash
curl http://localhost:8000/api/v1/todos/1/status-reports
```

**Get a specific status report:**
```bash
curl http://localhost:8000/api/v1/status-reports/1
```

**Update a status report:**
```bash
curl -X PUT http://localhost:8000/api/v1/status-reports/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "submitted"
  }'
```

**Delete a status report:**
```bash
curl -X DELETE http://localhost:8000/api/v1/status-reports/1
```

### Community

**Create a community entry:**
```bash
curl -X POST http://localhost:8000/api/v1/community \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "team": [
      {
        "name": "John Doe",
        "email": "john@example.com"
      },
      {
        "name": "Jane Smith",
        "email": "jane@example.com"
      }
    ],
    "role": "owner"
  }'
```

**List all community entries:**
```bash
curl http://localhost:8000/api/v1/community
```

**Get a specific community entry:**
```bash
curl http://localhost:8000/api/v1/community/1
```

**Get community for a specific project:**
```bash
curl http://localhost:8000/api/v1/projects/1/community
```

**Update a community entry:**
```bash
curl -X PUT http://localhost:8000/api/v1/community/1 \
  -H "Content-Type: application/json" \
  -d '{
    "role": "contributor"
  }'
```

**Delete a community entry:**
```bash
curl -X DELETE http://localhost:8000/api/v1/community/1
```

### Foundry Chat

**Send a message to Foundry Agent:**
```bash
curl -X POST http://localhost:8000/api/v1/foundry/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, can you help me with my project?",
    "context": {
      "project_id": 1,
      "user": "john@example.com"
    }
  }'
```

## Using Python Requests

If you prefer using Python to test the API:

```python
import requests

base_url = "http://localhost:8000"

# Create a project
response = requests.post(
    f"{base_url}/api/v1/projects",
    json={
        "scope": {
            "project_title": "My Project",
            "project_description": "Project description"
        },
        "status": "active"
    }
)
print(f"Created project: {response.json()}")

# Get all projects
response = requests.get(f"{base_url}/api/v1/projects")
print(f"All projects: {response.json()}")

# Chat with Foundry
response = requests.post(
    f"{base_url}/api/v1/foundry/chat",
    json={
        "message": "Hello!",
        "context": {"user": "test"}
    }
)
print(f"Foundry response: {response.json()}")
```

## Notes

- All dates should be in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
- JSON fields (scope, team) are flexible and can contain any valid JSON structure
- All delete operations are soft deletes - records are marked as deleted but not removed from the database
- Use the `/docs` endpoint for interactive testing with Swagger UI
