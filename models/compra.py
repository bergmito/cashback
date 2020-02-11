"""Model Compra"""
from sqlalchemy import Column, String, BigInteger, DECIMAL, Date
from models.base import MYSQL_BASE

class Compra(MYSQL_BASE):
    """Class for Compra"""
    __tablename__ = 'compra'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    codigo = Column(String(10), nullable=False)
    valor = Column(DECIMAL(18, 2), default=0)
    data = Column(Date, nullable=False)
    revendedor_cpf = Column(String(15), nullable=False, unique=True)
    status = Column(String(32), nullable=False, unique=True)