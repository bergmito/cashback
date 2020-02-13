import os
import unittest

from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.revendedor import Revendedor
from models.compra import Compra
from utils import float_to_decimal


class MainModelTest(unittest.TestCase):
    """Main Test"""

    def setUp(self):
        """Setup test"""
        self._engine = create_engine('mysql+pymysql://root:hinade2019@localhost')
        self._engine.execute('CREATE DATABASE IF NOT EXISTS `test`')
        self._engine.execute('USE `test`')
        Revendedor.metadata.create_all(self._engine)
        self.connection = self._engine.connect()
        self.session = sessionmaker(bind=self.connection)()

    def tearDown(self):
        """Tear down test"""
        self.session.commit()
        self._engine.execute(
            'DROP DATABASE IF EXISTS `test`')


class CompraModelTest(MainModelTest):
    """Compra model testing"""

    def test_create(self):
        """Compra creation"""
        compra = Compra()
        compra.codigo = 'AAA-1000'
        compra.valor = 2000.00
        compra.data = date(2020, 2, 11)
        compra.revendedor_cpf = '377.432.218-40'
        compra.create(self.session)
        self.assertEqual(compra.cashback_percentual, float(20))
        self.assertEqual(compra.cashback_valor, 400)
        self.assertEqual(compra.status, 'Em validação')
        compra = Compra()
        compra.codigo = 'AAA-1001'
        compra.valor = float_to_decimal(1340.50)
        compra.data = date(2020, 2, 11)
        compra.revendedor_cpf = '153.509.460-56'
        compra.create(self.session)
        self.assertEqual(compra.cashback_percentual, float(15))
        self.assertEqual(compra.cashback_valor, float_to_decimal(201.07))
        self.assertEqual(compra.status, 'Aprovado')        


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
    