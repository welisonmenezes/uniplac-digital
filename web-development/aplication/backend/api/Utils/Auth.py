import jwt

def hasPermissionByToken(token):                            
    def decorator(fn):                                            
        def decorated(*args,**kwargs): 
            if (token):
                try:
                    decoded = jwt.decode(token, 'welisonmenezes', algorithms=['HS256'])
                    return decoded, 200
                except:
                    return {'message': 'token inválido'}, 403
        return decorated                                          
    return decorator

def getJWTEncode():
    return jwt.encode({'user': 'welison', 'permission': 'admin'}, 'welisonmenezes', algorithm='HS256')
