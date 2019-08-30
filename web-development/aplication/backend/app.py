from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from api import api
import sys
sys.path.insert(0, './api/Models')
from ImageModel import registerModels


def create_app():

    # start Flask app
    app = Flask(__name__, template_folder='ui', static_folder='ui/static')
    
    # apply app configurations
    app.config.from_pyfile('config.py')
    
    """
    db = SQLAlchemy(app)
    Image = registerModels(db)
    img = Image('img-here')
    db.session.add(img)
    db.session.commit()
    """

    # routes all nonexistent route to /
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def index(path):
        return render_template('index.html'), 200

    # initialize the api blueprint
    app.register_blueprint(api.api_bp)

    return app