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
    configuration = Configuration.query.first()
    

    if configuration:
        form.name.data = configuration.name
        form.description.data = configuration.description
        form.phone.data = configuration.phone
        form.email.data = configuration.email
        form.address.data = configuration.address
        form.schedules.data = configuration.schedules
        
        

    if form.validate_on_submit():
        if configuration:        

            try:           
                form = ConfiguracaoForm(request.form)   
                # atualiza as configurações recuperado  com os dados do formulário
                configuration.name = form.name.data
                configuration.description = form.description.data
                configuration.phone = form.phone.data
                configuration.email = form.email.data
                configuration.address = form.address.data
                configuration.schedules = form.schedules.data
                         

            # commita os dados na base de dados
                db.session.commit()

            # flash message e redireciona pra mesma tela para limpar o objeto request
                flash('Configuração editada com sucesso', 'success')
                return redirect(url_for('configuracoes.cadastrar'))
            except:
                # remove qualquer vestígio da configuração da sessin e flash message
                db.session.rollback()
                flash('Erro ao tentar editar o configuração', 'danger')


        else:  
            
            
            try:        
                # cria a configuracao com os dados do formulário
                configuration = Configuration(
                    form.name.data,
                    form.description.data,
                    form.phone.data,
                    form.email.data,
                    form.address.data,
                    form.schedules.data
                    
                )
                

                # adiciona e commita a configuracao na base de dadso
                db.session.add(configuration)
                db.session.commit()

                # flash message e redireciona pra mesma tela para limpar o objeto request
                flash('Configuração criada com sucesso', 'success')
                return redirect(url_for('configuracoes.cadastrar'))
            except:
            # remove qualquer vestígio de configuração da sessin e flash message 
                db.session.rollback()
                flash('Erro ao tentar cadastrar a Configuração', 'danger')
        
            
            
            
    return render_template('configuracoes/formulario.html', titulo=titulo, form=form, mode='cadastrar'), 200


