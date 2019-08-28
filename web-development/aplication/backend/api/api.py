from flask import current_app, Blueprint, request
from flask_restful import Resource, Api
import jwt

# add custom path for imports
import sys
sys.path.insert(0, './api/Resources')

# initialize the api blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

# import the resources
from UserResource import UserResource

# register the resources
api.add_resource(UserResource, '/user')