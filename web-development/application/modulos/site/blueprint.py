import os
from flask import current_app, Blueprint, render_template, request, url_for, flash, redirect
from datetime import datetime
from flask_mail import Message
from sqlalchemy import desc, and_, or_
from app import mail
from modulos.site.formularios import ContactForm
from database.Model import Configuration, Category, Post, ConfigurationImage

siteBP = Blueprint('site', __name__, url_prefix='/', template_folder='templates', static_folder='static')
current_datetime = datetime.now()

@siteBP.route('/')
def index():
    configuration = Configuration.query.first()
    categories = Category.query.order_by(desc(Category.id)).all()
    categories_highlighted = Category.query.filter((Category.is_highlighted==1)).order_by(desc(Category.id)).all()
    
    news = Post.query.filter(and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime, Post.genre=='news', Post.status=='approved')).order_by(desc(Post.id)).limit(10)
    ads = Post.query.filter(and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime, Post.genre=='ad', Post.status=='approved')).order_by(desc(Post.id)).limit(6)
    notices = Post.query.filter(and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime, Post.genre=='notice', Post.status=='approved')).order_by(desc(Post.id)).limit(6)

    return render_template('site/site.html', news=news, ads=ads, notices=notices, configuration=configuration, categories=categories, categories_highlighted=categories_highlighted), 200


@siteBP.route('/noticias')
def noticias():
    titulo = 'Notícias'
    configuration = Configuration.query.first()
    categories = Category.query.order_by(desc(Category.id)).all()
    categories_highlighted = Category.query.filter((Category.is_highlighted==1)).order_by(desc(Category.id)).all()
    
    notices = Post.query.filter(and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime, Post.genre=='notice', Post.status=='approved')).order_by(desc(Post.id)).limit(6)

    # pega os argumentos da string, se existir, senão, seta valores padrão
    page = 1 if (request.args.get('page') == None) else int(request.args.get('page'))
    name = '' if (request.args.get('name') == None) else request.args.get('name')
    genre = '' if (request.args.get('genre') == None) else request.args.get('genre')
    category = '' if (request.args.get('category') == None) else request.args.get('category')

    # implementa o filtro se necessário
    filter = (and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime, Post.genre=='news', Post.status=='approved'))
    if category:
        filter = filter + (Post.category_id == category,)
    if name:
        filter = filter + (or_(Post.title.like('%'+name+'%'), Post.description.like('%'+name+'%'), Post.content.like('%'+name+'%')),)
    if genre:
        filter = filter + (Post.genre == genre,)
    
    # consulta o banco de dados retornando o paginate e os dados
    paginate = Post.query.filter(*filter).order_by(desc(Post.id)).paginate(page=page, per_page=10, error_out=False)
    posts = paginate.items

    return render_template('site/posts.html', posts=posts, notices=notices, paginate=paginate, currentPage=page, name=name, genre=genre, category=category, titulo=titulo, configuration=configuration, categories=categories, categories_highlighted=categories_highlighted), 200


@siteBP.route('/noticias/detalhes')
def noticias_detalhes():
    titulo = 'Notícias' 
    configuration = Configuration.query.first()
    categories = Category.query.order_by(desc(Category.id)).all()
    categories_highlighted = Category.query.filter((Category.is_highlighted==1)).order_by(desc(Category.id)).all()
    
    return render_template('/site/detalhes.html', titulo=titulo, configuration=configuration, categories=categories, categories_highlighted=categories_highlighted), 200


@siteBP.route('/anuncios')
def anuncios():
    titulo = 'Anúncios'
    configuration = Configuration.query.first()
    categories = Category.query.order_by(desc(Category.id)).all()
    categories_highlighted = Category.query.filter((Category.is_highlighted==1)).order_by(desc(Category.id)).all()
    
    notices = Post.query.filter(and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime, Post.genre=='notice', Post.status=='approved')).order_by(desc(Post.id)).limit(6)

    # pega os argumentos da string, se existir, senão, seta valores padrão
    page = 1 if (request.args.get('page') == None) else int(request.args.get('page'))
    name = '' if (request.args.get('name') == None) else request.args.get('name')
    genre = '' if (request.args.get('genre') == None) else request.args.get('genre')
    category = '' if (request.args.get('category') == None) else request.args.get('category')

    # implementa o filtro se necessário
    filter = (and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime, Post.genre=='ad', Post.status=='approved'))
    if category:
        filter = filter + (Post.category_id == category,)
    if name:
        filter = filter + (or_(Post.title.like('%'+name+'%'), Post.description.like('%'+name+'%'), Post.content.like('%'+name+'%')),)
    if genre:
        filter = filter + (Post.genre == genre,)
    
    # consulta o banco de dados retornando o paginate e os dados
    paginate = Post.query.filter(*filter).order_by(desc(Post.id)).paginate(page=page, per_page=10, error_out=False)
    posts = paginate.items

    return render_template('site/posts.html', posts=posts, notices=notices, category=category, name=name, genre=genre, paginate=paginate, currentPage=page, titulo=titulo, configuration=configuration, categories=categories, categories_highlighted=categories_highlighted), 200


