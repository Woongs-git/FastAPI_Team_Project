from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
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
    async def get_by_booktitle(db: AsyncSession, title: str) -> Book | None:
        result = await db.execute(select(Book).filter((Book.book_title == title)))
        return result.scalars().all()


    @staticmethod
    async def get_by_author(db: AsyncSession, author: str) -> Book | None:
        result = await db.execute(
            select(Book)
            .join(Author, Book.author_id == Author.author_id)
            .filter(Author.author_name == author)
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_genre(db: AsyncSession, genre: str) -> Book | None:
        result = await db.execute(
            select(Book)
            .join(Author, Book.genre_id == genre.genre_id)
            .filter(Genre.genre_name == genre)
        )
        return result.scalars().all()

    @staticmethod
    async def update_by_id(
        db: AsyncSession, book_id: int, book: BookUpdate
    ) -> Book | None:
        db_book = await db.get(Book, book_id)  # select *from books where book_id=(1)
        if db_book:
            update_data = book.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                setattr(db_book, key, value)  # 골라낸 필드를 자동으로 대입
            await db.flush()  # 수정한 내용을 DB에 전송 (update books set book_title='aa'...where book_id=(1))
            return db_book
        return None

    @staticmethod
    async def delete_by_id(db: AsyncSession, book_id: int) -> Book | None:
        db_book = await db.get(Book, book_id)
        if db_book:
            await db.delete(db_book)
            await db.flush()  # delete from books where book_id=(1)
            return db_book  # 삭제된 객체반환
        return None
