from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers.users import router as users_router

app = FastAPI(title="Dracco Backend Pro")

Base.metadata.create_all(bind=engine)

app.include_router(users_router)

@app.get("/")
def root():
    return {"message": "API is running 🚀"}
