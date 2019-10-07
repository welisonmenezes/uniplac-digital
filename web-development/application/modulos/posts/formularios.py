from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField, FileField, HiddenField, DateField
from wtforms.validators import DataRequired, InputRequired, ValidationError
import re
from datetime import date
import datetime

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

    def validate_entry_date(self, field):
        if field == '':
            raise ValidationError('A data de entrada é obrigatório')

    def validate_departure_date(self, field):
        if field == '':
            raise ValidationError('A data de saída é obrigatório')
        if not self.validateDate(field.data):
            raise ValidationError('Data inválida')
        if not self.compareDates(self.entry_date.data, field.data):
            raise ValidationError('A data de entrada deve ser maior que hoje e a data de saída deve ser maior que a data de entrada')


    # verifica se o campo é uma data válida
    def validateDate(self, data_date):
        try:
            str_date = str(data_date)
            year,month,day = str_date.split('-')
            month_validity = self.monthCheck(int(month)) 
            day_validity = self.dayCheck(int(month),int(day)) 
            year_validity = self.yearCheck(year)
            if month_validity and day_validity and year_validity:
                return True
            else:
                return False
        except:
            return False


    # vefifica se a data do index 0 é menor que a data do index 1 e é maior ou igual a data corrente
    def compareDates(self, entry_date, departure_date):
        try:
            today = date.today().strftime('%d-%m-%Y')
            t_day,t_month,t_year = today.split('-')
            t_date = datetime.datetime(int(t_year), int(t_month), int(t_day))
            entry = str(entry_date)
            e_year,e_month,e_day = entry.split('-')
            e_date = datetime.datetime(int(e_year), int(e_month), int(e_day)) 
            departure = str(departure_date)
            d_year,d_month,d_day = departure.split('-')
            d_date = datetime.datetime(int(d_year), int(d_month), int(d_day))
            if e_date >= t_date:
                if e_date < d_date:
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False


    # verifica se o dados mês é um mês válido
    def monthCheck(self, month):
        if month > 0 and month <= 12:
            return True
        else:
            return False


    # verifica se o dado dia é um dia válido
    def dayCheck(self, month, day):
        days_in_month = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
        if 0 < day <= days_in_month[month]:
            return True
        else:
            return False


    # verifica se o dado ano é um ano válido
    def yearCheck(self, year):
        if len(year) >= 1 and len(year) <= 4:
            return True
        else:
            return False