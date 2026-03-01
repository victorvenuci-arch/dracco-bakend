from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.database_core import engine, Base
from data_models.user import User
from routers.users import router as users_router

app = FastAPI(
    title="Dracco Backend",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(users_router)

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
