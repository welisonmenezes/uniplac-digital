from flask import current_app, Blueprint
from flask_restful import Api
from flask_cors import CORS

# initialize the api blueprint
apiBP = Blueprint('api', __name__, url_prefix='/api')
cors = CORS(apiBP, resources={r"/api/*": {"origins": "*"}})
api = Api(apiBP)

# import the resources
from modulos.api.Resources import MediaResource, ImageByIdResource, ImageResource

# register the resources
api.add_resource(MediaResource, '/media/<int:id>')
api.add_resource(ImageByIdResource,'/image/<int:id>')
api.add_resource(ImageResource, '/image', '/image/<int:id>')