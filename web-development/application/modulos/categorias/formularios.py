from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class CategoriaForm(FlaskForm):
    name = StringField(
        'Nome',
        validators = [
            DataRequired(message="Campo obrigatório")
        ],
        render_kw = {
            'placeholder':'Nome'
        }
    )

    description = TextAreaField(
        'Descrição',
        render_kw = {
            'placeholder':'Descrição'
        }
    )
