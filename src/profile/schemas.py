import platform

from pydantic import BaseModel, constr, Field


class FeedbackBase(BaseModel):
    text: str


class FeedbackCreate(BaseModel):
    text: constr(max_length=1000)
    device_name: str = Field(platform.node(), alias="deviceName")
    os_version: str = Field(platform.system() + " " + platform.release(), alias="osVersion")
    app_version: str = Field("1.0.0", alias="appVersion")


class Feedback(FeedbackBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
