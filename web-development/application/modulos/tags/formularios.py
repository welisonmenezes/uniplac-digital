from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class TagForm(FlaskForm):
    name = StringField(
        'Nome',
        validators = [
            DataRequired(message="Campo obrigatório")
        ],
        render_kw = {
            'placeholder':'Nome',
            'data-async-key': 'tag-input'
        }
    )