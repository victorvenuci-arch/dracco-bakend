import os
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session

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
# MODEL
# =========================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    active = Column(Boolean, default=True)

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
        print("Banco conectado e tabelas criadas.")
    except Exception as e:
        print("Erro ao conectar no banco:", e)
        raise e

# =========================
# SCHEMA
# =========================

class UserCreate(BaseModel):
    name: str
    email: str

# =========================
# DEPENDÊNCIA DB
# =========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# ROTAS
# =========================

@app.get("/")
def home():
    return {"status": "online"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
