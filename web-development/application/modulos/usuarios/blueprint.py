import os
from flask import current_app, Blueprint, render_template, request, url_for


usuarioBP = Blueprint('usuarios', __name__, url_prefix='/admin/usuarios', template_folder='templates', static_folder='static')


@usuarioBP.route('/')
def index():
    titulo = 'Lista de Usuários'
    return render_template('usuarios/index.html', titulo=titulo), 200


@usuarioBP.route('/cadastrar')
def cadastrar():
    titulo = 'Cadastrar usuário'
    return render_template('usuarios/formulario.html', titulo=titulo), 200


@usuarioBP.route('/editar')
def editar():
    titulo = 'Editar usuário'
    return render_template('usuarios/formulario.html', titulo=titulo), 200


@usuarioBP.route('/deletar', methods=['GET', 'POST'])
def deletar():
    titulo = 'Deseja realmente excluir o usuário [0002223]'
    return render_template('usuarios/deletar.html', titulo=titulo), 200
