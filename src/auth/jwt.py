import jwt
from datetime import datetime, timedelta
from fastapi.responses import Response

SECRET_KEY = "e95a3684b9982fcfd46eea716707f80cef515906eb49c4cb961dfde39a41ce21"
ALGORITHM = "HS256"
EXPIRATION_TIME = timedelta(minutes=30)

def create_jwt_token(response: Response, data: dict):
    expiration = datetime.utcnow() + EXPIRATION_TIME
    data.update({"exp": expiration})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    print("Созданный токен:", token)
    response.set_cookie(key="access_token", value=token, httponly=True)

def verify_jwt_token(token: str): # Походу эта функция не рботает
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Декодированные данные:", decoded_data)
        return decoded_data
    except jwt.PyJWTError as e:
        print("JWT ошибка декодированияr:", e)
        return None