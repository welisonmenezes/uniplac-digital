from modulos.api.Validations.Validators import Validators
from database.Model import Image

class ImageValidation(Validators):
    def __init__(self, req):

        # objeto da requisiçõa
        self.req = req

        # objeto de resposta
        self.response = None

        # o modelo a ser validado
        self.model = Image

        # campos necessários
        self.fields = ['image']

        # campos obrigatórios e suas respectivas mensagens de erro
        self.requiredFields = [('image', 'O campo Imagem é obrigatório')]

        self.imageFields = ['image']
    