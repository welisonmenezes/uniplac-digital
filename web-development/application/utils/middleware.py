from flask import request, redirect, url_for, flash, session
from app import app
import re

# middleware para rejeitar qualquer requisição ao admin para não autenticado
@app.before_request
def before_request_func():

    user = session.get('user_id', None)
    role = session.get('user_role', None)


    if bool(re.search(request.url_root+'admin*', request.url)):
        if not user:
            flash('Faça o seu login para poder acessar o painel administrativo', 'warning')
            return redirect(url_for('login.inicio', url=request.url))


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

    if bool(re.search(request.url_root+'admin/tags*', request.url)) or bool(re.search(request.url_root+'tag*', request.url)):
        return redirect(url_for('erro.pageError'))