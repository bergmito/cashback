import os
from flask import Flask, jsonify
from flask_restful import Resource, Api

from handlers.compra import ComprasHandler, CompraHandler
from handlers.revendedor import (RevendedoresHandler,
    RevendedorLoginHandler)

app = Flask(__name__)
api = Api(app)

class App(Resource):
    def get(self):
        return jsonify('API running')

api.add_resource(App, '/')
api.add_resource(RevendedoresHandler, '/revendedores')
api.add_resource(RevendedorLoginHandler, '/revendedor/login')
api.add_resource(ComprasHandler, '/compras')
api.add_resource(CompraHandler, '/compra/<compra_codigo>')

if __name__ == '__main__':
    os.environ['DB_NAME'] = 'cashback'
    app.run()