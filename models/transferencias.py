from core.database import Base
from sqlalchemy import Column, DateTime, Float, Integer, String


class Transferencias(Base):
    __tablename__ = "transferencias"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    codigo_rastreio = Column(String, nullable=False)
    cidade_id = Column(Integer, nullable=False)
    cidade_nome = Column(String, nullable=True)
    motorista_id = Column(String, nullable=True)
    motorista_nome = Column(String, nullable=True)
    data_hora = Column(DateTime(timezone=True), nullable=True)
    gps_lat = Column(Float, nullable=True)
    gps_lng = Column(Float, nullable=True)
    user_id = Column(String, nullable=False)