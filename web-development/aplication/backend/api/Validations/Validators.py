import re

class Validators():

    def isValid(self, currentModel=None):
        for field in self.requiredFields:
            if not self.validateRequired(field[0], field[1]):
                return False
                break

        if not currentModel:
            for field in self.uniqueFields:
                if not self.validateUnique(field[0], field[1]):
                    return False
                    break
        else:
            for field in self.uniqueFields:
                if not self.validateUniqueToUpdate(field[0], field[1], currentModel):
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
        
        return True


    def validateRequired(self, field, message):
        if not self.req[field] and self.req[field] == '':
            self.response = {
                'error': True,
                'code': '101',
                'message': message
            }, 501 
            return False
        return True

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

    def validateUniqueToUpdate(self, field, message, currentModel):
        if (getattr(currentModel, field) != self.req[field]):
            return self.validateUnique(field, message)
        else:
            return True


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