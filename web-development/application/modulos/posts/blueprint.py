import os
from flask import current_app, Blueprint, render_template, request, url_for, flash, session, redirect
from modulos.posts.formularios import PostForm
from app import app
from sqlalchemy import desc, or_, and_
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
    filter = (Post.genre == 'news', )
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
    titulo = 'Cadastrar Notícias'
    operacao = 'Cadastro'
    if form.validate_on_submit():
        try:
            form.user_id = session.get('user_id', '')

            # cria o post com os dados do formulário
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

@postBP.route('/noticias/editar/<int:id>', methods=['GET','POST'])
def noticias_editar(id):
    configuration = Configuration.query.first()

    # pega o post pelo id e com o genero noticia
    post = Post.query.filter(and_(Post.id==id, Post.genre=='news')).first()

    if not post:
        flash('A notícia não existe', 'info')
        return redirect(url_for('posts.noticias_index'))

    titulo = 'Editar notícia'
    
    if request.form:
        # formulário preenchido pelo objeto request, caso exista
        form = PostForm(request.form)
    else:
        # formulário vazio
        form = PostForm()

        # preenche formulário com post recuperado pelo id
        fillForm(form, post, 'news')


    # exemplo de entrada pra edição
    #form.entry_date.data = datetime.datetime.strptime('2000-11-11', '%Y-%m-%d')
    
    if form.validate_on_submit():
        try:
            post.title = form.title.data
            post.description = form.description.data
            post.content = form.content.data
            post.genre = 'news'
            post.status = form.status.data
            post.entry_date = form.entry_date.data
            post.departure_date = form.departure_date.data
            post.image_id = None
            if (form.image_id.data != ''):
                post.image_id = form.image_id.data
            post.user_id = session.get('user_id', '')
            post.category_id = form.category_id.data

            # commita os dados na base de dados
            db.session.commit()

            app.logger.warning(' %s editou a noticia %s', session.get('user_name', ''), post.id)

            # flash message e redireciona pra mesma tela para limpar o objeto request
            flash('Notícia editada com sucesso', 'success')
            return redirect(url_for('posts.noticias_editar', id=id))
        except:
            # remove qualquer vestígio do usuário da sessin e flash message
            db.session.rollback()
            flash('Erro ao tentar editar a notícia', 'danger')

    return render_template('/posts/formulario.html', titulo=titulo, form=form, post=post, configuration=configuration), 200

@postBP.route('/noticias/deletar/<int:id>', methods=['GET', 'POST'])
def noticias_deletar(id):
    configuration = Configuration.query.first()

    # pega o post pelo id e pelo genero notica
    post = Post.query.filter(and_(Post.id==id, Post.genre=='news')).first()


    # se não existe a noticia, bye
    if not post:
        flash('A notícia não existe', 'info')
        return redirect(url_for('posts.noticias_index'))

    if request.method == 'POST':
        postId = request.values.get('postId')
        if postId:
            try:
                app.logger.warning(' %s deletou a notícia %s', session.get('user_name', ''), post.id)
                db.session.delete(post)
                db.session.commit()
                flash('Notícia deletada com sucesso', 'success')
                return redirect(url_for('posts.noticias_index'))
            except:
                db.session.rollback()
                flash('Erro ao tentar deletar a notícia', 'danger')
            
    titulo = 'Notícias'
    pergunta = 'Deseja realmente excluir a notícia ' + post.title
    return render_template('/posts/deletar.html', titulo=titulo, pergunta=pergunta, postId=id, configuration=configuration), 200


@postBP.route('/anuncios')
def anuncios_index():
    #TODO se usuario comum listar apenas próprios anuncios
    configuration = Configuration.query.first()

    titulo = 'Anúncios'

    # pega os argumentos da string, se existir, senão, seta valores padrão
    page = 1 if (request.args.get('page') == None) else int(request.args.get('page'))
    name = '' if (request.args.get('name') == None) else request.args.get('name')
    category = '' if (request.args.get('category') == None) else request.args.get('category')

    # implementa o filtro se necessário
    filter = (Post.genre == 'ad', )
    if category:
        filter = filter + (Post.category_id == category,)
    if name:
        filter = filter + (or_(Post.title.like('%'+name+'%'), Post.description.like('%'+name+'%'), Post.content.like('%'+name+'%')),)

    # consulta o banco de dados retornando o paginate e os dados
    paginate = Post.query.filter(*filter).order_by(desc(Post.id)).paginate(page=page, per_page=10, error_out=False)
    posts = paginate.items

    categories = Category.query.filter()

    return render_template('/posts/index.html', categories=categories, paginate=paginate, posts=posts, currentPage=page, name=name, category=category, titulo=titulo, configuration=configuration), 200

