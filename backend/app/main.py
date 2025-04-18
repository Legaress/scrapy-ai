from fastapi import FastAPI, HTTPException, Query
from core.config import settings
from services.scrape_book import BookScraper
from services.scrape_hn import HackerNewsScraper
from utils.schemas import BookSearchResponse, HeadlinesResponse
from utils.models import BookRepository
import logging
import asyncio
from typing import List, Optional
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")   
async def root():
    """
    Root endpoint.
    
    Returns:
        dict: Welcome message
    """
    return {
        "message": "Welcome to the Book Scraper & Hacker News API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

@app.post("/init")
async def init_scrape():
    """
    Initialize book scraping process.
    
    Returns:
        dict: Status message indicating scraping has started
        
    Raises:
        HTTPException: If scraping fails or encounters an error
    """
    try:
        scraper = BookScraper()
        await scraper.scrape()
        return {"status": "success", "message": "Book scraping process initiated"}
    except Exception as e:
        logger.error(f"Error during book scraping: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initiate book scraping: {str(e)}"
        )

@app.get("/headlines")
async def get_headlines():
    """
    Get Hacker News headlines.
    
    Returns:
        HeadlinesResponse: List of headlines with their scores and URLs
        
    Raises:
        HTTPException: If headline scraping fails or encounters an error
    """
    try:
        scraper = HackerNewsScraper()
        # Run the multithreaded fetch_top_stories method in a separate thread
        headlines = await asyncio.to_thread(scraper.fetch_top_stories)
        return HeadlinesResponse(
            status="success",
            count=len(headlines),
            headlines=headlines
        )
    except Exception as e:
        logger.error(f"Error fetching headlines: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch headlines: {str(e)}"
        )

@app.get("/books/search")
async def get_books(
    category: Optional[str] = Query(None, description="Filtrar libros por categoría")
):
    """
    Obtiene una lista de libros, con opción de filtrar por categoría.
    
    Ejemplos de categorías disponibles:
    - novela
    - ciencia ficción
    - literatura infantil
    """
    try:
        books = BookRepository()
        result = books.get_books(category=category)
        print(category)
        print(result)
        return {
            "success": True,
            "count": len(result),
            "results": result
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener los libros: {str(e)}"
        )


