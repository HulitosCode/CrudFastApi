from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, Integer, Boolean, Text, ForeignKey, Enum as SqlENum, DateTime, func
from sqlalchemy.orm import relationship
from App.database import Base


class TodoState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(80), unique=True)
    password = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    todos = relationship('Todo', back_populates='user', cascade='all, delete-orphan')


class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    state = Column(SqlENum(TodoState), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='todos',)