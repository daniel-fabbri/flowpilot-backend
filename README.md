# FlowPilot Backend

A complete Python backend API for project management using FastAPI, integrated with Microsoft SQL Server and Foundry AI Agent.

## Features

- **Full CRUD API** for:
  - Projects
  - Todos
  - Status Reports
  - Community/Team Management
- **Microsoft SQL Server** integration with SQLAlchemy
- **Foundry AI Agent** integration for intelligent chat functionality
- **Soft delete** support for all resources
- **RESTful API** design with proper HTTP status codes
- **Auto-generated API documentation** via FastAPI

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **pyodbc** - ODBC driver for SQL Server
- **Pydantic** - Data validation using Python type annotations
- **httpx** - Async HTTP client for Foundry integration
- **Uvicorn** - ASGI server

## Prerequisites

- Python 3.8+
- Microsoft SQL Server (with ODBC Driver 17 for SQL Server)
- SQL Server Management Studio (SSMS) or equivalent
- Foundry instance with API access

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/daniel-fabbri/flowpilot-backend.git
   cd flowpilot-backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install ODBC Driver 17 for SQL Server** (if not already installed)
   - **Ubuntu/Debian:**
     ```bash
     curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
     curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list
     apt-get update
     ACCEPT_EULA=Y apt-get install -y msodbcsql17
     ```
   - **Windows:** Download from [Microsoft](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
   - **macOS:**
     ```bash
     brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
     brew update
     HOMEBREW_NO_ENV_FILTERING=1 ACCEPT_EULA=Y brew install msodbcsql17
     ```

## Configuration

1. **Copy the example environment file**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file with your settings**
   ```env
   # SQL Server Configuration
   SQLSERVER_USER=your_username
   SQLSERVER_PASSWORD=your_password
   SQLSERVER_SERVER=localhost
   SQLSERVER_PORT=1433
   SQLSERVER_DB=flowpilot_db

   # Foundry Configuration
   FOUNDRY_BASE_URL=https://your-foundry-instance.com
   FOUNDRY_API_KEY=your_foundry_api_key
   FOUNDRY_AGENT_ID=your_agent_id

   # Application Settings
   APP_NAME=FlowPilot Backend
   APP_VERSION=1.0.0
   DEBUG=False
   ```

3. **Create database tables**
   - Open SQL Server Management Studio (SSMS)
   - Connect to your SQL Server instance
   - Create a new database named `flowpilot_db` (or your chosen name)
   - Open and execute the script `scripts/create_tables.sql`

## Running the Application

1. **Start the API server**
   ```bash
   uvicorn app.main:app --reload
   ```

   The server will start at `http://localhost:8000`

2. **Access the interactive API documentation**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

3. **Check health status**
   ```bash
   curl http://localhost:8000/health
   ```

## API Endpoints

### Projects
- `POST /api/v1/projects` - Create a new project
- `GET /api/v1/projects` - List all projects
- `GET /api/v1/projects/{id}` - Get a specific project
- `PUT /api/v1/projects/{id}` - Update a project
- `DELETE /api/v1/projects/{id}` - Soft delete a project

### Todos
- `POST /api/v1/todos` - Create a new todo
- `GET /api/v1/todos` - List all todos
- `GET /api/v1/todos/{id}` - Get a specific todo
- `GET /api/v1/todos/projects/{project_id}/todos` - Get todos for a project
- `PUT /api/v1/todos/{id}` - Update a todo
- `DELETE /api/v1/todos/{id}` - Soft delete a todo

### Status Reports
- `POST /api/v1/status-reports` - Create a new status report
- `GET /api/v1/status-reports` - List all status reports
- `GET /api/v1/status-reports/{id}` - Get a specific status report
- `GET /api/v1/status-reports/todos/{todo_id}/status-reports` - Get status reports for a todo
- `PUT /api/v1/status-reports/{id}` - Update a status report
- `DELETE /api/v1/status-reports/{id}` - Soft delete a status report

### Community
- `POST /api/v1/community` - Create a new community entry
- `GET /api/v1/community` - List all community entries
- `GET /api/v1/community/projects/{project_id}/community` - Get community for a project
- `PUT /api/v1/community/{id}` - Update a community entry
- `DELETE /api/v1/community/{id}` - Soft delete a community entry

### Foundry AI Agent
- `POST /api/v1/foundry/chat` - Chat with Foundry AI Agent
  ```json
  {
    "message": "Your message here",
    "context": {
      "optional": "context data"
    }
  }
  ```

## Project Structure

```
flowpilot-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app with routes
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Environment configuration
│   │   └── database.py        # SQLAlchemy setup
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py          # SQLAlchemy models
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── project.py         # Pydantic schemas for projects
│   │   ├── todo.py            # Pydantic schemas for todos
│   │   ├── status_report.py   # Pydantic schemas for status reports
│   │   └── community.py       # Pydantic schemas for community
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── projects.py    # Project endpoints
│   │       ├── todos.py       # Todo endpoints
│   │       ├── status_reports.py  # Status report endpoints
│   │       ├── community.py   # Community endpoints
│   │       └── foundry_chat.py    # Foundry chat endpoint
│   └── services/
│       ├── __init__.py
│       └── foundry_chat_service.py  # Foundry integration service
├── integrations/
│   ├── __init__.py
│   └── foundry_config.py      # Foundry connection settings
├── scripts/
│   └── create_tables.sql      # SQL Server table creation script
├── .env.example               # Example environment variables
├── .gitignore
├── requirements.txt           # Python dependencies
└── README.md

```

## Database Schema

### Tables

1. **projects**
   - `id` (INT IDENTITY PK)
   - `scope` (NVARCHAR(MAX) - JSON)
   - `status` (NVARCHAR(50))
   - `created_at`, `updated_at`, `deleted_at` (DATETIME2)

2. **todos**
   - `id` (INT IDENTITY PK)
   - `project_id` (INT FK → projects)
   - `scope` (NVARCHAR(MAX) - JSON)
   - `status` (NVARCHAR(50))
   - `created_at`, `updated_at`, `deleted_at` (DATETIME2)

3. **status_reports**
   - `id` (INT IDENTITY PK)
   - `todo_id` (INT FK → todos)
   - `scope` (NVARCHAR(MAX) - JSON)
   - `status` (NVARCHAR(50))
   - `created_at`, `updated_at`, `deleted_at` (DATETIME2)

4. **community**
   - `id` (INT IDENTITY PK)
   - `project_id` (INT FK → projects)
   - `team` (NVARCHAR(MAX) - JSON array)
   - `role` (NVARCHAR(100))
   - `created_at`, `updated_at`, `deleted_at` (DATETIME2)

All foreign keys use `ON DELETE CASCADE` to maintain referential integrity.

## Development

### Running with auto-reload (development mode)
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Running in production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## License

This project is licensed under the terms specified in the LICENSE file.

## Support

For issues and questions, please open an issue on GitHub.
