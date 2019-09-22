import os
from flask import current_app, Blueprint, render_template, request, url_for

usuarioBP = Blueprint('usuarios', __name__, url_prefix='/usuarios', template_folder='templates', static_folder='static')

@usuarioBP.route('/')
def index():
    return 'listagem de usuários aqui', 200


@usuarioBP.route('/cadastrar')
def cadastrar():
    return 'formulário de cadastro de usuário aqui', 200


@usuarioBP.route('/editar')
def editar():
    return 'formulário de edição de usuário aqui', 200


@usuarioBP.route('/deletar')
def deletar():
    return 'lógica para remover usuário aqui', 200
