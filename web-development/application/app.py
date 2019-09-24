from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

# create a Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# apply app configurations
app.config.from_pyfile('config.py')

# initialize app dependencies
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)


# @app.route('/')
# def index():
#     return render_template('base.html'), 200

# @app.route('/admin')
# def admin():
#     return render_template('base-admin.html'), 200

# @app.route('/login')
# def login():
#     return render_template('base-login.html'), 200


from modulos import *
from database import *
app.register_blueprint(usuarioBP)
app.register_blueprint(categoriaBP)
app.register_blueprint(configuracaoBP)
app.register_blueprint(postBP)
app.register_blueprint(loginBP)
app.register_blueprint(siteBP)
app.register_blueprint(dashboardBP)
app.register_blueprint(apiBP)

if __name__ == "__main__":
    app.run()