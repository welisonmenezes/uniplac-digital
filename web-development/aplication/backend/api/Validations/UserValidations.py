from Validators import Validators
import sys
sys.path.insert(0, './api/Models')
from Model import User

class UserValidation(Validators):
    def __init__(self, req):

        # objeto da requisiçõa
        self.req = req

        # objeto de resposta
        self.response = None

        # o modelo a ser validado
        self.model = User

        # campos necessários
        self.fields = [
            'first_name',
            'last_name',
            'registry',
            'password',
            'role',
            'email',
            'phone',
            'image_id'
        ]

        # campos obrigatórios e suas respectivas mensagens de erro
        self.requiredFields = [
            ('first_name', 'O campo Nome é obrigatório'),
            ('last_name', 'O campo Sobrenome é obrigatório'),
            ('registry', 'O campo Matrícula é obrigatório'),
            ('password', 'O campo Senha é obrigatório'),
            ('role', 'O campo Permissão é obrigatório'),
            ('email', 'O campo email é obrigatório')
        ]

        # campos únicos e suas respectivas mensagens de erro
        self.uniqueFields = [
            ('email', 'O email informado já foi cadastrado'),
            ('registry', 'A matrícula informada já foi cadastrada')
        ]

        # campos numéricos e suas respectivas mensagens de erro
        self.numberFields = [
            ('image_id', 'O id da imagem deve ser um número')
        ]

        # campos de email e suas respectivas mensagens de erro
        self.emailFields = [
            ('email', 'O email informado é inválido')
        ]

        # campos de chave estrangeira e suas respectivas mensagens de erro
        self.foreignFields = [
            ('image_id', 'A imagem informada não existe')
        ]
    