from core.database import Base
from sqlalchemy import Column, DateTime, Integer, String


class Cidades(Base):
    __tablename__ = "cidades"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    nome = Column(String, nullable=False)
    entregador_padrao_id = Column(String, nullable=True)
    entregador_padrao_nome = Column(String, nullable=True)
    motorista_id = Column(String, nullable=True)
    motorista_nome = Column(String, nullable=True)
    veiculo_tipo = Column(String, nullable=True)
    status = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=True)