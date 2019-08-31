from flask import request
from flask_restful import Resource
import sys
sys.path.insert(0, './api/Utils')
from Auth import hasPermissionByToken, getJWTEncode

encoded_jwt = getJWTEncode()
class UserResource(Resource):
    @hasPermissionByToken(encoded_jwt)
    def get(self):
        return {'user': 'get'}

    def post(self):
        return {'user': 'post'}

    def put(self):
        return {'user': 'put'}

    def delete(self):
        return {'user': 'delete'}

