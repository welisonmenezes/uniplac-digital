from flask import request, redirect, url_for, flash, session
from app import app
import re

# middleware para rejeitar qualquer requisição ao admin para não autenticado
@app.before_request
def before_request_func():
    if bool(re.search(request.url_root+'admin*', request.url)):
        user = session.get('user_id', None)
        if not user:
            flash('Faça o seu login para poder acessar o painel administrativo', 'warning')
            return redirect(url_for('login.inicio'))