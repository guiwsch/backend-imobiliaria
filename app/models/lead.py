from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.sql import func
import enum
from app.db.session import Base


class LeadStatus(str, enum.Enum):
    novo = "novo"
    contatado = "contatado"
    visitaAgendada = "visitaAgendada"
    negociacao = "negociacao"
    convertido = "convertido"
    perdido = "perdido"


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    telefone = Column(String(20), nullable=False)
    mensagem = Column(Text, nullable=True)
    origem = Column(String(50), nullable=True)
    status = Column(Enum(LeadStatus), default=LeadStatus.novo)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
