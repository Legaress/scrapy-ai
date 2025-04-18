from redis.asyncio import Redis
from core.config import settings
from pydantic import BaseModel
from typing import Optional, List
import json
import hashlib
import logging

class Book(BaseModel):
    """Model representing a book with its details"""
    id: Optional[str] = None
    title: str
    price: float
    category: str
    image_url: str

    def generate_id(self) -> str:
        """Generate a unique ID for the book based on its content"""
        content = f"{self.title.lower()}|{self.category.lower()}|{self.price}"
        hash_object = hashlib.sha256(content.encode())
        return hash_object.hexdigest()[:12]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "The Great Gatsby",
                "price": 19.99,
                "category": "Fiction",
                "image_url": "https://example.com/book.jpg",
            }
        }

class RedisManager:
    """Singleton class to manage Redis connection"""
    _instance = None
    _redis_client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._redis_client = Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                decode_responses=True,
                socket_timeout=5,
                retry_on_timeout=True
            )
        return cls._instance

    @property
    def client(self) -> Redis:
        return self._redis_client

class BookRepository:
    """Repository class for Book operations"""
    def __init__(self):
        self.redis = RedisManager().client

    async def store_book(self, book: Book) -> str:
        """Store book in Redis"""
        book.id = book.generate_id()
        book_key = f'book:{book.id}'
        
        # Check if book already exists
        if await self.redis.exists(book_key):
            return book.id
        
        # Store book data and add to category index in a single transaction
        async with self.redis.pipeline() as pipe:
            await pipe.set(book_key, book.model_dump_json()).execute()
            await pipe.sadd(f"category:{book.category.lower()}", book_key).execute()
        
        return book.id

    async def get_books(self, category: Optional[str] = None) -> List[str]:
        """Retrieve BOOK TITLES from Redis, optionally filtered by category"""
        try:
            # 1. Get book keys
            book_keys = (
                [f"book:{book_id}" for book_id in await self.redis.smembers(f"category:{category.lower()}")]
                if category
                else [key for key in await self.redis.keys('book:*')]
            )
            
            if not book_keys:
                return []

            # 2. Get data in pipeline
            async with self.redis.pipeline() as pipe:
                for key in book_keys:
                    await pipe.get(key)
                book_data_list = await pipe.execute()

            # 3. Extract only titles
            titles = []
            for key, book_data in zip(book_keys, book_data_list):
                if book_data:
                    try:
                        book_dict = json.loads(book_data)
                        titles.append(book_dict['title'])
                    except (json.JSONDecodeError, KeyError) as e:
                        logging.warning(f"Error processing book {key}: {str(e)}")
                        continue
            
            return titles

        except Exception as e:
            logging.error(f"Error in get_books: {str(e)}")
            return []

    async def clear_all(self):
        """Clear all book data from Redis"""
        await self.redis.flushdb()