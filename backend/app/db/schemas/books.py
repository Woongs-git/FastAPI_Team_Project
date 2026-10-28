from pydantic import BaseModel


class BookBase(BaseModel):
    book_title: str
    genre_id: int
    author_id: int
    pub_id: int


class BookCreate(BaseModel):
    book_title: str
    genre_id: int
    author_id: int
    pub_id: int


class BookUpdate(BaseModel):
    book_title: str | None = None
    genre_id: int | None = None
    author_id: int | None = None
    pub_id: int | None = None


class BookInDB(BookBase):
    book_id: int

    class Config:
        from_attributes = True


class BookRead(BookInDB):
    pass
