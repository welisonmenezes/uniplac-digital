from flask import request, redirect, url_for, flash, session
from app import app
import re
from database.Model import User

# middleware para rejeitar qualquer requisição ao admin para não autenticado
@app.before_request
def before_request_func():

    user = session.get('user_id', None)
    role = session.get('user_role', None)


    if bool(re.search(request.url_root+'admin*', request.url)):
        if not user:
            flash('Faça o seu login para poder acessar o painel administrativo', 'warning')
            return redirect(url_for('login.inicio', url=request.url))
        else:
            l_user = User.query.filter((User.id==user)).first()
            if not l_user:
                try:
                    app.logger.warning(' %s deslogou da aplicação', session.get('user_name', ''))
                    session.pop('user_id')
                    session.pop('user_avatar')
                    session.pop('user_name')
                    session.pop('user_role')
                except:
                    app.logger.warning('Logout por inatividade realizado')
                session.clear()
                return redirect(url_for('login.inicio'))


    if bool(re.search(request.url_root+'admin/usuarios*', request.url)):
        if bool(re.search(request.url_root+'admin/usuarios/editar/*', request.url)):
            paths = request.url.split('/')
            id = paths[-1]
            if (role != 'admin' and int(user) != int(id)):
                flash('Você não tem acesso à esse recurso', 'warning')
                return redirect(url_for('dashboard.dash')) 
        elif not role or role != 'admin':
            flash('Você não tem acesso à esse recurso', 'warning')
            return redirect(url_for('dashboard.dash'))

    
    if bool(re.search(request.url_root+'admin/configuracoes*', request.url)):
        if not role or role != 'admin':
            flash('Você não tem acesso à esse recurso', 'warning')
            return redirect(url_for('dashboard.dash'))

    
    if bool(re.search(request.url_root+'admin/categorias*', request.url)):
        if not role or role != 'admin':
            flash('Você não tem acesso à esse recurso', 'warning')
            return redirect(url_for('dashboard.dash'))
    
    if bool(re.search(request.url_root+'admin/tags*', request.url)):
        if not role or role != 'admin':
            flash('Você não tem acesso à esse recurso', 'warning')
            return redirect(url_for('dashboard.dash'))

    
    if bool(re.search(request.url_root+'admin/noticias*', request.url)):
        if not role or (role != 'admin' and role != 'editor'):
            flash('Você não tem acesso à esse recurso', 'warning')
            return redirect(url_for('dashboard.dash'))


    if bool(re.search(request.url_root+'admin/avisos*', request.url)):
        if not role or (role != 'admin' and role != 'author'):
            flash('Você não tem acesso à esse recurso', 'warning')
            return redirect(url_for('dashboard.dash'))