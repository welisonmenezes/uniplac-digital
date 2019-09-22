import os
from flask import current_app, Blueprint, render_template, request, url_for

siteBP = Blueprint('site', __name__, url_prefix='/site', template_folder='templates', static_folder='static')

@siteBP.route('/')
def index():
    return 'Tela principal', 200


@siteBP.route('/noticias')
def noticias():
    return 'Visualização de noticias', 200


@siteBP.route('/anuncios')
def anuncios():
    return 'Visualização de anuncios', 200


@siteBP.route('/avisos')
def avisos():
    return 'Visualização de avisos', 200

 
@siteBP.route('/contato')
def contato():
    return 'Dados da universidade', 200


@siteBP.route('/login')
def login():
    return 'Acesso a tela de login', 200
