from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# 프로젝트 구조에 맞는 임포트 경로로 수정해 주세요
# from db.database import get_db
# from db.crud import book as crud_book
# from db.schemas import book as schema_book

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

# 1. 도서 목록 조회 (Read - 여러 개)
@router.get("/")
def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # books = crud_book.get_books(db, skip=skip, limit=limit)
    # return books
    return {"message": "도서 목록 조회 성공"}

# 2. 특정 도서 상세 조회 (Read - 단건)
@router.get("/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    # book = crud_book.get_book(db, book_id=book_id)
    # if not book:
    #     raise HTTPException(status_code=404, detail="Book not found")
    # return book
    return {"message": f"{book_id}번 도서 조회 성공"}

# 3. 도서 등록 (Create)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_book(book: dict, db: Session = Depends(get_db)): # schema_book.BookCreate 등으로 변경 가능
    # return crud_book.create_book(db=db, book=book)
    return {"message": "도서 등록 성공", "data": book}

# 4. 도서 수정 (Update - 전체 또는 일부 수정)
@router.put("/{book_id}")
def update_book(book_id: int, book: dict, db: Session = Depends(get_db)):
    # updated_book = crud_book.update_book(db=db, book_id=book_id, book=book)
    # if not updated_book:
    #     raise HTTPException(status_code=404, detail="Book not found")
    # return updated_book
    return {"message": f"{book_id}번 도서 수정 성공", "data": book}

# 5. 도서 삭제 (Delete)
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    # success = crud_book.delete_book(db=db, book_id=book_id)
    # if not success:
    #     raise HTTPException(status_code=404, detail="Book not found")
    # return None
    return {"message": f"{book_id}번 도서 삭제 성공"}
