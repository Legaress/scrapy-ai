from redis import Redis
from config import settings
from pydantic import BaseModel
from typing import Optional, List
import json
import hashlib

class Book(BaseModel):
    """Model representing a book with its details"""
    id: Optional[str] = None
    title: str
    price: float
    category: str
    image_url: str

    def generate_id(self) -> str:
        """Generate a unique ID for the book based on its content"""
        # Create a string with book details that should be unique
        content = f"{self.title.lower()}|{self.category.lower()}|{self.price}"
        # Generate SHA-256 hash
        hash_object = hashlib.sha256(content.encode())
        # Return first 12 characters of the hash as the ID
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

    def store_book(self, book: Book) -> str:
        """Store book in Redis"""
        # Generate a hash-based ID for the book
        book.id = book.generate_id()
        book_key = f'book:{book.id}'
        
        # Check if book already exists
        if self.redis.exists(book_key):
            return book.id
        
        # Store book data and add to category index in a single transaction
        pipe = self.redis.pipeline()
        pipe.set(book_key, book.model_dump_json())
        pipe.sadd(f"category:{book.category.lower()}", book_key)
        pipe.execute()
        
        return book.id

    def get_books(self, category: Optional[str] = None) -> List[Book]:
        """Retrieve books from Redis, optionally filtered by category"""
        book_keys = (self.redis.smembers(f"category:{category.lower()}") 
                    if category else self.redis.keys('book:*'))
        
        if not book_keys:
            return []
            
        # Use pipeline for better performance when fetching multiple books
        pipe = self.redis.pipeline()
        for key in book_keys:
            pipe.get(key)
        book_data_list = pipe.execute()
        
        books = []
        for key, book_data in zip(book_keys, book_data_list):
            if book_data:
                book_dict = json.loads(book_data)
                book_dict['id'] = key.split(':')[1]
                books.append(Book(**book_dict))
        return books

    def search_books(self, query: str, category: Optional[str] = None) -> List[Book]:
        """Search books by title, optionally filtered by category"""
        query = query.lower()
        return [book for book in self.get_books(category) 
                if query in book.title.lower()]

    def clear_all(self):
        """Clear all book data from Redis"""
        self.redis.flushdb()