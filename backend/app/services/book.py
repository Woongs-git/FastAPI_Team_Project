from sqlalchemy.ext.asyncio import AsyncSession
from app.db.crud.book import BookCrud
from app.db.schemas.books import BookCreate, BookUpdate

class BookService:
    
    @staticmethod
    async def create_book(db: AsyncSession, book: BookCreate):
        # 도서 생성 비즈니스 로직 처리
        return await BookCrud.create(db=db, book=book)

    @staticmethod
    async def get_book_by_id(db: AsyncSession, book_id: int):
        # ID로 도서 조회 로직
        book = await BookCrud.get_by_id(db=db, book_id=book_id)
        return book

    @staticmethod
    async def get_book_by_title(db: AsyncSession, title: str):
        # 제목으로 도서 조회 로직
        return await BookCrud.get_by_booktitle(db=db, title=title)

    @staticmethod
    async def update_book(db: AsyncSession, book_id: int, book: BookUpdate):
        # 도서 수정 로직
        return await BookCrud.update_by_id(db=db, book_id=book_id, book=book)

    @staticmethod
    async def delete_book(db: AsyncSession, book_id: int):
        # 도서 삭제 로직
        return await BookCrud.delete_by_id(db=db, book_id=book_id)
