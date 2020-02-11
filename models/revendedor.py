"""Model Revendedor"""
from sqlalchemy import Column, String, BigInteger
from models.base import MYSQL_BASE

class Revendedor(MYSQL_BASE):
    """Class for revendedores"""
    __tablename__ = 'revendedor'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nome = Column(String(128), nullable=False)
    cpf = Column(String(15), nullable=False, unique=True)
    email = Column(String(128), nullable=False, unique=True)
    senha = Column(String(128), nullable=False)

    def create(self, session):
        """Create new Revendedor"""        
        session.add(self)
        session.commit()

    @classmethod
    def get_all(cls, session):
        """List all Revendedores"""
        return session.query(cls).all()

    @classmethod
    def get_by_cpf(cls, session, cpf):
        """Get revendedor by cpf"""
        return session.query(cls).filter(
            cls.cpf == cpf).first()
