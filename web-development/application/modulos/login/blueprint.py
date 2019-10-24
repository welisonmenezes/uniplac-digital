import os
from flask import current_app, Blueprint, render_template, request, url_for, redirect, flash, session
from app import app, bcrypt
from sqlalchemy import and_, desc
from flask_mail import Message
from app import mail
from database.Model import db, User
from modulos.login.formularios import LoginForm, RecoverForm, RequestResetForm, ResetPasswordForm
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
    return render_template('login.html', form=form, configuration=configuration), 200


@loginBP.route('/recuperar-senha', methods=['GET','POST'])
def recuperar():
    configuration = Configuration.query.first()
    """
    form= RecoverForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter(User.registry == form.registry.data).first()
        if user:
            msg = Message('Recuperação de senha do Usuário - ' + user.first_name, sender='cntato@uniplacdigital.com.br', recipients=['uniplacdigital@gmail.com'])
            msg.html = "<h1>"+ user.first_name + " " + user.last_name +" - Requisição de nova senha</h1>"
            msg.html += "<ul>"
            msg.html += "<li><b>Nome: </b> "+ user.first_name + " " + user.last_name +"</li>"
            msg.html += "<li><b>Email: </b> "+ user.email +"</li>"
            msg.html += "<li><b>Matrícula: </b> "+ user.registry +"</li>"
            msg.html += "</ul>"
            mail.send(msg)
            return redirect( url_for('login.recuperada') )
        else:
            flash('Número de matrícula inválido.', 'danger')
    """
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #send_reset_email(user)
        flash('Um email foi enviado com instruções para a recuperação de sua senha', 'info')
        return redirect(url_for('login.inicio'))
    return render_template('recover.html', form=form, configuration=configuration), 200



@loginBP.route("/resetar-senha/<token>", methods=['GET', 'POST'])
def reset_token(token):
    configuration = Configuration.query.first()
    user = User.verify_reset_token(token)
    if user is None:
        flash('O token de recuperação de senha é inválido ou está expirado. Por favor, tente novamente.', 'warning')
        #return redirect(url_for('login.recuperar'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Sua senha foi atualizada com sucesso.', 'success')
        return redirect(url_for('login.inicio'))
    return render_template('reset.html', form=form, configuration=configuration), 200

"""
@loginBP.route('/senha-recuperada', methods=['GET','POST'])
def recuperada():
    configuration = Configuration.query.first()
    return render_template('recover-success.html', configuration=configuration) , 200
"""


@loginBP.route('/logout')
def logout():
    configuration = Configuration.query.first()
    try:
        app.logger.warning(' %s deslogou da aplicação', session.get('user_name', ''))
        session.pop('user_id')
        session.pop('user_avatar')
        session.pop('user_name')
        session.pop('user_role')
    except:
        app.logger.warning('Logout por inatividade realizado')
    session.clear()
    return redirect( url_for('login.inicio') )
