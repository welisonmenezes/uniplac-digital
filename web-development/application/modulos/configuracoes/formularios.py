from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, HiddenField
from wtforms.validators import DataRequired

class ConfiguracaoForm(FlaskForm):
    name = StringField(
        'Título do Site',
        validators = [
            DataRequired(message="Campo obrigatório")
        ],
        render_kw = {
            'placeholder':'Título do Site'
        }
    )

    description = TextAreaField(
        'Descrição do Site',
        validators = [
            DataRequired(message="Campo obrigatório")
        ],
        render_kw = {
            'placeholder':'Descrição do Site'
        }
    )

    phone = StringField(
        'Telefone',
        validators = [DataRequired(message="Campo obrigatório")],
        render_kw = {
            'placeholder':'Telefone'
        }
    )

    email = StringField(
        'Email',
        validators = [DataRequired(message="Campo obrigatório")],
        render_kw = {
            'placeholder':'Email'
        }
    )

    address = StringField(
        'Endereço',
        validators = [DataRequired(message="Campo obrigatório")],
        render_kw = {
            'placeholder':'Endereço'
        }
    )

    schedules = StringField(
        'Horários',
        validators = [DataRequired(message="Campo obrigatório")],
        render_kw = {
            'placeholder':'Horários'
        }
    )

    map = StringField(
        'Embed do Mapa',
        validators = [DataRequired(message="Campo obrigatório")],
        render_kw = {
            'placeholder':'Mapa'
        }
    )

    city = StringField(
        'Cidade/Estado',
        validators = [DataRequired(message="Campo obrigatório")],
        render_kw = {
            'placeholder':'Cidade/Estado'
        }
    )

    image = FileField(
        'Adicionar Imagem',
        validators = []
    )

    old_images = HiddenField('')
    new_images = HiddenField('')