from fastapi import FastAPI
from routers import api_router
from atleta.models import AtletaModel
from categorias.models import CategoriaModel
from centro_treinamento.models import CentroTreinamentoModel
from fastapi_pagination import add_pagination

app = FastAPI(title='WorkoutAPI')
app.include_router(api_router)
add_pagination(app)