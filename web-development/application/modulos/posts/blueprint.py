import os
from flask import current_app, Blueprint, render_template, request, url_for, flash, session, redirect
from modulos.posts.formularios import PostForm
from modulos.tags.formularios import TagForm

from app import app
from sqlalchemy import desc, or_, and_, asc
from database.Model import Configuration, db, Post, Category, User, Tag, TagPost
from datetime import datetime

postBP = Blueprint('posts', __name__, url_prefix='/admin', template_folder='templates', static_folder='static')

@postBP.route('/noticias')
def noticias_index():
    configuration = Configuration.query.first()
    users = User.query.filter(or_(User.role == 'admin', User.role == 'editor')).all()
    titulo = 'Notícias'

    current_datetime = datetime.now()

    # pega os argumentos da string, se existir, senão, seta valores padrão
    page = '1' if (request.args.get('page') == None) else request.args.get('page')
    name = '' if (request.args.get('name') == None) else request.args.get('name')
    category = '' if (request.args.get('category') == None) else request.args.get('category')
    status = '' if (request.args.get('status') == None) else request.args.get('status')
    order_by = 'id' if (request.args.get('order_by') == None) else request.args.get('order_by')
    order = 'desc' if (request.args.get('order') == None) else request.args.get('order')
    author = '' if (request.args.get('author') == None) else request.args.get('author')
    publication = '' if (request.args.get('publication') == None) else request.args.get('publication')
    tagg = '' if (request.args.get('tagg') == None) else request.args.get('tagg')

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
    filter = (Post.genre == 'news', )
    if category:
        filter = filter + (Post.category_id == category,)
    if name:
        filter = filter + (or_(Post.title.like('%'+name+'%'), Post.description.like('%'+name+'%'), Post.content.like('%'+name+'%')),)
    if status:
        filter = filter + (Post.status == status,)

    if tagg:
        for tag in post.tags:
            if tag.id == tagg:
                filter = filter + (tag.id == tagg)

    if author:
        filter = filter + (Post.user_id == author, )
    if publication == 'current':
        filter = filter + (and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime),)
    elif publication == 'expired':
        filter = filter + (and_(Post.departure_date < current_datetime),)
    elif publication == 'scheduled':
        filter = filter + (and_(Post.entry_date > current_datetime),)

    # gera o order_by
    if order == 'asc':
        query_order = asc(order_by)
    else:
        query_order = desc(order_by)

    # consulta o banco de dados retornando o paginate e os dados
    paginate = Post.query.filter(*filter).order_by(query_order).paginate(page=page, per_page=10, error_out=False)
    posts = paginate.items

    categories = Category.query.filter()

    return render_template('/posts/index.html', tagg=tagg, categories=categories, paginate=paginate, posts=posts, currentPage=page, name=name, category=category, status=status, order_by=order_by, order=order, titulo=titulo, configuration=configuration, users=users, author=author, publication=publication), 200


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
            
            #adiciona a tag no banco
            
            tags = form.tag.data
            array_tags = tags.split(',')
            for t in array_tags:
                tag = Tag.query.filter((Tag.name==t)).first()
                if tag:
                    post.tags.append(tag)
        
                else:
                    tag = Tag(t)
                    post.tags.append(tag)


            # adiciona e commita a categoria na base de dados
            db.session.add(post)
            db.session.commit()



            app.logger.warning(' %s cadastrou a noticia %s', session.get('user_name', ''), post.title)

            # flash message e redireciona pra mesma tela para limpar o objeto request
            flash('Notícia cadastrada com sucesso', 'success')
            return redirect(url_for('posts.noticias_index'))
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

    
    strtags = ''
    for tag in post.tags:
        strtags = strtags+str(tag.name)+','

    if strtags.endswith(','):
        strtags = strtags[:-1]
        

    titulo = 'Editar Notícia'
    
    if request.form:
        # formulário preenchido pelo objeto request, caso exista
        form = PostForm(request.form)
    else:
        # formulário vazio
        form = PostForm()
        form.tag.data = strtags

        # preenche formulário com post recuperado pelo id
        fillForm(form, post, 'news')


    


    clearDateValidatons(post, form)

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
            #post.user_id = session.get('user_id', '')
            post.category_id = form.category_id.data

                           

            id_tags=[]
            #Edição de tags
            for t in post.tags:
                id_tags.append(t.id)
            
            for t in id_tags:   
                tag=Tag.query.get(t)
                post.tags.remove(tag)

            tags = form.tag.data
            array_tags = tags.split(',')

            for t in array_tags:
                tag = Tag.query.filter((Tag.name==t)).first()
                if tag:
                    post.tags.append(tag)
        
                else:
                    tag = Tag(t)
                    post.tags.append(tag)

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
    configuration = Configuration.query.first()
    users = User.query.all()
    titulo = 'Anúncios'

    current_datetime = datetime.now()

    # pega os argumentos da string, se existir, senão, seta valores padrão
    page = '1' if (request.args.get('page') == None) else request.args.get('page')
    name = '' if (request.args.get('name') == None) else request.args.get('name')
    category = '' if (request.args.get('category') == None) else request.args.get('category')
    status = '' if (request.args.get('status') == None) else request.args.get('status')
    order_by = 'id' if (request.args.get('order_by') == None) else request.args.get('order_by')
    order = 'desc' if (request.args.get('order') == None) else request.args.get('order')
    author = '' if (request.args.get('author') == None) else request.args.get('author')
    publication = '' if (request.args.get('publication') == None) else request.args.get('publication')
    tagg = '' if (request.args.get('tagg') == None) else request.args.get('tagg')


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
    filter = (Post.genre == 'ad', )
    if category:
        filter = filter + (Post.category_id == category,)
    if name:
        filter = filter + (or_(Post.title.like('%'+name+'%'), Post.description.like('%'+name+'%'), Post.content.like('%'+name+'%')),)
    
    
    
    if status:
        filter = filter + (Post.status == status,)


    if tagg:
        for tag in post.tags:
            if tag.id == tagg:
                filter = filter + (tag.id == tagg)

    if author:
        filter = filter + (Post.user_id == author, )
    if publication == 'current':
        filter = filter + (and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime),)
    elif publication == 'expired':
        filter = filter + (and_(Post.departure_date < current_datetime),)
    elif publication == 'scheduled':
        filter = filter + (and_(Post.entry_date > current_datetime),)

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

    categories = Category.query.filter()

    return render_template('/posts/index.html',tagg=tagg ,categories=categories, paginate=paginate, posts=posts, currentPage=page, name=name, category=category, status=status, order_by=order_by, order=order, titulo=titulo, configuration=configuration, users=users, author=author, publication=publication), 200

