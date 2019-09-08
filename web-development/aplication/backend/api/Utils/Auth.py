from flask import request
import jwt
import sys
sys.path.insert(0, './api/Utils')
from Model import User

def hasPermissionByToken(roles, canSeeOwn=False):                            
    def decorator(fn):                                            
        def decorated(*args,**kwargs): 
            token = request.headers.get('Authorization')
            if (token):
                try:
                    decoded = jwt.decode(token, '#$#gdFDKF#993FDVKkfdkj#$$2@@@@dfdlafFGÇPLO^dfe__fd', algorithms=['HS256'])
                    user = User.query.filter_by(registry=decoded['registry']).first()
                    if user:
                        if 'user' in kwargs:
                            kwargs['user'] = user
                        if user.role in roles:
                            return fn(*args,**kwargs)
                        else:
                            if 'id' in kwargs and canSeeOwn:
                                if kwargs['id'] == user.id:
                                    return fn(*args,**kwargs)
                            return {'message': 'permissao negada'}, 403
                    else:
                        return {'message': 'este usuario nao existe'}
                except:
                    return {'message': 'token inválido'}, 403
            else:
                return {'message': 'missing token'}, 403
        return decorated                                          
    return decorator

def getJWTEncode(user):
    return jwt.encode({'registry': user.registry, 'role': user.role}, '#$#gdFDKF#993FDVKkfdkj#$$2@@@@dfdlafFGÇPLO^dfe__fd', algorithm='HS256')
