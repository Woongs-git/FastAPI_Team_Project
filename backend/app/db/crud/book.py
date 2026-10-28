from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.book import Book, Author, Genre
from app.db.schemas.books import BookCreate


class BookCrud:
    @staticmethod
    async def create(db:AsyncSession, book:BookCreate):
        db_book=Book(**book.model_dump())
        db.add(db_book)
        await db.flush()
        return db_book

    @staticmethod
    async def get_by_id(db:AsyncSession, book_id:int) -> Book | None:
        result = await db.execute(select(Book).filter(Book.book_id==book_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_booktitle(db:AsyncSession, title:str) -> Book | None :
        result = await db.execute(select(Book).filter((Book.book_title == title)))
        return result

    @staticmethod
    async def get_by_author(db: AsyncSession, author: str) -> Book | None:
        result = await db.execute(
            select(Book)
            .join(Author, Book.author_id == Author.author_id)
            .filter(Author.author_name == author)
        )
        return result

    @staticmethod
    async def get_by_genre(db:AsyncSession, genre:str) -> Book | None :
        result = await db.execute(
            select(Book)
            .join(Author, Book.genre_id == genre.genre_id)
            .filter(Genre.genre_name == genre)
        )
        return result
    



