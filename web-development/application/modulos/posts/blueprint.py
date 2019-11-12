import os
from flask import current_app, Blueprint, render_template, request, url_for, flash, session, redirect
from modulos.posts.formularios import PostForm
from app import app
from sqlalchemy import desc, or_, and_, asc
from database.Model import Configuration, db, Post, Category, User, Tag, TagPost, Category
from datetime import datetime
from flask_mail import Message
from app import mail, executor

postBP = Blueprint('posts', __name__, url_prefix='/admin', template_folder='templates', static_folder='static')

@postBP.route('/noticias')
def noticias_index():
    return render_post_list_by_type('news', 'Notícias')


@postBP.route('/noticias/cadastrar', methods=['GET','POST'])
def noticias_cadastrar():
    return render_post_register_by_type('news', 'Cadastrar Notícia')


@postBP.route('/noticias/editar/<int:id>', methods=['GET','POST'])
def noticias_editar(id):
    return render_post_edit_by_type('news', 'Editar Notícia', id)


@postBP.route('/noticias/deletar/<int:id>', methods=['GET', 'POST'])
def noticias_deletar(id):
    return render_post_delete_by_type('news', 'Deseja realmente excluir a notícia', id)


@postBP.route('/anuncios')
def anuncios_index():
    return render_post_list_by_type('ad', 'Anúncios')


@postBP.route('/anuncios/cadastrar', methods=['GET','POST'])
def anuncios_cadastrar():
    return render_post_register_by_type('ad', 'Cadastrar Anúncio')


@postBP.route('/anuncios/editar/<int:id>', methods=['GET','POST'])
def anuncios_editar(id):
    return render_post_edit_by_type('ad', 'Editar Anúncio', id)


@postBP.route('/anuncios/deletar/<int:id>', methods=['GET', 'POST'])
def anuncios_deletar(id):
    return render_post_delete_by_type('ad', 'Deseja realmente excluir o anúncio', id)


@postBP.route('/avisos')
def avisos_index():
    return render_post_list_by_type('notice', 'Avisos')


@postBP.route('/avisos/cadastrar', methods=['GET','POST'])
def avisos_cadastrar():
    return render_post_register_by_type('notice', 'Cadastrar Aviso')


@postBP.route('/avisos/editar/<int:id>', methods=['GET','POST'])
def avisos_editar(id):
    return render_post_edit_by_type('notice', 'Editar Aviso', id)


@postBP.route('/avisos/deletar/<int:id>', methods=['GET', 'POST'])
def avisos_deletar(id):
    return render_post_delete_by_type('notice', 'Deseja realmente excluir o aviso', id)


@postBP.route('/meus-posts')
def meus_posts():
    return render_post_list_by_type('meus-posts', 'Minhas Publicações')


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
    form.category_id.data = str(post.category_id)


# remove as validações de data
def clearDateValidatons(post, form):
    if post.entry_date == form.entry_date.data:
        form.entry_date.validators = []
        field = form.entry_date
        def nullValidate(self, field):
            return True
        form.entry_date.validate = nullValidate

    if post.departure_date == form.departure_date.data:
        form.departure_date.validators = []
        field = form.departure_date
        def nullValidate(self, field):
            return True
        form.departure_date.validate = nullValidate


