from sqlalchemy import Table, Column, Integer, String, MetaData, JSON, ForeignKey
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
    hashed_password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey(role.c.id))

class Token(Base):
    __tablename__ = "token"

    id = Column(Integer, primary_key=True)
    access_token = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey(user.c.id))