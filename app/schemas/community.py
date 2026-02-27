from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


# Community Schemas
class CommunityBase(BaseModel):
    project_id: int
    team: List[Dict[str, str]]
    role: Optional[str] = None


class CommunityCreate(CommunityBase):
    pass


class CommunityUpdate(BaseModel):
    team: Optional[List[Dict[str, str]]] = None
    role: Optional[str] = None


class CommunityRead(CommunityBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
