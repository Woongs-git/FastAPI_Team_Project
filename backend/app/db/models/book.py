from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, func, ForeignKey
from typing import Optional


class Genre(Base):
    __tablename__ = "genres"

    genre_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    genre_name: Mapped[str] = mapped_column(String(100), nullable=False)
    books: Mapped[list["Book"]] = relationship(back_populates="genre")



class Author(Base):
    __tablename__ = "authors"

    author_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    author_name: Mapped[str] = mapped_column(String(40), nullable=False)
    books: Mapped[list["Book"]] = relationship(back_populates="author")



class Publisher(Base):
    __tablename__ = "publishers"

    pub_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    pub_name: Mapped[str] = mapped_column(String(100), nullable=False)
    books: Mapped[list["Book"]] = relationship(back_populates="publisher")



class Book(Base):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    book_title: Mapped[str] = mapped_column(String(300), nullable=False)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.genre_id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.author_id"))
    pub_id: Mapped[int] = mapped_column(ForeignKey("publishers.pub_id"))

    genre: Mapped["Genre"] = relationship(back_populates="books")
    author: Mapped["Author"] = relationship(back_populates="books")
    publisher: Mapped["Publisher"] = relationship(back_populates="books")
