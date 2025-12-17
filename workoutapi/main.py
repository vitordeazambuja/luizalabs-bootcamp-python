from fastapi import FastAPI
from routers import api_router
from atleta.models import AtletaModel
from categorias.models import CategoriaModel
from centro_treinamento.models import CentroTreinamentoModel

app = FastAPI(title='WorkoutAPI')
app.include_router(api_router)