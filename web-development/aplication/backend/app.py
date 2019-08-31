from flask import Flask, render_template, make_response
from api import api
import base64
import re

from api.Models.ImageModel import db, Image

def create_app():

    # start Flask app
    app = Flask(__name__, template_folder='ui', static_folder='ui/static')
    
    # apply app configurations
    app.config.from_pyfile('config.py')

    # initialize the db conexion
    db.init_app(app)

    # routes all nonexistent route to /
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def index(path):
        return render_template('index.html'), 200

    @app.route('/media/<int:id>')
    def displayMedia(id):
        image = Image.query.get(id)
        if image:

            imageType = 'image/png'
            baseType = re.search('data:image/(.+?);base64,', image.image)
            cleanBase64 = image.image

            if baseType:
                cleanBase64 = cleanBase64.replace(baseType.group(0), '')
                if (baseType.group(1) == 'png'):
                    imageType = 'image/png'
                elif (baseType.group(1) == 'jpg' or baseType.group(1) == 'jpeg'):
                    imageType = 'image/jpg'
                elif (baseType.group(1) == 'gif'):
                    imageType = 'image/gif'

            imgdata = base64.b64decode(cleanBase64)
            response = make_response(imgdata)
            response.headers.set('Content-Type', 'image/png')
            return response
            
        return 'no image found', 404

    # initialize the api blueprint
    app.register_blueprint(api.api_bp)

    return app