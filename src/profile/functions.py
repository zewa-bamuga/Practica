from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.functions import pwd_context
from src.auth.models import User, Feedback
from src.database import get_async_session
from src.profile.schemas import FeedbackCreate


async def change_password_async(user_email: str, old_password: str, new_password: str,
                                session: AsyncSession = Depends(get_async_session)):
    existing_user = await session.execute(select(User).where(User.email == user_email))
    user = existing_user.scalar()

    if not user:
        raise HTTPException(status_code=400, detail="Пользователь не найден")

    is_old_password_correct = pwd_context.verify(old_password, user.hashed_password)
    if not is_old_password_correct:
        raise HTTPException(status_code=400, detail="Неправильный старый пароль")

    user.hashed_password = pwd_context.hash(new_password)
    await session.commit()
    return {"message": "Пароль успешно обновлен"}


async def leave_feedback_async(feedback_data: FeedbackCreate, user_id: int, device_name: str, os_version: str,
                               app_version: str,
                               session: AsyncSession = Depends(get_async_session)):

    feedback = Feedback(user_id=user_id, text=feedback_data.text, device_name=device_name,
                        os_version=os_version, app_version=app_version)
    session.add(feedback)
    await session.commit()
    return feedback
