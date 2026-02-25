from core.database import Base
from sqlalchemy import Column, DateTime, Integer, String


class Leituras_auxiliar(Base):
    __tablename__ = "leituras_auxiliar"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    codigo_rastreio = Column(String, nullable=False)
    cidade_id = Column(Integer, nullable=False)
    cidade_nome = Column(String, nullable=False)
    data_vencimento = Column(String, nullable=True)
    auxiliar_nome = Column(String, nullable=True)
    user_id = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=True)