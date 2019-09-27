import os
from flask import current_app, Blueprint, render_template, request, url_for, redirect
from modulos.login.formularios import LoginForm


loginBP = Blueprint('login', __name__, url_prefix='/login', template_folder='templates', static_folder='static')

@loginBP.route('/', methods=['GET','POST'])
def inicio():
    form= LoginForm(request.form)
    if form.validate_on_submit():
        print('valido')
        return redirect(url_for('dashboard.dash'))
    return render_template('login.html', form=form) , 200


@loginBP.route('/logout')
def logout():
    return 'logica de logout', 200