@postBP.route('/anuncios/cadastrar', methods=['GET','POST'])
def anuncios_cadastrar():
    #TODO se usuario comum cadastro entrar como pendente
    configuration = Configuration.query.first()
    form = PostForm(request.form)
    titulo = 'Cadastrar Anúncios'
    operacao = 'Cadastro'
    
    if form.validate_on_submit():
        try:
            form.user_id = session.get('user_id', '')

            # cria o post com os dados do formulário
            post = Post(
                form.title.data,
                form.description.data,
                form.content.data,
                'ad',
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

            app.logger.warning(' %s cadastrou o anúncio %s', session.get('user_name', ''), post.title)

            # flash message e redireciona pra mesma tela para limpar o objeto request
            flash('Anúncio cadastrado com sucesso', 'success')
            return redirect(url_for('posts.anuncios_cadastrar'))
        except:
            # remove qualquer vestígio do usuário da sessin e flash message 
            db.session.rollback()
            flash('Erro ao tentar cadastrar o anúncio', 'danger')
    return render_template('/posts/formulario.html', titulo=titulo, operacao=operacao, form=form, configuration=configuration), 200

@postBP.route('/anuncios/editar/<int:id>', methods=['GET','POST'])
def anuncios_editar(id):
    #TODO se usuario comum permitir editar apenas o próprio anúncio e se ainda estiver pendente
    configuration = Configuration.query.first()

    # pega o post pelo id e com o genero anuncio
    post = Post.query.filter(and_(Post.id==id, Post.genre=='ad')).first()

    if not post:
        flash('O anúncio não existe', 'info')
        return redirect(url_for('posts.anuncios_index'))

    titulo = 'Editar anúncio'

    if request.form:
        # formulário preenchido pelo objeto request, caso exista
        form = PostForm(request.form)
    else:
        # formulário vazio
        form = PostForm()

        # preenche formulário com post recuperado pelo id
        fillForm(form, post, 'ad')

    if form.validate_on_submit():
        try:
            post.title = form.title.data
            post.description = form.description.data
            post.content = form.content.data
            post.genre = 'ad'
            post.status = form.status.data
            post.entry_date = form.entry_date.data
            post.departure_date = form.departure_date.data
            post.image_id = None
            if (form.image_id.data != ''):
                post.image_id = form.image_id.data
            post.user_id = session.get('user_id', '')
            post.category_id = form.category_id.data

            # commita os dados na base de dados
            db.session.commit()

            app.logger.warning(' %s editou o anúncio %s', session.get('user_name', ''), post.id)

            # flash message e redireciona pra mesma tela para limpar o objeto request
            flash('Anúncio editado com sucesso', 'success')
            return redirect(url_for('posts.anuncios_editar', id=id))
        except:
            # remove qualquer vestígio do usuário da sessin e flash message
            db.session.rollback()
            flash('Erro ao tentar editar o anúncio', 'danger')

    return render_template('/posts/formulario.html', titulo=titulo, form=form, post=post, configuration=configuration), 200

@postBP.route('/anuncios/deletar/<int:id>', methods=['GET', 'POST'])
def anuncios_deletar(id):
    #TODO se usuario comum permitir deletar apenas o próprio anúnico e se ainda estiver pendente
    configuration = Configuration.query.first()

    # pega o post pelo id e pelo genero anuncio
    post = Post.query.filter(and_(Post.id==id, Post.genre=='ad')).first()

    # se não existe a noticia, bye
    if not post:
        flash('O anúncio não existe', 'info')
        return redirect(url_for('posts.anuncios_index'))

    if request.method == 'POST':
        postId = request.values.get('postId')
        if postId:
            try:
                app.logger.warning(' %s deletou o anúncio %s', session.get('user_name', ''), post.id)
                db.session.delete(post)
                db.session.commit()
                flash('Anúncio deletado com sucesso', 'success')
                return redirect(url_for('posts.anuncios_index'))
            except:
                db.session.rollback()
                flash('Erro ao tentar deletar o anúncio', 'danger')
            
    titulo = 'Anúncios'
    pergunta = 'Deseja realmente excluir o anúncio ' + post.title
    return render_template('/posts/deletar.html', titulo=titulo, pergunta=pergunta, postId=id, configuration=configuration), 200


@postBP.route('/avisos')
def avisos_index():
    configuration = Configuration.query.first()
    titulo = 'Avisos'

    # pega os argumentos da string, se existir, senão, seta valores padrão
    page = 1 if (request.args.get('page') == None) else int(request.args.get('page'))
    name = '' if (request.args.get('name') == None) else request.args.get('name')
    category = '' if (request.args.get('category') == None) else request.args.get('category')

    # implementa o filtro se necessário
    filter = (Post.genre == 'notice', )
    if category:
        filter = filter + (Post.category_id == category,)
    if name:
        filter = filter + (or_(Post.title.like('%'+name+'%'), Post.description.like('%'+name+'%'), Post.content.like('%'+name+'%')),)

    # consulta o banco de dados retornando o paginate e os dados
    paginate = Post.query.filter(*filter).order_by(desc(Post.id)).paginate(page=page, per_page=10, error_out=False)
    posts = paginate.items

    categories = Category.query.filter()

    return render_template('/posts/index.html', categories=categories, paginate=paginate, posts=posts, currentPage=page, name=name, category=category, titulo=titulo, configuration=configuration), 200

@postBP.route('/avisos/cadastrar', methods=['GET','POST'])
def avisos_cadastrar():
    configuration = Configuration.query.first()
    form = PostForm(request.form)
    titulo = 'Cadastrar Avisos'
    operacao = 'Cadastro'

    if form.validate_on_submit():
        try:
            form.user_id = session.get('user_id', '')

            # cria o post com os dados do formulário
            post = Post(
                form.title.data,
                form.description.data,
                form.content.data,
                'notice',
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

            app.logger.warning(' %s cadastrou o aviso %s', session.get('user_name', ''), post.title)

            # flash message e redireciona pra mesma tela para limpar o objeto request
            flash('Aviso cadastrado com sucesso', 'success')
            return redirect(url_for('posts.avisos_cadastrar'))
        except:
            # remove qualquer vestígio do usuário da sessin e flash message 
            db.session.rollback()
            flash('Erro ao tentar cadastrar o aviso', 'danger')
    return render_template('/posts/formulario.html', titulo=titulo, operacao=operacao, form=form, configuration=configuration), 200

@postBP.route('/avisos/editar/<int:id>', methods=['GET','POST'])
def avisos_editar(id):
    configuration = Configuration.query.first()
    
    # pega o post pelo id e com o genero anuncio
    post = Post.query.filter(and_(Post.id==id, Post.genre=='notice')).first()

    if not post:
        flash('O aviso não existe', 'info')
        return redirect(url_for('posts.avisos_index'))

    titulo = 'Editar aviso'

    if request.form:
        # formulário preenchido pelo objeto request, caso exista
        form = PostForm(request.form)
    else:
        # formulário vazio
        form = PostForm()

        # preenche formulário com post recuperado pelo id
        fillForm(form, post, 'notice')

    if form.validate_on_submit():
        try:
            post.title = form.title.data
            post.description = form.description.data
            post.content = form.content.data
            post.genre = 'notice'
            post.status = form.status.data
            post.entry_date = form.entry_date.data
            post.departure_date = form.departure_date.data
            post.image_id = None
            if (form.image_id.data != ''):
                post.image_id = form.image_id.data
            post.user_id = session.get('user_id', '')
            post.category_id = form.category_id.data

            # commita os dados na base de dados
            db.session.commit()

            app.logger.warning(' %s editou o aviso %s', session.get('user_name', ''), post.id)

            # flash message e redireciona pra mesma tela para limpar o objeto request
            flash('Aviso editado com sucesso', 'success')
            return redirect(url_for('posts.avisos_editar', id=id))
        except:
            # remove qualquer vestígio do usuário da sessin e flash message
            db.session.rollback()
            flash('Erro ao tentar editar o aviso', 'danger')

    return render_template('/posts/formulario.html', titulo=titulo, form=form, post=post, configuration=configuration), 200

@postBP.route('/avisos/deletar/<int:id>', methods=['GET', 'POST'])
def avisos_deletar(id):
    configuration = Configuration.query.first()

    # pega o post pelo id e pelo genero anuncio
    post = Post.query.filter(and_(Post.id==id, Post.genre=='notice')).first()

    # se não existe a noticia, bye
    if not post:
        flash('O aviso não existe', 'info')
        return redirect(url_for('posts.avisos_index'))

    if request.method == 'POST':
        postId = request.values.get('postId')
        if postId:
            try:
                app.logger.warning(' %s deletou o aviso %s', session.get('user_name', ''), post.id)
                db.session.delete(post)
                db.session.commit()
                flash('Aviso deletado com sucesso', 'success')
                return redirect(url_for('posts.avisos_index'))
            except:
                db.session.rollback()
                flash('Erro ao tentar deletar o aviso', 'danger')
            
    titulo = 'Avisos'
    pergunta = 'Deseja realmente excluir o aviso ' + post.title
    return render_template('/posts/deletar.html', titulo=titulo, pergunta=pergunta, postId=id, configuration=configuration), 200


# popula os campos do formuário
def fillForm(form, post, genre):
    form.title.data = post.title 
    form.description.data = post.description 
    form.content.data = post.content 
    form.genre = genre
    form.status.data = post.status
    form.entry_date.data = post.entry_date
    form.departure_date.data = post.departure_date
    form.image_id.data = None
    if (post.image_id != ''):
        form.image_id.data = post.image_id 
    form.user_id = session.get('user_id', '')
    form.category_id.data = post.category_id 