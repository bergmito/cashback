"""Handlers of Revendedor"""
from flask import jsonify, request
from flask_restful import Resource, Api
from models.revendedor import Revendedor
from session_management import session

class RevendedoresHandler(Resource):

    def post(self):
        """Create a new Revendedor"""
        try:
            params = request.get_json()
            if not self._post_params_is_valid(params):
                return 'Bad request', 400
            revendedor = Revendedor()
            revendedor.email = params['email']
            revendedor.nome = params['nome']
            revendedor.cpf = params['cpf']
            revendedor.senha = params['senha']        
            revendedor.create(session)

            return '', 204
        except Exception as error:
            return str(error), 500

    
    def get(self):
        """List all Revendedores"""
        revendedores = []
        for revendedor in Revendedor.get_all(session):
            revendedores.append(revendedor.__dict__)

        return revendedores

    def _post_params_is_valid(self, params):
        """Check all params is correct"""
        required_params = ['nome', 'email', 'cpf', 'senha']
        for param in required_params:
            if not param in params.keys():
                return False
        return True


class RevendedorLoginHandler(Resource):

    def post(self):
        """Revendedor Login"""
        pass
