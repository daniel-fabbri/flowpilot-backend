from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import json

from app.core.database import get_db
from app.models.models import Community
from app.schemas.community import CommunityCreate, CommunityUpdate, CommunityRead

router = APIRouter(prefix="/api/v1/community", tags=["community"])


@router.post("", response_model=CommunityRead, status_code=status.HTTP_201_CREATED)
def create_community(community: CommunityCreate, db: Session = Depends(get_db)):
    """
    Create a new community entry.
    """
    db_community = Community(
        project_id=community.project_id,
        team=json.dumps(community.team),
        role=community.role
    )
    db.add(db_community)
    db.commit()
    db.refresh(db_community)
    
    result = CommunityRead.model_validate(db_community)
    result.team = json.loads(db_community.team)
    return result


@router.get("", response_model=List[CommunityRead])
def list_community(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all community entries (excluding soft-deleted ones).
    """
    communities = db.query(Community).filter(Community.deleted_at.is_(None)).offset(skip).limit(limit).all()
    
    results = []
    for community in communities:
        result = CommunityRead.model_validate(community)
        result.team = json.loads(community.team)
        results.append(result)
    
    return results


@router.get("/{id}", response_model=CommunityRead)
def get_community(id: int, db: Session = Depends(get_db)):
    """
    Get a specific community entry by ID.
    """
    community = db.query(Community).filter(Community.id == id, Community.deleted_at.is_(None)).first()
    if not community:
        raise HTTPException(status_code=404, detail="Community entry not found")
    
    result = CommunityRead.model_validate(community)
    result.team = json.loads(community.team)
    return result





@router.put("/{id}", response_model=CommunityRead)
def update_community(id: int, community_update: CommunityUpdate, db: Session = Depends(get_db)):
    """
    Update a community entry.
    """
    community = db.query(Community).filter(Community.id == id, Community.deleted_at.is_(None)).first()
    if not community:
        raise HTTPException(status_code=404, detail="Community entry not found")
    
    if community_update.team is not None:
        community.team = json.dumps(community_update.team)
    if community_update.role is not None:
        community.role = community_update.role
    
    community.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(community)
    
    result = CommunityRead.model_validate(community)
    result.team = json.loads(community.team)
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_community(id: int, db: Session = Depends(get_db)):
    """
    Soft delete a community entry.
    """
    community = db.query(Community).filter(Community.id == id, Community.deleted_at.is_(None)).first()
    if not community:
        raise HTTPException(status_code=404, detail="Community entry not found")
    
    community.deleted_at = datetime.utcnow()
    db.commit()
    return None
