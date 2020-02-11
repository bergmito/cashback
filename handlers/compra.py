"""Handlers of Compra"""
from flask_restful import Resource, Api

class CompraHandler(Resource):

    def get(self, compra_id):
        """Get Compra"""
        pass

    def put(self, compra_id):
        """Update Compra"""
        pass

    def delete(self, compra_id):
        """Delete Compra"""
        pass


class ComprasHandler(Resource):

    def post(self):
        """Create a new Compra"""
        pass
