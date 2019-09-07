from flask import request
from flask_restful import Resource
from flask_bcrypt import Bcrypt
import sys
sys.path.insert(0, './api/Utils')
sys.path.insert(0, './api/Models')
sys.path.insert(0, './api/Validations')
from Auth import hasPermissionByToken, getJWTEncode
from Model import db, User, UserSchema, Image
from MustHaveId import mustHaveId
from UserValidations import UserValidation
bcrypt = Bcrypt()

class AuthResource(Resource):
    def post(self):
        json_data = request.get_json()
        if json_data:
            user_schema = UserSchema()
            user = User.query.filter_by(registry=json_data['registry']).first()
            if user:
                if bcrypt.check_password_hash(user.password, json_data['password']):
                    token = getJWTEncode(user).decode('utf-8')
                    return {
                        'token': token
                    }
                else:
                    return {
                        'error': True,
                        'code': '101',
                        'message': 'Senha inválida'
                    }, 501
            else:
                return {
                    'error': True,
                    'code': '101',
                    'message': 'O usuário informado não existe na base de dados'
                }, 501 
        else:
            return {
                'error': True,
                'code': '103',
                'message': 'Dados não enviados'
            }, 400

