import re
from datetime import date, datetime
from modulos.api.Utils import getBase64Size

class Validators():

    # percorre todas as validações necessários
    def isValid(self, currentResult=None):

        # percorre campos necessários
        for field in self.fields:
            if not self.validateReqFields(field):
                return False
                break
        
        # se não é update
        if not currentResult:
            # percorre campos obrigatórios
            for field in self.requiredFields:
                if not self.validateRequired(field[0], field[1]):
                    return False
                    break
        # se é update
        else:
            # percorre campos obrigatórios
            for field in self.requiredFields:
                if not self.validateRequiredToUpdate(field[0], field[1]):
                    return False
                    break
        
        # percorre campos de imagem
        for field in self.imageFields:
            if not self.validateImageType(field) or not self.validateImageSize(field):
                return False
                break

        return True


    # verifica se um campo necessári existe na requisição
    def validateReqFields(self, field):
        if not self.req.get(field) and self.req.get(field) != '' and self.req.get(field) != []:
            self.response = { 'message': 'O campo ' + field + ' não foi enviado' }, 501
            return False
        else:
            return True


    # verifica se um campo obrigatório está preenchido
    def validateRequired(self, field, message):
        if not self.req[field] and self.req[field] == '':
            self.response = { 'message': message }, 501 
            return False
        return True

    
    # verifica se um campo obrigatório está preenchido menos o password se for edição
    def validateRequiredToUpdate(self, field, message):
        if (field == 'password'):
            return True
        else:
            return self.validateRequired(field, message)


    # verifica se o tipo do arquivo é uma imagem válida
    def validateImageType(self, field):
        baseType = re.search('data:image/(.+?);base64,', self.req[field])
        if (baseType and ( baseType.group(1) == 'png' or
                            baseType.group(1) == 'jpg' or
                            baseType.group(1) == 'jpeg' or
                            baseType.group(1) == 'gif') ):
            return True
        else:
            self.response = { 'message': 'Tipo de arquivo inválido' }, 501
            return False


    # verfifica se o tamanho do arquivo é válido
    def validateImageSize(self, field):
        if (int(getBase64Size(self.req[field])) <= int(5017969)):
            return True
        else:
            self.response = { 'message': 'O tamanho da imagem não deve exceder 5mb' }, 501
            return False
