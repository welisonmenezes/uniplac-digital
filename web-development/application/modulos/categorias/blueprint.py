import os
from flask import current_app, Blueprint, render_template, request, url_for

categoriaBP = Blueprint('categorias', __name__, url_prefix='/admin/categorias', template_folder='templates', static_folder='static')

@categoriaBP.route('/')
def index():
    return 'listagem de categorias aqui', 200

@categoriaBP.route('/cadastrar')
def cadastrar():
    return 'formulário de cadastro de categoria aqui', 200


@categoriaBP.route('/editar')
def editar():
    return 'formulário de edição de categoria aqui', 200


@categoriaBP.route('/deletar')
def deletar():
    return 'lógica para remover categoria aqui', 200
