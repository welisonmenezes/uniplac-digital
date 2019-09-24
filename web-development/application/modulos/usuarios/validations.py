from flask import flash
from database.Model import User

def validateUserData(form):
    try:
        userWithRegistry = User.query.filter((User.registry == form.registry.data)).first()
        if userWithRegistry:
            flash('A matrícula informada já foi cadastrada', 'danger')
            return False
        
        userWithEmail = User.query.filter((User.email == form.email.data)).first()
        if userWithEmail:
            flash('O email informado já foi cadastrado', 'danger')
            return False

        return True
    except:
        flash('Erro ao tentar validar o usuário', 'danger')
        return False