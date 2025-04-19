from fastapi import FastAPI, HTTPException, Query
from core.config import settings
from services.scrape_book import BookScraper
from services.scrape_hn import HackerNewsScraper
from utils.schemas import BookSearchResponse, HeadlinesResponse, CategoriesResponse
from utils.models import BookRepository
import logging
import asyncio
from typing import List, Optional
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="BookScraper & Hacker News API",
    description="API for scraping books and fetching Hacker News headlines",
    version="1.0.0",
    license_info={
        "name": "MIT",
    },
)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint that provides API information.
    
    Returns basic information about the API and documentation URLs.
    """
    return {
        "message": "Welcome to the Book Scraper & Hacker News API",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "api_version": app.version
    }

@app.post("/init", tags=["Books"], response_model=dict)
async def init_scrape():
    """
    Initialize the book scraping process.
    
    Starts the scraping process to fetch books from configured sources.
    
    Returns:
        dict: Status message with scraping initiation result
        
    Raises:
        HTTPException: 500 if scraping fails
    """
    try:
        scraper = BookScraper()
        await scraper.scrape()
        return {
            "status": "success",
            "message": "Book scraping process initiated successfully",
            "timestamp": int(time.time())
        }
    except Exception as e:
        logger.error(f"Error during book scraping: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": f"Failed to initiate book scraping: {str(e)}",
                "timestamp": int(time.time())
            }
        )

@app.get("/headlines", tags=["Hacker News"], response_model=HeadlinesResponse)
async def get_headlines():
    """
    Get top Hacker News headlines.
    
    Fetches the current top stories from Hacker News with their scores and URLs.
    
    Returns:
        HeadlinesResponse: Structured response containing headlines data
        
    Raises:
        HTTPException: 500 if fetching headlines fails
    """
    try:
        scraper = HackerNewsScraper()
        headlines = await asyncio.to_thread(scraper.fetch_top_stories)
        return HeadlinesResponse(
            status="success",
            count=len(headlines),
            headlines=headlines,
            timestamp=int(time.time())
        )
    except Exception as e:
        logger.error(f"Error fetching headlines: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": f"Failed to fetch headlines: {str(e)}",
                "timestamp": int(time.time())
            }
        )

@app.get("/books/search", tags=["Books"], response_model=BookSearchResponse)
async def search_books(
    category: Optional[str] = Query(
        None,
        description="Filter books by category",
        example="fiction",
        min_length=2,
        max_length=50
    )
):
    """
    Search books with optional category filtering.
    
    Args:
        category (Optional[str]): Category to filter books by
        
    Returns:
        BookSearchResponse: Structured response containing books data
        
    Raises:
        HTTPException: 500 if search fails
    """
    try:
        books = BookRepository()
        result = await books.get_books(category=category)
        return BookSearchResponse(
            success=True,
            count=len(result),
            books=result,
            timestamp=int(time.time())
        )
    except Exception as e:
        logger.error(f"Error searching books: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": f"Error searching books: {str(e)}",
                "timestamp": int(time.time())
            }
        )

@app.get("/books/categories", tags=["Books"], response_model=CategoriesResponse)
async def get_book_categories():
    """
    Get all available book categories.
    
    Returns a list of all distinct book categories in the system.
    
    Returns:
        dict: Structured response containing categories data
        
    Raises:
        HTTPException: 500 if fetching categories fails
    """
    try:
        books = BookRepository()
        result = await books.get_categories()
        return {
            "success": True,
            "count": len(result),
            "categories": result,
            "timestamp": int(time.time())
        }
    except Exception as e:
        logger.error(f"Error fetching categories: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": f"Error fetching categories: {str(e)}",
                "timestamp": int(time.time())
            }
        )