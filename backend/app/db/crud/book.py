from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.models.book import Book, Author, Genre
from app.db.schemas.books import BookCreate, BookUpdate


class BookCrud:
    @staticmethod
    async def create(db: AsyncSession, book: BookCreate):
        db_book = Book(**book.model_dump())
        db.add(db_book)
        await db.flush()
        return db_book

    @staticmethod
    async def get_by_id(db: AsyncSession, book_id: int) -> Book | None:
        result = await db.execute(select(Book).filter(Book.book_id == book_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_booktitle(db: AsyncSession, title: str) -> list[Book]:
        result = await db.execute(select(Book).filter((Book.book_title == title)))
        return result.scalars().all()

    @staticmethod
    async def get_by_author(db: AsyncSession, author: str) -> list[Book]:
        result = await db.execute(
            select(Book)
            .join(Author, Book.author_id == Author.author_id)
            .filter(Author.author_name == author)
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_genre(db: AsyncSession, genre: str) -> list[Book]:
        result = await db.execute(
            select(Book)
            .join(Genre, Book.genre_id == Genre.genre_id)
            .filter(Genre.genre_name == genre)
        )
        return result.scalars().all()

    @staticmethod
    async def update_by_id(
        db: AsyncSession, book_id: int, book: BookUpdate
    ) -> Book | None:
        db_book = await db.get(Book, book_id)
        if db_book:
            update_data = book.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                setattr(db_book, key, value)
            await db.flush()
            return db_book
        return None

    @staticmethod
    async def delete_by_id(db: AsyncSession, book_id: int) -> Book | None:
        db_book = await db.get(Book, book_id)
        if db_book:
            await db.delete(db_book)
            await db.flush()
            return db_book
        return None
