import os
from flask import current_app, Blueprint, render_template, request, url_for, redirect
from database.Model import Configuration


dashboardBP = Blueprint('dashboard', __name__, url_prefix='/admin', template_folder='templates', static_folder='static')

@dashboardBP.route('/')
def index():
    return redirect(url_for('dashboard.dash'))

@dashboardBP.route('/dashboard')
def dash():
    configuration = Configuration.query.first()
    
    titulo = 'Dashboard'
    return render_template('dashboard/index.html',titulo=titulo, configuration=configuration), 200

