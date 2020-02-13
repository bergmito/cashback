import os
import unittest

from datetime import date
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from session_management import DBSessionManagement
from models.revendedor import Revendedor
from models.compra import Compra
from utils import float_to_decimal


class MainModelTest(unittest.TestCase):
    """Main Test"""

    def setUp(self):
        """Setup test"""
        os.environ['DB_NAME'] = 'testdb'
        self.session_manager = DBSessionManagement()
        self.session_manager.generate_db()
        self.session = self.session_manager.get_db_session()

    def tearDown(self):
        """Tear down test"""
        self.session.commit()
        self.session_manager.drop_db()


class CompraModelTest(MainModelTest):
    """Compra model testing"""

    def test_create(self):
        """Compra creation"""
        compra = Compra()
        compra.codigo = 'AAA-1000'
        compra.valor = 2000.00
        compra.data = date(2020, 2, 11)
        compra.revendedor_cpf = '377.432.218-40'
        compra.put(self.session)
        self.assertEqual(compra.cashback_percentual, float(20))
        self.assertEqual(compra.cashback_valor, 400)
        self.assertEqual(compra.status, 'Em validação')
        compra = Compra()
        compra.codigo = 'AAA-1001'
        compra.valor = float_to_decimal(1340.50)
        compra.data = date(2020, 2, 11)
        compra.revendedor_cpf = '153.509.460-56'
        compra.put(self.session)
        self.assertEqual(compra.cashback_percentual, float(15))
        self.assertEqual(compra.cashback_valor, float_to_decimal(201.07))
        self.assertEqual(compra.status, 'Aprovado')

    def test_get_by_codigo(self):
        """Compra by codigo"""
        compra1 = Compra()
        compra1.codigo = 'AAA-1000'
        compra1.valor = 2000.00
        compra1.data = date(2020, 2, 11)
        compra1.revendedor_cpf = '377.432.218-40'
        compra1.put(self.session)
        compra2 = Compra()
        compra2.codigo = 'AAA-1001'
        compra2.valor = 2055.13
        compra2.data = date(2020, 3, 11)
        compra2.revendedor_cpf = '377.432.218-40'
        compra2.put(self.session)
        compra = Compra.get_by_codigo(self.session, 'AAA-1001')
        self.assertEqual(float(compra.valor), 2055.13)

    def test_delete(self):
        """Delete Compra"""
        compra = Compra()
        compra.codigo = 'AAA-1000'
        compra.valor = 2000.00
        compra.data = date(2020, 2, 11)
        compra.revendedor_cpf = '377.432.218-40'
        compra.put(self.session)
        self.assertEqual(len(Compra.get_all(self.session)), 1)
        compra.delete(self.session)
        self.assertEqual(len(Compra.get_all(self.session)), 0)


class RevendedorModelTest(MainModelTest):
    """Revendedor model testing"""

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


    def test_revendedor_get_by_email(self):
        """Revendedor by email"""
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
        revendedor = Revendedor.get_by_email(self.session, 'joao@gmail.com')
        self.assertEqual(revendedor.nome, 'Joao Bergmans')
        revendedor = Revendedor.get_by_email(self.session, 'felipe@test.com')
        self.assertIsNone(revendedor)
    