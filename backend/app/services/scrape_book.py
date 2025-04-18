import time
import logging
import httpx
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import chardet
from core.config import settings
from utils.models import Book, BookRepository
from typing import Optional, List, Tuple
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BookScraper:
    def __init__(self):
        """Initialize the scraper with an async HTTP client"""
        self.client = httpx.AsyncClient()
        self.client.headers.update({'User-Agent': settings.user_agent})
        self.book_repository = BookRepository()

    async def _get_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch a page and return BeautifulSoup object"""
        try:
            response = await self.client.get(url, timeout=settings.request_timeout)
            response.raise_for_status()

            detected_encoding = chardet.detect(response.content)['encoding'] or 'utf-8'
            return BeautifulSoup(response.content.decode(detected_encoding, errors='replace'), 'html.parser')
        
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} when fetching {url}")
        except httpx.RequestError as e:
            logger.error(f"Request failed for {url}: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error fetching page {url}: {str(e)}")
        return None

    async def _extract_book_details(self, book_url: str) -> Optional[Book]:
        """Extract book details from a book page"""
        soup = await self._get_page(book_url)
        if not soup:
            return None

        try:
            # Find required elements
            title = soup.select_one('h1')
            price = soup.select_one('p.price_color')
            category = soup.select_one('ul.breadcrumb li:nth-child(3) a')
            image_element = soup.select_one('div.item.active img')

            if not all([title, price, category, image_element]):
                logger.warning(f"Missing required elements for book at {book_url}")
                return None

            # Extract and parse price - remove currency symbol and convert to float
            price_text = price.text.strip().lstrip('£€$')
            try:
                price_value = float(price_text)
            except ValueError:
                logger.error(f"Invalid price format: {price_text}")
                return None

            # Extract image URL
            image_url = urljoin(book_url, image_element['src']) if image_element and 'src' in image_element.attrs else ""

            return Book(
                title=title.text.strip(),
                category=category.text.strip().lower(),
                price=str(price_value),
                image_url=image_url
            )
        except Exception as e:
            logger.error(f"Failed to parse book at {book_url}: {str(e)}", exc_info=True)
            return None

    async def _process_book(self, book_url: str) -> bool:
        """Process a single book"""
        book_details = await self._extract_book_details(book_url)
        if not book_details:
            return False

        try:
            price = float(book_details.price)
            if price >= settings.max_price:
                logger.info(f"Skipping book {book_details.title} - price {price} exceeds maximum {settings.max_price}")
                return False

            return bool(await self.book_repository.store_book(book_details))
        except ValueError:
            logger.error(f"Invalid price format for book {book_details.title}: {book_details.price}")
            return False
        except Exception as e:
            logger.error(f"Error storing book {book_details.title}: {str(e)}")
            return False

    async def _process_page(self, page_url: str) -> Tuple[int, List[str]]:
        """Process a single page of books"""
        soup = await self._get_page(page_url)
        if not soup:
            return 0, []

        books = soup.find_all('article', class_='product_pod')
        logger.info(f"Found {len(books)} books on page {page_url}")

        # Process books concurrently
        tasks = []
        for book in books:
            link = book.find('h3').find('a')
            if link and 'href' in link.attrs:
                book_url = urljoin(page_url, link['href'])
                tasks.append(self._process_book(book_url))

        results = await asyncio.gather(*tasks)
        successful_books = sum(results)

        # Get next page
        next_pages = []
        next_button = soup.select_one('li.next a')
        if next_button and 'href' in next_button.attrs:
            next_pages.append(urljoin(page_url, next_button['href']))

        return successful_books, next_pages

    async def scrape(self) -> int:
        """Scrape books from the website"""
        logger.info("Starting book scraping")

        books_collected = 0

        try:
            await self.book_repository.clear_all()
            logger.info("Database cleared")

            pages_to_process = [settings.book_base_url + "index.html"]
            processed_pages = set()

            while books_collected < settings.max_books and pages_to_process:
                current_page = pages_to_process.pop(0)
                if current_page in processed_pages:
                    continue

                processed_pages.add(current_page)
                logger.info(f"Processing page: {current_page}")

                new_books, next_pages = await self._process_page(current_page)
                books_collected += new_books
                pages_to_process.extend(p for p in next_pages if p not in processed_pages)

                if books_collected >= settings.max_books:
                    break

                logger.info(f"Successfully collected {books_collected} books so far")
                await asyncio.sleep(settings.request_delay)  # Be polite

            logger.info(f"Finished scraping. Total books collected: {books_collected}")
            return books_collected

        except Exception as e:
            logger.error(f"Unexpected error during scraping: {str(e)}", exc_info=True)
            return books_collected
        finally:
            await self.client.aclose()
            logger.info("HTTP client closed")