"""
    Esse código é o módulo principal do projeto, responsável por iniciar
todas funcionalidades do sistema.

author: github.com/gustavosett
"""
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import session
from .routes import routers

from fastapi.responses import RedirectResponse


app = FastAPI()
# Atualiza/cria os modelos sqlalchemy
session.initialize_db()

# Grava origens permitidas para fazer requisições na API
origins = [
    "*",
]

# Adiciona middlewares a engine
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# adiciona as rotas a engine
for route in routers:
    app.include_router(route)

@app.get("/", include_in_schema=False)
async def redirect():
    return RedirectResponse("/docs#")

# Essa função salva a documentação OpenAPI dos dados do FastApi em um JSON
@app.on_event("startup")
def save_openapi_json():
    openapi_data = app.openapi()
    # salva arquivo
    with open("openapi.json", "w") as file:
        json.dump(openapi_data, file)
