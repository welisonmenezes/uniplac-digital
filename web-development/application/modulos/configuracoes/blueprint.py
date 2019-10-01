import os
from flask import current_app, Blueprint, render_template, request, url_for, redirect, flash
from modulos.configuracoes.formularios import ConfiguracaoForm
from database.Model import db, Configuration, Image
from sqlalchemy import or_, desc


configuracaoBP = Blueprint('configuracoes', __name__, url_prefix='/admin/configuracoes', template_folder='templates', static_folder='static')





@configuracaoBP.route('/cadastrar', methods=['GET','POST'])
def cadastrar():
    
    titulo = 'Cadastrar Configuracao'
    form = ConfiguracaoForm(request.form)
    configuration = Configuration.query.first()
    images = None

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
                
                # pega parametros e os formata para convertê-los em array
                str_old_img = form.old_images.data.replace(']', '').replace('[', '')
                arr_old_img = str_old_img.split(',')
                str_new_img = form.new_images.data.replace(']', '').replace('[', '')
                arr_new_img = str_new_img.split(',')

                # pega as diferenças (para deletar e adicionar imagens)
                delete_images = set(arr_old_img) - set(arr_new_img)
                add_images = set(arr_new_img) - set(arr_old_img)

                print(delete_images)
                print(add_images)

                # deleta a imagens para deletar
                for image_id in delete_images:
                    if image_id == '':
                        continue
                    try:
                        id = int(image_id)
                    except:
                        flash('O ID da imagem deve ser um número inteiro', 'danger')
                    image = Image.query.get(id)
                    if not image:
                        flash('A imagem ' +  str(image_id) + ' não existe na base de dados', 'danger')
                    else:
                        if image in configuration.images:
                            configuration.images.remove(image)

                # adiciona as imagens para adicionar
                for image_id in add_images:
                    if image_id == '':
                        continue
                    try:
                        id = int(image_id)
                    except:
                        flash('O ID da imagem deve ser um número inteiro', 'danger')
                    image = Image.query.get(id)
                    if not image:
                        flash('A imagem ' +  str(image_id) + ' não existe na base de dados', 'danger')
                    else:
                        configuration.images.append(image)
                            

                db.session.commit()
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

                str_new_img = form.new_images.data.replace(']', '').replace('[', '')
                arr_new_img = str_new_img.split(',')

                for image_id in arr_new_img:
                    if image_id == '':
                        continue
                    try:
                        id = int(image_id)
                    except:
                        flash('O ID da imagem deve ser um número inteiro', 'danger')
                    image = Image.query.get(id)
                    if not image:
                        flash('A imagem ' +  str(image_id) + ' não existe na base de dados', 'danger')
                    else:
                        configuration.images.append(image)
                

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
    else:
        if configuration:
            form.name.data = configuration.name
            form.description.data = configuration.description
            form.phone.data = configuration.phone
            form.email.data = configuration.email
            form.address.data = configuration.address
            form.schedules.data = configuration.schedules
            #form.old_images 
            images = configuration.images
            str_image = '['
            for image in configuration.images:
                str_image = str_image + str(image.id) + ','
            
            str_image = str_image + ']'
            str_image = str_image.replace(',]', ']')
            
            form.old_images.data = str_image
            form.new_images.data = str_image
        
    return render_template('configuracoes/formulario.html', titulo=titulo, form=form, mode='cadastrar', images=images), 200


