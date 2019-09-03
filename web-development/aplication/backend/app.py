from flask import Flask, render_template
from api import api

from api.Models.Model import db

def create_app():

    # start Flask app
    app = Flask(__name__, template_folder='ui', static_folder='ui/static')
    
    # apply app configurations
    app.config.from_pyfile('config.py')

    # initialize the db conexion
    db.init_app(app)
    
    # ATENTION: uncomment only when recreate all database
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()

    # fix bug: flask_sqlalchemy close connection
    @app.teardown_appcontext
    def shutdown_session(response_or_exc):
        try:
            db.session.close_all()
        except:
            print('Falha ao fechar a conexão')
        return response_or_exc

    # routes all nonexistent route to /
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def index(path):
        return render_template('index.html'), 200

    # initialize the api blueprint
    app.register_blueprint(api.api_bp)

    return app