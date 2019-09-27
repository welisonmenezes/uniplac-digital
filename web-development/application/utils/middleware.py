from flask import request, redirect, url_for, flash
from app import app
import re

# middleware para rejeitar qualquer requisição ao admin para não autenticado
@app.before_request
def before_request_func():
    if bool(re.search(request.url_root+'admin*', request.url)):
        print('middleware here')
        #flash('Você não tem permissão para acessar este recurso', 'danger')
        #return redirect(url_for('login.inicio'))