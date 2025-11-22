from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class ConfiguracaoBase(BaseModel):
    nome_empresa: str
    email: EmailStr
    telefone: str
    whatsapp: str
    site: Optional[str] = None
    endereco: str
    sobre: Optional[str] = None
    notificacao_email: bool = True
    notificacao_sms: bool = False
    notificacao_whatsapp: bool = True


class ConfiguracaoUpdate(ConfiguracaoBase):
    pass


class Configuracao(ConfiguracaoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
