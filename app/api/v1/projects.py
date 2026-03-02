from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import json

from app.core.database import get_db
from app.models.models import Project, Todo, Community
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectRead
from app.schemas.todo import TodoRead
from app.schemas.community import CommunityRead

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """
    Create a new project.
    """
    db_project = Project(
        scope=json.dumps(project.scope),
        status=project.status
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    # Parse JSON back to dict for response
    return ProjectRead(
        id=db_project.id,
        scope=json.loads(db_project.scope),
        status=db_project.status,
        created_at=db_project.created_at,
        updated_at=db_project.updated_at,
        deleted_at=db_project.deleted_at
    )


@router.get("", response_model=List[ProjectRead])
def list_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all projects (excluding soft-deleted ones).
    """
    projects = db.query(Project).filter(Project.deleted_at.is_(None)).order_by(Project.id).offset(skip).limit(limit).all()
    
    # Parse JSON for all projects
    return [
        ProjectRead(
            id=p.id,
            scope=json.loads(p.scope),
            status=p.status,
            created_at=p.created_at,
            updated_at=p.updated_at,
            deleted_at=p.deleted_at
        )
        for p in projects
    ]


@router.get("/{id}", response_model=ProjectRead)
def get_project(id: int, db: Session = Depends(get_db)):
    """
    Get a specific project by ID.
    """
    project = db.query(Project).filter(Project.id == id, Project.deleted_at.is_(None)).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return ProjectRead(
        id=project.id,
        scope=json.loads(project.scope),
        status=project.status,
        created_at=project.created_at,
        updated_at=project.updated_at,
        deleted_at=project.deleted_at
    )


@router.put("/{id}", response_model=ProjectRead)
def update_project(id: int, project_update: ProjectUpdate, db: Session = Depends(get_db)):
    """
    Update a project.
    """
    project = db.query(Project).filter(Project.id == id, Project.deleted_at.is_(None)).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project_update.scope is not None:
        project.scope = json.dumps(project_update.scope)
    if project_update.status is not None:
        project.status = project_update.status
    
    project.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(project)
    
    return ProjectRead(
        id=project.id,
        scope=json.loads(project.scope),
        status=project.status,
        created_at=project.created_at,
        updated_at=project.updated_at,
        deleted_at=project.deleted_at
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(id: int, db: Session = Depends(get_db)):
    """
    Soft delete a project.
    """
    project = db.query(Project).filter(Project.id == id, Project.deleted_at.is_(None)).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project.deleted_at = datetime.utcnow()
    db.commit()
    return None


@router.get("/{project_id}/todos", response_model=List[TodoRead])
def get_project_todos(project_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all todos for a specific project.
    """
    todos = db.query(Todo).filter(
        Todo.project_id == project_id,
        Todo.deleted_at.is_(None)
    ).order_by(Todo.id).offset(skip).limit(limit).all()
    
    return [
        TodoRead(
            id=t.id,
            project_id=t.project_id,
            scope=json.loads(t.scope),
            status=t.status,
            created_at=t.created_at,
            updated_at=t.updated_at,
            deleted_at=t.deleted_at
        )
        for t in todos
    ]


@router.get("/{project_id}/community", response_model=List[CommunityRead])
def get_project_community(project_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all community entries for a specific project.
    """
    communities = db.query(Community).filter(
        Community.project_id == project_id,
        Community.deleted_at.is_(None)
    ).order_by(Community.id).offset(skip).limit(limit).all()
    
    return [
        CommunityRead(
            id=c.id,
            project_id=c.project_id,
            team=json.loads(c.team),
            role=c.role,
            created_at=c.created_at,
            updated_at=c.updated_at,
            deleted_at=c.deleted_at
        )
        for c in communities
    ]
