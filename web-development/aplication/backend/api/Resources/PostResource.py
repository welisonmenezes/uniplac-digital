from flask import  request
from flask_restful import Resource

from api.Model import db, Post, PostSchema

from api.Validations.Auth import hasPermissionByToken, getJWTEncode
from api.Validations.MustHaveId import mustHaveId

class PostResource(Resource):
    def get(self, id=None):
        if not id:
            args = request.args
            page = 1
            if (args and args['page']):
                page = int(args['page'])
            post_schema = PostSchema(many=True)
            paginate = Post.query.filter(id==None).paginate(page=page, per_page=10, error_out=False)
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
                    json_data['image_id'],
                    json_data['user_id'],
                    None)

                if json_data.get('category_id'):
                    try:
                        cat_id = int(json_data['category_id'])
                        if (cat_id):
                            post.category_id = cat_id
                    except:
                        return {
                            'error': True,
                            'code': '101',
                            'message': 'O Id da categoria deve ser um número.'
                        }, 501 

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
        

    @mustHaveId
    def put(self, id=None):
        json_data = request.get_json()
        if json_data:
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
                    post.user_id = json_data['user_id']
                    post.category_id = None

                    if json_data.get('category_id'):
                        try:
                            cat_id = int(json_data['category_id'])
                            if (cat_id):
                                post.category_id = cat_id
                        except:
                            return {
                                'error': True,
                                'code': '101',
                                'message': 'O Id da categoria deve ser um número.'
                            }, 501 


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
                'message': 'Dados não enviados'
            }, 400


    @mustHaveId
    def delete(self, id=None):
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
