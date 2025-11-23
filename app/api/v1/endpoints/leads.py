from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.lead import Lead
from app.models.imovel import Imovel
from app.models.configuracao import Configuracao
from app.models.user import User
from app.schemas.lead import Lead as LeadSchema, LeadCreate, LeadUpdate
from app.services.email_service import email_service
import logging

logger = logging.getLogger(__name__)

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

    # Enviar notificação por email
    try:
        # Buscar configurações para pegar email do admin
        config = db.query(Configuracao).first()

        if config and config.notificacao_email and config.email:
            # Preparar dados do lead
            lead_data = {
                'nome': db_lead.nome,
                'email': db_lead.email,
                'telefone': db_lead.telefone,
                'origem': db_lead.origem or 'Site',
                'mensagem': db_lead.mensagem,
            }

            # Adicionar título do imóvel se houver
            if db_lead.imovel_id:
                imovel = db.query(Imovel).filter(Imovel.id == db_lead.imovel_id).first()
                if imovel:
                    lead_data['imovel_titulo'] = imovel.titulo

            # Enviar email
            email_service.send_new_lead_notification(lead_data, config.email)
            logger.info(f"Notificação de novo lead enviada para: {config.email}")
    except Exception as e:
        logger.error(f"Erro ao enviar notificação de lead: {str(e)}")
        # Não falhar a requisição se o email falhar

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
