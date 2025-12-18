from datetime import datetime, timezone
from uuid import uuid4
from fastapi import APIRouter, HTTPException, status, Body
from pydantic import UUID4
from contrib.dependencies import DatabaseDependency
from atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from atleta.models import AtletaModel
from categorias.models import CategoriaModel
from sqlalchemy.future import select
from centro_treinamento.models import CentroTreinamentoModel

router = APIRouter()

@router.post('/', summary='Criar um novo atleta', status_code=status.HTTP_201_CREATED, response_model=AtletaOut)
async def post(db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)):
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in..centro_treinamento.nome

    result = await db_session.execute(select(CategoriaModel).filter_by(nome=categoria_nome))
    categoria= result.scalars().first()

    if not categoria:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f'A categoria {categoria_nome} não foi encontrada')
    
    result = await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))
    centro_treinamento= result.scalars().first()

    if not centro_treinamento:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f'O centro de treinamento {centro_treinamento_nome} não foi encontrado')

    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.now(timezone.utc), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria','centro_treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Ocorreu um erro ao inserir os dados no banco')
    
    db_session.add(atleta_model)
    await db_session.commit()

    return atleta_out

@router.get('/', summary='Consultar todos os atletas', status_code=status.HTTP_200_OK, response_model=list[AtletaOut])
async def query(db_session: DatabaseDependency) -> list[AtletaOut]:
    result = await db_session.execute(select(AtletaModel))
    atletas= result.scalars().all()

    return [AtletaOut.model_validate(a) for a in atletas]

@router.get('/{id}', summary='Consultar um atleta pelo id', status_code=status.HTTP_200_OK, response_model=AtletaOut)
async def query(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    result = await db_session.execute(select(AtletaModel).filter_by(id=id))
    atleta= result.scalars().first()

    if not atleta:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id: {id}')
    

    return AtletaOut.model_validate(atleta)

@router.patch('/{id}', summary='Editar um atleta pelo id', status_code=status.HTTP_200_OK, response_model=AtletaOut)
async def query(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
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
async def query(id: UUID4, db_session: DatabaseDependency) -> None:
    result = await db_session.execute(select(AtletaModel).filter_by(id=id))
    atleta= result.scalars().first()

    if not atleta:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id: {id}')
    
    await db_session.delete(atleta)
    await db_session.commit()