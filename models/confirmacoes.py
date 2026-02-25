from core.database import Base
from sqlalchemy import Column, DateTime, Float, Integer, String


class Confirmacoes(Base):
    __tablename__ = "confirmacoes"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    cidade_id = Column(Integer, nullable=False)
    cidade_nome = Column(String, nullable=True)
    entregador_id = Column(String, nullable=True)
    entregador_nome = Column(String, nullable=True)
    data_hora = Column(DateTime(timezone=True), nullable=True)
    gps_lat = Column(Float, nullable=True)
    gps_lng = Column(Float, nullable=True)
    user_id = Column(String, nullable=False)