# LISTAGEM DE POSTS
def render_post_list_by_type(post_type, title):
    configuration = Configuration.query.first()
    titulo = title
    current_datetime = datetime.now()
    categories = Category.query.filter()
    users = None
    if post_type != 'meus-posts':
        users = User.query.filter(or_(User.role == 'admin', User.role == 'editor')).all()

    # pega os argumentos da string, se existir, senão, seta valores padrão
    page = '1' if (request.args.get('page') == None) else request.args.get('page')
    name = '' if (request.args.get('name') == None) else request.args.get('name')
    category = '' if (request.args.get('category') == None) else request.args.get('category')
    status = '' if (request.args.get('status') == None) else request.args.get('status')
    order_by = 'id' if (request.args.get('order_by') == None) else request.args.get('order_by')
    order = 'desc' if (request.args.get('order') == None) else request.args.get('order')
    publication = '' if (request.args.get('publication') == None) else request.args.get('publication')
    author = ''
    if post_type != 'meus-posts':
        author = '' if (request.args.get('author') == None) else request.args.get('author')

    # previne erro ao receber string
    try:
        page = int(page)
    except:
        page = 1

    # previne erro ao recebe string inválida
    if not order_by in ['id', 'title', 'created_at']:
        order_by = 'id'

    # previne erro ao recebe string inválida
    if not order in ['desc', 'asc']:
        order = 'desc'

    # implementa o filtro se necessário
    if post_type != 'meus-posts':
        filter = (Post.genre == post_type, )
    else:
        filter = (Post.user_id == session.get('user_id', ''), )
    if category:
        filter = filter + (Post.category_id == category,)
    if name:
        filter = filter + (or_(Post.title.like('%'+name+'%'), Post.description.like('%'+name+'%'), Post.content.like('%'+name+'%')),)
    if status:
        filter = filter + (Post.status == status,)
    if publication == 'current':
        filter = filter + (and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime),)
    elif publication == 'expired':
        filter = filter + (and_(Post.departure_date < current_datetime),)
    elif publication == 'scheduled':
        filter = filter + (and_(Post.entry_date > current_datetime),)

    if post_type != 'meus-posts':
        if author:
            filter = filter + (Post.user_id == author, )
    
    if post_type == 'ad':
        if session.get('user_role', '') == 'user':
            filter = filter + (Post.user_id == session.get('user_id', ''), )

    # gera o order_by
    if order == 'asc':
        query_order = asc(order_by)
    else:
        query_order = desc(order_by)

    # consulta o banco de dados retornando o paginate e os dados
    paginate = Post.query.filter(*filter).order_by(query_order).paginate(page=page, per_page=10, error_out=False)
    posts = paginate.items

    return render_template('/posts/index.html', current_datetime=current_datetime, categories=categories, paginate=paginate, posts=posts, currentPage=page, name=name, category=category, status=status, order_by=order_by, order=order, titulo=titulo, configuration=configuration, publication=publication, users=users), 200


# CADASTRO DE POSTS
def render_post_register_by_type(post_type, title):
    configuration = Configuration.query.first()
    form = PostForm(request.form)
    titulo = title

    if post_type == 'ad':
        if session.get('user_role', '') == 'user':
            form.status.validators = []

    form.category_id.choices = [('', 'Selecione')]
    try:
        categories = Category.query.all()
        for category in categories:
            form.category_id.choices.append((str(category.id), category.name))
    except:
        pass

    if form.validate_on_submit():
        try:
            form.user_id = session.get('user_id', '')

            # cria o post com os dados do formulário
            post = Post(
                form.title.data,
                form.description.data,
                form.content.data,
                post_type,
                '',
                form.entry_date.data,
                form.departure_date.data,
                None,
                form.user_id,
                None
            )

            if post_type == 'ad':
                if session.get('user_role', '') == 'user':
                    post.status = 'pending'
                else:
                    post.status = form.status.data
            else:
                post.status = form.status.data

            if form.image_id.data != '':
                post.image_id = form.image_id.data

            #adiciona a tag no banco
            tags = form.tag.data
            array_tags = tags.split(',')
            for t in array_tags:
                if t.strip() == '':
                    continue
                tag = Tag.query.filter((Tag.name==t)).first()
                if tag:
                    post.tags.append(tag)
        
                else:
                    tag = Tag(t)
                    post.tags.append(tag)

            if form.category_id.data != '':
                post.category_id = form.category_id.data

            db.session.add(post)
            db.session.commit()

            if post_type == 'news':
                executor.submit(send_post_email, 'Novo cadastro de notícia', 'O usuário ' + session.get('user_name', '') + ' cadastrou uma nova notícia.')
                app.logger.warning(' %s cadastrou a notícia %s', session.get('user_name', ''), post.title)
                flash('Notícia cadastrada com sucesso', 'success')
                return redirect(url_for('posts.noticias_index'))
            elif post_type == 'notice':
                executor.submit(send_post_email, 'Novo cadastro de aviso', 'O usuário ' + session.get('user_name', '') + ' cadastrou um novo aviso.')
                app.logger.warning(' %s cadastrou o aviso %s', session.get('user_name', ''), post.title)
                flash('Aviso cadastrado com sucesso', 'success')
                return redirect(url_for('posts.avisos_index'))
            elif post_type == 'ad':
                executor.submit(send_post_email, 'Novo cadastro de anúncio', 'O usuário ' + session.get('user_name', '') + ' cadastrou um novo anúncio.')
                app.logger.warning(' %s cadastrou o anúncio %s', session.get('user_name', ''), post.title)
                flash('Anúncio cadastrado com sucesso', 'success')
                return redirect(url_for('posts.anuncios_index'))
        except:
            # remove qualquer vestígio do usuário da sessin e flash message 
            db.session.rollback()
            if post_type == 'news':
                flash('Erro ao tentar cadastrar a notícia', 'danger')
            elif post_type == 'notice':
                flash('Erro ao tentar cadastrar o aviso', 'danger')
            elif post_type == 'ad':
                flash('Erro ao tentar cadastrar o anúncio', 'danger')

    return render_template('/posts/formulario.html', titulo=titulo, form=form, configuration=configuration), 200


