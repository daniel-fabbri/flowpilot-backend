from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import json

from app.core.database import get_db
from app.models.models import Todo, StatusReport
from app.schemas.todo import TodoCreate, TodoUpdate, TodoRead
from app.schemas.status_report import StatusReportRead

router = APIRouter(prefix="/api/v1/todos", tags=["todos"])


@router.post("", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """
    Create a new todo.
    """
    db_todo = Todo(
        project_id=todo.project_id,
        scope=json.dumps(todo.scope),
        status=todo.status
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    
    return TodoRead(
        id=db_todo.id,
        project_id=db_todo.project_id,
        scope=json.loads(db_todo.scope),
        status=db_todo.status,
        created_at=db_todo.created_at,
        updated_at=db_todo.updated_at,
        deleted_at=db_todo.deleted_at
    )


@router.get("", response_model=List[TodoRead])
def list_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all todos (excluding soft-deleted ones).
    """
    todos = db.query(Todo).filter(Todo.deleted_at.is_(None)).order_by(Todo.id).offset(skip).limit(limit).all()
    
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


@router.get("/{id}", response_model=TodoRead)
def get_todo(id: int, db: Session = Depends(get_db)):
    """
    Get a specific todo by ID.
    """
    todo = db.query(Todo).filter(Todo.id == id, Todo.deleted_at.is_(None)).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return TodoRead(
        id=todo.id,
        project_id=todo.project_id,
        scope=json.loads(todo.scope),
        status=todo.status,
        created_at=todo.created_at,
        updated_at=todo.updated_at,
        deleted_at=todo.deleted_at
    )





@router.put("/{id}", response_model=TodoRead)
def update_todo(id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    """
    Update a todo.
    """
    todo = db.query(Todo).filter(Todo.id == id, Todo.deleted_at.is_(None)).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo_update.scope is not None:
        todo.scope = json.dumps(todo_update.scope)
    if todo_update.status is not None:
        todo.status = todo_update.status
    
    todo.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(todo)
    
    return TodoRead(
        id=todo.id,
        project_id=todo.project_id,
        scope=json.loads(todo.scope),
        status=todo.status,
        created_at=todo.created_at,
        updated_at=todo.updated_at,
        deleted_at=todo.deleted_at
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, db: Session = Depends(get_db)):
    """
    Soft delete a todo.
    """
    todo = db.query(Todo).filter(Todo.id == id, Todo.deleted_at.is_(None)).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo.deleted_at = datetime.utcnow()
    db.commit()
    return None


@router.get("/{todo_id}/status-reports", response_model=List[StatusReportRead])
def get_todo_status_reports(todo_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all status reports for a specific todo.
    """
    status_reports = db.query(StatusReport).filter(
        StatusReport.todo_id == todo_id,
        StatusReport.deleted_at.is_(None)
    ).order_by(StatusReport.id).offset(skip).limit(limit).all()
    
    return [
        StatusReportRead(
            id=sr.id,
            todo_id=sr.todo_id,
            scope=json.loads(sr.scope),
            status=sr.status,
            created_at=sr.created_at,
            updated_at=sr.updated_at,
            deleted_at=sr.deleted_at
        )
        for sr in status_reports
    ]
