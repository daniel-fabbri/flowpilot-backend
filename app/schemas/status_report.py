from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


# Status Report Schemas
class StatusReportBase(BaseModel):
    todo_id: int
    scope: Dict[str, Any]
    status: str = "draft"


class StatusReportCreate(StatusReportBase):
    pass


class StatusReportUpdate(BaseModel):
    scope: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class StatusReportRead(StatusReportBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
