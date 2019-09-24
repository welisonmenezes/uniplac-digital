import os
from flask import current_app, Blueprint, render_template, request, url_for
from modulos.configuracoes.formularios import ConfiguracaoForm

configuracaoBP = Blueprint('configuracoes', __name__, url_prefix='/admin/configuracoes', template_folder='templates', static_folder='static')

@configuracaoBP.route('/editar', methods=['GET','POST'])
def editar():
    form = ConfiguracaoForm(request.form)
    if form.validate_on_submit():
        print("valido")
    return render_template('/configuracoes/formulario.html', form=form), 200
