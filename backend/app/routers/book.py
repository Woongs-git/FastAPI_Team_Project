from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.crud.book import BookCrud
from app.db.schemas.books import BookCreate, BookUpdate

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

# 1. 도서 등록 (Create)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    return await BookCrud.create(db=db, book=book)

# 2. 특정 도서 상세 조회 (Read - ID로 단건 조회)
@router.get("/{book_id}")
async def get_book_by_id(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await BookCrud.get_by_id(db=db, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# 3. 도서 제목으로 조회
@router.get("/title/{title}")
async def get_book_by_title(title: str, db: AsyncSession = Depends(get_db)):
    book = await BookCrud.get_by_booktitle(db=db, title=title)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# 4. 도서 수정 (Update)
@router.put("/{book_id}")
async def update_book(book_id: int, book: BookUpdate, db: AsyncSession = Depends(get_db)):
    updated_book = await BookCrud.update_by_id(db=db, book_id=book_id, book=book)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

# 5. 도서 삭제 (Delete)
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    deleted_book = await BookCrud.delete_by_id(db=db, book_id=book_id)
    if not deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return None
