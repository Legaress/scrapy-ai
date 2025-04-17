import time
import logging
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import chardet
from core.config import settings
from utils.models import Book, BookRepository
from typing import Optional, List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BookScraper:
    def __init__(self):
        """Initialize the book scraper"""
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': settings.user_agent})
        self.book_repository = BookRepository()
        self.executor = ThreadPoolExecutor(max_workers=5)

    def _get_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch a page and return BeautifulSoup object"""
        try:
            time.sleep(settings.request_delay)
            response = self.session.get(url, timeout=settings.request_timeout)
            response.raise_for_status()
            
            detected_encoding = chardet.detect(response.content)['encoding'] or 'utf-8'
            return BeautifulSoup(response.content.decode(detected_encoding, errors='replace'), 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Failed to fetch page {url}: {str(e)}")
            return None

    def _extract_book_details(self, book_url: str) -> Optional[Book]:
        """Extract book details from a book page"""
        soup = self._get_page(book_url)
        if not soup:
            return None

        try:
            # Find required elements
            title = soup.select_one('h1')
            price = soup.select_one('p.price_color')
            category = soup.select_one('ul.breadcrumb li:nth-child(3)')
            image_element = soup.select_one('div.item.active img')

            if not all([title, price, category,image_element]):
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
            image_url = ""
            if image_element and 'src' in image_element.attrs:
                image_url = urljoin(book_url, image_element['src'])

            return Book(
                title=title.text.strip(),
                category=category.text.strip(),
                price=str(price_value),
                image_url=image_url
            )
        except Exception as e:
            logger.error(f"Failed to parse book: {str(e)}")
            return None

    def _get_next_page(self, soup: BeautifulSoup, current_url: str) -> Optional[str]:
        """Get the URL of the next page"""
        next_button = soup.select_one('li.next a')
        return urljoin(current_url, next_button['href']) if next_button and 'href' in next_button.attrs else None

    def _process_book(self, book_url: str) -> bool:
        """Process a single book"""
        book_details = self._extract_book_details(book_url)
        if not book_details:
            return False

        try:
            price = float(book_details.price)
            if price >= settings.max_price:
                logger.info(f"Skipping book {book_details.title} - price {price} exceeds maximum {settings.max_price}")
                return False

            return bool(self.book_repository.store_book(book_details))
        except ValueError:
            logger.error(f"Invalid price format for book {book_details.title}: {book_details.price}")
            return False

    def _process_page(self, page_url: str) -> Tuple[int, List[str]]:
        """Process a single page of books"""
        soup = self._get_page(page_url)
        if not soup:
            return 0, []

        books = soup.find_all('article', class_='product_pod')
        logger.info(f"Found {len(books)} books on page")

        # Process books in parallel
        futures = []
        for book in books:
            book_link = book.find('h3').find('a')
            if book_link and 'href' in book_link.attrs:
                book_url = urljoin(page_url, book_link['href'])
                futures.append(self.executor.submit(self._process_book, book_url))

        # Collect results
        books_collected = sum(1 for future in as_completed(futures) if future.result())

        # Get next page URL
        next_page = self._get_next_page(soup, page_url)
        next_pages = [next_page] if next_page else []

        return books_collected, next_pages

    def scrape(self) -> int:
        """Scrape books from the website"""
        logger.info("Starting book scraping")

        try:
            self.book_repository.clear_all()
            logger.info("Redis database cleared")

            books_collected = 0
            pages_to_process = [settings.book_base_url + "index.html"]
            processed_pages = set()

            while books_collected < settings.max_books and pages_to_process:
                current_page = pages_to_process.pop(0)
                if current_page in processed_pages:
                    continue

                processed_pages.add(current_page)
                logger.info(f"Processing page: {current_page}")

                new_books, next_pages = self._process_page(current_page)
                books_collected += new_books
                pages_to_process.extend(p for p in next_pages if p not in processed_pages)

                if books_collected >= settings.max_books:
                    break

            if books_collected < settings.min_books:
                logger.warning(f"Only collected {books_collected} books (minimum requested: {settings.min_books})")
            else:
                logger.info(f"Successfully collected {books_collected} books")

            return books_collected

        except Exception as e:
            logger.error(f"Unexpected error during scraping: {str(e)}")
            return books_collected
        finally:
            self.session.close()
            self.executor.shutdown(wait=True)