from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField, FileField, HiddenField
from wtforms.validators import DataRequired, InputRequired

class PostForm(FlaskForm):
    title = StringField(
        'Título',
        validators = [
            DataRequired(message="Campo obrigatório")
        ],
        render_kw = {
            'placeholder':'Título'
        }
    )

    description = TextAreaField(
        'Descrição',
        validators = [
            DataRequired(message="Campo obrigatório")
        ],
        render_kw = {
            'placeholder':'Descrição'
        }
    )

    content = TextAreaField(
        'Conteúdo',
        validators = [
            DataRequired(message="Campo obrigatório")
        ],
        render_kw = {
            'placeholder':'Conteúdo'
        }
    )
    
    image = FileField(
        'Imagem de Destaque',
        validators = []
    )

    image_id = HiddenField('')

    genre = SelectField(
        'Categoria',
        validators = [
            DataRequired(message="Campo obrigatório")
        ],
         choices=[('', 'Selecione'), ('admin', 'Sistemas de Informação'), ('editor', 'Direito'), ('author', 'Administração'), ('user', 'Odontologia')]
    )

    entry_date = StringField(
        'Data de Entrada',
        validators = [
            DataRequired(message="Campo obrigatório")
        ],
        render_kw = {
            'placeholder':'Informe a data'
        }
    )

    departure_date = StringField(
        'Data de Saída',
        validators = [
            DataRequired(message="Campo obrigatório")
        ],
        render_kw = {
            'placeholder':'Informe a data'
        }
    )