import os
from flask import current_app, Blueprint, render_template, request, url_for

configuracaoBP = Blueprint('configuracoes', __name__, url_prefix='/admin/configuracoes', template_folder='templates', static_folder='static')

@configuracaoBP.route('/')
def index():
    return 'listagem das configuracoes aqui', 200

@configuracaoBP.route('/editar')
def editar():
    return 'formulário de edição de configuracoes aqui', 200
