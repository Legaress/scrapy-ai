from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
import time
import logging
import concurrent.futures
from core.config import settings
import urllib3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure urllib3 to use a larger connection pool
urllib3.PoolManager(maxsize=10)

class HackerNewsScraper:
    def __init__(self):
        self.driver = None
        # Reduce the number of worker threads to avoid connection pool exhaustion
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=3)
        
    def connect(self):
        """Establishes connection with the Selenium container"""
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-dev-shm-usage')
            
            # Set logging preferences in options instead of capabilities
            chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
            
            logger.info(f"Connecting to Selenium at {settings.selenium_command_executor}")
            self.driver = webdriver.Remote(
                command_executor=settings.selenium_command_executor,
                options=chrome_options
            )
            # Set page load timeout to prevent hanging
            self.driver.set_page_load_timeout(30)
            logger.info("Successfully connected to Selenium")
        except WebDriverException as e:
            logger.error(f"Failed to connect to Selenium: {str(e)}")
            raise
    
    def _scrape_page(self, page):
        """
        Scrape a single page of Hacker News
        :param page: Page number to scrape
        :return: List of stories from this page
        """
        # Create a new driver for each thread to avoid connection pool issues
        thread_driver = None
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-dev-shm-usage')
            
            thread_driver = webdriver.Remote(
                command_executor=settings.selenium_command_executor,
                options=chrome_options
            )
            thread_driver.set_page_load_timeout(30)
            
            stories = []
            base_url = settings.hnews_site_url
            
            if page > 1:
                url = f"{base_url}?p={page}"
            else:
                url = base_url
                
            logger.info(f"Fetching page {page}: {url}")
            try:
                thread_driver.get(url)
                # Wait for the page to load properly
                time.sleep(3)  # Increased wait time
            except TimeoutException:
                logger.warning(f"Timeout loading page {page}, trying to continue")
                return stories
            
            # Find all story rows
            try:
                rows = thread_driver.find_elements(By.CSS_SELECTOR, "tr.athing")
                logger.info(f"Found {len(rows)} stories on page {page}")
            except Exception as e:
                logger.error(f"Error finding story rows: {str(e)}")
                return stories
            
            for row in rows:
                try:
                    title_element = row.find_element(By.CSS_SELECTOR, "td.title a")
                    title = title_element.text
                    url = title_element.get_attribute("href")
                    
                    score = 0
                    # Get the score from the next row
                    try:
                        score_row = row.find_element(By.XPATH, "./following-sibling::tr")
                        score_element = score_row.find_element(By.CSS_SELECTOR, "span.score")
                        score_text = score_element.text
                        # Extract the number, handling different formats
                        score = int(''.join(filter(str.isdigit, score_text)))
                    except (NoSuchElementException, ValueError) as e:
                        # If no score element found or can't parse score, default to 0
                        logger.warning(f"No valid score found for story: {title}. Error: {str(e)}")
                    
                    stories.append({
                        "title": title,
                        "score": score,
                        "url": url
                    })
                except NoSuchElementException as e:
                    logger.warning(f"Failed to extract story details: {str(e)}")
                    continue
                    
            return stories
        except Exception as e:
            logger.error(f"Error scraping page {page}: {str(e)}")
            return []
        finally:
            # Always close the thread-specific driver
            if thread_driver:
                try:
                    thread_driver.quit()
                except Exception as e:
                    logger.error(f"Error closing thread driver: {str(e)}")
    
    def fetch_top_stories(self, pages: int = 5):
        """
        Fetch top stories from Hacker News using multiple threads
        :param pages: Number of pages to scrape (default: 5)
        :return: List of dictionaries containing title, score, and URL for each story
        """
        all_stories = []
        
        try:
            # Submit all page scraping tasks to the thread pool
            future_to_page = {
                self.thread_pool.submit(self._scrape_page, page): page 
                for page in range(1, pages + 1)
            }
            
            # Process results as they complete
            for future in concurrent.futures.as_completed(future_to_page):
                page = future_to_page[future]
                try:
                    page_stories = future.result()
                    all_stories.extend(page_stories)
                    logger.info(f"Completed scraping page {page}, found {len(page_stories)} stories")
                except Exception as e:
                    logger.error(f"Error processing page {page}: {str(e)}")
                    
        except Exception as e:
            logger.error(f"Error during scraping: {str(e)}")
            raise
        finally:
            self.close()
        
        return all_stories
    
    def close(self):
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