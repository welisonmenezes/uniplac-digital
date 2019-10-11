import os
from flask import current_app, Blueprint, render_template, request, url_for, flash, session
from modulos.posts.formularios import PostForm
from sqlalchemy import desc, or_
from database.Model import Configuration, db, Post, Category
import datetime

postBP = Blueprint('posts', __name__, url_prefix='/admin', template_folder='templates', static_folder='static')

@postBP.route('/noticias')
def noticias_index():
    configuration = Configuration.query.first()
    titulo = 'Notícias'

    # pega os argumentos da string, se existir, senão, seta valores padrão
    page = 1 if (request.args.get('page') == None) else int(request.args.get('page'))
    name = '' if (request.args.get('name') == None) else request.args.get('name')
    category = '' if (request.args.get('category') == None) else request.args.get('category')

    # implementa o filtro se necessário
    filter = ()
    if category:
        filter = filter + (Post.category_id == category,)
    if name:
        filter = filter + (or_(Post.title.like('%'+name+'%'), Post.description.like('%'+name+'%'), Post.content.like('%'+name+'%')),)

    # consulta o banco de dados retornando o paginate e os dados
    paginate = Post.query.filter(*filter).order_by(desc(Post.id)).paginate(page=page, per_page=10, error_out=False)
    posts = paginate.items

    categories = Category.query.filter()

    return render_template('/posts/index.html', categories=categories, paginate=paginate, posts=posts, currentPage=page, name=name, category=category, titulo=titulo, configuration=configuration), 200

@postBP.route('/noticias/cadastrar', methods=['GET','POST'])
def noticias_cadastrar():
    configuration = Configuration.query.first()
    form = PostForm(request.form)
    titulo = 'Notícias'
    operacao = 'Cadastro'
    if form.validate_on_submit():
        try:
            # cria a categoria com os dados do formulário

            form.user_id = session.get('user_id', '')

            post = Post(
                form.title.data,
                form.description.data,
                form.content.data,
                'news',
                form.status.data,
                form.entry_date.data,
                form.departure_date.data,
                None,
                form.user_id,
                form.category_id.data
            )
            
            if form.image_id.data != '':
                post.image_id = form.image_id.data

            # adiciona e commita a categoria na base de dados
            db.session.add(post)
            db.session.commit()

            app.logger.warning(' %s cadastrou a noticia %s', session.get('user_name', ''), post.title)

            # flash message e redireciona pra mesma tela para limpar o objeto request
            flash('Notícia cadastrada com sucesso', 'success')
            return redirect(url_for('posts.noticias_cadastrar'))
        except:
            # remove qualquer vestígio do usuário da sessin e flash message 
            db.session.rollback()
            flash('Erro ao tentar cadastrar a notícia', 'danger')
    return render_template('/posts/formulario.html', titulo=titulo, operacao=operacao, form=form, configuration=configuration), 200

@postBP.route('/noticias/editar', methods=['GET','POST'])
def noticias_editar():
    configuration = Configuration.query.first()
    form = PostForm(request.form)
    titulo = 'Notícias'
    operacao = 'Edição'

    # exemplo de entrada pra edição
    #form.entry_date.data = datetime.datetime.strptime('2000-11-11', '%Y-%m-%d')
    
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