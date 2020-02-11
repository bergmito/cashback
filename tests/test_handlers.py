"""Test app"""
import unittest
import os
from main import app
from models.revendedor import Revendedor
from session_management import DBSessionManagement

class MainTest(unittest.TestCase):
    """Main test"""

    def setUp(self):
        """Setup Test"""
        os.environ['DB_NAME'] = 'testdb'
        app.config['TESTING'] = True
        self.session_manager = DBSessionManagement()
        self.session_manager.generate_db()        
        self.client = app.test_client

    def tearDown(self):
        """Tear down Test"""
        self.session_manager.drop_db()

    def test_app_running(self):
        """Test app is running"""
        response = self.client().get('/')
        self.assertEqual(response.json, 'API running')


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

    def _create_revendedor(self):
        """Create revendedor for test"""
        revendedor = Revendedor()
        revendedor.nome = 'Felipe Silva'
        revendedor.cpf = '856.456.789-32'
        revendedor.cidade = 'São Paulo'
        revendedor.email = 'f@test.com'
        revendedor.senha = '5555'
        session = self.session_manager.get_db_session()
        revendedor.create(session)
