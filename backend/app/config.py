from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Redis Configuration
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0
    
    # Selenium Configuration
    selenium_host: str = "selenium"  # Docker service name for Selenium container
    selenium_port: int = 4444  # External port mapped to Selenium container
    selenium_command_executor: str = "http://selenium:4444/wd/hub"  # Internal Selenium hub URL
    
    # Book Scraper Configuration
    book_base_url: str = "https://books.toscrape.com/"
    max_books: int = 100
    min_books: int = 50
    max_price: float = 20.0
    request_delay: float = 1.0
    request_timeout: int = 10
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

    hnews_site_url: str = "https://news.ycombinator.com/news"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()