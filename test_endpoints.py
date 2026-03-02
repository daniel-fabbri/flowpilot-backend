"""
FlowPilot API Endpoints Test
This script tests data insertion in all main endpoints
"""

import httpx
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"

def print_response(endpoint: str, response: httpx.Response):
    """Print response in formatted way"""
    print(f"\n{'='*60}")
    print(f"Endpoint: {endpoint}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)
    print(f"{'='*60}\n")


def test_health():
    """Test health check endpoint"""
    print("\n🏥 Testing Health Check...")
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/health")
        print_response("GET /health", response)
        return response.status_code == 200


def test_create_project():
    """Test project creation"""
    print("\n📁 Testing project creation...")
    
    project_data = {
        "scope": {
            "project_title": "FlowPilot Management System",
            "project_description": "Development of a complete project management system with AI integration"
        },
        "status": "active"
    }
    
    with httpx.Client() as client:
        response = client.post(
            f"{BASE_URL}/api/v1/projects",
            json=project_data
        )
        print_response("POST /api/v1/projects", response)
        
        if response.status_code == 201:
            return response.json()
        return None


def test_create_todo(project_id: int):
    """Test todo creation"""
    print(f"\n✅ Testing todo creation for project {project_id}...")
    
    todo_data = {
        "project_id": project_id,
        "scope": {
            "project_title": "FlowPilot Management System",
            "project_description": "Development of a complete project management system",
            "tasks": [
                {
                    "id": 1,
                    "title": "Setup development environment",
                    "description": "Install dependencies and configure database",
                    "status": "done",
                    "priority": "high"
                },
                {
                    "id": 2,
                    "title": "Implement authentication",
                    "description": "Add login and authorization system",
                    "status": "in_progress",
                    "priority": "high"
                },
                {
                    "id": 3,
                    "title": "Create dashboard",
                    "description": "Develop data visualization interface",
                    "status": "open",
                    "priority": "medium"
                }
            ]
        },
        "status": "in_progress"
    }
    
    with httpx.Client() as client:
        response = client.post(
            f"{BASE_URL}/api/v1/todos",
            json=todo_data
        )
        print_response("POST /api/v1/todos", response)
        
        if response.status_code == 201:
            return response.json()
        return None


def test_create_status_report(todo_id: int):
    """Test status report creation"""
    print(f"\n📊 Testing status report creation for todo {todo_id}...")
    
    status_report_data = {
        "todo_id": todo_id,
        "scope": {
            "title": "Weekly Report - Sprint 1",
            "description": "Progress on environment setup and implementation start",
            "owners": [
                {
                    "name": "Daniel Fabbri",
                    "email": "daniel.fabbri@example.com"
                },
                {
                    "name": "John Smith",
                    "email": "john.smith@example.com"
                }
            ],
            "createdAt": datetime.now().isoformat(),
            "highlights": [
                "Development environment successfully configured",
                "Database created and tested",
                "REST API working correctly"
            ],
            "blockers": [
                "Waiting for Foundry AI credentials"
            ]
        },
        "status": "submitted"
    }
    
    with httpx.Client() as client:
        response = client.post(
            f"{BASE_URL}/api/v1/status-reports",
            json=status_report_data
        )
        print_response("POST /api/v1/status-reports", response)
        
        if response.status_code == 201:
            return response.json()
        return None


def test_create_community(project_id: int):
    """Test community member creation"""
    print(f"\n👥 Testing community creation for project {project_id}...")
    
    community_data = {
        "project_id": project_id,
        "team": [
            {
                "name": "Daniel Fabbri",
                "email": "daniel.fabbri@example.com",
                "role": "Lead Developer",
                "responsibilities": "Backend development, Database design, API implementation"
            },
            {
                "name": "John Smith",
                "email": "john.smith@example.com",
                "role": "Frontend Developer",
                "responsibilities": "UI/UX, React development"
            }
        ],
        "role": "Development Team"
    }
    
    with httpx.Client() as client:
        response = client.post(
            f"{BASE_URL}/api/v1/community",
            json=community_data
        )
        print_response("POST /api/v1/community", response)
        
        if response.status_code == 201:
            return response.json()
        return None


def test_list_all():
    """Test listing all resources"""
    print("\n📋 Testing resource listing...")
    
    with httpx.Client() as client:
        # List projects
        response = client.get(f"{BASE_URL}/api/v1/projects")
        print_response("GET /api/v1/projects", response)
        
        # List todos
        response = client.get(f"{BASE_URL}/api/v1/todos")
        print_response("GET /api/v1/todos", response)
        
        # List status reports
        response = client.get(f"{BASE_URL}/api/v1/status-reports")
        print_response("GET /api/v1/status-reports", response)
        
        # List community
        response = client.get(f"{BASE_URL}/api/v1/community")
        print_response("GET /api/v1/community", response)


def main():
    """Execute all tests"""
    print("🚀 Starting FlowPilot API tests")
    print(f"Base URL: {BASE_URL}")
    
    try:
        # 1. Health Check
        if not test_health():
            print("❌ API is not responding. Check if server is running.")
            return
        
        # 2. Create Project
        project = test_create_project()
        if not project:
            print("❌ Failed to create project")
            return
        
        project_id = project.get("id")
        print(f"✅ Project created successfully! ID: {project_id}")
        
        # 3. Create Todo
        todo = test_create_todo(project_id)
        if not todo:
            print("❌ Failed to create todo")
            return
        
        todo_id = todo.get("id")
        print(f"✅ Todo created successfully! ID: {todo_id}")
        
        # 4. Create Status Report
        status_report = test_create_status_report(todo_id)
        if status_report:
            print(f"✅ Status Report created successfully! ID: {status_report.get('id')}")
        
        # 5. Create Community
        community = test_create_community(project_id)
        if community:
            print(f"✅ Community created successfully! ID: {community.get('id')}")
        
        # 6. List all resources
        test_list_all()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60)
        
    except httpx.ConnectError:
        print("\n❌ ERROR: Could not connect to API.")
        print("Make sure the server is running at http://localhost:8000")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
