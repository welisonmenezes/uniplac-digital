import os
from flask import current_app, Blueprint, render_template, request, url_for

dashboardBP = Blueprint('dashboard', __name__, url_prefix='/dashboard', template_folder='templates', static_folder='static')

@dashboardBP.route('/')
def dash():
    return 'Tela inicial', 200
