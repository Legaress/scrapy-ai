from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time
import logging
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HackerNewsScraper:
    def __init__(self):
        self.driver = None
        
    def connect(self):
        """Establishes connection with the Selenium container"""
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-dev-shm-usage')
            
            logger.info(f"Connecting to Selenium at {settings.selenium_command_executor}")
            self.driver = webdriver.Remote(
                command_executor=settings.selenium_command_executor,
                options=chrome_options
            )
            logger.info("Successfully connected to Selenium")
        except WebDriverException as e:
            logger.error(f"Failed to connect to Selenium: {str(e)}")
            raise
    
    def fetch_top_stories(self, pages: int = 5):
        """
        Fetch top stories from Hacker News
        :param pages: Number of pages to scrape (default: 5)
        :return: List of dictionaries containing title, score, and URL for each story
        """
        if not self.driver:
            self.connect()
            
        stories = []
        base_url = settings.hnews_site_url
        
        try:
            for page in range(1, pages + 1):
                if page > 1:
                    url = f"{base_url}?p={page}"
                else:
                    url = base_url
                    
                logger.info(f"Fetching page {page}: {url}")
                self.driver.get(url)
                time.sleep(2)  # Allow page to load
                
                # Find all story rows
                rows = self.driver.find_elements(By.CSS_SELECTOR, "tr.athing")
                logger.info(f"Found {len(rows)} stories on page {page}")
                
                for row in rows:
                    try:
                        title_element = row.find_element(By.CSS_SELECTOR, "td.title a")
                        title = title_element.text
                        url = title_element.get_attribute("href")
                        
                        # Get the score from the next row
                        score_row = row.find_element(By.XPATH, "./following-sibling::tr")
                        score_element = score_row.find_element(By.CSS_SELECTOR, "span.score")
                        score = score_element.text.split()[0]  # Extract the number
                        
                        stories.append({
                            "title": title,
                            "score": int(score),
                            "url": url
                        })
                    except NoSuchElementException as e:
                        logger.warning(f"Failed to extract story details: {str(e)}")
                        continue
        except Exception as e:
            logger.error(f"Error during scraping: {str(e)}")
            raise
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                except Exception as e:
                    logger.error(f"Error closing Selenium driver: {str(e)}")
        
        return stories

def get_hacker_news_top_stories():
    """
    Get fresh Hacker News top stories (real-time fetch)
    :return: List of stories with title, score, and URL
    """
    scraper = HackerNewsScraper()
    try:
        return scraper.fetch_top_stories()
    except Exception as e:
        logger.error(f"Error fetching Hacker News: {str(e)}")
        return []