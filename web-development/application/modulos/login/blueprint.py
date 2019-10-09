import os
from flask import current_app, Blueprint, render_template, request, url_for, redirect, flash, session
from app import app, bcrypt
from sqlalchemy import and_, desc
from database.Model import db, User
from modulos.login.formularios import LoginForm, RecoverForm
from database.Model import Configuration


loginBP = Blueprint('login', __name__, url_prefix='/login', template_folder='templates', static_folder='static')

@loginBP.route('/', methods=['GET','POST'])
def inicio():
    configuration = Configuration.query.first()
    form= LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter(User.registry == form.registry.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                session.clear()
                session.permanent = True
                session['user_id'] = user.id
                session['user_avatar'] = user.image_id
                session['user_name'] = user.first_name
                session['user_role'] = user.role
                app.logger.warning(' %s se logou na aplicação', user.first_name)
                return redirect( url_for('dashboard.dash') )
            else:
                flash('Credenciais inválidas', 'danger')
        else:
            flash('Credenciais inválidas', 'danger')
    return render_template('login.html', form=form, configuration=configuration) , 200


@loginBP.route('/recuperar-senha', methods=['GET','POST'])
def recuperar():
    configuration = Configuration.query.first()
    form= RecoverForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter(User.registry == form.registry.data).first()
        if user:
            print('sucesso')
        else:
            flash('Número de matrícula inválido.', 'danger')
    return render_template('recover.html', form=form, configuration=configuration) , 200


@loginBP.route('/logout')
def logout():
    configuration = Configuration.query.first()
    app.logger.warning(' %s deslogou da aplicação', session.get('user_name', ''))
    session.pop('user_id')
    session.pop('user_avatar')
    session.pop('user_name')
    session.pop('user_role')
    session.clear()
    return redirect( url_for('login.inicio') )
