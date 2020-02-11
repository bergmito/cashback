"""Test app"""
import unittest
from main import app

class MainTest(unittest.TestCase):
    """Main test"""

    def setUp(self):
        """Setup Test"""
        app.config['TESTING'] = True
        self.client = app.test_client

    def test_app_running(self):
        """Test app is running"""
        response = self.client().get('/')
        self.assertEqual(response.json, 'API running')
            
