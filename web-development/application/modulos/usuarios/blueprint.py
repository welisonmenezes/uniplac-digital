import os
from flask import current_app, Blueprint, render_template, request, url_for
from modulos.usuarios.formularios import UsuarioForm

usuarioBP = Blueprint('usuarios', __name__, url_prefix='/admin/usuarios', template_folder='templates', static_folder='static')


@usuarioBP.route('/')
def index():
    titulo = 'Lista de Usuários'
    return render_template('usuarios/index.html', titulo=titulo), 200


@usuarioBP.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    titulo = 'Cadastrar usuário'
    form = UsuarioForm(request.form)
    if form.validate_on_submit():
        print('valido')
    return render_template('usuarios/formulario.html', titulo=titulo, form=form, mode='cadastrar'), 200


@usuarioBP.route('/editar', methods=['GET', 'POST'])
def editar():
    titulo = 'Editar usuário'
    if request.form:
        form = UsuarioForm(request.form)
    else:
        form = UsuarioForm()
        form.first_name.data = 'Welison'
        form.last_name.data = 'Menezes'
        form.registry.data = '111111'
        form.role.data = 'admin'
        form.email.data = 'welison@email.com'
        form.phone.data = '2222-3333'
    form.password.validators = []
    if form.validate_on_submit():
        print('valido')
    return render_template('usuarios/formulario.html', titulo=titulo, form=form, mode='editar'), 200


@usuarioBP.route('/deletar', methods=['GET', 'POST'])
def deletar():
    titulo = 'Deseja realmente excluir o usuário [0002223]'
    return render_template('usuarios/deletar.html', titulo=titulo), 200
