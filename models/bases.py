from core.database import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String


class Bases(Base):
    __tablename__ = "bases"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    code = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=True)