import importlib
import logging
import pkgutil
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from services.database import initialize_database, close_database
from services.mock_data import initialize_mock_data
from services.auth import initialize_admin_user

# ===============================
# LOGGING
# ===============================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(_name_)

# ===============================
# LIFESPAN
# ===============================

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=== Application startup initiated ===")

    # Inicializa conexão com banco
    await initialize_database()

    # Cria tabela users com segurança
    try:
        from services.database_core import engine
        from data_models.user import User

        User._table_.create(bind=engine, checkfirst=True)
        logger.info("Users table verified/created successfully.")
    except Exception as e:
        logger.error(f"Error creating users table: {e}")

    await initialize_mock_data()
    await initialize_admin_user()

    logger.info("=== Application startup completed successfully ===")
    yield

    await close_database()
    logger.info("=== Application shutdown completed ===")

# ===============================
# FASTAPI APP
# ===============================

app = FastAPI(
    title="Dracco Backend",
    description="Sistema Logístico Dracco",
    version="1.0.0",
    lifespan=lifespan,
)

# ===============================
# CORS
# ===============================

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# AUTO ROUTER DISCOVERY
# ===============================

def include_routers_from_package(app: FastAPI, package_name: str = "routers") -> None:
    try:
        pkg = importlib.import_module(package_name)
    except Exception as exc:
        logger.warning(f"Routers package '{package_name}' not loaded: {exc}")
        return

    for , module_name, is_pkg in pkgutil.walk_packages(pkg.path, pkg.name_ + "."):
        if is_pkg:
            continue
        try:
            module = importlib.import_module(module_name)
        except Exception as exc:
            logger.warning(f"Failed to import module '{module_name}': {exc}")
            continue

        for attr_name in ("router", "admin_router"):
            if hasattr(module, attr_name):
                attr = getattr(module, attr_name)
                if isinstance(attr, APIRouter):
                    app.include_router(attr)
                    logger.info(f"Included router: {module_name}.{attr_name}")

include_routers_from_package(app)

# ===============================
# ROOT ROUTES
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
async def general_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        raise exc

    logger.error(f"Exception: {traceback.format_exc()}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"},
    )
