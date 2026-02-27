from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import json

from app.core.database import get_db
from app.models.models import StatusReport
from app.schemas.status_report import StatusReportCreate, StatusReportUpdate, StatusReportRead

router = APIRouter(prefix="/api/v1/status-reports", tags=["status-reports"])


@router.post("", response_model=StatusReportRead, status_code=status.HTTP_201_CREATED)
def create_status_report(status_report: StatusReportCreate, db: Session = Depends(get_db)):
    """
    Create a new status report.
    """
    db_status_report = StatusReport(
        todo_id=status_report.todo_id,
        scope=json.dumps(status_report.scope),
        status=status_report.status
    )
    db.add(db_status_report)
    db.commit()
    db.refresh(db_status_report)
    
    result = StatusReportRead.model_validate(db_status_report)
    result.scope = json.loads(db_status_report.scope)
    return result


@router.get("", response_model=List[StatusReportRead])
def list_status_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all status reports (excluding soft-deleted ones).
    """
    status_reports = db.query(StatusReport).filter(StatusReport.deleted_at.is_(None)).offset(skip).limit(limit).all()
    
    results = []
    for status_report in status_reports:
        result = StatusReportRead.model_validate(status_report)
        result.scope = json.loads(status_report.scope)
        results.append(result)
    
    return results


@router.get("/{id}", response_model=StatusReportRead)
def get_status_report(id: int, db: Session = Depends(get_db)):
    """
    Get a specific status report by ID.
    """
    status_report = db.query(StatusReport).filter(StatusReport.id == id, StatusReport.deleted_at.is_(None)).first()
    if not status_report:
        raise HTTPException(status_code=404, detail="Status report not found")
    
    result = StatusReportRead.model_validate(status_report)
    result.scope = json.loads(status_report.scope)
    return result





@router.put("/{id}", response_model=StatusReportRead)
def update_status_report(id: int, status_report_update: StatusReportUpdate, db: Session = Depends(get_db)):
    """
    Update a status report.
    """
    status_report = db.query(StatusReport).filter(StatusReport.id == id, StatusReport.deleted_at.is_(None)).first()
    if not status_report:
        raise HTTPException(status_code=404, detail="Status report not found")
    
    if status_report_update.scope is not None:
        status_report.scope = json.dumps(status_report_update.scope)
    if status_report_update.status is not None:
        status_report.status = status_report_update.status
    
    status_report.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(status_report)
    
    result = StatusReportRead.model_validate(status_report)
    result.scope = json.loads(status_report.scope)
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_status_report(id: int, db: Session = Depends(get_db)):
    """
    Soft delete a status report.
    """
    status_report = db.query(StatusReport).filter(StatusReport.id == id, StatusReport.deleted_at.is_(None)).first()
    if not status_report:
        raise HTTPException(status_code=404, detail="Status report not found")
    
    status_report.deleted_at = datetime.utcnow()
    db.commit()
    return None
