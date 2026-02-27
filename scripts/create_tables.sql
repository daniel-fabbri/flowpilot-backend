-- FlowPilot Backend Database Schema
-- SQL Server (T-SQL) syntax
-- Run this script in SQL Server Management Studio to create the database tables

-- Create projects table
CREATE TABLE projects (
    id INT IDENTITY(1,1) PRIMARY KEY,
    scope NVARCHAR(MAX) NOT NULL,  -- JSON: {"project_title": "", "project_description": ""}
    status NVARCHAR(50) NOT NULL DEFAULT 'active',  -- e.g., "active", "archived"
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    deleted_at DATETIME2 NULL
);

-- Create todos table
CREATE TABLE todos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    project_id INT NOT NULL,
    scope NVARCHAR(MAX) NOT NULL,  -- JSON: {"project_title": "", "project_description": "", "tasks": [...]}
    status NVARCHAR(50) NOT NULL DEFAULT 'open',  -- e.g., "open", "in_progress", "done"
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    deleted_at DATETIME2 NULL,
    CONSTRAINT FK_todos_project FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- Create status_reports table
CREATE TABLE status_reports (
    id INT IDENTITY(1,1) PRIMARY KEY,
    todo_id INT NOT NULL,
    scope NVARCHAR(MAX) NOT NULL,  -- JSON: {"title": "", "description": "", "owners": [...], "createdAt": ""}
    status NVARCHAR(50) NOT NULL DEFAULT 'draft',  -- e.g., "draft", "submitted", "approved"
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    deleted_at DATETIME2 NULL,
    CONSTRAINT FK_status_reports_todo FOREIGN KEY (todo_id) REFERENCES todos(id) ON DELETE CASCADE
);

-- Create community table
CREATE TABLE community (
    id INT IDENTITY(1,1) PRIMARY KEY,
    project_id INT NOT NULL,
    team NVARCHAR(MAX) NOT NULL,  -- JSON array: [{"name": "", "email": ""}, ...]
    role NVARCHAR(100) NULL,  -- e.g., "owner", "contributor"
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    deleted_at DATETIME2 NULL,
    CONSTRAINT FK_community_project FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX IX_todos_project_id ON todos(project_id);
CREATE INDEX IX_status_reports_todo_id ON status_reports(todo_id);
CREATE INDEX IX_community_project_id ON community(project_id);
CREATE INDEX IX_projects_deleted_at ON projects(deleted_at);
CREATE INDEX IX_todos_deleted_at ON todos(deleted_at);
CREATE INDEX IX_status_reports_deleted_at ON status_reports(deleted_at);
CREATE INDEX IX_community_deleted_at ON community(deleted_at);
