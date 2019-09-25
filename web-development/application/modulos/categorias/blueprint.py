import os
from flask import current_app, Blueprint, render_template, request, url_for
from modulos.categorias.formularios import CategoriaForm

categoriaBP = Blueprint('categorias', __name__, url_prefix='/admin/categorias', template_folder='templates', static_folder='static')

@categoriaBP.route('/')
def index():
    return render_template('/categorias/index.html'), 200

@categoriaBP.route('/cadastrar', methods=['GET','POST'])
def cadastrar():
    form = CategoriaForm(request.form)
    titulo = 'Cadastro'
    if form.validate_on_submit():
        print("valido")
    return render_template('/categorias/formulario.html' , titulo=titulo, form=form), 200

@categoriaBP.route('/editar')
def editar():
    titulo = 'Edição'
    return render_template('/categorias/formulario.html' , titulo=titulo), 200

@categoriaBP.route('/deletar', methods=['GET', 'POST'])
def deletar():
    titulo = 'Deseja realmente excluir a categoria [00321]'
    return render_template('/categorias/deletar.html', titulo=titulo), 200
