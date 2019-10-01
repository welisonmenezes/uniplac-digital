from flask import flash
from database.Model import Category

def validateCategoryToCreate(form):
    try:
        if hasCategoryWithName(form.name.data):
            return False

        return True
    except:
        flash('Erro ao tentar validar a categoria', 'danger')
        return False

def validateCategoryToUpdate(form, category):
    try:
        # se a matrícula for diferente, chama validação
        if (category.name != form.name.data):
            if hasCategoryWithName(form.name.data):
                return False
        
        return True
    except:
        flash('Erro ao tentar validar a categoria', 'danger')
        return False

def hasCategoryWithName(name):
    categoryWithName = Category.query.filter((Category.name == name)).first()
    if categoryWithName:
        flash('O nome informado já foi cadastrado', 'danger')
        return False