from fastapi import FastAPI
from app.database import listar_categorias

app = FastAPI()

@app.get("/categorias")
def rota_listar_categorias():
    return listar_categorias()
