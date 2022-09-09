from sqlalchemy import Boolean, Column, String, Integer, DateTime, func, Float
from api.utils.base import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    date_registered = Column(DateTime(), default=func.now())
    updated_at = Column(DateTime(), onupdate=datetime.now())


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, nullable=False)
    customer_name = Column(String(255), nullable=False)
    gas_price = Column(Float, nullable=False)
    gas_quantity = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    create_at = Column(DateTime(), default=func.now())
    updated_at = Column(DateTime(), onupdate=datetime.now())
