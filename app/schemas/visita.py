from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


class VisitaStatusEnum(str, Enum):
    agendada = "agendada"
    confirmada = "confirmada"
    realizada = "realizada"
    cancelada = "cancelada"


class VisitaBase(BaseModel):
    imovel_id: int
    nome_cliente: str
    email_cliente: EmailStr
    telefone_cliente: str
    data_hora: datetime
    observacoes: Optional[str] = None


class VisitaCreate(VisitaBase):
    lead_id: Optional[int] = None


class VisitaUpdate(BaseModel):
    status: Optional[VisitaStatusEnum] = None
    data_hora: Optional[datetime] = None
    observacoes: Optional[str] = None


class Visita(VisitaBase):
    id: int
    lead_id: Optional[int] = None
    status: VisitaStatusEnum
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
