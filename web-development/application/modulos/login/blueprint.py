import os
from flask import current_app, Blueprint, render_template, request, url_for

loginBP = Blueprint('login', __name__, url_prefix='/login', template_folder='templates', static_folder='static')

@loginBP.route('/')
def inicio():
    return 'Tela de login', 200


@loginBP.route('/logout')
def logout():
    return 'logica de logout', 200
