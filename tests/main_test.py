"""Test app"""
from main import app


def test_app_main():
    """Test index app response"""
    with app.test_client() as c:
        response = c.get('/')
        response_json = response.get_json()

        assert 'Desafio Cashback' == response_json

