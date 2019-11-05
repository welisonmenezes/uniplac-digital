import os
from flask import current_app, Blueprint, render_template, request, url_for, flash, redirect, session
from datetime import datetime
from flask_mail import Message
from sqlalchemy import desc, and_, or_, asc
from app import mail
from modulos.site.formularios import ContactForm
from database.Model import Configuration, Category, Post, ConfigurationImage, User, Tag, TagPost

siteBP = Blueprint('site', __name__, url_prefix='/', template_folder='templates', static_folder='static')

@siteBP.route('/')
def index():
    configuration = Configuration.query.first()
    categories = Category.query.order_by(desc(Category.id)).all()
    categories_highlighted = Category.query.filter((Category.is_highlighted==1)).order_by(desc(Category.id)).all()
    users = User.query.order_by(asc(User.first_name)).all()
    current_datetime = datetime.now()
    tags = Tag.query.join(Post, Tag.posts).filter(and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime, Post.status=='approved')).order_by(asc(Tag.name)).all()

    news = Post.query.outerjoin(User, User.id == Post.user_id).outerjoin(Category, Category.id == Post.category_id).filter(and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime, Post.genre=='news', Post.status=='approved')).order_by(desc(Post.id)).limit(10)
    ads = Post.query.filter(and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime, Post.genre=='ad', Post.status=='approved')).order_by(desc(Post.id)).limit(6)
    notices = Post.query.filter(and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime, Post.genre=='notice', Post.status=='approved')).order_by(desc(Post.id)).limit(6)

    return render_template('site/site.html',tags=tags, news=news, ads=ads, notices=notices, configuration=configuration, categories=categories, categories_highlighted=categories_highlighted, users=users), 200


@siteBP.route('/noticias')
def noticias():
    return render_post_list_by_type('news', 'Notícias')


@siteBP.route('/noticias/<int:id>')
def noticias_detalhes(id):
    return render_post_detail_by_type('news', 'Notícias', id)


@siteBP.route('/anuncios')
def anuncios():
    return render_post_list_by_type('ad', 'Anúncios')


@siteBP.route('/anuncios/<int:id>')
def anuncios_detalhes(id):
    return render_post_detail_by_type('ad', 'Anúncios', id)


@siteBP.route('/avisos')
def avisos():
    return render_post_list_by_type('notice', 'Avisos')


@siteBP.route('/avisos/<int:id>')
def avisos_detalhes(id):
    return render_post_detail_by_type('notice', 'Avisos', id)


@siteBP.route('/filtro')
def filtro():
    return render_post_list_by_type('filter', 'Filtro')


@siteBP.route('/tag')
def tag():
    return render_post_list_by_type('tag', 'Tag')


@siteBP.route('/contato', methods=['GET','POST'])
def contato():
    configuration = Configuration.query.first()
    categories = Category.query.order_by(desc(Category.id)).all()
    categories_highlighted = Category.query.filter((Category.is_highlighted==1)).order_by(desc(Category.id)).all()
    users = User.query.order_by(asc(User.first_name)).all()

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
            flash('Desculpe, ocorreu um problema ao tentar enviar sua mensagem.', 'warning')
        
    return render_template('site/contato.html', form=form, configuration=configuration, categories=categories, categories_highlighted=categories_highlighted, users=users), 200


