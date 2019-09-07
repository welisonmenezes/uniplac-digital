from Validators import Validators
import sys
sys.path.insert(0, './api/Models')
from Model import User

class UserValidation(Validators):
    def __init__(self, req):
        self.req = req
        self.response = None
        self.model = User

        self.requiredFields = [
            ('first_name', 'O campo Nome é obrigatório'),
            ('last_name', 'O campo Sobrenome é obrigatório'),
            ('registry', 'O campo Matrícula é obrigatório'),
            ('password', 'O campo Senha é obrigatório'),
            ('role', 'O campo Permissão é obrigatório'),
            ('email', 'O campo email é obrigatório')
        ]

        self.uniqueFields = [
            ('email', 'O email informado já foi cadastrado'),
            ('registry', 'A matrícula informada já foi cadastrada')
        ]

        self.numberFields = [
            ('image_id', 'O id da imagem deve ser um número')
        ]

        self.emailFields = [
            ('email', 'O email informado é inválido')
        ]
    

    