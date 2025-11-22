from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TipoImovelEnum(str, Enum):
    casa = "casa"
    apartamento = "apartamento"
    terreno = "terreno"
    comercial = "comercial"


class TipoNegocioEnum(str, Enum):
    venda = "venda"
    aluguel = "aluguel"


class ImovelImagemBase(BaseModel):
    imagem_url: str
    ordem: int = 0
    principal: bool = False


class ImovelImagemCreate(ImovelImagemBase):
    pass


class ImovelImagem(ImovelImagemBase):
    id: int

    class Config:
        from_attributes = True


class ImovelBase(BaseModel):
    titulo: str
    descricao: str
    tipo_imovel: TipoImovelEnum
    tipo_negocio: TipoNegocioEnum
    preco_venda: Optional[float] = None
    valor_aluguel: Optional[float] = None
    area_total: float
    area_construida: Optional[float] = None
    quartos: int = 0
    banheiros: int = 0
    vagas_garagem: int = 0
    rua: str
    numero: str
    complemento: Optional[str] = None
    bairro: str
    cidade: str
    estado: str = Field(..., min_length=2, max_length=2)
    cep: str
    piscina: bool = False
    aceita_pets: bool = False
    mobiliado: bool = False
    destaque: bool = False


class ImovelCreate(ImovelBase):
    pass


class ImovelUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    tipo_imovel: Optional[TipoImovelEnum] = None
    tipo_negocio: Optional[TipoNegocioEnum] = None
    preco_venda: Optional[float] = None
    valor_aluguel: Optional[float] = None
    area_total: Optional[float] = None
    area_construida: Optional[float] = None
    quartos: Optional[int] = None
    banheiros: Optional[int] = None
    vagas_garagem: Optional[int] = None
    rua: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    piscina: Optional[bool] = None
    aceita_pets: Optional[bool] = None
    mobiliado: Optional[bool] = None
    destaque: Optional[bool] = None


class Imovel(ImovelBase):
    id: int
    preco: Optional[float] = None
    imagem_principal: Optional[str] = None
    imagens: List[ImovelImagem] = []
    criado_em: datetime
    atualizado_em: Optional[datetime] = None

    class Config:
        from_attributes = True


class ImovelInDB(Imovel):
    pass
