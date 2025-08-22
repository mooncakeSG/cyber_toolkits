#!/usr/bin/env python3
"""
ProProfs Quiz Scraper

This script scrapes quiz questions and answers from ProProfs using Selenium WebDriver.
It handles the quiz flow, extracts questions and options, and saves them to JSON format.
"""

import json
import time
import logging
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    WebDriverException,
    ElementClickInterceptedException
)
import chromedriver_autoinstaller

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ProProfsQuizScraper:
    """Scraper class for ProProfs quizzes."""
    
    def __init__(self, headless: bool = True):
        """
        Initialize the scraper.
        
        Args:
            headless (bool): Whether to run Chrome in headless mode
        """
        self.driver = None
        self.wait = None
        self.headless = headless
        self.quiz_data = []
        
    def setup_driver(self) -> None:
        """Set up Chrome WebDriver with appropriate options."""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument("--headless")
            
            # Additional options for stability
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            
            # Disable images and CSS for faster loading
            chrome_options.add_argument("--disable-images")
            chrome_options.add_argument("--disable-css")
            
            # Use chromedriver-autoinstaller to automatically install the correct ChromeDriver
            chromedriver_autoinstaller.install()
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 15)  # Increased timeout for better reliability
            
            logger.info("Chrome WebDriver initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise
    
    def navigate_to_quiz(self, url: str) -> None:
        """
        Navigate to the quiz URL and handle iframes.
        
        Args:
            url (str): The quiz URL to navigate to
        """
        try:
            logger.info(f"Navigating to quiz URL: {url}")
            self.driver.get(url)
            
            # Wait for page to load
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(3)  # Wait for dynamic content to load
            
            # Check for iframes and switch to the quiz iframe if found
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            logger.info(f"Found {len(iframes)} iframes")
            
            if iframes:
                # Try to find the quiz iframe
                quiz_iframe = None
                for iframe in iframes:
                    try:
                        src = iframe.get_attribute("src")
                        style = iframe.get_attribute("style")
                        
                        # Skip hidden iframes
                        if style and ("display: none" in style or "visibility: hidden" in style):
                            continue
                        
                        # Use the first visible iframe
                        quiz_iframe = iframe
                        logger.info("Found quiz iframe, switching to it")
                        break
                    except:
                        continue
                
                if quiz_iframe:
                    self.driver.switch_to.frame(quiz_iframe)
                    logger.info("Switched to quiz iframe")
                    time.sleep(2)  # Wait for iframe content to load
                else:
                    logger.info("No suitable iframe found, staying in main content")
            
            logger.info("Successfully navigated to quiz page")
            
        except Exception as e:
            logger.error(f"Failed to navigate to quiz: {e}")
            raise
    
    def bypass_intro_page(self) -> None:
        """Bypass the intro page by clicking the 'Start Quiz' button."""
        try:
            logger.info("Attempting to bypass intro page...")
            
            # Use CSS selectors for better reliability as suggested
            start_button_selectors = [
                "a.start-quiz, button.start-quiz",
                "a[href*='start'], button[onclick*='start']",
                "input[value*='Start'], input[value*='start']",
                ".start-quiz a, .start-quiz button",
                "[class*='start'] a, [class*='start'] button"
            ]
            
            for selector in start_button_selectors:
                try:
                    start_button = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    start_button.click()
                    logger.info("Successfully clicked 'Start Quiz' button")
                    time.sleep(2)  # Wait for page transition
                    return
                except TimeoutException:
                    continue
            
            # Fallback to XPath selectors
            xpath_selectors = [
                "//button[contains(text(), 'Start Quiz')]",
                "//a[contains(text(), 'Start Quiz')]",
                "//input[@value='Start Quiz']",
                "//button[contains(@class, 'start')]",
                "//a[contains(@class, 'start')]",
                "//div[contains(@class, 'start-quiz')]//button",
                "//div[contains(@class, 'start-quiz')]//a"
            ]
            
            for selector in xpath_selectors:
                try:
                    start_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    start_button.click()
                    logger.info("Successfully clicked 'Start Quiz' button")
                    time.sleep(2)  # Wait for page transition
                    return
                except TimeoutException:
                    continue
            
            logger.info("No 'Start Quiz' button found, proceeding with quiz...")
            
        except Exception as e:
            logger.warning(f"Could not bypass intro page: {e}")
            # Continue anyway as the quiz might already be started
    
    def extract_question_and_options(self) -> Optional[Dict]:
        """
        Extract the current question and its options.
        
        Returns:
            Dict containing question text and options, or None if not found
        """
        try:
            # Wait for question to load
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(1)  # Additional wait for dynamic content
            
            # Common selectors for question text
            question_selectors = [
                "//div[contains(@class, 'question')]//p",
                "//div[contains(@class, 'question')]//h3",
                "//div[contains(@class, 'question')]//h2",
                "//div[contains(@class, 'question')]//span",
                "//p[contains(@class, 'question')]",
                "//h3[contains(@class, 'question')]",
                "//div[contains(@class, 'quiz-question')]//p",
                "//div[contains(@class, 'quiz-question')]//h3"
            ]
            
            question_text = None
            for selector in question_selectors:
                try:
                    question_element = self.driver.find_element(By.XPATH, selector)
                    question_text = question_element.text.strip()
                    if question_text:
                        break
                except NoSuchElementException:
                    continue
            
            if not question_text:
                logger.warning("Could not find question text")
                return None
            
            # Common selectors for answer options
            option_selectors = [
                "//input[@type='radio']/following-sibling::label",
                "//input[@type='checkbox']/following-sibling::label",
                "//div[contains(@class, 'option')]//label",
                "//div[contains(@class, 'answer')]//label",
                "//label[contains(@class, 'option')]",
                "//label[contains(@class, 'answer')]",
                "//div[contains(@class, 'quiz-option')]//label",
                "//span[contains(@class, 'option')]"
            ]
            
            options = []
            for selector in option_selectors:
                try:
                    option_elements = self.driver.find_elements(By.XPATH, selector)
                    for element in option_elements:
                        option_text = element.text.strip()
                        if option_text and option_text not in options:
                            options.append(option_text)
                    if options:
                        break
                except NoSuchElementException:
                    continue
            
            if not options:
                logger.warning("Could not find answer options")
                return None
            
            logger.info(f"Extracted question: {question_text[:50]}...")
            logger.info(f"Found {len(options)} options")
            
            return {
                "question": question_text,
                "options": options
            }
            
        except Exception as e:
            logger.error(f"Error extracting question and options: {e}")
            return None
    
    def click_next_button(self) -> bool:
        """
        Click the 'Next' button to proceed to the next question.
        
        Returns:
            bool: True if next button was clicked, False if no more questions
        """
        try:
            # Common selectors for next buttons
            next_button_selectors = [
                "//button[contains(text(), 'Next')]",
                "//a[contains(text(), 'Next')]",
                "//input[@value='Next']",
                "//button[contains(@class, 'next')]",
                "//a[contains(@class, 'next')]",
                "//div[contains(@class, 'next')]//button",
                "//div[contains(@class, 'next')]//a",
                "//button[contains(text(), 'Continue')]",
                "//a[contains(text(), 'Continue')]",
                "//input[@value='Continue']"
            ]
            
            for selector in next_button_selectors:
                try:
                    next_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    next_button.click()
                    logger.info("Clicked 'Next' button")
                    time.sleep(2)  # Wait for page transition
                    return True
                except TimeoutException:
                    continue
            
            logger.info("No 'Next' button found - likely reached the end of the quiz")
            return False
            
        except Exception as e:
            logger.error(f"Error clicking next button: {e}")
            return False
    
    def scrape_quiz(self, url: str) -> List[Dict]:
        """
        Scrape the entire quiz.
        
        Args:
            url (str): The quiz URL
            
        Returns:
            List[Dict]: List of questions and options
        """
        try:
            self.setup_driver()
            self.navigate_to_quiz(url)
            self.bypass_intro_page()
            
            question_count = 0
            max_questions = 100  # Safety limit
            
            while question_count < max_questions:
                # Extract current question
                question_data = self.extract_question_and_options()
                
                if question_data:
                    # Check if this question is already in our data
                    if not any(q["question"] == question_data["question"] for q in self.quiz_data):
                        self.quiz_data.append(question_data)
                        question_count += 1
                        logger.info(f"Scraped question {question_count}")
                    else:
                        logger.info("Duplicate question found, skipping...")
                
                # Try to go to next question
                if not self.click_next_button():
                    logger.info("Reached end of quiz")
                    break
                
                # Additional wait for page load
                time.sleep(1)
            
            logger.info(f"Successfully scraped {len(self.quiz_data)} questions")
            return self.quiz_data
            
        except Exception as e:
            logger.error(f"Error during quiz scraping: {e}")
            raise
        finally:
            self.cleanup()
    
    def save_to_json(self, filename: str = "quiz_data.json") -> None:
        """
        Save scraped data to JSON file.
        
        Args:
            filename (str): Output filename
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.quiz_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Quiz data saved to {filename}")
            
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")
            raise
    
    def cleanup(self) -> None:
        """Clean up WebDriver resources safely."""
        if self.driver:
            try:
                # Switch back to default content if we're in an iframe
                try:
                    self.driver.switch_to.default_content()
                except:
                    pass
                
                self.driver.quit()
                logger.info("WebDriver cleaned up successfully")
            except OSError:
                # Handle WinError 6 gracefully
                pass
            except Exception as e:
                logger.warning(f"Error during cleanup: {e}")


def main():
    """Main function to run the quiz scraper."""
    quiz_url = "https://www.proprofs.com/quiz-school/ugc/story.php?title=sfia-service-operations-practitioner0h&token=Z3FlYmVyaGFkZW1hbmRAY2FwYWNpdGkub3JnLnph"
    
    try:
        logger.info("Starting ProProfs Quiz Scraper")
        
        # Initialize scraper
        scraper = ProProfsQuizScraper(headless=True)
        
        # Scrape the quiz
        quiz_data = scraper.scrape_quiz(quiz_url)
        
        # Save to JSON
        scraper.save_to_json("quiz_data.json")
        
        logger.info("Quiz scraping completed successfully!")
        logger.info(f"Total questions scraped: {len(quiz_data)}")
        
    except Exception as e:
        logger.error(f"Quiz scraping failed: {e}")
        raise


if __name__ == "__main__":
    main()
