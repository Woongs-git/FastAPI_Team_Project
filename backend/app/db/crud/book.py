from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.book import Book, Genre, Author, Publisher
from app.db.schemas.books import BookUpdate


class BookCrud:

   
    @staticmethod
    async def get_or_create(db:AsyncSession, model, name_column, name_value:str):
        result = await db.execute(select(model).filter(name_column == name_value))
        row = result.scalars().first() 
        if row is None:
            row = model(**{name_column.key: name_value})
            db.add(row)
            await db.flush()  # 새 id를 받아오려고 DB에 전송 (commit 아님, 롤백 가능)
        return row


    #수정
    @staticmethod
    async def update_by_id(db:AsyncSession, book_id:int, book:BookUpdate) -> Book | None:
        db_book = await db.get(Book, book_id)  
        if db_book:
            update_data = book.model_dump(exclude_unset=True)  

            if update_data.get("book_title"):
                db_book.book_title = update_data["book_title"]

            
            if update_data.get("genre_name"):
                genre = await BookCrud.get_or_create(db, Genre, Genre.genre_name, update_data["genre_name"])
                db_book.genre_id = genre.genre_id

            if update_data.get("author_name"):
                author = await BookCrud.get_or_create(db, Author, Author.author_name, update_data["author_name"])
                db_book.author_id = author.author_id

            if update_data.get("pub_name"):
                publisher = await BookCrud.get_or_create(db, Publisher, Publisher.pub_name, update_data["pub_name"])
                db_book.pub_id = publisher.pub_id

            await db.flush()  
            return db_book
        return None

    #삭제
    @staticmethod
    async def delete_by_id(db:AsyncSession, book_id:int) -> Book | None:
        db_book = await db.get(Book, book_id)
        if db_book:
            await db.delete(db_book)
            await db.flush()  
            return db_book 
        return None