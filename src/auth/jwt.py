#создание и верификация jwt (по сути, ничего менять не надо)
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "e95a3684b9982fcfd46eea716707f80cef515906eb49c4cb961dfde39a41ce21"
ALGORITHM = "HS256"
EXPIRATION_TIME = timedelta(minutes=30)

def create_jwt_token(data: dict):
    expiration = datetime.utcnow() + EXPIRATION_TIME
    data.update({"exp": expiration})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_jwt_token(token: str):
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_data
    except jwt.PyJWTError:
        return None