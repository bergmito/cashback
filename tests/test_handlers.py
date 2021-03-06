"""Test app"""
import os
import json
import unittest

from unittest.mock import patch, Mock
from main import app
from models.revendedor import Revendedor
from models.compra import Compra
from session_management import DBSessionManagement
from utils import str_date_to_date

class MainTest(unittest.TestCase):
    """Main test"""

    def setUp(self):
        """Setup Test"""
        os.environ['DB_NAME'] = 'testdb'
        app.config['TESTING'] = True
        self.session_manager = DBSessionManagement()
        self.session_manager.generate_db()
        self.session = self.session_manager.get_db_session()
        self.client = app.test_client

    def tearDown(self):
        """Tear down Test"""
        self.session_manager.drop_db()

    def test_app_running(self):
        """Test app is running"""
        response = self.client().get('/')
        self.assertEqual(response.json, 'API running')


class CompraHandlerTest(MainTest):
    """Compra Test"""

    def test_post(self):
        """Create new Compra"""
        json_body = {
            "codigo": "FFF-1000",
            "valor": 1000,
            "data": '2020-02-20',
            "revendedor_cpf": "377.432.218-40"
        }
        response = self.client().post('/compras', json=json_body)
        self.assertEqual(response.status, '204 NO CONTENT')
        compras = Compra.get_all(self.session)
        self.assertGreater(len(compras), 0)
        self.assertEqual(compras[0].codigo, 'FFF-1000')
        self.session.commit()

    def test_get_all(self):
        """Get all compras"""
        self._create_compra('677.478.111-78', 'FBS-1002')
        response = self.client().get('/compras')
        compras = response.json
        self.assertEqual(len(compras), 1)

    def test_update(self):
        """Compra update"""
        self._create_compra('677.478.111-78', 'FBS-1002')
        json_body = {
            "codigo": "FBI-1002",
            "valor": 1050,
            "data": '2020-02-20',
            "revendedor_cpf": "377.432.218-40"
        }
        response = self.client().put('/compra/{compra_codigo}'.format(
            compra_codigo='FBS-1002'), json=json_body)
        self.assertEqual(response.status, '204 NO CONTENT')
        self._create_compra('153.509.460-56', 'FBS-1014')
        response = self.client().put('/compra/{compra_codigo}'.format(
            compra_codigo='FBS-1002'), json=json_body)
        self.assertEqual(response.status, '404 NOT FOUND')
        response = self.client().put('/compra/{compra_codigo}'.format(
            compra_codigo='FBS-1014'), json=json_body)        
        self.assertEqual(response.status, '423 LOCKED')

    def test_delete(self):
        """Compra delete"""
        self._create_compra('456.213.789-88', 'AAA-4444')
        compras = Compra.get_all(self.session)
        self.session.commit()
        self.assertEqual(len(compras), 1)
        response = self.client().delete('/compra/{compra_codigo}'.format(
            compra_codigo='AAA-4444'))
        self.assertEqual(response.status, '204 NO CONTENT')
        compras = Compra.get_all(self.session)
        self.session.commit()
        self.assertEqual(len(compras), 0)
        response = self.client().delete('/compra/{compra_codigo}'.format(
            compra_codigo='AAA-0000'))
        self.assertEqual(response.status, '404 NOT FOUND')
        self._create_compra('153.509.460-56', 'FBS-1014')
        response = self.client().delete('/compra/{compra_codigo}'.format(
            compra_codigo='FBS-1014'))
        self.assertEqual(response.status, '423 LOCKED')

    
    def _create_compra(self, revendedor_cpf, codigo):
        """Create Compra for test"""
        compra = Compra()
        compra.codigo = codigo
        compra.valor = 1600
        compra.data = str_date_to_date('2020-02-10')
        compra.revendedor_cpf = revendedor_cpf
        compra.put(self.session)                


class RevendedorHandlerTest(MainTest):
    """Revendedor Test"""

    def test_post(self):
        """Create new Revendedor"""
        json_body = {
            "nome": "Felipe",
            "email": "felipe@gmail.com",
            "cpf": "377.432.218-40",
            "senha": "123"
        }
        response = self.client().post('/revendedores', json=json_body)
        self.assertEqual(response.status, '204 NO CONTENT')
    
    def test_get(self):
        """Get all revendedores"""
        self._create_revendedor()
        response = self.client().get('/revendedores')
        revendedores = response.json
        self.assertEqual(len(revendedores), 1)

    def test_login(self):
        """Revendedor login"""
        self._create_revendedor()
        json_body = {
            "email": "f@test.com",
        }
        response = self.client().post('/revendedor/login', json=json_body)
        self.assertEqual(response.status, '400 BAD REQUEST')
        json_body['senha'] = "5555"
        response = self.client().post('/revendedor/login', json=json_body)
        self.assertEqual(response.json, 'Authorized')

    def test_cashback_amount(self):
        """Cashback amount"""
        with patch('requests.get') as mock_request:
            mock_resp = Mock()
            mock_resp.status_code = 200
            mock_resp.json = Mock(return_value={
                "body": {
                    "statusCode": 200,
                    "credit": 1000
                }
            })
            mock_request.return_value = mock_resp
            response = self.client().get('/revendedor/2222/cashback')
            self.assertEqual(response.json, 1000)

    def _create_revendedor(self):
        """Create Revendedor for test"""
        revendedor = Revendedor()
        revendedor.nome = 'Felipe Silva'
        revendedor.cpf = '856.456.789-32'
        revendedor.cidade = 'São Paulo'
        revendedor.email = 'f@test.com'
        revendedor.senha = '5555'
        session = self.session_manager.get_db_session()
        revendedor.create(session)
