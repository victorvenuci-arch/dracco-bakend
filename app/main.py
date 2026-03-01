from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, User
from pydantic import BaseModel
import hashlib

# recria as tabelas (temporário para corrigir estrutura)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dracco Backend")


# dependency de banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


@app.get("/")
def root():
    return {"message": "API funcionando 🚀"}


@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # verifica se email já existe
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # hash simples (pode melhorar depois)
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()

    db_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password,
        is_active=True,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "id": db_user.id,
        "email": db_user.email,
        "active": db_user.is_active,
    }
