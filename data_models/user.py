rom sqlalchemy import Column, Integer, String, Boolean
from services.database_core import Base

class User(Base):
    _tablename_ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    base = Column(String, nullable=False)
    active = Column(Boolean, default=True)
