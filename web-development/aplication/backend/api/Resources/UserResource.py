from flask import request
from flask_restful import Resource
import sys
sys.path.insert(0, './api/Utils')
sys.path.insert(0, './api/Models')
from Auth import hasPermissionByToken, getJWTEncode
from Model import db, User, UserSchema
from MustHaveId import mustHaveId

encoded_jwt = getJWTEncode()
class UserResource(Resource):
    @hasPermissionByToken(encoded_jwt)
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

    def post(self):
        json_data = request.get_json()
        if json_data:
            try:

                user = User(
                    json_data['first_name'],
                    json_data['last_name'],
                    json_data['registry'],
                    json_data['password'],
                    json_data['role'],
                    json_data['email'],
                    json_data['phone'],
                    None)

                if json_data.get('image_id'):
                    try:
                        image_id = int(json_data['image_id'])
                        if (image_id):
                            user.image_id = image_id
                    except:
                        return {
                            'error': True,
                            'code': '101',
                            'message': 'O Id da imagem deve ser um número.'
                        }, 501 

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
            return {
                'error': True,
                'code': '103',
                'message': 'Dados não enviados'
            }, 400


    @mustHaveId
    def put(self, id=None):
        json_data = request.get_json()
        if json_data:
            user = User.query.filter_by(id=id).first()
            if user:
                try:
                    user.first_name = json_data['first_name']
                    user.last_name = json_data['last_name']
                    user.registry = json_data['registry']
                    user.password = json_data['password']
                    user.role = json_data['role']
                    user.email = json_data['email']
                    user.phone = json_data['phone']
                    user.image_id = None

                    if json_data.get('image_id'):
                        try:
                            image_id = int(json_data['image_id'])
                            if (image_id):
                                user.image_id = image_id
                        except:
                            return {
                                'error': True,
                                'code': '101',
                                'message': 'O Id da imagem deve ser um número.'
                            }, 501 


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

