from sqlalchemy import Column, Integer, String

from src.db.dbms import Base


class Security(Base):
    __tablename__ = "security"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)


class SecurityTrades(Base):
    __tablename__ = "security_trades"

    id = Column(Integer, primary_key=True, autoincrement=True)
