"""Handlers of Revendedor"""
import requests
from flask import jsonify, request
from flask_restful import Resource
from models.revendedor import Revendedor
from session_management import DBSessionManagement
from utils import post_params_is_valid

class RevendedoresHandler(Resource):

    def post(self):
        """Create a new Revendedor"""
        session = DBSessionManagement().get_db_session()
        try:
            params = request.get_json()
            required_params = ['nome', 'email', 'cpf', 'senha']
            if not post_params_is_valid(params, required_params):
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
            if not post_params_is_valid(params, ['email', 'senha']):
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


class RevendedorCashbackHandler(Resource):

    def get(self, revendedor_cpf):
        """Get cashback amount of Revendedor"""
        try:
            EXTERNAL_URL_CASHBACK = (
                'https://mdaqk8ek5j.execute-api.us-east-1.amazonaws.com'
                '/v1/cashback?cpf={revendedor_cpf}'.format(
                    revendedor_cpf=revendedor_cpf))
            TOKEN = 'ZXPURQOARHiMc6Y0flhRC1LVlZQVFRnm'
            response = requests.get(
                EXTERNAL_URL_CASHBACK, headers={'token': TOKEN})
            if response.status_code == 200:
                return response.json()["body"]['credit']
            else:
                return ('Cashback API is down. '
                        'Please try again in a few minutes.'), 500
        except Exception:
            return ('Sorry, occur error. '
                    'Please try again in a few minutes.'), 500
        
