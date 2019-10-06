from flask import current_app, Blueprint, render_template, url_for
from database.Model import Configuration

errorBP = Blueprint('error', __name__, url_prefix='/', template_folder='templates/', static_folder='static/')

@errorBP.errorhandler(404)
def notFound(error):
    configuration = Configuration.query.first()
    return render_template('error404.html', configuration=configuration), 404

@errorBP.errorhandler(500)
def serverError(error):
    configuration = Configuration.query.first()
    return render_template('error500.html', configuration=configuration), 500
