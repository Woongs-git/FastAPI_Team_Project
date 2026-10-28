from fastapi import APIRouter

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

@router.get("/")
def get_books():
    return {"message": "도서 목록 조회 성공"}
