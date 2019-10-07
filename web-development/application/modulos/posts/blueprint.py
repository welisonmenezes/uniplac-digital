import os
from flask import current_app, Blueprint, render_template, request, url_for
from modulos.posts.formularios import PostForm
from database.Model import Configuration

postBP = Blueprint('posts', __name__, url_prefix='/admin', template_folder='templates', static_folder='static')

@postBP.route('/noticias')
def noticias_index():
    configuration = Configuration.query.first()
    titulo = 'Notícias'
    return render_template('/posts/index.html', titulo=titulo, configuration=configuration), 200

@postBP.route('/noticias/cadastrar', methods=['GET','POST'])
def noticias_cadastrar():
    configuration = Configuration.query.first()
    form = PostForm(request.form)
    titulo = 'Notícias'
    operacao = 'Cadastro'
    #print(form.content.data)
    if form.validate_on_submit():
        print('valido')
    return render_template('/posts/formulario.html', titulo=titulo, operacao=operacao, form=form, configuration=configuration), 200

@postBP.route('/noticias/editar', methods=['GET','POST'])
def noticias_editar():
    configuration = Configuration.query.first()
    form = PostForm(request.form)
    titulo = 'Notícias'
    operacao = 'Edição'
    if form.validate_on_submit():
        print('valido')
    return render_template('/posts/formulario.html', titulo=titulo, operacao=operacao, form=form, configuration=configuration), 200

@postBP.route('/noticias/deletar', methods=['GET', 'POST'])
def noticias_deletar():
    configuration = Configuration.query.first()
    titulo = 'Notícias'
    pergunta = 'Deseja realmente excluir a notícia [0002223]'
    return render_template('/posts/deletar.html', titulo=titulo, pergunta=pergunta, configuration=configuration), 200


@postBP.route('/anuncios')
def anuncios_index():
    configuration = Configuration.query.first()
    #TODO se usuario comum listar apenas próprios anuncios
    titulo = 'Anúncios'
    return render_template('/posts/index.html', titulo=titulo, configuration=configuration), 200

@postBP.route('/anuncios/cadastrar', methods=['GET','POST'])
def anuncios_cadastrar():
    configuration = Configuration.query.first()
    #TODO se usuario comum cadastro entrar como pendente
    form = PostForm(request.form)
    titulo = 'Anúncios'
    operacao = 'Cadastro'
    if form.validate_on_submit():
        print('valido')
    return render_template('/posts/formulario.html', titulo=titulo, operacao=operacao, form=form, configuration=configuration), 200

@postBP.route('/anuncios/editar', methods=['GET','POST'])
def anuncios_editar():
    configuration = Configuration.query.first()
    #TODO se usuario comum permitir editar apenas o próprio anúncio e se ainda estiver pendente
    form = PostForm(request.form)
    titulo = 'Anúncios'
    operacao = 'Edição'    
    if form.validate_on_submit():
        print('valido')
    return render_template('/posts/formulario.html', titulo=titulo, operacao=operacao, form=form, configuration=configuration), 200

@postBP.route('/anuncios/deletar', methods=['GET', 'POST'])
def anuncios_deletar():
    configuration = Configuration.query.first()
    #TODO se usuario comum permitir deletar apenas o próprio anúnico e se ainda estiver pendente
    titulo = 'Anúncios'
    pergunta = 'Deseja realmente excluir a anúncio [0002223]'
    return render_template('/posts/deletar.html', titulo=titulo, pergunta=pergunta, configuration=configuration), 200


@postBP.route('/avisos')
def avisos_index():
    configuration = Configuration.query.first()
    titulo = 'Avisos'
    return render_template('/posts/index.html', titulo=titulo, configuration=configuration), 200

@postBP.route('/avisos/cadastrar', methods=['GET','POST'])
def avisos_cadastrar():
    configuration = Configuration.query.first()
    form = PostForm(request.form)
    titulo = 'Avisos'
    operacao = 'Cadastro'
    if form.validate_on_submit():
        print('valido')
    return render_template('/posts/formulario.html', titulo=titulo, operacao=operacao, form=form, configuration=configuration), 200

@postBP.route('/avisos/editar', methods=['GET','POST'])
def avisos_editar():
    configuration = Configuration.query.first()
    form = PostForm(request.form)
    titulo = 'Avisos'
    operacao = 'Edição'
    if form.validate_on_submit():
        print('valido')
    return render_template('/posts/formulario.html', titulo=titulo, operacao=operacao, form=form, configuration=configuration), 200

@postBP.route('/avisos/deletar', methods=['GET', 'POST'])
def avisos_deletar():
    configuration = Configuration.query.first()
    titulo = 'Avisos'
    pergunta = 'Deseja realmente excluir a avisos [0002223]'
    return render_template('/posts/deletar.html', titulo=titulo, pergunta=pergunta, configuration=configuration), 200