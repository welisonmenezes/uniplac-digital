def mustHaveId(fn):
    def wrapper(*args,**kwargs):
        print(kwargs)
        if not kwargs.get('id'):
            return {
                'error': True,
                'code': '103',
                'message': 'Identificador não enviado'
            }, 400 
        return fn(*args,**kwargs)
    return wrapper