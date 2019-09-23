from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, FileField, HiddenField
from wtforms.validators import DataRequired

class UsuarioForm(FlaskForm):
    first_name = StringField(
        'Nome',
        validators = [
            DataRequired(message="Campo obrigatório")
        ],
        render_kw = {
            'placeholder':'Nome'
        }
    )

    last_name = StringField(
        'Sobrenome',
        validators = [DataRequired(message="Campo obrigatório")],
        render_kw = {
            'placeholder':'Sobrenome'
        }
    )

    registry = StringField(
        'Nº da matrícula',
        validators = [DataRequired(message="Campo obrigatório")],
        render_kw = {
            'placeholder':'Nº da matrícula'
        }
    )

    password = PasswordField(
        'Senha',
        validators = [DataRequired(message="Campo obrigatório")],
        render_kw = {
            'placeholder':'Senha'
        }
    )

    role = SelectField(
        'Permissão',
        validators = [DataRequired(message="Campo obrigatório")],
        choices=[('', 'Selecione'), ('admin', 'Administrador'), ('editor', 'Editor'), ('author', 'Autor'), ('user', 'Usuário')]
    )

    email = StringField(
        'Email',
        validators = [DataRequired(message="Campo obrigatório")],
        render_kw = {
            'placeholder':'Email'
        }
    )

    phone = StringField(
        'Telefone',
        validators = [],
        render_kw = {
            'placeholder':'Telefone'
        }
    )

    image = FileField(
        'Avatar',
        validators = []
    )

    image_id = HiddenField('')