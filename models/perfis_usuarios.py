from core.database import Base
from sqlalchemy import Boolean, Column, Integer, String


class Perfis_usuarios(Base):
    __tablename__ = "perfis_usuarios"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    user_id = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    perfil = Column(String, nullable=False)
    cidade_vinculada_id = Column(Integer, nullable=True)
    cidade_vinculada_nome = Column(String, nullable=True)
    ativo = Column(Boolean, nullable=True)