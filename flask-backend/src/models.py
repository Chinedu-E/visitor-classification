from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from typing import List
from datetime import datetime

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Website(Base):
    __tablename__ = 'websites'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    last_scraped: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    
    questions: Mapped[List["Question"]] = relationship(back_populates="website")
    

class Question(Base):
    __tablename__ = 'questions'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    website_id: Mapped[int] = mapped_column(ForeignKey('websites.id'))
    text: Mapped[str] = mapped_column(Text, nullable=False)
    
    website: Mapped["Website"] = relationship(back_populates="questions")
    options: Mapped[List["QuestionOption"]] = relationship(back_populates="question")
    

class QuestionOption(Base):
    __tablename__ = 'question_options'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id'))
    text: Mapped[str] = mapped_column(Text, nullable=False)
    
    question: Mapped["Question"] = relationship(back_populates="options")
