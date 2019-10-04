from flask import Flask, render_template
import logging
import datetime
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_mail import Mail

# create a Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

app.logger.removeHandler(default_handler)
current_date = datetime.datetime.now()
logging.basicConfig(
    filename='logging/app-log-' + str(current_date.month) + '-' + str(current_date.year) + '.log',
    format='%(asctime)s %(name)s %(levelname)s:%(message)s',
    level=logging.INFO
)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# apply app configurations
app.config.from_pyfile('config.py')

# initialize app dependencies
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

import utils.middleware
from modulos import *
from database import *

app.register_blueprint(errorBP)
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