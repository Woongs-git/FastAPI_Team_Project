from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.book import BookService
from app.db.schemas.books import BookCreate, BookUpdate

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

# 1. 도서 등록 (Create)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    return await BookService.create_book(db=db, book=book)

# 2. 도서 제목으로 조회 (고정 경로가 포함된 것을 위로 배치)
@router.get("/title/{title}")
async def get_book_by_title(title: str, db: AsyncSession = Depends(get_db)):
    books = await BookService.get_book_by_title(db=db, title=title)
    if not books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books

# 3. [추가] 작가 이름으로 도서 조회
@router.get("/author/{author}")
async def get_book_by_author(author: str, db: AsyncSession = Depends(get_db)):
    books = await BookService.get_book_by_author(db=db, author=author)
    if not books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books

# 4. [추가] 장르 이름으로 도서 조회
@router.get("/genre/{genre}")
async def get_book_by_genre(genre: str, db: AsyncSession = Depends(get_db)):
    books = await BookService.get_book_by_genre(db=db, genre=genre)
    if not books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books

# 5. 특정 도서 상세 조회 (ID로 단건 조회)
@router.get("/{book_id}")
async def get_book_by_id(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await BookService.get_book_by_id(db=db, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# 6. 도서 수정 (Update)
@router.put("/{book_id}")
async def update_book(book_id: int, book: BookUpdate, db: AsyncSession = Depends(get_db)):
    updated_book = await BookService.update_book(db=db, book_id=book_id, book=book)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

# 7. 도서 삭제 (Delete)
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    deleted_book = await BookService.delete_book(db=db, book_id=book_id)
    if not deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return None
