from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.functions import is_user_authenticated
from src.auth.models import User
from src.auth.schemas import UserGet, ChangePasswordRequest
from src.database import get_async_session
from src.profile.functions import change_password_async, leave_feedback_async
from src.profile.schemas import FeedbackCreate, Feedback, FeedbackBase

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


@router.get("/get-me", response_model=UserGet)
async def get_user_info(user: UserGet = Depends(is_user_authenticated)):
    return user


@router.post("/change-password")
async def change_password(request_data: ChangePasswordRequest, current_user: User = Depends(is_user_authenticated),
                          session: AsyncSession = Depends(get_async_session)):
    user_email = current_user.email
    old_password = request_data.old_password
    new_password = request_data.new_password
    return await change_password_async(user_email, old_password, new_password, session=session)


@router.post("/leave-feedback", response_model=FeedbackBase)
async def leave_feedback_route(feedback_data: FeedbackCreate, current_user: User = Depends(is_user_authenticated),
                               session: AsyncSession = Depends(get_async_session)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return await leave_feedback_async(feedback_data=feedback_data, user_id=current_user.id,
                                      device_name=feedback_data.device_name, os_version=feedback_data.os_version,
                                      app_version=feedback_data.app_version, session=session)
