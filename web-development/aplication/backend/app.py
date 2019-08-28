from flask import Flask, render_template
from api import api

def create_app():

    # start Flask app
    app = Flask(__name__, template_folder='ui', static_folder='ui/static')
    
    # apply app configurations
    app.config.from_pyfile('config.py')

    # routes all nonexistent route to /
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def index(path):
        return render_template('index.html'), 200

    # initialize the api blueprint
    app.register_blueprint(api.api_bp)

    return app