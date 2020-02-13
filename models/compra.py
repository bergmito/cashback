"""Model Compra"""
from sqlalchemy import (Column, String, BigInteger, DECIMAL,
    Date, Float)
from models.base import MYSQL_BASE
from utils import float_to_decimal

class Compra(MYSQL_BASE):
    """Class for Compra"""
    __tablename__ = 'compra'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    codigo = Column(String(10), nullable=False, unique=True)
    valor = Column(DECIMAL(18, 2), default=0)
    data = Column(Date, nullable=False)
    revendedor_cpf = Column(String(15), nullable=False)
    status = Column(String(32), nullable=False)
    cashback_valor = Column(DECIMAL(18, 2), nullable=False, default=0)
    cashback_percentual = Column(Float, nullable=False, default=0)

    def create(self, session):
        """Create a new Compra"""
        self._set_status()
        self._set_cashback()
        session.add(self)
        session.commit()   

    def _set_cashback(self):
        """Set cashback values"""
        self.cashback_percentual = self._get_cashback_percent(self.valor)
        self.cashback_valor = float_to_decimal(
            float(self.valor) * (self.cashback_percentual / 100))

    def _set_status(self):
        """Set status for Compra"""
        if self.revendedor_cpf == '153.509.460-56':
            self.status = 'Aprovado'
        else:
            self.status = 'Em validação'

    @staticmethod
    def _get_cashback_percent(compra_valor):
        """Get percent of cashback by compra_valor"""
        if compra_valor < 1000:
            return float(10)
        elif (compra_valor >= 1000) and (compra_valor <= 1500):
            return float(15)
        elif compra_valor > 1500:
            return float(20)
