import os
from flask import current_app, Blueprint, render_template, request, url_for

configuracaoBP = Blueprint('configuracoes', __name__, url_prefix='/admin/configuracoes', template_folder='templates', static_folder='static')

@configuracaoBP.route('/editar')
def editar():
    return render_template('/configuracoes/formulario.html'), 200
