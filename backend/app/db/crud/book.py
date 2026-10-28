from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.book import Book
from app.db.schemas.books import BookUpdate


class BookCrud:

 
    @staticmethod
    async def update_by_id(db:AsyncSession, book_id:int, book:BookUpdate) -> Book | None:
        db_book=await db.get(Book, book_id) #select *from books where book_id=(1)
        if db_book:
            update_data=book.model_dump(exclude_unset=True) 
          
            for key, value in update_data.items():
                setattr(db_book, key, value) #골라낸 필드를 자동으로 대입
            await db.flush() #수정한 내용을 DB에 전송 (update books set book_title='aa'...where book_id=(1))
            return db_book
        return None


    @staticmethod
    async def delete_by_id(db:AsyncSession, book_id:int) -> Book | None:
        db_book=await db.get(Book, book_id)
        if db_book:
            await db.delete(db_book)
            await db.flush()  #delete from books where book_id=(1)
            return db_book  #삭제된 객체반환
        return None