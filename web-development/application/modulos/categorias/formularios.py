from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired

class CategoriaForm(FlaskForm):
    name = StringField(
        'Nome',
        validators = [
            DataRequired(message="Campo obrigatório")
        ],
        render_kw = {
            'placeholder':'Nome',
            'data-async-key': 'category-input'
        }
    )

    description = TextAreaField(
        'Descrição',
        render_kw = {
            'placeholder':'Descrição'
        }
    )

    destacado =  BooleanField(
        ''
    )
