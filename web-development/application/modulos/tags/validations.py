from flask import flash
from database.Model import Tag

def validateTagToCreate(form):
    try:
        if not hasTagWithName(form.name.data):
            return False

        return True
    except:
        flash('Erro ao tentar validar a tag', 'danger')
        return False

def validateTagToUpdate(form, tag):
    try:
        # se a matrícula for diferente, chama validação
        if (tag.name != form.name.data):
            if not hasTagWithName(form.name.data):
                return False
        
        return True
    except:
        flash('Erro ao tentar validar a tag', 'danger')
        return False



def hasTagWithName(name):
    tagWithName = Tag.query.filter((Tag.name == name)).first()
    if tagWithName:
        flash('O nome informado já foi cadastrado', 'danger')
        return False
    return True
