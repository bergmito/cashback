"""Handlers of Compra"""
from flask_restful import Resource, request
from models.compra import Compra
from session_management import DBSessionManagement
from utils import post_params_is_valid, str_date_to_date, set_value_if_exist

class CompraHandler(Resource):

    def put(self, compra_codigo):
        """Update Compra"""
        session = DBSessionManagement().get_db_session()
        try:
            params = request.get_json()
            compra = Compra.get_by_codigo(session, compra_codigo)
            if not compra:
                session.rollback()
                return 'Compra not found', 404
            if compra.status != 'Em validação':
                session.rollback()
                return 'Compra locked to update', 423
            set_value_if_exist(params, 'codigo', compra)
            set_value_if_exist(params, 'valor', compra)
            set_value_if_exist(params, 'revendedor_cpf', compra)
            if 'data' in params:
                compra.data = str_date_to_date(params['data'])
            compra.put(session)

            return '', 204
        except Exception as error:
            session.rollback()
            return str(error), 500

    def delete(self, compra_codigo):
        """Delete Compra"""
        pass


class ComprasHandler(Resource):

    def post(self):
        """Create a new Compra"""
        session = DBSessionManagement().get_db_session()
        try:
            params = request.get_json()
            required_params = ['codigo', 'valor', 'data', 'revendedor_cpf']
            if not post_params_is_valid(params, required_params):
                return 'Bad request', 400
            compra = Compra()
            compra.codigo = params['codigo']
            compra.valor = params['valor']
            compra.data = str_date_to_date(params['data']).date()
            compra.revendedor_cpf = params['revendedor_cpf']
            compra.put(session)

            return '', 204
        except Exception as error:
            session.rollback()
            return str(error), 500

    def get(self):
        """Get all Compras"""
        session = DBSessionManagement().get_db_session()
        try:
            compras = []
            for compra in Compra.get_all(session):
                compras.append(compra.to_json())
            session.commit()

            return compras
        except Exception as error:
            session.rollback()
            return str(error), 500
