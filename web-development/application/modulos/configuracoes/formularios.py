from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, FileField, HiddenField
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

    description = StringField(
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

    image = FileField(
        'Adicionar Imagem',
        validators = []
    )

    image_id = HiddenField('')