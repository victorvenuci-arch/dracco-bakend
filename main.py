import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from services.database import initialize_database, close_database
from services.mock_data import initialize_mock_data
from services.auth import initialize_admin_user

# ===============================
# LOGGING
# ===============================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===============================
# LIFESPAN
# ===============================

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=== Application startup initiated ===")

    await initialize_database()

    try:
        from services.database_core import engine
        from data_models.user import User

        User.__table__.create(bind=engine, checkfirst=True)
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
# APP
# ===============================

app = FastAPI(
    title="Dracco Backend",
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
# ROUTES
# ===============================

@app.get("/")
def root():
    return {"message": "Dracco Backend está rodando 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}

# ===============================
# ERROR HANDLER
# ===============================

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        raise exc

    logger.error(str(exc))

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"},
    )