@postBP.route('/anuncios/cadastrar', methods=['GET','POST'])
def anuncios_cadastrar():
    configuration = Configuration.query.first()
    form = PostForm(request.form)
    titulo = 'Cadastrar Anúncios'
    operacao = 'Cadastro'
    
    if session.get('user_role', '') == 'user':
        form.status.validators = []

    
        
    if form.validate_on_submit():
        try:
            form.user_id = session.get('user_id', '')

            # cria o post com os dados do formulário
            post = Post(
                form.title.data,
                form.description.data,
                form.content.data,
                'ad',
                '',
                form.entry_date.data,
                form.departure_date.data,
                None,
                form.user_id,
                form.category_id.data
            )
            
            if session.get('user_role', '') == 'user':
                post.status = 'pending'
            else:
                post.status = form.status.data
            
            if form.image_id.data != '':
                post.image_id = form.image_id.data


            #adiciona a tag no banco
            
            tags = form.tag.data
            array_tags = tags.split(',')
            for t in array_tags:
                tag = Tag.query.filter((Tag.name==t)).first()
                if tag:
                    post.tags.append(tag)
        
                else:
                    tag = Tag(t)
                    post.tags.append(tag)

            # adiciona e commita a categoria na base de dados
            db.session.add(post)
            db.session.commit()

            app.logger.warning(' %s cadastrou o anúncio %s', session.get('user_name', ''), post.title)

            # flash message e redireciona pra mesma tela para limpar o objeto request
            flash('Anúncio cadastrado com sucesso', 'success')
            return redirect(url_for('posts.anuncios_index'))
        except:
            # remove qualquer vestígio do usuário da sessin e flash message 
            db.session.rollback()
            flash('Erro ao tentar cadastrar o anúncio', 'danger')
    return render_template('/posts/formulario.html', titulo=titulo, operacao=operacao, form=form, configuration=configuration), 200

