from core.database import Base
from sqlalchemy import Column, DateTime, Integer, String


class Rotas(Base):
    __tablename__ = "rotas"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    motorista_id = Column(String, nullable=False)
    motorista_nome = Column(String, nullable=False)
    veiculo_tipo = Column(String, nullable=False)
    cidades_ids = Column(String, nullable=True)
    cidades_nomes = Column(String, nullable=True)
    status = Column(String, nullable=True)
    user_id = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=True)