def render_post_list_by_type(post_type, title):
    titulo = title
    configuration = Configuration.query.first()
    categories = Category.query.order_by(desc(Category.id)).all()
    categories_highlighted = Category.query.filter((Category.is_highlighted==1)).order_by(desc(Category.id)).all()
    users = User.query.order_by(asc(User.first_name)).all()
    current_datetime = datetime.now()
    tags = Tag.query.join(Post, Tag.posts).filter(and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime, Post.status=='approved')).order_by(asc(Tag.name)).all()
    tag = ''
    

    # sidebar avisos
    if post_type == 'notice':
        notices = None
    else:
        notices = Post.query.filter(and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime, Post.genre=='notice', Post.status=='approved')).order_by(desc(Post.id)).limit(6)

    # filtro/paginação
    page = 1 if (request.args.get('page') == None) else int(request.args.get('page'))
    if post_type == 'filter':
        name = '' if (request.args.get('name') == None) else request.args.get('name')
        genre = '' if (request.args.get('genre') == None) else request.args.get('genre')
        category = '' if (request.args.get('category') == None) else request.args.get('category')
        author  = '' if (request.args.get('author') == None) else request.args.get('author')
        tag = '' if(request.args.get('tag') == None) else request.args.get('tag')
        
        
        # filtro
        filter = (and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime, Post.status=='approved'),)
        if category:
            filter = filter + (Post.category_id == category,)
        if name:
            filter = filter + (or_(Post.title.like('%'+name+'%'), Post.description.like('%'+name+'%'), Post.content.like('%'+name+'%')),)
        if genre:
            filter = filter + (Post.genre == genre,)
        if author:
            filter = filter + (Post.user_id == author,)
    elif(post_type == 'tag'): 
        filter = (and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime, Post.status=='approved'),)
        tag = '' if (request.args.get('tag') == None) else request.args.get('tag')
        filter = filter + ( Post.tags.any(id=tag),)
    else:
        # fitro
        filter = (and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime, Post.genre==post_type, Post.status=='approved'))
    
    # consulta o banco de dados retornando o paginate e os dados
    paginate = Post.query.outerjoin(User, User.id == Post.user_id).outerjoin(Category, Category.id == Post.category_id).filter(*filter).order_by(desc(Post.id)).paginate(page=page, per_page=10, error_out=False)
    posts = paginate.items

    if post_type == 'filter':
        return render_template('site/posts.html', tags=tags, tag=tag, notices=notices, posts=posts, titulo=titulo, name=name, category=category, genre=genre, currentPage=page, paginate=paginate, configuration=configuration, categories=categories, categories_highlighted=categories_highlighted, users=users, author=author), 200
    else:
        return render_template('site/posts.html', tags=tags, tag=tag, posts=posts, notices=notices, paginate=paginate, currentPage=page, titulo=titulo, configuration=configuration, categories=categories, categories_highlighted=categories_highlighted, users=users), 200


def render_post_detail_by_type(post_type, title, id):
    titulo = title 
    configuration = Configuration.query.first()
    categories = Category.query.order_by(desc(Category.id)).all()
    categories_highlighted = Category.query.filter((Category.is_highlighted==1)).order_by(desc(Category.id)).all()
    users = User.query.order_by(asc(User.first_name)).all()
    current_datetime = datetime.now()
    tags = Tag.query.join(Post, Tag.posts).filter(and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime, Post.status=='approved')).order_by(asc(Tag.name)).all()

    post = None

    # notícia
    if post_type == 'news':
        if session.get('user_role', '') == 'admin' or session.get('user_role', '') == 'editor':
            post = Post.query.filter(and_(Post.id==id, Post.genre=='news')).first()
        else:
            post = Post.query.filter(and_(Post.id==id, Post.genre=='news', Post.status=='approved', Post.entry_date <= current_datetime, Post.departure_date >= current_datetime)).first()

    # anuncio
    if post_type == 'ad':
        ps = Post.query.filter(Post.id==id).first()
        if ps:
            if session.get('user_role', '') == 'user':
                if session.get('user_id', '') == ps.user_id:
                    post = Post.query.filter(and_(Post.id==id, Post.user_id==session.get('user_id', ''), Post.genre=='ad', Post.status!='denied')).first()
                else: 
                    post = Post.query.filter(and_(Post.id==id, Post.genre=='ad', Post.status=='approved', Post.entry_date <= current_datetime, Post.departure_date >= current_datetime)).first()
            elif session.get('user_role', '') == '':
                post = Post.query.filter(and_(Post.id==id, Post.genre=='ad', Post.status=='approved', Post.entry_date <= current_datetime, Post.departure_date >= current_datetime)).first()
            else:
                post = Post.query.filter(and_(Post.id==id, Post.genre=='ad')).first()

    # aviso
    if post_type == 'notice':
        if session.get('user_role', '') == 'admin' or session.get('user_role', '') == 'author':
            post = Post.query.filter(and_(Post.id==id, Post.genre=='notice')).first()
        else:
            post = Post.query.filter(and_(Post.id==id, Post.genre=='notice', Post.status=='approved', Post.entry_date <= current_datetime, Post.departure_date >= current_datetime)).first()

    if not post:
        return redirect(url_for('error.pageNotFound'))

    user = User.query.filter(User.id==post.user_id).first()
    
    category = Category.query.filter(Category.id==post.category_id).first()
    notices = Post.query.filter(and_(Post.entry_date <= current_datetime, Post.departure_date >= current_datetime, Post.genre=='notice', Post.status=='approved')).order_by(desc(Post.id)).limit(6)

    return render_template('/site/detalhes.html', tags=tags, post=post, user=user, category=category, notices=notices, titulo=titulo, configuration=configuration, categories=categories, categories_highlighted=categories_highlighted, users=users), 200