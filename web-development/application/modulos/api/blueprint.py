from flask import current_app, Blueprint
from flask_restful import Api
from flask_cors import CORS

# inicializa a blueprint api
apiBP = Blueprint('api', __name__, url_prefix='/api')
cors = CORS(apiBP, resources={r"/api/*": {"origins": "*"}})
api = Api(apiBP)

# import e registra os recursos da api
from modulos.api.Resources import *
api.add_resource(MediaResource, '/media/<id>')
api.add_resource(ImageByIdResource,'/image/<int:id>')
api.add_resource(ImageResource, '/image', '/image/<int:id>')