import jwt
import time
from datetime import datetime, timedelta

from src.auth.schemas import User

ALGORITHM = "HS256"
EXPIRATION_TIME = timedelta(minutes=30)
SECRET_KEY = "e95a3684b9982fcfd46eea716707f80cef515906eb49c4cb961dfde39a41ce21"

def token_response(token: str):
    return {
        "access_token": token
    }

def signJWT(user: User):
    payload = {
        "user": user,
        "exp": time.time() + 600
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token_response(token)

def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
        return decode_token if decode_token['exp'] >= time.time() else None
    except:
        return {}