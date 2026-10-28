from sqlalchemy.ext.asyncio import AsyncSession
from app.db.crud.book import BookCrud
from app.db.schemas.books import BookCreate, BookUpdate


class BookService:
    @staticmethod
    async def create_book(db: AsyncSession, book: BookCreate):
        db_book = await BookCrud.create(db=db, book=book)
        await db.commit()          # DB에 영구 저장
        await db.refresh(db_book)  # 생성된 최신 데이터 불러오기
        return db_book

    @staticmethod
    async def get_book_by_id(db: AsyncSession, book_id: int):
        return await BookCrud.get_by_id(db=db, book_id=book_id)

    @staticmethod
    async def get_book_by_title(db: AsyncSession, title: str):
        result = await BookCrud.get_by_booktitle(db=db, title=title)
        # crud에서 데이터 추출을 안 했을 경우 여기서 대신 꺼내줌 (500 에러 방지)
        if hasattr(result, "scalars"):
            return result.scalars().all()
        return result

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
