"""Handlers of Revendedor"""
from flask import jsonify
from flask_restful import Resource, Api
from models.revendedor import Revendedor
from session_management import session

class RevendedoresHandler(Resource):

    def post(self):
        """Create a new Revendedor"""
        # revendedor = Revendedor()
        # revendedor.email = 'felipe@felipe.com'
        # revendedor.nome = 'Felipe Bergmans'
        # revendedor.put()    
    
    def get(self):
        """List all Revendedores"""
        revendedores = []
        for revendedor in Revendedor.get_all(session):
            revendedores.append(revendedor.__dict__)

        return revendedores


class RevendedorLoginHandler(Resource):

    def post(self):
        """Revendedor Login"""
        pass
