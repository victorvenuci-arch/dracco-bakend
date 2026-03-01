import os
import logging
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Boolean

# ===============================
# DATABASE CONFIG
# ===============================

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL não encontrada nas variáveis de ambiente.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ===============================
# MODEL USER
# ===============================

class User(Base):
    _tablename_ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    base = Column(String, nullable=False)
    active = Column(Boolean, default=True)

# ===============================
# CREATE TABLES
# ===============================

Base.metadata.create_all(bind=engine)

# ===============================
# FASTAPI APP
# ===============================

app = FastAPI(
    title="Dracco Backend",
    description="Sistema Logístico Dracco",
    version="1.0.0"
)

# ===============================
# CORS
# ===============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# ROUTES
# ===============================

@app.get("/")
def root():
    return {"message": "Dracco Backend está rodando 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}

# ===============================
# GLOBAL ERROR HANDLER
# ===============================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(str(exc))
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"},
    )
