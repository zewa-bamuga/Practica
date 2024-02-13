from sqlalchemy import Column, Integer, String, ForeignKey, JSON, MetaData, Table, Float
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
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("survey_id", Integer, ForeignKey("survey.id")),
)

question = Table(
    "question",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("description", String),
    Column("short_description", String),

    Column("points", Integer),
    Column("distanse", Float),
    Column("time", Float),

    Column("price", Float),
    Column("rating", Float),
    Column("survey_id", Integer, ForeignKey("survey.id")),
)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey(role.c.id))


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
    distanse = Column(Float)
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
