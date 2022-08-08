from functools import wraps
from flask import request, make_response
import jwt

SECRET_KEY = 'secretkey123'

def token_requirement(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'X_ACCES_TOKEN' in request.headers:
            token = request.headers['X_ACCES_TOKEN']
        if not token:
            return make_response({'message': 'Token is missing'})
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except:
            return make_response({'message':'Token is invalid'})

        return f(data['access_level'],*args, **kwargs)

    return decorated
