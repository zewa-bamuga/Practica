# from sqlalchemy import Column, Integer, String, ForeignKey, JSON, MetaData, Table
# from sqlalchemy.orm import relationship
# from src.database import Base
#
# metadata = MetaData()
#
# survey = Table(
#     "survey",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("category", String, nullable=False),
# )
#
# question = Table(
#     "question",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("text", String),
#     Column("survey_id", Integer, ForeignKey("survey.id")),
# )
#
# user_response = Table(
#     "user_response",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("question_id", Integer, ForeignKey("question.id")),
#     Column("answer", JSON),
# )
#
# class Survey(Base):
#     __tablename__ = "survey"
#     id = Column(Integer, primary_key=True, index=True)
#     category = Column(String, index=True)
#     questions = relationship("Question", back_populates="survey")
#
# class Question(Base):
#     __tablename__ = 'question'
#     id = Column(Integer, primary_key=True, index=True)
#     text = Column(String)
#     survey_id = Column(Integer, ForeignKey('survey.id'))
#     survey = relationship("Survey", back_populates="questions")
#
#
# class UserResponse(Base):
#     __tablename__ = 'user_response'
#
#     id = Column(Integer, primary_key=True)
#     question_id = Column(Integer, ForeignKey('question.id'))
#     answer = Column(JSON)
#
#     # Связь с таблицей question
#     question = relationship("Question", back_populates="user_responses")
