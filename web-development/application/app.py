from flask import Flask, render_template
import logging
import datetime
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from datetime import datetime

# create a Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# app.logger.removeHandler(default_handler)
# current_date = datetime.datetime.now()
# logging.basicConfig(
#     filename='logging/app-log-' + str(current_date.month) + '-' + str(current_date.year) + '.log',
#     format='%(asctime)s %(name)s %(levelname)s:%(message)s',
#     level=logging.INFO
# )
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

# apply app configurations
app.config.from_pyfile('config.py')

# configurações do recaptcha
app.config['RECAPTCHA_USE_SSL']= False
app.config['RECAPTCHA_PUBLIC_KEY']= '6LccGOISAAAAAPVdDHhzpAXI64FnnX1vYL7Yea23'
app.config['RECAPTCHA_PRIVATE_KEY']='6LccGOISAAAAAFhRBXgRg5-1x_U2S0m9sxQJjdOW'
app.config['RECAPTCHA_OPTIONS'] = {'theme':'white'}

print(app.config)

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



#formata a data para padrão PT_BR
@app.template_filter('format_datetime')
def format_datetime(value, format="%d-%m-%Y %H:%M:%S"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)





if __name__ == "__main__":
    app.run()