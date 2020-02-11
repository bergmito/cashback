import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.revendedor import Revendedor

class RevendedorModelTest(unittest.TestCase):
    """Revendedor model testing"""

    def setUp(self):
        """Setup test"""
        self._engine = create_engine('mysql+pymysql://root:hinade2019@localhost')
        self._engine.execute('CREATE DATABASE IF NOT EXISTS `{0}`'.format('test'))
        self._engine.execute('USE `test`')
        Revendedor.metadata.create_all(self._engine)
        self.connection = self._engine.connect()
        self.session = sessionmaker(bind=self.connection)()

    def tearDown(self):
        """Tear down test"""
        self.session.commit()
        self._engine.execute('DROP DATABASE IF EXISTS test')

    def test_create(self):
        """Revendedor creation"""
        revendedor = Revendedor()
        revendedor.email = 'felipe@gmail.com'
        revendedor.nome = 'Felipe Bergmans'
        revendedor.cpf = '377.432.218-40'
        revendedor.cidade = 'São Paulo'
        revendedor.senha = '123'
        revendedor.create(self.session)
        revendedores = Revendedor.get_all(self.session)
        self.assertEqual(len(revendedores), 1)
        self.assertEqual(revendedores[0].nome, 'Felipe Bergmans')


    def test_revendedor_get_by_cpf(self):
        """Revendedor by cpf"""
        revendedor1 = Revendedor()
        revendedor1.email = 'joao@gmail.com'
        revendedor1.nome = 'Joao Bergmans'
        revendedor1.cpf = '243.432.218-40'
        revendedor1.senha = '123'
        revendedor1.create(self.session)
        revendedor2 = Revendedor()
        revendedor2.email = 'jose@gmail.com'
        revendedor2.nome = 'Jose Bergmans'
        revendedor2.cpf = '379.153.218-50'
        revendedor2.senha = '123'
        revendedor2.create(self.session)
        revendedor = Revendedor.get_by_cpf(self.session, '379.153.218-50')
        self.assertEqual(revendedor.email, 'jose@gmail.com')
        revendedor = Revendedor.get_by_cpf(self.session, '111.111.111-11')
        self.assertIsNone(revendedor)
    