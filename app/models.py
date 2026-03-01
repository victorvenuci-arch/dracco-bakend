from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class User(Base):
    _tablename_ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    active = Column(Boolean, default=True)
