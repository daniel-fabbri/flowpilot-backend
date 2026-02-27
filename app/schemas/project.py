from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


# Project Schemas
class ProjectScopeBase(BaseModel):
    project_title: str
    project_description: str


class ProjectBase(BaseModel):
    scope: Dict[str, Any]
    status: str = "active"


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    scope: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class ProjectRead(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
