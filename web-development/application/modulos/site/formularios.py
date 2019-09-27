from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, FileField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp, Email

class ContactForm(FlaskForm):

    text= TextAreaField(
        'Descrição',
        validators = [
            DataRequired(message="Campo obrigatório")
        ],
        render_kw = {
            'placeholder':'Descrição'
        }
    )

    name = StringField(
        'Nome',
        validators = [DataRequired(message="Campo obrigatório")
        ],
        render_kw = {
            'placeholder':'Nome'
        }
    )

    email = StringField(
        'Email',
        validators = [
            DataRequired(message="Campo obrigatório"),
            Email(message="Email inválido")
        ],
        render_kw = {
            'placeholder':'Email'
        }
    )

    assunto = StringField(
        'Assunto',
        validators = [DataRequired(message="Campo obrigatório")
        ],
        render_kw = {
            'placeholder':'Assunto'
        }
    )