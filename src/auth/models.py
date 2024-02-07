from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, Boolean, MetaData, JSON, ForeignKey

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

    # Column("username", String, nullable=False),
    # Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    # Column("role_id", Integer, ForeignKey(role.c.id)),
)

token = Table(
    "token",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("access_token", String, unique=True, index=True),
    Column("user_id", Integer, ForeignKey(user.c.id)),
)

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey(role.c.id))
    hashed_password: str = Column(String(length=1024), nullable=False)

class Token(Base):
    __tablename__ = "token"

    id = Column(Integer, primary_key=True)
    access_token = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey(user.c.id))


# class User(SQLAlchemyBaseUserTable[int], Base):
#     id = Column(Integer, primary_key=True)
#     email = Column(String, nullable=False)
#     # username = Column(String, nullable=False)
#     registered_at = Column(TIMESTAMP, default=datetime.utcnow)
#     role_id = Column(Integer, ForeignKey(role.c.id))
#     hashed_password: str = Column(String(length=1024), nullable=False)
#     # is_active: bool = Column(Boolean, default=True, nullable=False)
#     # is_superuser: bool = Column(Boolean, default=False, nullable=False)
#     # is_verified: bool = Column(Boolean, default=False, nullable=False)