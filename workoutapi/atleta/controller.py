from datetime import datetime, timezone
from uuid import uuid4
from fastapi import APIRouter, HTTPException, status, Body, Query
from pydantic import UUID4
from contrib.dependencies import DatabaseDependency
from atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate, AtletaListOut
from atleta.models import AtletaModel
from categorias.models import CategoriaModel
from sqlalchemy.future import select
from centro_treinamento.models import CentroTreinamentoModel

from typing import Optional
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

router = APIRouter()

@router.post(
    '/',
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post_atleta(
    db_session: DatabaseDependency,
    atleta_in: AtletaIn = Body(...),
):
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

    categoria = (
        await db_session.execute(
            select(CategoriaModel).filter_by(nome=categoria_nome)
        )
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f'A categoria {categoria_nome} não foi encontrada',
        )

    centro_treinamento = (
        await db_session.execute(
            select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome)
        )
    ).scalars().first()

    if not centro_treinamento:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f'O centro de treinamento {centro_treinamento_nome} não foi encontrado',
        )

    atleta_model = AtletaModel(
        **atleta_in.model_dump(exclude={'categoria', 'centro_treinamento'}),
        categoria_id=categoria.pk_id,
        centro_treinamento_id=centro_treinamento.pk_id,
        created_at=datetime.now(timezone.utc),
    )

    db_session.add(atleta_model)
    await db_session.commit()
    await db_session.refresh(atleta_model)

    return AtletaOut.model_validate(atleta_model)

@router.get('/', summary='Consultar todos os atletas', status_code=status.HTTP_200_OK, response_model=Page[AtletaListOut])
async def get_atletas(db_session: DatabaseDependency, nome: Optional[str] = Query(None), cpf: Optional[str] = Query(None)):
    query = (
    select(
        AtletaModel.id,
        AtletaModel.nome,
        AtletaModel.cpf,
        CategoriaModel.nome.label("categoria"),
        CentroTreinamentoModel.nome.label("centro_treinamento"),
    )
    .join(CategoriaModel)
    .join(CentroTreinamentoModel)
)

    if nome:
        query = query.filter(AtletaModel.nome.ilike(f'%{nome}'))
    if cpf:
        query = query.filter(AtletaModel.cpf == cpf)
    
    return await paginate(db_session, query)

@router.get('/{id}', summary='Consultar um atleta pelo id', status_code=status.HTTP_200_OK, response_model=AtletaOut)
async def get_atleta(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    result = await db_session.execute(select(AtletaModel).filter_by(id=id))
    atleta= result.scalars().first()

    if not atleta:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id: {id}')
    

    return AtletaOut.model_validate(atleta)

@router.patch('/{id}', summary='Editar um atleta pelo id', status_code=status.HTTP_200_OK, response_model=AtletaOut)
async def patch_atleta(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    result = await db_session.execute(select(AtletaModel).filter_by(id=id))
    atleta= result.scalars().first()

    if not atleta:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id: {id}')
    
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta,key,value)
    
    await db_session.commit()
    await db_session.refresh(atleta)

    return AtletaOut.model_validate(atleta)

@router.delete('/{id}', summary='Deletar um atleta pelo id', status_code=status.HTTP_204_NO_CONTENT)
async def delete_atleta(id: UUID4, db_session: DatabaseDependency) -> None:
    result = await db_session.execute(select(AtletaModel).filter_by(id=id))
    atleta= result.scalars().first()

    if not atleta:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id: {id}')
    
    await db_session.delete(atleta)
    await db_session.commit()