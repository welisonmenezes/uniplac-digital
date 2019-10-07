from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField, FileField, HiddenField, DateField
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

    entry_date = DateField(
        'Data de Entrada',
        validators = [
            InputRequired(message="Campo obrigatório")
        ],
        render_kw = {
            'placeholder':'Informe a data'
        },
        format='%d-%m-%Y'
    )

    departure_date = DateField(
        'Data de Saída',
        validators = [
            InputRequired(message="Campo obrigatório")
        ],
        render_kw = {
            'placeholder':'Informe a data'
        },
        format='%d-%m-%Y'
    )

    def validateDepartureDate(self):
        result = super(PostForm, self).validate()
        if (self.departure_date.data < self.entry_date.data):
            return False
        else:
            return result