from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class User(Base):
    _tablename_ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    active = Column(Boolean, default=True)
