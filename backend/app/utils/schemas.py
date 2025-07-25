from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    category: str
    price: float
    image_url: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: str

    class Config:
        from_attributes = True

class Headline(BaseModel):
    title: str
    score: int
    url: str

class BookSearchResponse(BaseModel):
    status: str = "success"
    count: int
    books: list[Book]

class HeadlinesResponse(BaseModel):
    status: str = "success"
    count: int
    headlines: list[Headline]

class CategoriesResponse(BaseModel):
    status: str = "success"
    count: int
    categories : list[str]