# EDIÇÃO DE POSTS
def render_post_edit_by_type(post_type, title, id):
    configuration = Configuration.query.first()
    titulo = title

    # pega o post pelo id 
    post = Post.query.filter(and_(Post.id==id)).first()

    if not post or post.genre != post_type:
        if post_type == 'news':
            flash('A notícia solicitada não existe', 'info')
            return redirect(url_for('posts.noticias_index'))
        elif post_type == 'notice':
            flash('O aviso solicitado não existe', 'info')
            return redirect(url_for('posts.avisos_index'))
        elif post_type == 'ad':
            flash('O anúncio solicitado não existe', 'info')
            return redirect(url_for('posts.anuncios_index'))

    if post_type == 'ad':
        # se for user nivel 4
        if session.get('user_role', '') == 'user':
            # se não for seu anuncio
            if post.user_id != session.get('user_id', ''):
                flash('Você não tem permissão para editar este anúncio', 'info')
                return redirect(url_for('posts.anuncios_index'))
            
            # se anúncio não for pendente 
            if post.status != 'pending':
                flash('Este anúncio não pode ser mais editado', 'info')
                return redirect(url_for('posts.anuncios_index'))

    strtags = ''
    for tag in post.tags:
        strtags = strtags+str(tag.name)+','
    if strtags.endswith(','):
        strtags = strtags[:-1]

    if request.form:
        # formulário preenchido pelo objeto request, caso exista
        form = PostForm(request.form)
    else:
        # formulário vazio
        form = PostForm()
        form.tag.data = strtags

        # preenche formulário com post recuperado pelo id
        fillForm(form, post, post_type)

    form.category_id.choices = [('', 'Selecione')]
    try:
        categories = Category.query.all()
        for category in categories:
            form.category_id.choices.append((str(category.id), category.name))
    except:
        pass

    if post_type == 'ad':
        # se usuário nível 4, remove validator
        if session.get('user_role', '') == 'user':
            form.status.validators = []

    clearDateValidatons(post, form)

    if form.validate_on_submit():
        try:
            post.title = form.title.data
            post.description = form.description.data
            post.content = form.content.data
            post.genre = post_type
            post.entry_date = form.entry_date.data
            post.departure_date = form.departure_date.data
            
            if post_type == 'ad':
                if session.get('user_role', '') == 'user':
                    post.status = 'pending'
                else:
                    post.status = form.status.data
            else:
                post.status = form.status.data
                
            post.image_id = None
            if (form.image_id.data != ''):
                post.image_id = form.image_id.data

            post.category_id = None
            if form.category_id.data != '':
                post.category_id = form.category_id.data

            id_tags=[]
            for t in post.tags:
                id_tags.append(t.id)
            
            for t in id_tags:   
                tag=Tag.query.get(t)
                post.tags.remove(tag)

            tags = form.tag.data
            array_tags = tags.split(',')

            for t in array_tags:
                if t.strip() == '':
                    continue
                tag = Tag.query.filter((Tag.name==t)).first()
                if tag:
                    post.tags.append(tag)
        
                else:
                    tag = Tag(t)
                    post.tags.append(tag)

            # commita os dados na base de dados
            db.session.commit()

            if post_type == 'news':
                app.logger.warning(' %s editou a noticia %s', session.get('user_name', ''), post.id)
                flash('Notícia editada com sucesso', 'success')
                return redirect(url_for('posts.noticias_editar', id=id))
            elif post_type == 'notice':
                app.logger.warning(' %s editou o aviso %s', session.get('user_name', ''), post.id)
                flash('Aviso editado com sucesso', 'success')
                return redirect(url_for('posts.avisos_editar', id=id))
            elif post_type == 'ad':
                app.logger.warning(' %s editou o anúncio %s', session.get('user_name', ''), post.id)
                flash('Anúncio editado com sucesso', 'success')
                return redirect(url_for('posts.anuncios_editar', id=id))
        except:
            # remove qualquer vestígio do usuário da sessin e flash message
            db.session.rollback()
            if post_type == 'news':
                flash('Erro ao tentar editar a notícia', 'danger')
            elif post_type == 'notice':
                flash('Erro ao tentar editar o aviso', 'danger')
            elif post_type == 'ad':
                flash('Erro ao tentar editar o anúncio', 'danger')

    return render_template('/posts/formulario.html', titulo=titulo, form=form, post=post, configuration=configuration), 200
        
    
