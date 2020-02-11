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
    cidade = Column(String(128), nullable=True)

    def create(self, session):
        """Create new Revendedor"""
        session.add(self)
        session.commit()

    def to_json(self):
        """Convert db entry instance to json"""
        return {
            "email": self.email,
            "nome": self.nome,
            "cpf": self.cpf,
            "cidade": self.cidade,
            "senha": self.senha
        }

    @classmethod
    def get_all(cls, session):
        """List all Revendedores"""
        return session.query(cls).all()

    @classmethod
    def get_by_email(cls, session, email):
        """Get revendedor by email"""
        return session.query(cls).filter(
            cls.email == email).first()
