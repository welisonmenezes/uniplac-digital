from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# create a Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# apply app configurations
app.config.from_pyfile('config.py')

# initialize app dependencies
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('base.html'), 200

@app.route('/admin')
def admin():
    return render_template('base-admin.html'), 200

@app.route('/login')
def login():
    return render_template('base-login.html'), 200


from modulos import *
app.register_blueprint(usuarioBP)

if __name__ == "__main__":
    app.run()