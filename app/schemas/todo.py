from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


# Todo Schemas
class TodoBase(BaseModel):
    project_id: int
    scope: Dict[str, Any]
    status: str = "open"


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    scope: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class TodoRead(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
