from fastapi import FastAPI
from .database import engine
from .models import Base
from .routers import users

app = FastAPI(title="Dracco Backend Pro")

Base.metadata.create_all(bind=engine)

app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "API is running 🚀"}
