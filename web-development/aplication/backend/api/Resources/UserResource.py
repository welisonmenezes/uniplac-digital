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

class UserResource(Resource):
    @hasPermissionByToken(['admin'], True)
    def get(self, id=None):
        if not id:
            args = request.args
            page = 1
            if (args and args['page']):
                page = int(args['page'])
            user_schema = UserSchema(many=True)
            paginate = User.query.filter(id==None).paginate(page=page, per_page=10, error_out=False)
            users = paginate.items
            users = user_schema.dump(users)
            if users:
                return {
                    'data': users,
                    'pagination': {
                        'next_num': paginate.next_num,
                        'prev_num': paginate.prev_num,
                        'total': paginate.total
                    }
                }, 200
            else:
                return {
                    'error': True,
                    'code': '101',
                    'message': 'Nenhum usuário encontrado'
                }, 404
        else:
            user_schema = UserSchema()
            user = User.query.get(id)
            if user:
                user = user_schema.dump(user)
                return user, 200
            return {
                'error': True,
                'code': '101',
                'message': 'Nenhum usuário encontrado'
            }, 404

    @hasPermissionByToken(['admin'], False)
    def post(self):
        json_data = request.get_json()
        if json_data:
            # validate the fields
            userValidator = UserValidation(json_data)
            if userValidator.isValid(None, Image) == True:
                try:
                    user = User(
                        json_data['first_name'],
                        json_data['last_name'],
                        json_data['registry'],
                        bcrypt.generate_password_hash(json_data['password']),
                        json_data['role'],
                        json_data['email'],
                        json_data['phone'],
                        None)
                    if json_data['image_id'] != '':
                        user.image_id = json_data['image_id']
                    db.session.add(user)
                    db.session.commit()
                    last_id = user.id
                    return {
                        'message': 'Usuário salvo com sucesso',
                        'id': last_id
                    }, 200
                except:
                    db.session.rollback()
                    return {
                        'error': True,
                        'code': '101',
                        'message': 'Error ao conectar como banco de dados'
                    }, 501
            else:
                return userValidator.response
        else:
            return {
                'error': True,
                'code': '103',
                'message': 'Dados não enviados'
            }, 400


    @hasPermissionByToken(['admin'], True)
    @mustHaveId
    def put(self, id=None):
        json_data = request.get_json()
        if json_data:
            user = User.query.filter_by(id=id).first()
            if user:
                # validate the fields
                userValidator = UserValidation(json_data)
                if userValidator.isValid(user, Image) == True:
                    try:
                        user.first_name = json_data['first_name']
                        user.last_name = json_data['last_name']
                        user.registry = json_data['registry']
                        user.role = json_data['role']
                        user.email = json_data['email']
                        user.phone = json_data['phone']

                        if json_data['image_id'] != '':
                            user.image_id = json_data['image_id']

                        if json_data['password'] != '':
                            pw_hash = bcrypt.generate_password_hash(json_data['password'])
                            user.password = pw_hash

                        db.session.commit()
                        return {
                            'message': 'Usuário editado com sucesso',
                            'id': id
                        }, 200
                    except:
                        db.session.rollback()
                        return {
                            'error': True,
                            'code': '103',
                            'message': 'Erro ao tentar editar o usuário'
                        }, 500
                else:
                    return userValidator.response
            else:
                return {
                    'error': True,
                    'code': '103',
                    'message': 'Usuário não encontrado'
                }, 404
        else:
            return {
                'error': True,
                'code': '103',
                'message': 'Dados não enviados'
            }, 400


    @hasPermissionByToken(['admin'], False)
    @mustHaveId
    def delete(self, id=None):
        user = User.query.filter_by(id=id).first()
        if user:
            try:
                db.session.delete(user)
                db.session.commit()
                return {
                    'message': 'Usuário deletado com sucesso',
                    'id': id
                }, 200
            except:
                db.session.rollback()
                return {
                    'error': True,
                    'code': '103',
                    'message': 'Erro ao tentar deletar o usuário'
                }, 500
        else:
            return {
                'error': True,
                'code': '103',
                'message': 'Usuário não encontrado'
            }, 404