# DELEÇÃO DE POSTS
def render_post_delete_by_type(post_type, title, id):
    configuration = Configuration.query.first()

    # pega o post pelo id
    post = Post.query.filter(and_(Post.id==id)).first()

    # se não existe a noticia, bye
    if not post or post.genre != post_type:
        if post_type == 'news':
            flash('A notícia solicitada não existe', 'info')
            return redirect(url_for('posts.noticias_index'))
        elif post_type == 'notice':
            flash('O aviso solicitado não existe', 'info')
            return redirect(url_for('posts.avisos_index'))
        elif post_type == 'ad':
            flash('O anúncio solicitado não existe', 'info')
            return redirect(url_for('posts.anuncios_index'))

    if post_type == 'ad':
        # se for user nivel 4
        if session.get('user_role', '') == 'user':
            # se não for seu anuncio
            if post.user_id != session.get('user_id', ''):
                flash('Você não tem permissão para deletar este anúncio', 'info')
                return redirect(url_for('posts.anuncios_index'))
            
            # se anúncio não for pendente 
            if post.status != 'pending':
                flash('Este anúncio não pode ser mais deletado', 'info')
                return redirect(url_for('posts.anuncios_index'))

    pergunta = title + ' ' + post.title

    if request.method == 'POST':
        postId = request.values.get('postId')
        if postId:
            try:

                # deleta as tags relacionadas
                db.engine.execute('DELETE FROM tagpost WHERE post_id =' + str(post.id))
                db.session.commit()

                db.session.delete(post)
                db.session.commit()
                if post_type == 'news':
                    app.logger.warning(' %s deletou a notícia %s', session.get('user_name', ''), post.id)
                    flash('Notícia deletada com sucesso', 'success')
                    return redirect(url_for('posts.noticias_index'))
                elif post_type == 'notice':
                    app.logger.warning(' %s deletou o aviso %s', session.get('user_name', ''), post.id)
                    flash('Aviso deletado com sucesso', 'success')
                    return redirect(url_for('posts.avisos_index'))
                elif post_type == 'ad':
                    app.logger.warning(' %s deletou o anúncio %s', session.get('user_name', ''), post.id)
                    flash('Anúncio deletado com sucesso', 'success')
                    return redirect(url_for('posts.anuncios_index'))
            except:
                db.session.rollback()
                if post_type == 'news':
                    flash('Erro ao tentar deletar a notícia', 'danger')
                elif post_type == 'notice':
                    flash('Erro ao tentar deletar o aviso', 'danger')
                elif post_type == 'ad':
                    flash('Erro ao tentar deletar o anúncio', 'danger')
            
    return render_template('/posts/deletar.html', post_type=post_type, pergunta=pergunta, postId=id, configuration=configuration), 200


# NOTIFICA USUÁRIO ADMINISTRADORES POR EMAIL
def send_post_email(title, message):
    reci = ['uniplacdigital@gmail.com']
    users = User.query.filter(User.role == 'admin').all()
    for user in users:
        reci.append(user.email)

    msg = Message(title,
                  sender='contato@uniplacdigital.com.br',
                  recipients=reci)
    msg.body = f'''{message}'''
    mail.send(msg)