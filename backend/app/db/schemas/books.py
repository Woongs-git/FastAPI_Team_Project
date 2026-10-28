from pydantic import BaseModel


class BookBase(BaseModel):
    book_title: str
    genre_name: str
    author_name: str
    pub_name: str


class BookCreate(BaseModel):
    book_title: str
    genre_name: str
    author_name: str
    pub_name: str


class BookUpdate(BaseModel):
    book_title: str | None = None
    genre_name: str | None = None
    author_name: str | None = None
    pub_name: str | None = None


class BookInDB(BookBase):
    book_id: int

    class Config:
        from_attributes = True


class BookRead(BookInDB):
    pass
