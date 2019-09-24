import os
from flask import current_app, Blueprint, render_template, request, url_for, flash, redirect
from sqlalchemy import or_, desc
from app import bcrypt
from modulos.usuarios.formularios import UsuarioForm
from database.Model import db, User
from modulos.usuarios.validations import validateUserToCreate, validateUserToUpdate

usuarioBP = Blueprint('usuarios', __name__, url_prefix='/admin/usuarios', template_folder='templates', static_folder='static')


@usuarioBP.route('/')
def index():
    titulo = 'Lista de Usuários'
    page = 1 if (request.args.get('page') == None) else int(request.args.get('page'))
    paginate = User.query.filter().order_by(desc(User.id)).paginate(page=page, per_page=1, error_out=False)
    users = paginate.items
    return render_template('usuarios/index.html', titulo=titulo, users=users, paginate=paginate, currentPage=page), 200


@usuarioBP.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    titulo = 'Cadastrar usuário'
    form = UsuarioForm(request.form)
    if form.validate_on_submit():
        try:
            if validateUserToCreate(form):
                # cria o usuario com os dados do formulário
                user = User(
                    form.first_name.data,
                    form.last_name.data,
                    form.registry.data,
                    bcrypt.generate_password_hash(form.password.data),
                    form.role.data,
                    form.email.data,
                    form.phone.data,
                    None
                )
                if form.image_id.data != '':
                    user.image_id = form.image_id.data

                # adiciona e commita o usuário na base de dadso
                db.session.add(user)
                db.session.commit()

                # flash message e redireciona pra mesma tela para limpar o objeto request
                flash('Usuário cadastrado com sucesso', 'success')
                return redirect(url_for('usuarios.cadastrar'))
        except:
            # remove qualquer vestígio do usuário da sessin e flash message 
            db.session.rollback()
            flash('Erro ao tentar cadastrar o usuário', 'danger')
    return render_template('usuarios/formulario.html', titulo=titulo, form=form, mode='cadastrar'), 200


@usuarioBP.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):

    # pega o usuário pelo id
    user = User.query.filter((User.id==id)).first()

    # se não existe o usuário, bye
    if not user:
        flash('O usuário não existe', 'info')
        return redirect(url_for('usuarios.index'))

    titulo = 'Editar usuário'

    if request.form:
        # formulário preenchido pelo objeto request, caso exista
        form = UsuarioForm(request.form)
    else:
        # formulário vazio
        form = UsuarioForm()

        # preenche formulário com usuário recuperado pelo id
        fillForm(form, user)

    # remove validação da senha
    form.password.validators = []
    if form.validate_on_submit():
        try:
            if validateUserToUpdate(form, user):

                # atualiza o usuário recuperado pelo id com os dados do formulário
                user.first_name = form.first_name.data
                user.last_name = form.last_name.data
                user.registry = form.registry.data
                user.role = form.role.data
                user.email = form.email.data
                user.phone = form.phone.data
                if (form.image_id.data != ''):
                    user.image_id = form.image_id.data
                if (form.password.data != ''):
                    user.password = bcrypt.generate_password_hash(form.password.data)

                # commita os dados na base de dados
                db.session.commit()

                # flash message e redireciona pra mesma tela para limpar o objeto request
                flash('Usuário editado com sucesso', 'success')
                return redirect(url_for('usuarios.editar', id=id))
        except:
            # remove qualquer vestígio do usuário da sessin e flash message
            db.session.rollback()
            flash('Erro ao tentar editar o usuário', 'danger')
    return render_template('usuarios/formulario.html', titulo=titulo, form=form, mode='editar'), 200


@usuarioBP.route('/deletar', methods=['GET', 'POST'])
def deletar():
    titulo = 'Deseja realmente excluir o usuário [0002223]'
    return render_template('usuarios/deletar.html', titulo=titulo), 200


# popula os campos do formuário
def fillForm(form, user):
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.registry.data = user.registry
    form.role.data = user.role
    form.email.data = user.email
    form.phone.data = user.phone
    form.image_id.data = None
    if (user.image_id != ''):
        form.image_id.data = user.image_id