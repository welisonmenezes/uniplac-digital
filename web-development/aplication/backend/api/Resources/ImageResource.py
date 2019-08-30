from flask import current_app, Blueprint, request
from flask_restful import Resource, Api
import sys
sys.path.insert(0, './api/Utils')
sys.path.insert(0, './api/Models')
from ImageModel import db, Image
from Auth import hasPermissionByToken, getJWTEncode

encoded_jwt = getJWTEncode()
class ImageResource(Resource):
    #@hasPermissionByToken(encoded_jwt)
    def get(self):
        img = Image('img-here')
        db.session.add(img)
        db.session.commit()
        return {'image': 'get'}

    def post(self):
        return {'image': 'post'}

    def put(self):
        return {'image': 'put'}

    def delete(self):
        return {'image': 'delete'}

