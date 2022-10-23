import cryptocode
import jwt
import secrets

from functools import wraps
from datetime import datetime, timedelta

from flask import request, Response, jsonify, redirect

from models.User import User
from main import SUPERMEGASECRET, JWT_ALGORITHM, JWT_EXP_DELTA_SECONDS, REF_EXP_DELTA_SECONDS
from models.JWT import JWT

def auth_middleware(API=False):
    def middleware(f):
        @wraps(f)
        def _middleware(*args, **kwargs):
            request.user = None
            jwt_token = request.cookies.get('token')

            print("IS", jwt_token)
            if not(jwt_token):
                request.user = None
                if API:
                    request.stat = 0
                    return f(*args, **kwargs)
                    
                return redirect("login")

            try:
                jwt_token = cryptocode.decrypt(jwt_token, SUPERMEGASECRET)
            except:
                if API:
                    request.stat = 0
                    return f(*args, **kwargs)
                    
                return redirect("login")

            kid = jwt.get_unverified_header(jwt_token)['kid']
            print('KID', kid)

            try:
                secret = JWT.query.filter_by(kid=kid).first().secret
            except Exception as e:
                print('1', e)
                if API:
                    request.stat = 0
                    return f(*args, **kwargs)
                    
                return redirect("login")

            if jwt_token:
                try:
                    payload = jwt.decode(jwt_token, secret,
                                        algorithms=[JWT_ALGORITHM])

                except jwt.ExpiredSignatureError:
                    refresh_token = request.cookies.get('ref_token')
                    
                    try:
                        refresh_token = cryptocode.decrypt(refresh_token, SUPERMEGASECRET)
                    except Exception as e:
                        print('7', e)
                        if API:
                            request.stat = 0
                            return f(*args, **kwargs)
                            
                        return redirect("login")


                    try:
                        ref_kid = jwt.get_unverified_header(refresh_token)['kid']

                        try:
                            secret = JWT.query.filter_by(kid=ref_kid).first().secret
                        except Exception as e:
                            print('2', e)
                            if API:
                                request.stat = 0
                                return f(*args, **kwargs)
                                
                            return redirect("login")

                        payload = jwt.decode(refresh_token, secret, algorithms=[JWT_ALGORITHM])

                    except jwt.ExpiredSignatureError:
                        print('EXP')
                        if API:
                            request.stat = 0
                            return f(*args, **kwargs)
                            
                        return redirect("login")

                    try:
                        request.user = User.query.filter_by(id=payload['user_id']).first()

                        r = f(*args, **kwargs)
                        
                        if API:
                            return

                        token = create_access_token(request.user)
                        refresh = create_access_token(request.user, refresh=True)
                            
                        r.set_cookie('token', cryptocode.encrypt(token, SUPERMEGASECRET))

                        expire_date = datetime.now()
                        expire_date = expire_date + timedelta(seconds=REF_EXP_DELTA_SECONDS)

                        r.set_cookie('ref_token', cryptocode.encrypt(refresh, SUPERMEGASECRET), expires=expire_date)

                        return r
                    except AttributeError:
                        print('err', r)
                        if API:
                            request.stat = 0
                            return f(*args, **kwargs)
                            
                        return redirect("login")

                except Exception as e:
                    print(e)
                    if API:
                        request.stat = 0
                        return f(*args, **kwargs)
                        
                    return redirect("login")

                request.user = User.query.filter_by(id=payload['user_id']).first()
                print(request.user.email)

                return f(*args, **kwargs)

        return _middleware
    
    return middleware

def create_access_token(user, refresh=False, token=None):
    if refresh:
        payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(seconds=REF_EXP_DELTA_SECONDS)
    }

    else:
        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS),
        }

    JWT_SECRET = secrets.token_urlsafe(32)
    KID = secrets.token_urlsafe(16)

    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM, headers={'kid': KID})
    db.session.add(JWT(kid=KID, secret=JWT_SECRET, jwt=jwt_token if jwt_token else None))
    db.session.commit()

    print(jwt_token, JWT_SECRET)
    return jwt_token

def delete_auth_token():
    token = request.cookies.get('token')

    try:
        token = cryptocode.decrypt(token, SUPERMEGASECRET)
    except:
        return jsonify({'message': 'Invalid token!'})

    tkid = jwt.get_unverified_header(token)['kid']

    ref_token = request.cookies.get('ref_token')

    try:
        ref_token = cryptocode.decrypt(ref_token, SUPERMEGASECRET)
    except:
        return jsonify({'message': 'Invalid ref token!'})

    rkid = jwt.get_unverified_header(ref_token)['kid']

    JWT.query.filter_by(kid=tkid).delete()
    JWT.query.filter_by(kid=rkid).delete()

    db.session.commit()