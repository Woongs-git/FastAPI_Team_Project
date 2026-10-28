from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_db
from app.db.models.book import Book, Genre, Author, Publisher
from app.db.schemas.books import BookUpdate, BookRead

router = APIRouter(prefix="/books", tags=["Book"])


# 이름으로 장르/작가/출판사를 찾고, 없으면 새로 만들어서 돌려주는 도우미 함수
async def get_or_create(db: AsyncSession, model, name_column, name_value: str):
    result = await db.execute(select(model).filter(name_column == name_value))
    row = result.scalars().first()
    if row is None:
        row = model(**{name_column.key: name_value})
        db.add(row)
        await db.flush()  
    return row


async def to_book_read(db: AsyncSession, book: Book) -> dict:
    genre = await db.get(Genre, book.genre_id)
    author = await db.get(Author, book.author_id)
    publisher = await db.get(Publisher, book.pub_id)
    return {
        "book_id": book.book_id,
        "book_title": book.book_title,
        "genre_name": genre.genre_name,
        "author_name": author.author_name,
        "pub_name": publisher.pub_name,
    }


# 도서 수정 (보낸 필드만 수정)
@router.put("/{book_id}", response_model=BookRead)
async def update_book(
    book_id: int, body: BookUpdate, db: AsyncSession = Depends(get_db)
):
    book = await db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="도서를 찾을 수 없습니다.")

    data = body.model_dump(exclude_unset=True)  # 요청에 실제로 담겨 온 값만

    try:
        if data.get("book_title"):
            book.book_title = data["book_title"]

        if data.get("genre_name"):
            genre = await get_or_create(db, Genre, Genre.genre_name, data["genre_name"])
            book.genre_id = genre.genre_id

        if data.get("author_name"):
            author = await get_or_create(db, Author, Author.author_name, data["author_name"])
            book.author_id = author.author_id

        if data.get("pub_name"):
            publisher = await get_or_create(db, Publisher, Publisher.pub_name, data["pub_name"])
            book.pub_id = publisher.pub_id

        await db.commit()
        await db.refresh(book)
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="도서 수정 중 오류가 발생했습니다.")

    return await to_book_read(db, book)


# 도서 삭제
@router.delete("/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="도서를 찾을 수 없습니다.")

    try:
        await db.delete(book)
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="도서 삭제 중 오류가 발생했습니다.")

    return {"message": "도서가 삭제되었습니다.", "book_id": book_id}