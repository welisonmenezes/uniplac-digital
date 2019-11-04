from flask import flash
from database.Model import User

def validateUserToCreate(form):
    try:
        if hasUserWithRegistry(form.registry.data):
            return False

        if hasUserWithEmail(form.email.data):
            return False

        return True
    except:
        flash('Erro ao tentar validar o usuário', 'danger')
        return False


def validateUserToUpdate(form, user):
    try:
        # se a matrícula for diferente, chama validação
        if (user.registry != form.registry.data):
            if hasUserWithRegistry(form.registry.data):
                return False
        
        # se a email for diferente, chama validação
        if (user.email != form.email.data):
            if hasUserWithEmail(form.email.data):
                return False

        return True
    except:
        flash('Erro ao tentar validar o usuário', 'danger')
        return False


# verifica se existe usuário com uma dada matrícula    
def hasUserWithRegistry(registry):
    userWithRegistry = User.query.filter((User.registry == registry)).first()
    if userWithRegistry:
        flash('A matrícula informada já foi cadastrada', 'danger')
        return True
    return False


# verifica se existe usuário com um dado email
def hasUserWithEmail(email):
    userWithEmail = User.query.filter((User.email == email)).first()
    if userWithEmail:
        flash('O email informado já foi cadastrado', 'danger')
        return True
    return False