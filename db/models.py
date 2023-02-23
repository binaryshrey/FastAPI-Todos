from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class UserEntity(Base):
    __tablename__ = "users_table"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True, index=True)

    todos = relationship("TodoEntity", back_populates="owner")


class TodoEntity(Base):
    __tablename__ = "todos_table"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    is_complete = Column(Boolean, default=False, index=True)
    priority = Column(Integer, index=True)
    owner_id = Column(Integer, ForeignKey("users_table.id"))

    owner = relationship("UserEntity", back_populates="todos")