import os
from flask import current_app, Blueprint, render_template, request, url_for

postBP = Blueprint('posts', __name__, url_prefix='/admin', template_folder='templates', static_folder='static')

@postBP.route('/noticias')
def noticias_index():
    return 'listagem de notícias aqui', 200


@postBP.route('/noticias/cadastrar')
def noticias_cadastrar():
    return 'formulário de cadastro de notícias aqui', 200


@postBP.route('/noticias/editar')
def noticias_editar():
    return 'formulário de edição de notícias aqui', 200


@postBP.route('/noticias/deletar')
def noticias_deletar():
    return 'lógica para remover notícias aqui', 200

@postBP.route('/anuncios')
def anuncios_index():
    return 'listagem de anúncios aqui', 200


@postBP.route('/anuncios/cadastrar')
def anuncios_cadastrar():
    return 'formulário de cadastro de anúncios aqui', 200


@postBP.route('/anuncios/editar')
def anuncios_editar():
    return 'formulário de edição de anúncios aqui', 200


@postBP.route('/anuncios/deletar')
def anuncios_deletar():
    return 'lógica para remover anúncios aqui', 200

@postBP.route('/avisos')
def avisos_index():
    return 'listagem de avisos aqui', 200


@postBP.route('/avisos/cadastrar')
def avisos_cadastrar():
    return 'formulário de cadastro de avisos aqui', 200


@postBP.route('/avisos/editar')
def avisos_editar():
    return 'formulário de edição de avisos aqui', 200


@postBP.route('/avisos/deletar')
def avisos_deletar():
    return 'lógica para remover avisos aqui', 200