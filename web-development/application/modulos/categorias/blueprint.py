import os
from flask import current_app, Blueprint, render_template, request, url_for, redirect, flash
from sqlalchemy import or_, desc
from modulos.categorias.formularios import CategoriaForm
from modulos.categorias.validations import validateCategoryToCreate
from database.Model import db, Category

categoriaBP = Blueprint('categorias', __name__, url_prefix='/admin/categorias', template_folder='templates', static_folder='static')

@categoriaBP.route('/')
def index():
    titulo = 'Lista de Categorias'

    # pega os argumentos da string, se existir, senão, seta valores padrão
    page = 1 if (request.args.get('page') == None) else int(request.args.get('page'))
    name = '' if (request.args.get('name') == None) else request.args.get('name')

    # implementa o filtro se necessário
    filter = ()
    if name:
        filter = filter + (Category.name == name,)

    # consulta o banco de dados retornando o paginate e os dados
    paginate = Category.query.filter(*filter).order_by((Category.id)).paginate(page=page, per_page=10, error_out=False)
    categories = paginate.items

    return render_template('/categorias/index.html', paginate=paginate, categories=categories, currentPage=page, name=name, titulo=titulo), 200

@categoriaBP.route('/cadastrar', methods=['GET','POST'])
def cadastrar():
    form = CategoriaForm(request.form)
    titulo = 'Cadastro'
    if form.validate_on_submit():
        try:
            if validateCategoryToCreate(form):
                # cria a categoria com os dados do formulário
                category = Category(
                    form.name.data,
                    form.description.data
                )
                # adiciona e commita a categoria na base de dados
                db.session.add(category)
                db.session.commit()

                # flash message e redireciona pra mesma tela para limpar o objeto request
                flash('Categoria cadastrada com sucesso', 'success')
                return redirect(url_for('categorias.cadastrar'))
        except:
            # remove qualquer vestígio do usuário da sessin e flash message 
            db.session.rollback()
            flash('Erro ao tentar cadastrar a categoria', 'danger')
    return render_template('/categorias/formulario.html' , titulo=titulo, form=form), 200

@categoriaBP.route('/editar', methods=['GET', 'POST'])
def editar():
    form = CategoriaForm(request.form)
    titulo = 'Edição'
    if form.validate_on_submit():
        print("valido")
    return render_template('/categorias/formulario.html' , titulo=titulo, form=form), 200

@categoriaBP.route('/deletar', methods=['GET', 'POST'])
def deletar():
    titulo = 'Deseja realmente excluir a categoria [00321]'
    return render_template('/categorias/deletar.html', titulo=titulo), 200
