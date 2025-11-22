from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.imovel import Imovel, ImovelImagem
from app.models.user import User
from app.schemas.imovel import (
    Imovel as ImovelSchema,
    ImovelCreate,
    ImovelUpdate,
)
import os
import shutil
from datetime import datetime
from app.core.config import settings

router = APIRouter()


def get_imovel_preco(imovel: Imovel) -> float:
    if imovel.tipo_negocio.value == "venda":
        return imovel.preco_venda or 0
    else:
        return imovel.valor_aluguel or 0


def get_imagem_principal(imovel: Imovel) -> Optional[str]:
    imagem_principal = next(
        (img for img in imovel.imagens if img.principal), None
    )
    if imagem_principal:
        return imagem_principal.imagem_url
    elif imovel.imagens:
        return imovel.imagens[0].imagem_url
    return None


def serialize_imovel(imovel: Imovel) -> dict:
    return {
        **ImovelSchema.from_orm(imovel).dict(),
        "preco": get_imovel_preco(imovel),
        "imagem_principal": get_imagem_principal(imovel),
    }


@router.get("/", response_model=dict)
def list_imoveis(
    skip: int = 0,
    limit: int = 12,
    tipo_negocio: Optional[str] = None,
    tipo_imovel: Optional[str] = None,
    cidade: Optional[str] = None,
    bairro: Optional[str] = None,
    preco_venda__gte: Optional[float] = None,
    preco_venda__lte: Optional[float] = None,
    area_total__gte: Optional[float] = None,
    area_total__lte: Optional[float] = None,
    quartos: Optional[int] = None,
    banheiros: Optional[int] = None,
    vagas_garagem: Optional[int] = None,
    piscina: Optional[bool] = None,
    aceita_pets: Optional[bool] = None,
    mobiliado: Optional[bool] = None,
    search: Optional[str] = None,
    ordering: str = "-criado_em",
    page: int = 1,
    db: Session = Depends(get_db),
):
    query = db.query(Imovel)

    # Filtros
    if tipo_negocio:
        query = query.filter(Imovel.tipo_negocio == tipo_negocio)
    if tipo_imovel:
        query = query.filter(Imovel.tipo_imovel == tipo_imovel)
    if cidade:
        query = query.filter(Imovel.cidade.ilike(f"%{cidade}%"))
    if bairro:
        query = query.filter(Imovel.bairro.ilike(f"%{bairro}%"))
    if preco_venda__gte:
        query = query.filter(Imovel.preco_venda >= preco_venda__gte)
    if preco_venda__lte:
        query = query.filter(Imovel.preco_venda <= preco_venda__lte)
    if area_total__gte:
        query = query.filter(Imovel.area_total >= area_total__gte)
    if area_total__lte:
        query = query.filter(Imovel.area_total <= area_total__lte)
    if quartos:
        query = query.filter(Imovel.quartos >= quartos)
    if banheiros:
        query = query.filter(Imovel.banheiros >= banheiros)
    if vagas_garagem:
        query = query.filter(Imovel.vagas_garagem >= vagas_garagem)
    if piscina is not None:
        query = query.filter(Imovel.piscina == piscina)
    if aceita_pets is not None:
        query = query.filter(Imovel.aceita_pets == aceita_pets)
    if mobiliado is not None:
        query = query.filter(Imovel.mobiliado == mobiliado)
    if search:
        query = query.filter(
            or_(
                Imovel.titulo.ilike(f"%{search}%"),
                Imovel.descricao.ilike(f"%{search}%"),
                Imovel.cidade.ilike(f"%{search}%"),
                Imovel.bairro.ilike(f"%{search}%"),
            )
        )

    # Ordenação
    if ordering.startswith("-"):
        order_field = ordering[1:]
        query = query.order_by(getattr(Imovel, order_field).desc())
    else:
        query = query.order_by(getattr(Imovel, ordering))

    # Contagem total
    total_count = query.count()

    # Paginação
    offset = (page - 1) * limit
    imoveis = query.offset(offset).limit(limit).all()

    # Serialização
    results = [serialize_imovel(imovel) for imovel in imoveis]

    # Calcula URLs de próxima e anterior
    next_page = page + 1 if offset + limit < total_count else None
    previous_page = page - 1 if page > 1 else None

    return {
        "count": total_count,
        "next": next_page,
        "previous": previous_page,
        "results": results,
    }


