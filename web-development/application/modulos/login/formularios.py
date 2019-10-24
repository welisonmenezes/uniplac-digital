from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from database.Model import User


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

    recaptcha = RecaptchaField()


class RecoverForm(FlaskForm):
    registry = StringField(
        'Informe sua matrícula',
        validators = [DataRequired(message="Campo obrigatório")
        ],
        render_kw = {
            'placeholder':'Matrícula'
        }
    )

class RequestResetForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Campo obrigatório"),
            Email(message="E-mail inválido")
        ]
    )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Não há nenhuma conta com este email')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Campo obrigatório")
        ]
    )
    confirm_password = PasswordField(
        'Confirmação de senha',
        validators=[
            DataRequired(message="Campo obrigatório"),
            EqualTo('password', message="A senha deve ser igual")
        ]
    )