@postBP.route('/anuncios/editar/<int:id>', methods=['GET','POST'])
def anuncios_editar(id):
    
    configuration = Configuration.query.first()

    # pega o post pelo id e com o genero anuncio
    post = Post.query.filter(and_(Post.id==id, Post.genre=='ad')).first()

    if not post:
        flash('O anúncio não existe', 'info')
        return redirect(url_for('posts.anuncios_index'))

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


    titulo = 'Editar Anúncio'

    if request.form:
        # formulário preenchido pelo objeto request, caso exista
        form = PostForm(request.form)
    else:
        # formulário vazio
        form = PostForm()
        form.tag.data = strtags

        # preenche formulário com post recuperado pelo id
        fillForm(form, post, 'ad')

    # se usuário nível 4, remove validator
    if session.get('user_role', '') == 'user':
        form.status.validators = []

    clearDateValidatons(post, form)

    if form.validate_on_submit():
        try:
            post.title = form.title.data
            post.description = form.description.data
            post.content = form.content.data
            post.genre = 'ad'
            if session.get('user_role', '') == 'user':
                post.status = 'pending'
            else:
                post.status = form.status.data
            post.entry_date = form.entry_date.data
            post.departure_date = form.departure_date.data
            post.image_id = None
            if (form.image_id.data != ''):
                post.image_id = form.image_id.data
            #post.user_id = session.get('user_id', '')
            post.category_id = form.category_id.data


            id_tags=[]
            #Edição de tags
            for t in post.tags:
                id_tags.append(t.id)
            
            for t in id_tags:   
                tag=Tag.query.get(t)
                post.tags.remove(tag)

            tags = form.tag.data
            array_tags = tags.split(',')

            for t in array_tags:
                tag = Tag.query.filter((Tag.name==t)).first()
                if tag:
                    post.tags.append(tag)
        
                else:
                    tag = Tag(t)
                    post.tags.append(tag)

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
    users = User.query.filter(or_(User.role == 'admin', User.role == 'author')).all()
    titulo = 'Avisos'

    current_datetime = datetime.now()

    # pega os argumentos da string, se existir, senão, seta valores padrão
    page = '1' if (request.args.get('page') == None) else request.args.get('page')
    name = '' if (request.args.get('name') == None) else request.args.get('name')
    category = '' if (request.args.get('category') == None) else request.args.get('category')
    status = '' if (request.args.get('status') == None) else request.args.get('status')
    order_by = 'id' if (request.args.get('order_by') == None) else request.args.get('order_by')
    order = 'desc' if (request.args.get('order') == None) else request.args.get('order')
    author = '' if (request.args.get('author') == None) else request.args.get('author')
    publication = '' if (request.args.get('publication') == None) else request.args.get('publication')
    tagg = '' if (request.args.get('tagg') == None) else request.args.get('tagg')


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
    filter = (Post.genre == 'notice', )
    if category:
        filter = filter + (Post.category_id == category,)
    if name:
        filter = filter + (or_(Post.title.like('%'+name+'%'), Post.description.like('%'+name+'%'), Post.content.like('%'+name+'%')),)
    if status:
        filter = filter + (Post.status == status,)

    if tagg:
        for tag in post.tags:
            if tag.id == tagg:
                filter = filter + (tag.id == tagg)


    if author:
        filter = filter + (Post.user_id == author, )
    if publication == 'current':
        filter = filter + (and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime),)
    elif publication == 'expired':
        filter = filter + (and_(Post.departure_date < current_datetime),)
    elif publication == 'scheduled':
        filter = filter + (and_(Post.entry_date > current_datetime),)

    # gera o order_by
    if order == 'asc':
        query_order = asc(order_by)
    else:
        query_order = desc(order_by)

    # consulta o banco de dados retornando o paginate e os dados
    paginate = Post.query.filter(*filter).order_by(query_order).paginate(page=page, per_page=10, error_out=False)
    posts = paginate.items

    categories = Category.query.filter()

    return render_template('/posts/index.html', tagg=tagg, categories=categories, paginate=paginate, posts=posts, currentPage=page, name=name, category=category, status=status, order_by=order_by, order=order, titulo=titulo, configuration=configuration, users=users, author=author, publication=publication), 200

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

            #adiciona a tag no banco
            
            tags = form.tag.data
            array_tags = tags.split(',')
            for t in array_tags:
                tag = Tag.query.filter((Tag.name==t)).first()
                if tag:
                    post.tags.append(tag)
        
                else:
                    tag = Tag(t)
                    post.tags.append(tag)

            # adiciona e commita a categoria na base de dados
            db.session.add(post)
            db.session.commit()

            app.logger.warning(' %s cadastrou o aviso %s', session.get('user_name', ''), post.title)

            # flash message e redireciona pra mesma tela para limpar o objeto request
            flash('Aviso cadastrado com sucesso', 'success')
            return redirect(url_for('posts.avisos_index'))
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

    strtags = ''
    for tag in post.tags:
        strtags = strtags+str(tag.name)+','

    if strtags.endswith(','):
        strtags = strtags[:-1]

    titulo = 'Editar Aviso'

    if request.form:
        # formulário preenchido pelo objeto request, caso exista
        form = PostForm(request.form)
    else:
        # formulário vazio
        form = PostForm()
        form.tag.data = strtags

        # preenche formulário com post recuperado pelo id
        fillForm(form, post, 'notice')

    clearDateValidatons(post, form)
    
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
            #post.user_id = session.get('user_id', '')
            post.category_id = form.category_id.data

            id_tags=[]
            #Edição de tags
            for t in post.tags:
                id_tags.append(t.id)
            
            for t in id_tags:   
                tag=Tag.query.get(t)
                post.tags.remove(tag)

            tags = form.tag.data
            array_tags = tags.split(',')

            for t in array_tags:
                tag = Tag.query.filter((Tag.name==t)).first()
                if tag:
                    post.tags.append(tag)
        
                else:
                    tag = Tag(t)
                    post.tags.append(tag)

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



