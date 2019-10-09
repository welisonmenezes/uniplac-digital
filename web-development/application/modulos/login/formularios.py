from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    registry = StringField(
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
            DataRequired(message="Campo obrigatório")
            
        ],
        render_kw = {
            'placeholder':'Senha'
        }
    )


class RecoverForm(FlaskForm):
    registry = StringField(
        'Informe sua matrícula',
        validators = [DataRequired(message="Campo obrigatório")
        ],
        render_kw = {
            'placeholder':'Matrícula'
        }
    )