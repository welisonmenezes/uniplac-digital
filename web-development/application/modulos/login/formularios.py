from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length


class UsuarioForm(FlaskForm):
    login = StringField(
        'Login',
        validators = [DataRequired(message="Campo obrigatório")
        ],
        render_kw = {
            'placeholder':'Login'
        }
    )

password = PasswordField(
        'Senha',
        validators = [
            DataRequired(message="Campo obrigatório"),
            Length(min=6, message=("O campo seha deve conter no mínimo 6 dígitos")),
        ],
        render_kw = {
            'placeholder':'Senha'
        }
    )