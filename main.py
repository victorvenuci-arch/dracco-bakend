import os
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# =========================
# CONFIGURAÇÃO DO BANCO
# =========================

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL não encontrada nas variáveis de ambiente.")

# Corrige automaticamente caso venha como postgres://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql+psycopg2://",
        1
    )

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# =========================
# FASTAPI APP
# =========================

app = FastAPI(
    title="Dracco Backend",
    version="1.0.0"
)

# =========================
# STARTUP EVENT
# =========================

@app.on_event("startup")
def startup():
    try:
        Base.metadata.create_all(bind=engine)
        print("Banco conectado com sucesso.")
    except Exception as e:
        print("Erro ao conectar no banco:", e)
        raise e

# =========================
# ROTAS
# =========================

@app.get("/")
def home():
    return {"status": "online"}

@app.get("/health")
def health():
    return {"status": "ok"}
