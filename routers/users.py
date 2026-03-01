from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.database_core import SessionLocal
from data_models.user import User
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["Users"])


class UserCreate(BaseModel):
    username: str
    password: str
    role: str
    base: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        username=user.username,
        password=user.password,
        role=user.role,
        base=user.base,
        active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Usuário criado com sucesso",
        "id": new_user.id
    }
