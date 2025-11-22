from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.sql import func
import enum
from app.db.session import Base


class VisitaStatus(str, enum.Enum):
    agendada = "agendada"
    confirmada = "confirmada"
    realizada = "realizada"
    cancelada = "cancelada"


class Visita(Base):
    __tablename__ = "visitas"

    id = Column(Integer, primary_key=True, index=True)
    imovel_id = Column(Integer, ForeignKey("imoveis.id", ondelete="CASCADE"), nullable=False)
    lead_id = Column(Integer, ForeignKey("leads.id", ondelete="CASCADE"), nullable=True)

    nome_cliente = Column(String(200), nullable=False)
    email_cliente = Column(String(200), nullable=False)
    telefone_cliente = Column(String(20), nullable=False)

    data_hora = Column(DateTime(timezone=True), nullable=False)
    status = Column(Enum(VisitaStatus), default=VisitaStatus.agendada)
    observacoes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
