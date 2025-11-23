from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.lead import Lead
from app.models.user import User
from app.schemas.lead import Lead as LeadSchema, LeadCreate, LeadUpdate

router = APIRouter()


@router.post("/contatos/", response_model=LeadSchema, status_code=status.HTTP_201_CREATED)
def create_contato(
    lead: LeadCreate,
    db: Session = Depends(get_db),
):
    db_lead = Lead(**lead.dict())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)

    return db_lead


@router.get("/", response_model=List[LeadSchema])
def list_leads(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Lead)

    if status_filter:
        query = query.filter(Lead.status == status_filter)

    leads = query.order_by(Lead.created_at.desc()).offset(skip).limit(limit).all()
    return leads


@router.get("/{lead_id}/", response_model=LeadSchema)
def get_lead(
    lead_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()

    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead não encontrado",
        )

    return lead


@router.put("/{lead_id}/", response_model=LeadSchema)
def update_lead(
    lead_id: int,
    lead_update: LeadUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()

    if not db_lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead não encontrado",
        )

    update_data = lead_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_lead, field, value)

    db.commit()
    db.refresh(db_lead)

    return db_lead


@router.delete("/{lead_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_lead(
    lead_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()

    if not db_lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead não encontrado",
        )

    db.delete(db_lead)
    db.commit()

    return None
