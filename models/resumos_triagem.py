from core.database import Base
from sqlalchemy import Column, DateTime, Integer, String


class Resumos_triagem(Base):
    __tablename__ = "resumos_triagem"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    cidade_id = Column(Integer, nullable=False)
    cidade_nome = Column(String, nullable=False)
    quantidade_pacotes = Column(Integer, nullable=False)
    data_vencimento = Column(String, nullable=True)
    auxiliar_responsavel = Column(String, nullable=True)
    status = Column(String, nullable=True)
    user_id = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=True)