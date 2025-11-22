from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.session import Base


class TipoImovel(str, enum.Enum):
    casa = "casa"
    apartamento = "apartamento"
    terreno = "terreno"
    comercial = "comercial"


class TipoNegocio(str, enum.Enum):
    venda = "venda"
    aluguel = "aluguel"


class Imovel(Base):
    __tablename__ = "imoveis"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=False)
    tipo_imovel = Column(Enum(TipoImovel), nullable=False)
    tipo_negocio = Column(Enum(TipoNegocio), nullable=False)

    # Preços
    preco_venda = Column(Float, nullable=True)
    valor_aluguel = Column(Float, nullable=True)

    # Características
    area_total = Column(Float, nullable=False)
    area_construida = Column(Float, nullable=True)
    quartos = Column(Integer, nullable=False, default=0)
    banheiros = Column(Integer, nullable=False, default=0)
    vagas_garagem = Column(Integer, nullable=False, default=0)

    # Localização
    rua = Column(String(200), nullable=False)
    numero = Column(String(20), nullable=False)
    complemento = Column(String(100), nullable=True)
    bairro = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    estado = Column(String(2), nullable=False)
    cep = Column(String(10), nullable=False)

    # Extras
    piscina = Column(Boolean, default=False)
    aceita_pets = Column(Boolean, default=False)
    mobiliado = Column(Boolean, default=False)
    destaque = Column(Boolean, default=False)

    # Timestamps
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    imagens = relationship("ImovelImagem", back_populates="imovel", cascade="all, delete-orphan")


class ImovelImagem(Base):
    __tablename__ = "imovel_imagens"

    id = Column(Integer, primary_key=True, index=True)
    imovel_id = Column(Integer, ForeignKey("imoveis.id", ondelete="CASCADE"), nullable=False)
    imagem_url = Column(String(500), nullable=False)
    ordem = Column(Integer, default=0)
    principal = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    imovel = relationship("Imovel", back_populates="imagens")
