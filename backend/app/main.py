from fastapi import FastAPI, HTTPException, Query
from scrape_book import BookScraper
from models import BookRepository
from scrape_hn import HackerNewsScraper
from schemas import (
    BookSearchResponse, HeadlinesResponse, Book, Headline
)

app = FastAPI(
    title="Book Scraper & Hacker News API",
    description="API for book search and real-time Hacker News headlines",
    version="1.0.0"
)

@app.post("/init", summary="Initialize book database")
async def init_scrape():
    """Initialize the book database with sample data"""
    try:
        scraper =  BookScraper()
        count = scraper.scrape()
        return {"status": "success", "message": f"Initialized with {count} books"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/books/search", response_model=BookSearchResponse, summary="Search books")
async def search_books(
    query: str = Query(..., description="Search term for title or author"),
    category = Query(None, description="Filter by category")
):
    """Search books by title or author with optional category filter"""
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")
    
    books = BookRepository.search_books(query, category)
    return {"count": len(books), "books": books}

@app.get("/headlines", response_model=HeadlinesResponse, summary="Get Hacker News headlines")
async def get_headlines():
    """Get current Hacker News headlines (always fresh)"""
    try:
        with HackerNewsScraper() as scraper:
            headlines = scraper.fetch_top_stories(pages=1)
        return {"count": len(headlines), "headlines": headlines}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/books", response_model=BookSearchResponse, summary="Get books")
async def get_books(
    category: str = Query(None, description="Filter by category")
):
    """Get books with optional category filter"""
    books = BookRepository.get_books(category)
    return {"count": len(books), "books": books}

@app.get("/")
def read_root():
    return {"Hello": "World"}
