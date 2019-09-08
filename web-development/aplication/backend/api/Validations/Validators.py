import re

class Validators():

    # percorre todas as validações necessários
    def isValid(self, currentResult=None, relatedModel=None):

        for field in self.fields:
            if not self.validateReqFields(field):
                return False
                break

        if not currentResult:
            for field in self.requiredFields:
                if not self.validateRequired(field[0], field[1]):
                    return False
                    break

            for field in self.uniqueFields:
                if not self.validateUnique(field[0], field[1]):
                    return False
                    break
        else:
            for field in self.requiredFields:
                if not self.validateRequiredToUpdate(field[0], field[1]):
                    return False
                    break

            for field in self.uniqueFields:
                if not self.validateUniqueToUpdate(field[0], field[1], currentResult):
                    return False
                    break

        for field in self.numberFields:
            if not self.validateNumber(field[0], field[1]):
                return False
                break

        for field in self.emailFields:
            if not self.validateEmail(field[0], field[1]):
                return False
                break
        
        if relatedModel:
            for field in self.foreignFields:
                if not self.validateForeignField(field[0], field[1], relatedModel):
                    return False
                    break
        
        return True


    # verifica se um campo necessári existe na requisição
    def validateReqFields(self, field):
        if not self.req.get(field) and self.req.get(field) != '':
            self.response = {
                'error': True,
                'code': '101',
                'message': 'O campo ' + field + ' nao foi informado'
            }, 501
            return False
        else:
            return True


    # verifica se um campo obrigatório está preenchido
    def validateRequired(self, field, message):
        if not self.req[field] and self.req[field] == '':
            self.response = {
                'error': True,
                'code': '101',
                'message': message
            }, 501 
            return False
        return True

    
    # verifica se um campo obrigatório está preenchido menos o password se for edição
    def validateRequiredToUpdate(self, field, message):
        if (field == 'password'):
            return True
        else:
            return self.validateRequired(field, message)

    # verifica se um campo é unico no banco de dados
    def validateUnique(self, field, message):
        filters = { field: self.req[field] }
        result = self.model.query.filter_by(**filters).first()
        if result:
            self.response = {
                'error': True,
                'code': '101',
                'message': message
            }, 501
            return False
        return True


    # verifica se um campo é unico no banco de dados quando este é atualizado
    def validateUniqueToUpdate(self, field, message, currentResult):
        if (getattr(currentResult, field) != self.req[field]):
            return self.validateUnique(field, message)
        else:
            return True

    
    # verifica se uma chave estrangeira existe no banco de dados
    def validateForeignField(self, field, message, relatedModel):
        if self.req[field] != '':
            result = relatedModel.query.filter_by(id=self.req[field]).first()
            if result:
                return True
            else:
                self.response = {
                    'error': True,
                    'code': '101',
                    'message': message
                }, 501
                return False 
        else:
            return True


    # verifica se o campo é um número válido
    def validateNumber(self, field, message):
        if self.req.get(field):
            try:
                num = int(self.req.get(field))
                if (num):
                    return True
                else:
                    self.response = {
                        'error': True,
                        'code': '101',
                        'message': message
                    }, 501
                    return False
            except:
                self.response = {
                    'error': True,
                    'code': '101',
                    'message': message
                }, 501
                return False
        else:
            return True


    # verifica se o campo é um email válido
    def validateEmail(self, field, message):
        if bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", self.req[field])):
            return True
        else:
            self.response = {
                'error': True,
                'code': '101',
                'message': message
            }, 501
            return False