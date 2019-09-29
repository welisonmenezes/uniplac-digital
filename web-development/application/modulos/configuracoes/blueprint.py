import os
from flask import current_app, Blueprint, render_template, request, url_for, redirect, flash
from modulos.configuracoes.formularios import ConfiguracaoForm
from database.Model import db, Configuration
from sqlalchemy import or_, desc


configuracaoBP = Blueprint('configuracoes', __name__, url_prefix='/admin/configuracoes', template_folder='templates', static_folder='static')





@configuracaoBP.route('/cadastrar', methods=['GET','POST'])
def cadastrar():
    
    titulo = 'Cadastrar Configuracao'
    form = ConfiguracaoForm(request.form)
    
    
    if form.validate_on_submit():
        configuration = Configuration.query.first()  
        try:
                
                # cria a configuracao com os dados do formulário
                configuration = Configuration(
                    form.name.data,
                    form.description.data,
                    form.phone.data,
                    form.email.data,
                    form.address.data,
                    form.schedules.data,
                    None
                )
                if form.image_id.data != '':
                    configuration.image_id = form.image_id.data

                # adiciona e commita a configuracao na base de dadso
                db.session.add(configuration)
                db.session.commit()

                # flash message e redireciona pra mesma tela para limpar o objeto request
                flash('Configuração criada com sucesso', 'success')
                return redirect(url_for('configuracoes.cadastrar'))
        except:
            # remove qualquer vestígio do usuário da sessin e flash message 
            db.session.rollback()
            flash('Erro ao tentar cadastrar a Configuração', 'danger')
        else:
            try:
                if (form, configuration):

                # atualiza o usuário recuperado pelo id com os dados do formulário
                    configuration.name = form.name.data
                    configuration.description = form.description.data
                    user.phone = form.phone.data
                    user.email = form.email.data
                    user.address = form.address.data
                    user.schedules = form.schedules.data
                    user.image_id = None
                    if (form.image_id.data != ''):
                        user.image_id = form.image_id.data
                

                # commita os dados na base de dados
                    db.session.commit()

                # flash message e redireciona pra mesma tela para limpar o objeto request
                    flash('Configuração editada com sucesso', 'success')
                    return redirect(url_for('configuracoes.editar'))
            except:
                # remove qualquer vestígio da configuração da sessin e flash message
                db.session.rollback()
                flash('Erro ao tentar editar o configuração', 'danger')
            
            
    return render_template('configuracoes/formulario.html', titulo=titulo, form=form, mode='cadastrar'), 200


'''@configuracaoBP.route('/editar', methods=['GET','POST'])
def editar():

    

    # pega o usuário pelo id
    configuration = Configuration

    titulo = 'Editar Configuracoes'

    if request.form:
        # formulário preenchido pelo objeto request, caso exista
        form = ConfiguracaoForm(request.form)
    else:
        # formulário vazio
        form = ConfiguracaoForm()

   
    if form.validate_on_submit():
        try:
            if (form, configuration):

                # atualiza o usuário recuperado pelo id com os dados do formulário
                configuration.name = form.name.data
                configuration.description = form.description.data
                user.phone = form.phone.data
                user.email = form.email.data
                user.address = form.address.data
                user.schedules = form.schedules.data
                user.image_id = None
                if (form.image_id.data != ''):
                    user.image_id = form.image_id.data
                

                # commita os dados na base de dados
                db.session.commit()

                # flash message e redireciona pra mesma tela para limpar o objeto request
                flash('Configuração editada com sucesso', 'success')
                return redirect(url_for('configuracoes.editar'))
        except:
            # remove qualquer vestígio da configuração da sessin e flash message
            db.session.rollback()
            flash('Erro ao tentar editar o configuração', 'danger')
    return render_template('configuracoes/formulario.html', titulo=titulo, form=form, mode='editar', configuration=configuration), 200
'''