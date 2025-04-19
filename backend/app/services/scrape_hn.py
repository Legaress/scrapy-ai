from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
import time
import logging
import concurrent.futures
from core.config import settings
from typing import List, Dict, Optional
from functools import partial
import os
import urllib3
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure urllib3 to use a larger connection pool
urllib3.PoolManager(maxsize=30)

class HackerNewsScraper:
    def __init__(self):
        self.driver: Optional[webdriver.Remote] = None
        # Use ThreadPoolExecutor with optimal workers based on your system
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(
            max_workers=min(5, (os.cpu_count() or 1) * 2)
        )
        self.driver_options = self._get_driver_options()

    def _get_driver_options(self) -> webdriver.ChromeOptions:
        """Configure and return Chrome options"""
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
        return options

    def connect(self) -> None:
        """Establishes connection with the Selenium container"""
        try:
            logger.info(f"Connecting to Selenium at {settings.selenium_command_executor}")
            self.driver = webdriver.Remote(
                command_executor=settings.selenium_command_executor,
                options=self.driver_options
            )
            self.driver.set_page_load_timeout(30)
            self.driver.set_script_timeout(30)
            logger.info("Successfully connected to Selenium")
        except WebDriverException as e:
            logger.error(f"Failed to connect to Selenium: {str(e)}")
            raise

    def _create_driver_instance(self) -> webdriver.Remote:
        """Create a new driver instance with configured options"""
        return webdriver.Remote(
            command_executor=settings.selenium_command_executor,
            options=self.driver_options
        )

    def _scrape_story_row(self, row) -> Optional[Dict[str, any]]:
        """Scrape a single story row"""
        try:
            title_element = row.find_element(By.CSS_SELECTOR, "td.title a")
            title = title_element.text.strip()
            url = title_element.get_attribute("href")

            # Get the score from the next row
            score = 0
            try:
                score_row = row.find_element(By.XPATH, "./following-sibling::tr")
                score_element = score_row.find_element(By.CSS_SELECTOR, "span.score")
                score_text = score_element.text
                score = int(''.join(filter(str.isdigit, score_text)))
            except (NoSuchElementException, ValueError):
                pass  # Default score remains 0

            return {
                "title": title,
                "score": score,
                "url": url
            }
        except NoSuchElementException:
            logger.warning("Failed to extract story details from row")
            return None

    def _scrape_page(self, page: int) -> List[Dict[str, any]]:
        """
        Scrape a single page of Hacker News
        :param page: Page number to scrape
        :return: List of stories from this page
        """
        thread_driver = None
        try:
            thread_driver = self._create_driver_instance()
            thread_driver.set_page_load_timeout(30)
            thread_driver.set_script_timeout(30)

            url = f"{settings.hnews_site_url}?p={page}" if page > 1 else settings.hnews_site_url
            logger.debug(f"Fetching page {page}: {url}")

            try:
                thread_driver.get(url)
                # Wait for main content to load
                WebDriverWait(thread_driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "tr.athing"))
                )
            except TimeoutException:
                logger.warning(f"Timeout loading page {page}, trying to continue")
                return []

            # Find all story rows
            rows = thread_driver.find_elements(By.CSS_SELECTOR, "tr.athing")
            logger.info(f"Found {len(rows)} stories on page {page}")

            # Process rows in parallel using thread pool
            with concurrent.futures.ThreadPoolExecutor() as row_executor:
                stories = list(filter(None, row_executor.map(
                    self._scrape_story_row,
                    rows,
                    timeout=10
                )))

            return stories

        except Exception as e:
            logger.error(f"Error scraping page {page}: {str(e)}", exc_info=True)
            return []
        finally:
            if thread_driver:
                try:
                    thread_driver.quit()
                except Exception as e:
                    logger.error(f"Error closing thread driver: {str(e)}")

    def fetch_top_stories(self, pages: int = 1) -> List[Dict[str, any]]:
        """
        Fetch top stories from Hacker News using multiple threads
        :param pages: Number of pages to scrape (default: 5)
        :return: List of dictionaries containing title, score, and URL for each story
        """
        if not (1 <= pages <= 10):  # Reasonable limit
            raise ValueError("Pages must be between 1 and 10")

        all_stories = []
        try:
            # Use partial to avoid lambda in map
            scrape_func = partial(self._scrape_page)
            
            # Process pages in parallel
            for page_stories in self.thread_pool.map(scrape_func, range(1, pages + 1)):
                all_stories.extend(page_stories)
                logger.info(f"Added {len(page_stories)} stories to results")

            # Sort stories by score (descending)
            all_stories.sort(key=lambda x: x['score'], reverse=True)
            logger.info(f"Total {len(all_stories)} stories fetched")

        except Exception as e:
            logger.error(f"Error during scraping: {str(e)}", exc_info=True)
            raise
        finally:
            self.close()

        return all_stories

    def close(self) -> None:
        """Safely close the Selenium driver"""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                logger.info("Selenium driver closed successfully")
            except Exception as e:
                logger.error(f"Error closing Selenium driver: {str(e)}")
        # Shutdown the thread pool
        self.thread_pool.shutdown(wait=True)