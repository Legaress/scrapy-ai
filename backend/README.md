# Book Scraper & Hacker News API

A FastAPI-based backend service for scraping books and Hacker News headlines.

## Features

- Book scraping from books.toscrape.com
- Hacker News headlines scraping
- Redis caching for improved performance
- RESTful API with FastAPI
- Dependency injection pattern
- Modular and scalable architecture

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── books.py
│   │       │   └── headlines.py
│   │       └── api.py
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   └── redis.py
│   ├── scrapes/
│   │   ├── scrape_book.py
│   │   └── scrape_hn.py
│   ├── services/
│   │   ├── book_service.py
│   │   └── headlines_service.py
│   ├── utils/
│   │   └── helpers.py
│   ├── main.py
│   └── __init__.py
├── Dockerfile
├── poetry.lock
├── pyproject.toml
└── README.md
```

## API Endpoints

### Books

- `GET /api/v1/books/` - Get all books from cache
- `GET /api/v1/books/search?query={query}` - Search books by title or author
- `POST /api/v1/books/scrape` - Scrape books from the configured website

### Headlines

- `GET /api/v1/headlines/` - Get all headlines from cache
- `POST /api/v1/headlines/scrape` - Scrape headlines from Hacker News

## Setup

1. Install dependencies:

```bash
poetry install
```

2. Set up environment variables:

Create a `.env` file in the `backend` directory with the following variables:

```
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
SELENIUM_HOST=selenium
SELENIUM_PORT=4444
```

3. Run the application:

```bash
poetry run uvicorn app.main:app --reload
```

## Docker

Build and run the application with Docker:

```bash
docker-compose up -d
```

## License

MIT
