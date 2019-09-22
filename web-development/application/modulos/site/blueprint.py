import os
from flask import current_app, Blueprint, render_template, request, url_for

siteBP = Blueprint('site', __name__, url_prefix='/site', template_folder='templates', static_folder='static')

@siteBP.route('/')
def index():
    return 'listagem de usuários aqui', 200


@siteBP.route('/cadastrar')
def cadastrar():
    return 'formulário de cadastro de usuário aqui', 200
