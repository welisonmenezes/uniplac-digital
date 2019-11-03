from flask import current_app, Blueprint, render_template, request, url_for, redirect, flash, session
from sqlalchemy import desc, asc
from app import app
#trocar informações daqui.....
from modulos.tags.formularios import TagForm
from modulos.tags.validations import validateTagToCreate, validateTagToUpdate
from database.Model import db, Post, Tag
from database.Model import Configuration

tagBP = Blueprint('tags', __name__, url_prefix='/admin/tags', template_folder='templates', static_folder='static')

@tagBP.route('/')
def index():
    configuration = Configuration.query.first()
    titulo = 'Tags'

    # pega os argumentos da string, se existir, senão, seta valores padrão
    page = '1' if (request.args.get('page') == None) else request.args.get('page')
    name = '' if (request.args.get('name') == None) else request.args.get('name')
    order_by = 'id' if (request.args.get('order_by') == None) else request.args.get('order_by')
    order = 'desc' if (request.args.get('order') == None) else request.args.get('order')

    # previne erro ao receber string
    try:
        page = int(page)
    except:
        page = 1

    # previne erro ao recebe string inválida
    if not order_by in ['id', 'name', 'created_at']:
        order_by = 'id'

    # previne erro ao recebe string inválida
    if not order in ['desc', 'asc']:
        order = 'desc'

    # implementa o filtro se necessário
    filter = ()
    if name:
        filter = filter + (Tag.name.like('%'+name+'%'),)

    # gera o order_by
    if order == 'asc':
        query_order = asc(order_by)
    else:
        query_order = desc(order_by)

    # consulta o banco de dados retornando o paginate e os dados
    paginate = Tag.query.filter(*filter).order_by(query_order).paginate(page=page, per_page=10, error_out=False)
    tags = paginate.items

    return render_template('/tags/index.html', paginate=paginate, tags=tags, currentPage=page, name=name, order_by=order_by, order=order, titulo=titulo, configuration=configuration), 200

@tagBP.route('/cadastrar', methods=['GET','POST'])
def cadastrar():
    configuration = Configuration.query.first()
    form = TagForm(request.form)
    titulo = 'Cadastro'
    if form.validate_on_submit():
        try:
            if validateTagToCreate(form):
                # cria a tag com os dados do formulário
                tag = Tag(
                    form.name.data
                    
                )
                
                # adiciona e commita a tag na base de dados
                db.session.add(tag)
                db.session.commit()

                app.logger.warning(' %s cadastrou a tag %s', session.get('user_name', ''), tag.id)

                # flash message e redireciona pra mesma tela para limpar o objeto request
                flash('Tag cadastrada com sucesso', 'success')
                return redirect(url_for('tags.index'))
        except:
            # remove qualquer vestígio do usuário da sessin e flash message 
            db.session.rollback()
            flash('Erro ao tentar cadastrar a tag', 'danger')
    return render_template('/tags/formulario.html' , titulo=titulo, form=form, configuration=configuration), 200

@tagBP.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    configuration = Configuration.query.first()
    # pega a tags pelo id
    tag = Tag.query.filter((Tag.id==id)).first()
    
    # se não existe a tag
    if not tag:
        flash('A tag não exite', 'info')
        return redirect(url_for('tags.index'))
    
    titulo = 'Edição'

    if request.form:
        # formulário preenchido pelo objeto request, caso exista
        form = TagForm(request.form)
    else:
        # formulário vazio
        form = TagForm()

        #preenche formulário com a tag recuperada pelo id
        fillForm(form, tag)

    if form.validate_on_submit():
        try:
            if validateTagToUpdate(form, tag):
                # atualiza a tag recuperada pelo id com os dados do formulário
                tag.name = form.name.data
                

                 # commita os dados na base de dados
                db.session.commit()

                app.logger.warning(' %s editou a tag %s', session.get('user_name', ''), tag.id)

                 # flash message e redireciona pra mesma tela para limpar o objeto request
                flash('Tag editada com sucesso', 'success')
                return redirect(url_for('tags.index', id=id))
        except:
            # remove qualquer vestígio da tag do session e flash message
            db.session.rollback()
            flash('Erro ao tentar editar a tag', 'danger')
    return render_template('/tags/formulario.html' , titulo=titulo, form=form, configuration=configuration), 200

@tagBP.route('/deletar/<int:id>', methods=['GET', 'POST'])
def deletar(id):
    configuration = Configuration.query.first()

    #pega a tag pelo id
    tag = Tag.query.filter((Tag.id==id)).first()

    # se não existe a tag
    if not tag:
        flash('A tag não existe', 'info')
        return redirect(url_for('tags.index'))

    if request.method == 'POST':
        tagId = request.values.get('tagId')
        if tagId:
            # verifica se a tags esta em algum post
            post = Post.query.filter_by(tag_id=tagId).first()
            if not post:
            
                try:

                    app.logger.warning(' %s deletou a tag %s', session.get('user_name', ''), tag.id)

                    db.session.delete(tag)
                    db.session.commit()
                    flash('Tag deletada com sucesso', 'success')
                    return redirect(url_for('tags.index'))
                except:
                    db.session.rollback()
                    flash('Erro ao tentar excluir a tag', 'danger')
            else:
                flash('A tag não pode ser deletada pois existem posts relacionadas a ela na base de dados', 'warning')
            
    titulo = 'Deseja realmente excluir a tag ' + tag.name
    return render_template('/tags/deletar.html', titulo=titulo, tagId=id, configuration=configuration), 200

    # popula os campos do formuário
def fillForm(form, tag):
    form.name.data = tag.name
