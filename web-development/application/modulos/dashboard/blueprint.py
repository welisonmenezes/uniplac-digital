import os
from flask import current_app, Blueprint, render_template, request, url_for

dashboardBP = Blueprint('dashboard', __name__, url_prefix='/admin', template_folder='templates', static_folder='static')

@dashboardBP.route('/')
def dash():
    titulo = 'Dashboard'
    return render_template('dashboard/index.html',titulo=titulo), 200

