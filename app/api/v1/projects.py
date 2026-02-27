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
    result = ProjectRead.model_validate(db_project)
    result.scope = json.loads(db_project.scope)
    return result


@router.get("", response_model=List[ProjectRead])
def list_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all projects (excluding soft-deleted ones).
    """
    projects = db.query(Project).filter(Project.deleted_at.is_(None)).offset(skip).limit(limit).all()
    
    # Parse JSON for all projects
    results = []
    for project in projects:
        result = ProjectRead.model_validate(project)
        result.scope = json.loads(project.scope)
        results.append(result)
    
    return results


@router.get("/{id}", response_model=ProjectRead)
def get_project(id: int, db: Session = Depends(get_db)):
    """
    Get a specific project by ID.
    """
    project = db.query(Project).filter(Project.id == id, Project.deleted_at.is_(None)).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    result = ProjectRead.model_validate(project)
    result.scope = json.loads(project.scope)
    return result


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
    
    result = ProjectRead.model_validate(project)
    result.scope = json.loads(project.scope)
    return result


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
    ).offset(skip).limit(limit).all()
    
    results = []
    for todo in todos:
        result = TodoRead.model_validate(todo)
        result.scope = json.loads(todo.scope)
        results.append(result)
    
    return results


@router.get("/{project_id}/community", response_model=List[CommunityRead])
def get_project_community(project_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all community entries for a specific project.
    """
    communities = db.query(Community).filter(
        Community.project_id == project_id,
        Community.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()
    
    results = []
    for community in communities:
        result = CommunityRead.model_validate(community)
        result.team = json.loads(community.team)
        results.append(result)
    
    return results
