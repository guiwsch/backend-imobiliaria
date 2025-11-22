from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


class LeadStatusEnum(str, Enum):
    novo = "novo"
    contatado = "contatado"
    visitaAgendada = "visitaAgendada"
    negociacao = "negociacao"
    convertido = "convertido"
    perdido = "perdido"


class LeadBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: str
    mensagem: Optional[str] = None
    origem: Optional[str] = None


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    status: Optional[LeadStatusEnum] = None
    mensagem: Optional[str] = None


class Lead(LeadBase):
    id: int
    status: LeadStatusEnum
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
