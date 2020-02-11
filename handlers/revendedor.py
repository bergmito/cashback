"""Handlers of Revendedor"""
from flask import jsonify, request
from flask_restful import Resource, Api
from models.revendedor import Revendedor
from session_management import DBSessionManagement

class RevendedoresHandler(Resource):

    def post(self):
        """Create a new Revendedor"""
        session = DBSessionManagement().get_db_session()
        try:
            params = request.get_json()
            required_params = ['nome', 'email', 'cpf', 'senha']
            if not _post_params_is_valid(params, required_params):
                return 'Bad request', 400
            revendedor = Revendedor()
            revendedor.email = params['email']
            revendedor.nome = params['nome']
            revendedor.cpf = params['cpf']
            revendedor.senha = params['senha']        
            revendedor.create(session)

            return '', 204
        except Exception as error:
            session.rollback()
            return str(error), 500
    
    def get(self):
        """List all Revendedores"""
        session = DBSessionManagement().get_db_session()
        try:
            revendedores = []
            for revendedor in Revendedor.get_all(session):
                revendedores.append(revendedor.to_json())
            session.commit()

            return revendedores
        except Exception as error:
            session.rollback()
            return str(error), 500


class RevendedorLoginHandler(Resource):

    def post(self):
        """Revendedor Login"""
        session = DBSessionManagement().get_db_session()
        try:
            params = request.get_json()         
            if not _post_params_is_valid(params, ['email', 'senha']):
                return 'Bad request', 400        
            revendedor = Revendedor.get_by_email(session, params['email'])
            password_is_correct = (revendedor.senha == params['senha'])
            session.commit()
            if password_is_correct:
                return 'Authorized', 200
            else:
                return 'Not authorized', 401
        except Exception as error:
            return str(error), 500


def _post_params_is_valid(params, required_params):
    """Check all params is correct"""
    for param in required_params:
        if not param in params.keys():
            return False
    return True