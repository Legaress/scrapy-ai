# Project Frodo - Web Scraping & Automation Platform

## Overview
This project is a comprehensive solution for web scraping, API management, and workflow automation with the following key components:
1. Web scraping system for book data and real-time Hacker News headlines
2. FastAPI backend with Redis storage
3. n8n workflow automation with AI agent integration
4. Frontend virtual assistant interface

## Key Features

### 1. Web Scraping System
- **Book Scraper** (`scrape_books.py`):
  - Extracts book data (title, price, category, image URL) from books.toscrape.com
  - Handles pagination to scrape 50-100 books
  - Filters books priced under £20
  - Stores results in Redis with `book:<id>` key format
  - Automatic execution during container initialization

- **Hacker News Scraper** (`scrape_hn.py`):
  - Real-time fetching of top stories (title, score, URL)
  - Handles pagination for first 5 pages
  - No permanent storage - always fetches fresh data
  - Built with Selenium for dynamic content handling

### 2. FastAPI Backend
**Endpoints**:
- `POST /init`: Triggers initial book scraping (used during container startup)
- `GET /books/search`: Search books by title or category with filters
- `GET /headlines`: Real-time Hacker News headlines (never cached)
- `GET /books`: Retrieve books with optional category filtering

**Features**:
- Swagger UI documentation
- Poetry for dependency management
- Pydantic models for data validation
- Redis integration for book storage

### 3. n8n Workflow Automation
**AI Agent Integration**:
- Two configured tools:
  - Book data retrieval from Redis
  - Real-time Hacker News headline fetching
- Webhook endpoint `/ask` for user queries:
  - "Find me a book about science under £15"
  - "Show me trending tech headlines"

### 4. Frontend Virtual Assistant
- Communicates exclusively with n8n's webhook
- Supports text input and response display

## Technical Stack
- **Scraping**: BeautifulSoup + Selenium
- **Backend**: FastAPI + Redis
- **Automation**: n8n with Geminis Flash 2.0
- **Frontend**: Vuetufy
- **Infrastructure**: Docker Compose

## System Architecture
```User → Frontend → n8n Webhook → AI Agent → FastAPI → [Redis | Hacker News]```


## Getting Started

1. **Prerequisites**:
   - Docker and Docker Compose installed
   - Python 3.13

2. **Installation**:
   ```docker-compose up```
   
3. **Access Services**:
   - Frontend: http://localhost:13000
   - API Docs: http://localhost:18000/docs
   - n8n: http://localhost:5678 (admin/admin)
   - Selenium: http://localhost:14440

4. **Initialization**:
   - Book scraping runs automatically on startup
   - Trigger manually via POST /init if needed