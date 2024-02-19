import secrets
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, JSON, MetaData, Table, Float, Date, DateTime
from sqlalchemy.orm import relationship
from src.database import Base

metadata = MetaData()

role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("role_id", Integer, ForeignKey(role.c.id)),
)

survey = Table(
    "survey",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("category", String, nullable=False),
)

user_response = Table(
    "user_response",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(user.c.id)),
    Column("survey_id", Integer, ForeignKey(survey.c.id)),
)

question = Table(
    "question",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("description", String),
    Column("short_description", String),

    Column("points", Integer),
    Column("distance", Float),
    Column("time", Float),

    Column("price", Float),
    Column("rating", Float),
    Column("survey_id", Integer, ForeignKey(survey.c.id)),
)

route_rating = Table(
    "route_rating",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(user.c.id)),
    Column("question_id", Integer, ForeignKey(question.c.id)),
    Column("rating", Float),
)

historical_events = Table(
    "historical_events",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("event_date", Date),
    Column("event_description", String),
)

feedback = Table(
    "feedback",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.id"), nullable=False),
    Column("text", String, nullable=False),
    Column("device_name", String),
    Column("os_version", String),
    Column("app_version", String)
)

password_reset_code = Table(
    "password_reset_code",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("user_id", Integer, ForeignKey("user.id"), nullable=False),
    Column("code", String, nullable=False),
    Column("created_at", DateTime, nullable=False)
)


class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    permissions = Column(JSON)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey(Role.id))

    route_ratings = relationship("RouteRating", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")


class Survey(Base):
    __tablename__ = "survey"
    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    questions = relationship("Question", back_populates="survey")


class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    short_description = Column(String)
    points = Column(Integer)
    distance = Column(Float)
    time = Column(Float)
    price = Column(Float)
    rating = Column(Float)

    survey_id = Column(Integer, ForeignKey("survey.id"))
    survey = relationship("Survey", back_populates="questions")


class UserResponse(Base):
    __tablename__ = 'user_response'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    survey_id = Column(Integer, ForeignKey('survey.id'))


class RouteRating(Base):
    __tablename__ = 'route_rating'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    question_id = Column(Integer, ForeignKey('question.id'))
    rating = Column(Float)

    user = relationship("User")
    question = relationship("Question")


class HistoricalEvent(Base):
    __tablename__ = 'historical_events'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    event_date = Column(Date)
    event_description = Column(String)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    text = Column(String, nullable=False)
    device_name = Column(String)
    os_version = Column(String)
    app_version = Column(String)

    user = relationship("User", back_populates="feedbacks")


class PasswordResetCode(Base):
    __tablename__ = "password_reset_code"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    code = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")

    @classmethod
    def generate_code(cls) -> str:
        return secrets.token_urlsafe(6)
