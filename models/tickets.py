from core.database import Base
from sqlalchemy import Column, DateTime, Integer, String


class Tickets(Base):
    __tablename__ = "tickets"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    tbr = Column(String, nullable=False)
    motivo = Column(String, nullable=False)
    base_code = Column(String, nullable=False)
    created_by = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=True)