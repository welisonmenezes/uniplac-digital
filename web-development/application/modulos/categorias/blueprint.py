import os
from flask import current_app, Blueprint, render_template, request, url_for

categoriaBP = Blueprint('categorias', __name__, url_prefix='/admin/categorias', template_folder='templates', static_folder='static')

@categoriaBP.route('/')
def index():
    return render_template('/categorias/index.html'), 200

@categoriaBP.route('/cadastrar')
def cadastrar():
    titulo = 'Cadastro'
    return render_template('/categorias/formulario.html' , titulo=titulo), 200

@categoriaBP.route('/editar')
def editar():
    titulo = 'Edição'
    return render_template('/categorias/formulario.html' , titulo=titulo), 200

@categoriaBP.route('/deletar', methods=['GET', 'POST'])
def deletar():
    titulo = 'Deseja realmente excluir a categoria [00321]'
    return render_template('/categorias/deletar.html', titulo=titulo), 200
