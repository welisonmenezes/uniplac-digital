import os
from flask import current_app, Blueprint, render_template, request, url_for

postBP = Blueprint('posts', __name__, url_prefix='/admin', template_folder='templates', static_folder='static')

@postBP.route('/noticias')
def noticias_index():
    titulo = 'Notícias'
    return render_template('/posts/index.html', titulo=titulo), 200

@postBP.route('/noticias/cadastrar')
def noticias_cadastrar():
    titulo = 'Notícias'
    operacao = 'Cadastro'
    return render_template('/posts/formulario.html', titulo=titulo, operacao=operacao), 200

@postBP.route('/noticias/editar')
def noticias_editar():
    titulo = 'Notícias'
    operacao = 'Edição'
    return render_template('/posts/formulario.html', titulo=titulo, operacao=operacao), 200

@postBP.route('/noticias/deletar', methods=['GET', 'POST'])
def noticias_deletar():
    titulo = 'Notícias'
    pergunta = 'Deseja realmente excluir a notícia [0002223]'
    return render_template('/posts/deletar.html', titulo=titulo, pergunta=pergunta), 200


@postBP.route('/anuncios')
def anuncios_index():
    titulo = 'Anúncios'
    return render_template('/posts/index.html', titulo=titulo), 200

@postBP.route('/anuncios/cadastrar')
def anuncios_cadastrar():
    titulo = 'Anúncios'
    operacao = 'Cadastro'
    return render_template('/posts/formulario.html', titulo=titulo, operacao=operacao), 200

@postBP.route('/anuncios/editar')
def anuncios_editar():
    titulo = 'Anúncios'
    operacao = 'Edição'    
    return render_template('/posts/formulario.html', titulo=titulo, operacao=operacao), 200

@postBP.route('/anuncios/deletar', methods=['GET', 'POST'])
def anuncios_deletar():
    titulo = 'Anúncios'
    pergunta = 'Deseja realmente excluir a anúncio [0002223]'
    return render_template('/posts/deletar.html', titulo=titulo, pergunta=pergunta), 200


@postBP.route('/avisos')
def avisos_index():
    titulo = 'Avisos'
    return render_template('/posts/index.html', titulo=titulo), 200

@postBP.route('/avisos/cadastrar')
def avisos_cadastrar():
    titulo = 'Avisos'
    operacao = 'Cadastro'
    return render_template('/posts/formulario.html', titulo=titulo, operacao=operacao), 200

@postBP.route('/avisos/editar')
def avisos_editar():
    titulo = 'Avisos'
    operacao = 'Edição'
    return render_template('/posts/formulario.html', titulo=titulo, operacao=operacao), 200

@postBP.route('/avisos/deletar', methods=['GET', 'POST'])
def avisos_deletar():
    titulo = 'Avisos'
    pergunta = 'Deseja realmente excluir a avisos [0002223]'
    return render_template('/posts/deletar.html', titulo=titulo, pergunta=pergunta), 200