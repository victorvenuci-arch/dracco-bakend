from core.database import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String


class Dracco_users(Base):
    __tablename__ = "dracco_users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    nome = Column(String, nullable=False)
    login = Column(String, nullable=False)
    senha_hash = Column(String, nullable=False)
    level = Column(Integer, nullable=False)
    base_code = Column(String, nullable=False)
    permissions = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=True)
    is_online = Column(Boolean, nullable=True)
    last_activity = Column(DateTime(timezone=True), nullable=True)
    veiculo_tipo = Column(String, nullable=True)
    login_amazon = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=True)