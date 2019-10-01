import os
from flask import current_app, Blueprint, render_template, request, url_for, redirect, flash, session
from app import bcrypt
from sqlalchemy import and_, desc
from database.Model import db, User
from modulos.login.formularios import LoginForm


loginBP = Blueprint('login', __name__, url_prefix='/login', template_folder='templates', static_folder='static')

@loginBP.route('/', methods=['GET','POST'])
def inicio():
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
                return redirect( url_for('dashboard.dash') )
            else:
                flash('Credenciais inválidas', 'danger')
        else:
            flash('Credenciais inválidas', 'danger')
    return render_template('login.html', form=form) , 200


@loginBP.route('/logout')
def logout():
    session.pop('user_id')
    session.pop('user_avatar')
    session.pop('user_name')
    session.pop('user_role')
    session.clear()
    return redirect( url_for('login.inicio') )
