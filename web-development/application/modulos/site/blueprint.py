import os
from flask import current_app, Blueprint, render_template, request, url_for, flash, redirect
from flask_mail import Message
from app import mail
from modulos.site.formularios import ContactForm
from database.Model import Configuration

siteBP = Blueprint('site', __name__, url_prefix='/', template_folder='templates', static_folder='static')

@siteBP.route('/')
def index():
    return render_template('site/site.html'), 200


@siteBP.route('/noticias')
def noticias():
    titulo = 'Notícias'
    return render_template('site/posts.html', titulo=titulo), 200


@siteBP.route('/noticias/detalhes')
def noticias_detalhes():
    titulo = 'Notícias' 
    return render_template('/site/detalhes.html', titulo=titulo), 200


@siteBP.route('/anuncios')
def anuncios():
    titulo = 'Anuncios'
    return render_template('site/posts.html', titulo=titulo), 200


@siteBP.route('/anuncios/detalhes')
def anuncios_detalhes():
    titulo = 'Anuncios'
    return render_template('/site/detalhes.html', titulo=titulo), 200


@siteBP.route('/avisos')
def avisos():
    titulo = 'Avisos'
    return render_template('site/posts.html', titulo=titulo), 200


@siteBP.route('/avisos/detalhes')
def avisos_detalhes():
    titulo = 'Avisos'
    return render_template('/site/detalhes.html', titulo=titulo), 200


@siteBP.route('/contato', methods=['GET','POST'])
def contato():
    configuration = Configuration.query.first()
    form = ContactForm(request.form)
    if form.validate_on_submit():
        try:
            msg = Message('Mensagem de - ' + form.name.data, sender='cntato@uniplacdigital.com.br', recipients=['uniplacdigital@gmail.com'])
            msg.html = "<h1>"+ form.assunto.data +"</h1>"
            msg.html += "<ul>"
            msg.html += "<li><b>Nome: </b> "+ form.name.data +"</li>"
            msg.html += "<li><b>Email: </b> "+ form.email.data +"</li>"
            msg.html += "<li><b>Descrição: </b> "+ form.text.data +"</li>"
            msg.html += "</ul>"
            mail.send(msg)
            flash('Mensagem enviada com sucesso.', 'success')
            return redirect(url_for('site.contato', _anchor='formulario'))
        except:
            flash('Descuple, ocorreu um problema ao tentar enviar sua mensagem.', 'warning')
        
    return render_template('site/contato.html', form=form, configuration=configuration), 200


@siteBP.route('/login')
def login():
    return 'Acesso a tela de login', 200
