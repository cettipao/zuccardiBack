from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.sqlalchemy import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    token = Column(String)
