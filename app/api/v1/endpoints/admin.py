from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.imovel import Imovel
from app.models.lead import Lead, LeadStatus
from app.models.visita import Visita, VisitaStatus
from app.models.configuracao import Configuracao
from app.models.user import User
from app.schemas.visita import Visita as VisitaSchema, VisitaCreate, VisitaUpdate
from app.schemas.configuracao import Configuracao as ConfiguracaoSchema, ConfiguracaoUpdate

router = APIRouter()


# Dashboard Statistics
@router.get("/stats/")
def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    total_imoveis = db.query(func.count(Imovel.id)).scalar()
    total_leads = db.query(func.count(Lead.id)).scalar()
    visitas_agendadas = (
        db.query(func.count(Visita.id))
        .filter(Visita.status == VisitaStatus.agendada)
        .scalar()
    )
    conversoes = (
        db.query(func.count(Lead.id))
        .filter(Lead.status == LeadStatus.convertido)
        .scalar()
    )

    return {
        "total_imoveis": total_imoveis or 0,
        "total_leads": total_leads or 0,
        "visitas_agendadas": visitas_agendadas or 0,
        "conversoes": conversoes or 0,
    }


# Visitas Management
@router.get("/visitas/", response_model=List[VisitaSchema])
def list_visitas(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    data_inicio: Optional[datetime] = None,
    data_fim: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Visita)

    if status_filter:
        query = query.filter(Visita.status == status_filter)

    if data_inicio:
        query = query.filter(Visita.data_hora >= data_inicio)

    if data_fim:
        query = query.filter(Visita.data_hora <= data_fim)

    visitas = query.order_by(Visita.data_hora).offset(skip).limit(limit).all()
    return visitas


@router.post("/visitas/", response_model=VisitaSchema, status_code=status.HTTP_201_CREATED)
def create_visita(
    visita: VisitaCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Verifica se o imóvel existe
    imovel = db.query(Imovel).filter(Imovel.id == visita.imovel_id).first()
    if not imovel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imóvel não encontrado",
        )

    db_visita = Visita(**visita.dict())
    db.add(db_visita)
    db.commit()
    db.refresh(db_visita)

    return db_visita


@router.get("/visitas/{visita_id}/", response_model=VisitaSchema)
def get_visita(
    visita_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    visita = db.query(Visita).filter(Visita.id == visita_id).first()

    if not visita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visita não encontrada",
        )

    return visita


@router.put("/visitas/{visita_id}/", response_model=VisitaSchema)
def update_visita(
    visita_id: int,
    visita_update: VisitaUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_visita = db.query(Visita).filter(Visita.id == visita_id).first()

    if not db_visita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visita não encontrada",
        )

    update_data = visita_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_visita, field, value)

    db.commit()
    db.refresh(db_visita)

    return db_visita


@router.delete("/visitas/{visita_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_visita(
    visita_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_visita = db.query(Visita).filter(Visita.id == visita_id).first()

    if not db_visita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visita não encontrada",
        )

    db.delete(db_visita)
    db.commit()

    return None


# Configurações
@router.get("/configuracoes/", response_model=ConfiguracaoSchema)
def get_configuracoes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    config = db.query(Configuracao).first()

    if not config:
        # Retorna configuração padrão se não existir
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configurações não encontradas. Crie uma configuração primeiro.",
        )

    return config


@router.put("/configuracoes/", response_model=ConfiguracaoSchema)
def update_configuracoes(
    config_update: ConfiguracaoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    config = db.query(Configuracao).first()

    if not config:
        # Cria nova configuração se não existir
        config = Configuracao(**config_update.dict())
        db.add(config)
    else:
        # Atualiza configuração existente
        update_data = config_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(config, field, value)

    db.commit()
    db.refresh(config)

    return config
