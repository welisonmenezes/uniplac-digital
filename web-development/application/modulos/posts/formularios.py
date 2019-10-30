from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField, FileField, HiddenField, DateField, DateTimeField
from wtforms.validators import DataRequired, InputRequired, ValidationError
import re
from datetime import date, timedelta
from database.Model import Category 
import datetime


choice = []
try:
    categories = Category.query.all()
    for category in categories:
        choice.append((str(category.id), category.name))
except:
    pass

class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass

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

    category_id = SelectField(
        'Categoria',
        validators = [
            DataRequired(message="Campo obrigatório")
        ],
         choices=choice
    )

    status = NonValidatingSelectField(
        'Status',
        validators = [
            DataRequired(message="Campo obrigatório")
        ],
        choices=[('approved', 'Aprovado'), ('pending', 'Pendente'), ('denied', 'Negado')]
    )

    entry_date = DateTimeField(
        'Data/Hora de Entrada',
        validators = [
            InputRequired(message="Campo obrigatório")
        ],
        render_kw = {
            'placeholder':'Informe a data'
        },
        format='%d-%m-%Y %H:%M:%S'
    )

    departure_date = DateTimeField(
        'Data/Hora de Saída',
        validators = [
            InputRequired(message="Campo obrigatório")
        ],
        render_kw = {
            'placeholder':'Informe a data'
        },
        format='%d-%m-%Y %H:%M:%S'
    )

    tag = StringField(
        'Tags',
        validators = [
            DataRequired(message="Campo obrigatório")
        ],
        render_kw = {
            'placeholder':'Tags'
        }
    )


    def validate_entry_date(self, field):
        if field == '':
            raise ValidationError('A data de entrada é obrigatório')
        if not self.validateDate(field.data):
            raise ValidationError('Data inválida')
        if not self.compareDateWithNow(field):
            raise ValidationError('A data/hora selecionada precisa ser maior que a data/hora atual')


    def validate_departure_date(self, field):
        if field == '':
            raise ValidationError('A data de saída é obrigatório')
        if not self.validateDate(field.data):
            raise ValidationError('Data inválida')
        if not self.compareDateWithNow(field):
            raise ValidationError('A data/hora selecionada deve ser maior que a data/hora atual')
        if not self.compareDates(self.entry_date, field):
            raise ValidationError('A data/hora de saída deve ser 60 minutos maior que a data/hora de entrada')


    # verifica se o campo é uma data válida
    def validateDate(self, data_date):
        try:
            str_date = str(data_date)
            real_date = str_date.split(' ')
            year,month,day = real_date[0].split('-')
            month_validity = self.monthCheck(int(month)) 
            day_validity = self.dayCheck(int(month),int(day)) 
            year_validity = self.yearCheck(year)
            if month_validity and day_validity and year_validity:
                return True
            else:
                return False
        except:
            return False


    # compara a data/hora com a data/hora atual
    def compareDateWithNow(self, field):
        try:
            now = datetime.datetime.now()
            fieldDate = str(field.data)
            date, time = fieldDate.split(' ')
            year, month, day = date.split('-')
            hour, minute, second = time.split(':')
            second = second.split('.')[0]
            finalDate = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
            if finalDate <= now:
                return False
            else:
                return True
        except:
            return False

    
    # compara a data/hora com a data/hora entre dois dados campos
    def compareDates(self, entryField, departureField):
        try:
            entryDate = str(entryField.data)
            edate, etime = entryDate.split(' ')
            eyear, emonth, eday = edate.split('-')
            ehour, eminute, esecond = etime.split(':')
            esecond = esecond.split('.')[0]
            finalEntry = datetime.datetime(int(eyear), int(emonth), int(eday), int(ehour), int(eminute), int(esecond))

            departureDate = str(departureField.data)
            ddate, dtime = departureDate.split(' ')
            dyear, dmonth, dday = ddate.split('-')
            dhour, dminute, dsecond = dtime.split(':')
            dsecond = dsecond.split('.')[0]
            finalDeparture = datetime.datetime(int(dyear), int(dmonth), int(dday), int(dhour), int(dminute), int(dsecond))
            finalDeparture = finalDeparture - timedelta(hours=1)

            if finalDeparture <= finalEntry:
                return False
            else:
                return True
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


    