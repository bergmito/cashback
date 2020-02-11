"""Test app"""
import unittest
from main import app
from session_management import engine

class MainTest(unittest.TestCase):
    """Main test"""

    def setUp(self):
        """Setup Test"""
        app.config['TESTING'] = True
        self.client = app.test_client

    def tearDown(self):
        """Tear down Test"""
        engine.execute('DROP DATABASE IF EXISTS `test`')

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
            
