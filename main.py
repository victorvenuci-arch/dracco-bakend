from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importa banco
from services.database_core import engine, Base

# Importa modelos (IMPORTANTE para criar tabela)
from data_models.user import User

app = FastAPI(
    title="Dracco Backend",
    version="1.0.0"
)

# Cria todas as tabelas registradas no Base
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "online"}

@app.get("/health")
def health():
    return {"status": "ok"}
