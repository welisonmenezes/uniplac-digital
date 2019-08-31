from flask import current_app, Blueprint, request, jsonify
from flask_restful import Resource, Api
import sys
sys.path.insert(0, './api/Utils')
sys.path.insert(0, './api/Models')
from ImageModel import db, Image, ImageSchema
from Auth import hasPermissionByToken, getJWTEncode

encoded_jwt = getJWTEncode()
class ImageResource(Resource):
    #@hasPermissionByToken(encoded_jwt)
    def get(self, id=None):
        if not id:
            images_schema = ImageSchema(many=True)
            images = Image.query.all()
            images = images_schema.dump(images)
            return images, 200
        else:
            image_schema = ImageSchema()
            image = Image.query.get(id)
            if image:
                image = image_schema.dump(image)
                return image, 200
            return {'error': 'no image'}, 404


    def post(self):
        json_data = request.get_json()
        if json_data:
            try:
                image = Image(json_data['image'])
                db.session.add(image)
                db.session.commit()
                last_id = image.id
                return {
                    'message': 'Salvo com sucess',
                    'id': last_id
                }
            except:
                return {'image': 'erro ao salvar'}
        else:
            return {'image': 'dados vazios'}
        

    def put(self, id=None):
        json_data = request.get_json()
        if id and json_data:
            image = Image.query.filter_by(id=id).first()
            if image:
                try:
                    image.image = json_data['image']
                    db.session.commit()
                    return {'image': 'editado com sucesso'}
                except:
                    return {'image': 'erro ao editar'}
            else:
               return {'image': 'imagem não encontrada'} 
        else:
            return {'image': 'requisição errada'}

    @hasPermissionByToken(encoded_jwt)
    def delete(self, id=None):
        if id:
            image = Image.query.filter_by(id=id).first()
            if image:
                try:
                    db.session.delete(image)
                    db.session.commit()
                    return {'image': 'deletada com sucesso'}
                except:
                    return {'image': 'erro ao deletar'}
            else:
                return {'image': 'imagem não encontrada'} 
        else:
            return {'image': 'requisição errada'}
        return {'image': 'delete'}

