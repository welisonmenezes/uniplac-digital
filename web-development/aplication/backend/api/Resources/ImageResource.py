from flask import  request
from flask_restful import Resource
import sys
import base64
import re
sys.path.insert(0, './api/Utils')
sys.path.insert(0, './api/Models')
from Model import db, Image, ImageSchema
from Auth import hasPermissionByToken, getJWTEncode
from Utils import getBase64Size

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
            if (int(getBase64Size(json_data['image'])) <= int(5017969)):
                baseType = re.search('data:image/(.+?);base64,', json_data['image'])
                if (baseType and ( baseType.group(1) == 'png' or
                                    baseType.group(1) == 'jpg' or
                                    baseType.group(1) == 'jpeg' or
                                    baseType.group(1) == 'gif') ):
                    try:
                        image = Image(json_data['image'])
                        db.session.add(image)
                        db.session.commit()
                        last_id = image.id
                        return {
                            'message': 'Imagem salva com sucesso',
                            'id': last_id
                        }, 200
                    except:
                        return {
                            'error': True,
                            'code': '101',
                            'message': 'Error ao conectar como banco de dados'
                        }, 501
                else:
                    return {
                        'error': True,
                        'code': '104',
                        'message': 'Tipo de arquivo inválido'
                    }, 400
            else:
                return {
                        'error': True,
                        'code': '102',
                        'message': 'O tamanho da imagem não deve exceder 5mb'
                    }, 400
        else:
            return {
                        'error': True,
                        'code': '103',
                        'message': 'O campo image não pode ser vazio'
                    }, 400
        

    def put(self, id=None):
        json_data = request.get_json()
        if id and json_data:
            image = Image.query.filter_by(id=id).first()
            if image:
                try:
                    image.image = json_data['image']
                    db.session.commit()
                    return {'image': 'editado com sucesso'}, 200
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

