import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter


# ==============================
# LOGGING SIMPLIFICADO (Cloud Safe)
# ==============================

def setup_logging():
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(),  # Apenas console (Render usa console)
        ],
    )

    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)

    logger = logging.getLogger(__name__)
    logger.info("=== Logging inicializado ===")


# ==============================
# LIFESPAN SIMPLES (SEM BANCO)
# ==============================

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=== Aplicação iniciando ===")
    yield
    print("=== Aplicação encerrando ===")


# ==============================
# APP PRINCIPAL
# ==============================

app = FastAPI(
    title="Dracco Backend",
    description="Sistema Logístico Dracco",
    version="1.0.0",
    lifespan=lifespan,
)


# ==============================
# CORS LIBERADO
# ==============================

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================
# ROTAS BÁSICAS
# ==============================

@app.get("/")
def root():
    return {"status": "Dracco Backend Online 🚀"}


@app.get("/health")
def health():
    return {"status": "healthy"}


# ==============================
# HANDLER GLOBAL DE ERRO
# ==============================

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logging.error(f"Erro interno: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"},
    )


# ==============================
# EXECUÇÃO LOCAL (OPCIONAL)
# ==============================

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
    )
