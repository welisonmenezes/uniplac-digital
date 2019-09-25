import os
from flask import current_app, Blueprint, render_template, request, url_for

siteBP = Blueprint('site', __name__, url_prefix='/', template_folder='templates', static_folder='static')

@siteBP.route('/')
def index():
    return render_template('site/site.html'), 200


@siteBP.route('/noticias')
def noticias():
    titulo = 'Notícias'
    return render_template('site/posts.html', titulo=titulo), 200


@siteBP.route('/anuncios')
def anuncios():
    titulo = 'Anuncios'
    return render_template('site/posts.html', titulo=titulo), 200


@siteBP.route('/avisos')
def avisos():
    titulo = 'Avisos'
    return render_template('site/posts.html', titulo=titulo), 200

 
@siteBP.route('/contato')
def contato():
    return 'Dados da universidade', 200


@siteBP.route('/login')
def login():
    return 'Acesso a tela de login', 200
