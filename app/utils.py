from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from graphql import GraphQLError
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.config.settings import ALGORITHM, SECRET_KEY, TOKEN_EXPIRATION_TIME_IN_MINS
from app.db.database import Session
from app.db.models import User


def generate_token(email, role):
    expiration_time = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_TIME_IN_MINS)
    
    payload = {
        "sub": email,
        "role": role,
        "exp": expiration_time
    }
    
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)


def hash_password(pwd):
    ph = PasswordHasher()
    return ph.hash(pwd)


def verify_password(hashed_pwd, pwd):
    ph = PasswordHasher()
    
    try:
        ph.verify(hashed_pwd, pwd)
    except VerifyMismatchError:
        raise GraphQLError('Invalid password')
    
    
def get_authenticated_user(context):
    request = context.get('request')
    auth_header = request.headers.get('Authorization')
    
    token = auth_header.split(' ')
    
    if auth_header and token[0] == 'Bearer' and len(token) == 2:
        token = auth_header.split(' ')[1]  # jwt token
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
            if datetime.now(timezone.utc) > datetime.fromtimestamp(payload['exp'], tz=timezone.utc):
                raise GraphQLError('Token has expired')
            
            session = Session()
            user = session.query(User).filter(User.id == payload.get('sub')).first()
            
            if not user:
                raise GraphQLError('Could not authenticate user')
            
            return user
        except jwt.exceptions.PyJWTError:
            raise GraphQLError('Invalid authentication token')
        except Exception as e:
            raise GraphQLError('Could not authenticate user')
    else:
        raise GraphQLError('Missing authentication header')
    
    
def admin_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1] # 2nd positional argument
        user = get_authenticated_user(info.context)
        
        if user.role != 'admin':
            raise GraphQLError('You are not authorized to perform this action')
        
        return func(*args, **kwargs)
    return wrapper


def authd_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1] # 2nd positional argument
        get_authenticated_user(info.context)
        return func(*args, **kwargs)
    return wrapper


def authd_user_same_as(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1] # 2nd positional argument
        user_id = kwargs.get("user_id") # 3rd positional argument
        user = get_authenticated_user(info.context)
        
        if user.id != user_id:
            raise GraphQLError('You are not authorized to perform this action')
        
        return func(*args, **kwargs)
    return wrapper