from sqlalchemy.ext.asyncio import AsyncSession
from app.db.crud.book import BookCrud
from app.db.schemas.books import BookCreate, BookUpdate


class BookService:
    @staticmethod
    async def create_book(db: AsyncSession, book: BookCreate):
        db_book = await BookCrud.create(db=db, book=book)
        await db.commit()
        await db.refresh(db_book)
        return db_book

    @staticmethod
    async def get_book_by_id(db: AsyncSession, book_id: int):
        return await BookCrud.get_by_id(db=db, book_id=book_id)

    @staticmethod
    async def get_book_by_title(db: AsyncSession, title: str):
        result = await BookCrud.get_by_booktitle(db=db, title=title)
        if hasattr(result, "scalars"):
            return result.scalars().all()
        return result

    # [추가] 작가 이름으로 도서 조회
    @staticmethod
    async def get_book_by_author(db: AsyncSession, author: str):
        return await BookCrud.get_by_author(db=db, author=author)

    # [추가] 장르 이름으로 도서 조회
    @staticmethod
    async def get_book_by_genre(db: AsyncSession, genre: str):
        return await BookCrud.get_by_genre(db=db, genre=genre)

    @staticmethod
    async def update_book(db: AsyncSession, book_id: int, book: BookUpdate):
        updated_book = await BookCrud.update_by_id(db=db, book_id=book_id, book=book)
        if updated_book:
            await db.commit()
            await db.refresh(updated_book)
        return updated_book

    @staticmethod
    async def delete_book(db: AsyncSession, book_id: int):
        deleted_book = await BookCrud.delete_by_id(db=db, book_id=book_id)
        if deleted_book:
            await db.commit()
        return deleted_book
