from sqlalchemy import Integer, String, DateTime, ForeignKey
from datetime import datetime, timedelta
from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_login import UserMixin

class Base(DeclarativeBase):
  pass
db = SQLAlchemy(model_class=Base)

class Borrow(db.Model):
    __tablename__ = "borrow_table"

    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"), primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book_table.id"), primary_key=True)

    borrow_date: Mapped[str] = mapped_column(default=datetime.now().strftime("%d-%B-%Y"))
    due_date: Mapped[str] = mapped_column(default=(datetime.now() + timedelta(days=3)).strftime("%d-%B-%Y"))
    returned: Mapped[bool] = mapped_column(default=False)
    returned_date: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(default="borrowed")

    user: Mapped["User"] = relationship(back_populates="borrowed_book")
    book: Mapped["Book"] = relationship(back_populates="user_borrowed")

class User(db.Model, UserMixin):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(String(100))
    profile_url: Mapped[str] = mapped_column(String, default='../static/img/default.jpg')
    role: Mapped[str] = mapped_column(String, default='user')
    bio: Mapped[str] = mapped_column(String, default='I love reading books.')
    created_at: Mapped[int] = mapped_column(default=datetime.now().year)

    borrowed_book: Mapped[List["Borrow"]] = relationship(back_populates="user")

class Book(db.Model):
    __tablename__ = "book_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    author_name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(200))
    cover_url: Mapped[str] = mapped_column(String(100))
    copies_available: Mapped[int] = mapped_column(Integer, default=3)
    page_count: Mapped[int] = mapped_column(Integer)
    language: Mapped[str] = mapped_column(String)
    isbn: Mapped[str] = mapped_column(String)
    publisher: Mapped[str] = mapped_column(String)
    published_date: Mapped[str] = mapped_column(String)
    total_borrowed: Mapped[int] = mapped_column(Integer, default=0)

    user_borrowed: Mapped[List["Borrow"]] = relationship(back_populates="book")
