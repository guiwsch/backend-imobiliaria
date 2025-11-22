from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.session import Base


class Configuracao(Base):
    __tablename__ = "configuracoes"

    id = Column(Integer, primary_key=True, index=True)

    # Informações da empresa
    nome_empresa = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    telefone = Column(String(20), nullable=False)
    whatsapp = Column(String(20), nullable=False)
    site = Column(String(200), nullable=True)
    endereco = Column(Text, nullable=False)
    sobre = Column(Text, nullable=True)

    # Notificações
    notificacao_email = Column(Boolean, default=True)
    notificacao_sms = Column(Boolean, default=False)
    notificacao_whatsapp = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