@postBP.route('/meus-posts')
def meus_posts():
    configuration = Configuration.query.first()
    titulo = 'Minhas Publicações'

    # pega os argumentos da string, se existir, senão, seta valores padrão
    page = '1' if (request.args.get('page') == None) else request.args.get('page')
    name = '' if (request.args.get('name') == None) else request.args.get('name')
    category = '' if (request.args.get('category') == None) else request.args.get('category')
    status = '' if (request.args.get('status') == None) else request.args.get('status')
    order_by = 'id' if (request.args.get('order_by') == None) else request.args.get('order_by')
    order = 'desc' if (request.args.get('order') == None) else request.args.get('order')

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
    filter = (Post.user_id == session.get('user_id', ''), )
    if category:
        filter = filter + (Post.category_id == category,)
    if name:
        filter = filter + (or_(Post.title.like('%'+name+'%'), Post.description.like('%'+name+'%'), Post.content.like('%'+name+'%')),)
    if status:
        filter = filter + (Post.status == status,)

    # gera o order_by
    if order == 'asc':
        query_order = asc(order_by)
    else:
        query_order = desc(order_by)

    # consulta o banco de dados retornando o paginate e os dados
    paginate = Post.query.filter(*filter).order_by(query_order).paginate(page=page, per_page=10, error_out=False)
    posts = paginate.items

    categories = Category.query.filter()

    return render_template('/posts/index.html', categories=categories, paginate=paginate, posts=posts, currentPage=page, name=name, category=category, status=status, order_by=order_by, order=order, titulo=titulo, configuration=configuration, fromUser=True), 200



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