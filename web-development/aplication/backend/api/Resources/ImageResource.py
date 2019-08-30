from flask import current_app, Blueprint, request
from flask_restful import Resource, Api
import sys
sys.path.insert(0, './api/Utils')
from Auth import hasPermissionByToken, getJWTEncode

encoded_jwt = getJWTEncode()
class ImageResource(Resource):
    #@hasPermissionByToken(encoded_jwt)
    def get(self):
        return {'image': 'get'}

    def post(self):
        return {'image': 'post'}

    def put(self):
        return {'image': 'put'}

    def delete(self):
        return {'image': 'delete'}

