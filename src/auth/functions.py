from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import schemas
from src.auth.jwt import create_jwt_token, verify_jwt_token
from src.auth.models import User, PasswordResetCode
from src.auth.schemas import UserCreate
from src.database import get_async_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
apikey_scheme = APIKeyHeader(name="Authorization")


# Функция для регистрации пользователя
async def register_and_authenticate_async(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    existing_user = await session.execute(select(User).where(User.email == user_data.email))
    if existing_user.scalar():
        raise HTTPException(status_code=400, detail="Пользователь с этой электронной почтой уже существует!")

    user = User(email=user_data.email, hashed_password=pwd_context.hash(user_data.password), role_id=1)
    session.add(user)
    await session.commit()

    await send_hello(user)

    jwt_token = create_jwt_token({"sub": user.email})
    return {"access_token": jwt_token, "token_type": "bearer"}

# Функция для отправки на почту сообщение о регистрации
async def send_hello(user: User):
    email_address = "tikhonov.igor2028@yandex.ru"
    email_password = "abqiulywjvibrefg"

    msg = EmailMessage()
    msg['Subject'] = "Подтверждение регистрации"
    msg['From'] = email_address
    msg['To'] = user.email
    msg.set_content(
        f"""\
        Вы успешно зарегистрировались на платформе Путеводитель по необычным местам!
        """
    )

    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)


# Функция для создания запроса на восстановление пароля
async def request_password_reset(email: str, session: AsyncSession):
    user = await session.execute(select(User).where(User.email == email))
    user = user.scalar()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь с таким адресом электронной почты не найден")

    code = PasswordResetCode.generate_code()
    password_reset_code = PasswordResetCode(user_id=user.id, code=code)
    session.add(password_reset_code)
    await session.commit()

    await send_verification_token(user, code)


# Функция для отправки на почту кода для восстановления пароля
async def send_verification_token(user: User, code: str):
    email_address = "tikhonov.igor2028@yandex.ru"
    email_password = "abqiulywjvibrefg"

    msg = EmailMessage()
    msg['Subject'] = "Сброс пароля"
    msg['From'] = email_address
    msg['To'] = user.email
    msg.set_content(
        f"""\
        Здравствуйте,

        Вы запросили сброс пароля на платформе Путеводитель по необычным местам.

        Код для сброса пароля: {code}

        Если вы не запрашивали сброс пароля, проигнорируйте это письмо.

        С уважением,
        Ваша команда Путеводитель по необычным местам
        """
    )

    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)


# Функция для проверки кода и смена пароля
async def confirm_password_reset(email: str, code: str, new_password: str, session: AsyncSession):
    user = await session.execute(select(User).where(User.email == email))
    user = user.scalar()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь с таким адресом электронной почты не найден")

    reset_code = await session.execute(select(PasswordResetCode).where(PasswordResetCode.user_id == user.id).order_by(
        PasswordResetCode.created_at.desc()).limit(1))
    reset_code = reset_code.scalar()

    if not reset_code or reset_code.code != code:
        raise HTTPException(status_code=400, detail="Неверный код сброса пароля")

    expiration_time = datetime.utcnow() - timedelta(minutes=15)
    if reset_code.created_at < expiration_time:
        raise HTTPException(status_code=400, detail="Истек срок действия кода сброса пароля")

    user.hashed_password = pwd_context.hash(new_password)
    session.delete(reset_code)
    await session.commit()


# Функция для аутентификации пользователя
async def authenticate_async(user_data: schemas.UserAuth, session: AsyncSession = Depends(get_async_session)):
    user_email = user_data.email
    user_password = user_data.password

    existing_user = await session.execute(select(User).where(User.email == user_email))
    user = existing_user.scalar()

    if not user:
        raise HTTPException(status_code=400, detail="Неверное имя пользователя или пароль")

    is_password_correct = pwd_context.verify(user_password, user.hashed_password)
    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Неверное имя пользователя или пароль")

    jwt_token = create_jwt_token({"sub": user.email})
    return {"access_token": jwt_token, "token_type": "bearer"}


# Проверка на аутентификацию пользователя
async def is_user_authenticated(access_token: str = Depends(apikey_scheme),
                                session: AsyncSession = Depends(get_async_session)):
    decoded_token, user = await verify_jwt_token(access_token, session)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user