@siteBP.route('/anuncios/detalhes')
def anuncios_detalhes():
    configuration = Configuration.query.first()
    categories = Category.query.order_by(desc(Category.id)).all()
    categories_highlighted = Category.query.filter((Category.is_highlighted==1)).order_by(desc(Category.id)).all()
    
    titulo = 'Anuncios'
    return render_template('/site/detalhes.html', titulo=titulo, configuration=configuration, categories=categories, categories_highlighted=categories_highlighted), 200


@siteBP.route('/avisos')
def avisos():
    titulo = 'Avisos'
    configuration = Configuration.query.first()
    categories = Category.query.order_by(desc(Category.id)).all()
    categories_highlighted = Category.query.filter((Category.is_highlighted==1)).order_by(desc(Category.id)).all()
    
    # pega os argumentos da string, se existir, senão, seta valores padrão
    page = 1 if (request.args.get('page') == None) else int(request.args.get('page'))
    name = '' if (request.args.get('name') == None) else request.args.get('name')
    genre = '' if (request.args.get('genre') == None) else request.args.get('genre')
    category = '' if (request.args.get('category') == None) else request.args.get('category')

    # implementa o filtro se necessário
    filter = (and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime, Post.genre=='notice', Post.status=='approved'))
    if category:
        filter = filter + (Post.category_id == category,)
    if name:
        filter = filter + (or_(Post.title.like('%'+name+'%'), Post.description.like('%'+name+'%'), Post.content.like('%'+name+'%')),)
    if genre:
        filter = filter + (Post.genre == genre,)
    
    # consulta o banco de dados retornando o paginate e os dados
    paginate = Post.query.filter(*filter).order_by(desc(Post.id)).paginate(page=page, per_page=10, error_out=False)
    posts = paginate.items

    return render_template('site/posts.html', posts=posts, category=category, name=name, genre=genre, paginate=paginate, currentPage=page, titulo=titulo, configuration=configuration, categories=categories, categories_highlighted=categories_highlighted), 200


@siteBP.route('/avisos/detalhes')
def avisos_detalhes():
    configuration = Configuration.query.first()
    categories = Category.query.order_by(desc(Category.id)).all()
    categories_highlighted = Category.query.filter((Category.is_highlighted==1)).order_by(desc(Category.id)).all()
   
    titulo = 'Avisos'
    return render_template('/site/detalhes.html', titulo=titulo, configuration=configuration, categories=categories, categories_highlighted=categories_highlighted), 200


@siteBP.route('/filtro')
def filtro():
    titulo = 'Filtro'
    configuration = Configuration.query.first()
    categories = Category.query.order_by(desc(Category.id)).all()
    categories_highlighted = Category.query.filter((Category.is_highlighted==1)).order_by(desc(Category.id)).all()
    
    notices = Post.query.filter(and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime, Post.genre=='notice', Post.status=='approved')).order_by(desc(Post.id)).limit(6)

    # pega os argumentos da string, se existir, senão, seta valores padrão
    page = 1 if (request.args.get('page') == None) else int(request.args.get('page'))
    name = '' if (request.args.get('name') == None) else request.args.get('name')
    genre = '' if (request.args.get('genre') == None) else request.args.get('genre')
    category = '' if (request.args.get('category') == None) else request.args.get('category')

    # implementa o filtro se necessário
    filter = (and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime, Post.status=='approved'),)
    if category:
        filter = filter + (Post.category_id == category,)
    if name:
        filter = filter + (or_(Post.title.like('%'+name+'%'), Post.description.like('%'+name+'%'), Post.content.like('%'+name+'%')),)
    if genre:
        filter = filter + (Post.genre == genre,)

    # consulta o banco de dados retornando o paginate e os dados
    paginate = Post.query.filter(*filter).order_by(desc(Post.id)).paginate(page=page, per_page=10, error_out=False)
    
    posts = paginate.items

    return render_template('site/posts.html', notices=notices, posts=posts, titulo=titulo, name=name, category=category, genre=genre, currentPage=page, paginate=paginate, configuration=configuration, categories=categories, categories_highlighted=categories_highlighted), 200


@siteBP.route('/contato', methods=['GET','POST'])
def contato():
    configuration = Configuration.query.first()
    categories = Category.query.order_by(desc(Category.id)).all()
    categories_highlighted = Category.query.filter((Category.is_highlighted==1)).order_by(desc(Category.id)).all()

    form = ContactForm(request.form)
    if form.validate_on_submit():
        try:
            msg = Message('Mensagem de - ' + form.name.data, sender='cntato@uniplacdigital.com.br', recipients=['uniplacdigital@gmail.com'])
            msg.html = "<h1>"+ form.assunto.data +"</h1>"
            msg.html += "<ul>"
            msg.html += "<li><b>Nome: </b> "+ form.name.data +"</li>"
            msg.html += "<li><b>Email: </b> "+ form.email.data +"</li>"
            msg.html += "<li><b>Descrição: </b> "+ form.text.data +"</li>"
            msg.html += "</ul>"
            mail.send(msg)
            flash('Mensagem enviada com sucesso.', 'success')
            return redirect(url_for('site.contato', _anchor='formulario'))
        except:
            flash('Descuple, ocorreu um problema ao tentar enviar sua mensagem.', 'warning')
        
    return render_template('site/contato.html', form=form, configuration=configuration, categories=categories, categories_highlighted=categories_highlighted), 200



