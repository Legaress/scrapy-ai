from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
import time

class HackerNewsScraper:
    def __init__(self, selenium_host='selenium'):
        # Configurar conexión remota a Selenium
        self.selenium_host = selenium_host
        self.driver = None
        
    def connect(self):
        """Establece conexión con el contenedor Selenium"""
        self.driver = webdriver.Remote(
            command_executor=f'http://{self.selenium_host}:4444/wd/hub',
            options=webdriver.ChromeOptions()
        )
    
    def fetch_top_stories(self, pages: int = 5):
        """
        Fetch top stories from Hacker News
        :param pages: Number of pages to scrape (default: 5)
        :return: List of dictionaries containing title, score, and URL for each story
        """
        if not self.driver:
            self.connect()
            
        stories = []
        base_url = "https://news.ycombinator.com/news"
        
        try:
            for page in range(1, pages + 1):
                if page > 1:
                    url = f"{base_url}?p={page}"
                else:
                    url = base_url
                    
                self.driver.get(url)
                time.sleep(2)  # Allow page to load
                
                # Find all story rows
                rows = self.driver.find_elements(By.CSS_SELECTOR, "tr.athing")
                
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
                    except NoSuchElementException:
                        # Skip if any element is missing
                        continue
        finally:
            if self.driver:
                self.driver.quit()
        
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
        print(f"Error fetching Hacker News: {e}")
        return []