@router.get("/destaques/", response_model=List[dict])
def list_destaques(
    limit: int = 6,
    db: Session = Depends(get_db),
):
    imoveis = (
        db.query(Imovel)
        .filter(Imovel.destaque == True)
        .order_by(Imovel.criado_em.desc())
        .limit(limit)
        .all()
    )

    return [serialize_imovel(imovel) for imovel in imoveis]


@router.get("/{imovel_id}/", response_model=dict)
def get_imovel(
    imovel_id: int,
    db: Session = Depends(get_db),
):
    imovel = db.query(Imovel).filter(Imovel.id == imovel_id).first()

    if not imovel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imóvel não encontrado",
        )

    return serialize_imovel(imovel)


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_imovel(
    imovel: ImovelCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_imovel = Imovel(**imovel.dict())
    db.add(db_imovel)
    db.commit()
    db.refresh(db_imovel)

    return serialize_imovel(db_imovel)


@router.put("/{imovel_id}/", response_model=dict)
def update_imovel(
    imovel_id: int,
    imovel_update: ImovelUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_imovel = db.query(Imovel).filter(Imovel.id == imovel_id).first()

    if not db_imovel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imóvel não encontrado",
        )

    update_data = imovel_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_imovel, field, value)

    db.commit()
    db.refresh(db_imovel)

    return serialize_imovel(db_imovel)


@router.delete("/{imovel_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_imovel(
    imovel_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_imovel = db.query(Imovel).filter(Imovel.id == imovel_id).first()

    if not db_imovel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imóvel não encontrado",
        )

    db.delete(db_imovel)
    db.commit()

    return None


@router.patch("/{imovel_id}/toggle_destaque/", response_model=dict)
def toggle_destaque(
    imovel_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_imovel = db.query(Imovel).filter(Imovel.id == imovel_id).first()

    if not db_imovel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imóvel não encontrado",
        )

    # Alterna o valor de destaque
    db_imovel.destaque = not db_imovel.destaque
    db.commit()
    db.refresh(db_imovel)

    return serialize_imovel(db_imovel)


@router.post("/{imovel_id}/upload_imagem/")
async def upload_imagem(
    imovel_id: int,
    file: UploadFile = File(...),
    ordem: int = Form(0),
    principal: bool = Form(False),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_imovel = db.query(Imovel).filter(Imovel.id == imovel_id).first()

    if not db_imovel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imóvel não encontrado",
        )

    # Cria diretório de uploads se não existir
    upload_dir = os.path.join(settings.UPLOAD_DIR, "imoveis", str(imovel_id))
    os.makedirs(upload_dir, exist_ok=True)

    # Gera nome único para o arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"{timestamp}{file_extension}"
    file_path = os.path.join(upload_dir, filename)

    # Salva o arquivo
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Cria registro no banco
    imagem_url = f"/uploads/imoveis/{imovel_id}/{filename}"

    # Se for principal, remove principal de outras imagens
    if principal:
        db.query(ImovelImagem).filter(
            ImovelImagem.imovel_id == imovel_id
        ).update({"principal": False})

    db_imagem = ImovelImagem(
        imovel_id=imovel_id,
        imagem_url=imagem_url,
        ordem=ordem,
        principal=principal,
    )
    db.add(db_imagem)
    db.commit()
    db.refresh(db_imagem)

    return {
        "id": db_imagem.id,
        "imagem_url": db_imagem.imagem_url,
        "ordem": db_imagem.ordem,
        "principal": db_imagem.principal,
    }
