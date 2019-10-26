from flask import  request, session
from app import app
from flask_restful import Resource
from database.Model import db, Image, ImageSchema, User, Post, Configuration, ConfigurationImage
from modulos.api.Validations.MustHaveId import mustHaveId
from modulos.api.Validations.ImageValidations import ImageValidation

class ImageResource(Resource):
    def get(self, id=None):
        if not session.get('user_id', None):
            return {'message': 'Sem permissão para acessar este recurso'}, 401
        args = request.args
        page = 1
        if (args and args['page']):
            page = int(args['page'])
        images_schema = ImageSchema(many=True)
        paginate = Image.query.filter(id==None).paginate(page=page, per_page=10, error_out=False)
        images = paginate.items
        images = images_schema.dump(images)

        pages = []
        for p in paginate.iter_pages(left_edge=2, left_current=2, right_current=3, right_edge=2):
            pages.append(p)

        if images:
            return {
                'data': images,
                'pagination': {
                    'next_num': paginate.next_num,
                    'prev_num': paginate.prev_num,
                    'total': paginate.total,
                    'pages': pages
                }
            }, 200
        else:
            return {'message': 'Nenhuma imagem encontrada'}, 404


    def post(self):
        if not session.get('user_id', None):
            return {'message': 'Sem permissão para acessar este recurso'}, 401
        json_data = request.get_json()
        if json_data:
            imageValidator = ImageValidation(json_data)
            if imageValidator.isValid(None) == True:
                try:
                    image = Image(json_data['image'])
                    db.session.add(image)
                    db.session.commit()
                    last_id = image.id

                    app.logger.warning(' %s salvou a imagem %s', session.get('user_name', ''), image.id)

                    return {
                        'message': 'Imagem salva com sucesso',
                        'id': last_id
                    }, 200
                except:
                    db.session.rollback()
                    return {'message': 'Error ao conectar com o banco de dados'}, 501
            else:
                return imageValidator.response
        else:
            return {'message': 'Dados não enviados'}, 400
        

    @mustHaveId
    def put(self, id=None):
        if not session.get('user_id', None):
            return {'message': 'Sem permissão para acessar este recurso'}, 401
        json_data = request.get_json()
        if json_data:
            image = Image.query.filter_by(id=id).first()
            if image:
                imageValidator = ImageValidation(json_data)
                if imageValidator.isValid(image) == True:
                    try:
                        image.image = json_data['image']
                        db.session.commit()

                        app.logger.warning(' %s editou a imagem %s', session.get('user_name', ''), image.id)

                        return {
                            'message': 'Imagem editada com sucesso',
                            'id': id
                        }, 200
                    except:
                        db.session.rollback()
                        return {'message': 'Error ao conectar com o banco de dados'}, 501
                else:
                    return imageValidator.response
            else:
                return {'message': 'Imagem não encontrada'}, 404
        else:
            return {'message': 'Dados não enviados'}, 400


    @mustHaveId
    def delete(self, id=None):
        if not session.get('user_id', None):
            return {'message': 'Sem permissão para acessar este recurso'}, 401
        post = Post.query.filter_by(image_id=id).first()
        if post: 
            return {'message': 'A imagem não pode ser deletada pois possui posts relacionados a ela'}, 501
        user = User.query.filter_by(image_id=id).first()
        if user: 
            return {'message': 'A imagem não pode ser deletada pois possui usuários relacionados a ela'}, 501
        config = Configuration.query.join(ConfigurationImage).filter_by(image_id=id).first()
        if config: 
            return {'message': 'A imagem não pode ser deletada pois possui banners relacionados a ela'}, 501
        image = Image.query.filter_by(id=id).first()
        if image:
            try:

                app.logger.warning(' %s deletou a imagem %s', session.get('user_name', ''), image.id)

                db.session.delete(image)
                db.session.commit()
                return {
                    'message': 'Imagem deletada com sucesso',
                    'id': id
                }, 200
            except:
                db.session.rollback()
                return {'message': 'Erro ao conectar com o banco de dados'}, 501
        else:
            return {'message': 'Imagem não encontrada'}, 404



class ImageByIdResource(Resource):
    @mustHaveId
    def get(self, id=None):
        image_schema = ImageSchema()
        image = Image.query.get(id)
        if image:
            image = image_schema.dump(image)
            return image, 200
        return {'message': 'Imagem não encontrada'}, 404