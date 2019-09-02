from flask import  request
from flask_restful import Resource
import sys
sys.path.insert(0, './api/Models')
from Model import db, Post, PostSchema
from Auth import hasPermissionByToken, getJWTEncode

class PostResource(Resource):
    def get(self, id=None):
        if not id:
            args = request.args
            page = 1
            if (args and args['page']):
                page = int(args['page'])
            post_schema = PostSchema(many=True)
            paginate = Post.query.filter(id==None).paginate(page=page, per_page=1, error_out=False)
            posts = paginate.items
            posts = post_schema.dump(posts)
            if posts:
                return {
                    'data': posts,
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
                    'message': 'Nenhum post encontrado'
                }, 404
        else:
            post_schema = PostSchema()
            post = Post.query.get(id)
            if post:
                post = post_schema.dump(post)
                return post, 200
            return {
                'error': True,
                'code': '101',
                'message': 'Nenhum post encontrado'
            }, 404


    def post(self):
        json_data = request.get_json()
        if json_data:
            try:

                post = Post(
                    json_data['title'],
                    json_data['description'],
                    json_data['content'],
                    json_data['genre'],
                    json_data['status'],
                    json_data['entry_date'],
                    json_data['departure_date'],
                    json_data['image_id'])

                db.session.add(post)
                db.session.commit()
                last_id = post.id
                return {
                    'message': 'Post salvo com sucesso',
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
                'message': 'O campo image não pode ser vazio'
            }, 400
        

    def put(self, id=None):
        json_data = request.get_json()
        if id and json_data:
            post = Post.query.filter_by(id=id).first()
            if post:
                try:
                    post.title = json_data['title']
                    post.description = json_data['description']
                    post.content = json_data['content']
                    post.content = json_data['content']
                    post.genre = json_data['genre']
                    post.entry_date = json_data['entry_date']
                    post.departure_date = json_data['departure_date']
                    post.image_id = json_data['image_id']
                    db.session.commit()
                    return {
                        'message': 'Post editado com sucesso',
                        'id': id
                    }, 200
                except:
                    db.session.rollback()
                    return {
                        'error': True,
                        'code': '103',
                        'message': 'Erro ao tentar editar o post'
                    }, 500
            else:
                return {
                    'error': True,
                    'code': '103',
                    'message': 'Post não encontrado'
                }, 404
        else:
            return {
                'error': True,
                'code': '103',
                'message': 'Identificador do post não enviado'
            }, 400

    def delete(self, id=None):
        if id:
            post = Post.query.filter_by(id=id).first()
            if post:
                try:
                    db.session.delete(post)
                    db.session.commit()
                    return {
                        'message': 'Post deletado com sucesso',
                        'id': id
                    }, 200
                except:
                    db.session.rollback()
                    return {
                        'error': True,
                        'code': '103',
                        'message': 'Erro ao tentar deletar o post'
                    }, 500
            else:
                return {
                    'error': True,
                    'code': '103',
                    'message': 'Post não encontrado'
                }, 404
        else:
            return {
                'error': True,
                'code': '103',
                'message': 'Identificador do post não enviado'
            }, 400
