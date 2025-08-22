#!/usr/bin/env python3
"""
Timer Bypass ProProfs Quiz Scraper

This script handles ProProfs quizzes that use timers to delay quiz access.
It implements multiple strategies to bypass the timer and extract quiz data.
"""

import json
import time
import logging
from typing import List, Dict, Optional
from selenium import webdriver
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

class TimerBypassQuizScraper:
    """Scraper class for timer-based ProProfs quizzes."""
    
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
            
            # Enable DevTools Protocol for network interception
            chrome_options.add_argument("--remote-debugging-port=9222")
            
            # Use chromedriver-autoinstaller
            chromedriver_autoinstaller.install()
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 15)
            
            logger.info("Chrome WebDriver initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise
    
    def navigate_to_quiz(self, url: str) -> None:
        """
        Navigate to the quiz URL and handle timer-based access.
        
        Args:
            url (str): The quiz URL to navigate to
        """
        try:
            logger.info(f"Navigating to quiz URL: {url}")
            self.driver.get(url)
            
            # Wait for page to load
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(3)
            
            logger.info("Successfully navigated to quiz page")
            
        except Exception as e:
            logger.error(f"Failed to navigate to quiz: {e}")
            raise
    
    def attempt_timer_bypass(self) -> bool:
        """
        Attempt to bypass the timer using multiple strategies.
        
        Returns:
            bool: True if bypass was successful, False otherwise
        """
        try:
            logger.info("Attempting to bypass timer...")
            
            # Strategy 1: Try to fast-forward timer using JavaScript
            logger.info("Strategy 1: Attempting to fast-forward timer via JavaScript")
            try:
                # Common timer variable names
                timer_vars = [
                    "window.quizTimer = 0;",
                    "window.timer = 0;",
                    "window.countdown = 0;",
                    "window.quizCountdown = 0;",
                    "window.timeLeft = 0;",
                    "window.remainingTime = 0;",
                    "window.quizTime = 0;"
                ]
                
                for timer_var in timer_vars:
                    try:
                        self.driver.execute_script(timer_var)
                        logger.info(f"Executed: {timer_var}")
                    except:
                        continue
                
                # Try to trigger timer completion events
                completion_scripts = [
                    "if(typeof GetCount === 'function') { GetCount(); }",
                    "if(typeof startQuiz === 'function') { startQuiz(); }",
                    "if(typeof beginQuiz === 'function') { beginQuiz(); }",
                    "if(typeof submit_p_form === 'function') { submit_p_form(); }"
                ]
                
                for script in completion_scripts:
                    try:
                        self.driver.execute_script(script)
                        logger.info(f"Executed: {script}")
                    except:
                        continue
                
            except Exception as e:
                logger.warning(f"JavaScript timer bypass failed: {e}")
            
            # Strategy 2: Check for quiz data in localStorage/sessionStorage
            logger.info("Strategy 2: Checking for quiz data in storage")
            try:
                # Check localStorage
                local_storage = self.driver.execute_script("return Object.keys(localStorage);")
                logger.info(f"localStorage keys: {local_storage}")
                
                # Check sessionStorage
                session_storage = self.driver.execute_script("return Object.keys(sessionStorage);")
                logger.info(f"sessionStorage keys: {session_storage}")
                
                # Look for quiz-related data
                for key in local_storage + session_storage:
                    if any(term in key.lower() for term in ['quiz', 'question', 'answer', 'test']):
                        try:
                            data = self.driver.execute_script(f"return localStorage.getItem('{key}');")
                            if data:
                                logger.info(f"Found quiz data in localStorage['{key}']: {data[:200]}...")
                        except:
                            pass
                        
                        try:
                            data = self.driver.execute_script(f"return sessionStorage.getItem('{key}');")
                            if data:
                                logger.info(f"Found quiz data in sessionStorage['{key}']: {data[:200]}...")
                        except:
                            pass
                            
            except Exception as e:
                logger.warning(f"Storage check failed: {e}")
            
            # Strategy 3: Wait for timer to complete naturally (with polling)
            logger.info("Strategy 3: Polling for quiz data to appear")
            max_wait_time = 300  # 5 minutes max wait
            poll_interval = 5    # Check every 5 seconds
            elapsed_time = 0
            
            while elapsed_time < max_wait_time:
                try:
                    # Check if quiz questions are now visible
                    questions = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'question') or contains(@class, 'quiz-question')]")
                    if questions:
                        logger.info(f"Found {len(questions)} question elements after {elapsed_time} seconds")
                        return True
                    
                    # Check for any quiz-related content
                    quiz_content = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'quiz') or contains(@class, 'test')]")
                    if len(quiz_content) > 3:  # More than just the intro content
                        logger.info(f"Found quiz content after {elapsed_time} seconds")
                        return True
                    
                    # Check if timer is still running
                    timer_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'seconds') or contains(text(), 'minutes') or contains(text(), 'time')]")
                    if not timer_elements:
                        logger.info("Timer elements not found, quiz might be ready")
                        return True
                    
                    logger.info(f"Waiting for timer... ({elapsed_time}/{max_wait_time} seconds)")
                    time.sleep(poll_interval)
                    elapsed_time += poll_interval
                    
                except Exception as e:
                    logger.warning(f"Error during polling: {e}")
                    time.sleep(poll_interval)
                    elapsed_time += poll_interval
            
            logger.warning("Timer bypass timeout reached")
            return False
            
        except Exception as e:
            logger.error(f"Error during timer bypass: {e}")
            return False
    
    def extract_quiz_data_from_storage(self) -> Optional[List[Dict]]:
        """
        Extract quiz data from localStorage/sessionStorage if available.
        
        Returns:
            List[Dict]: Quiz data if found, None otherwise
        """
        try:
            logger.info("Attempting to extract quiz data from storage...")
            
            # Get all storage keys
            local_keys = self.driver.execute_script("return Object.keys(localStorage);")
            session_keys = self.driver.execute_script("return Object.keys(sessionStorage);")
            
            all_keys = local_keys + session_keys
            
            for key in all_keys:
                if any(term in key.lower() for term in ['quiz', 'question', 'answer', 'test', 'data']):
                    try:
                        # Try localStorage
                        data = self.driver.execute_script(f"return localStorage.getItem('{key}');")
                        if data:
                            logger.info(f"Found data in localStorage['{key}']")
                            try:
                                parsed_data = json.loads(data)
                                if isinstance(parsed_data, list) and len(parsed_data) > 0:
                                    logger.info(f"Successfully parsed quiz data from localStorage['{key}']")
                                    return parsed_data
                            except json.JSONDecodeError:
                                pass
                        
                        # Try sessionStorage
                        data = self.driver.execute_script(f"return sessionStorage.getItem('{key}');")
                        if data:
                            logger.info(f"Found data in sessionStorage['{key}']")
                            try:
                                parsed_data = json.loads(data)
                                if isinstance(parsed_data, list) and len(parsed_data) > 0:
                                    logger.info(f"Successfully parsed quiz data from sessionStorage['{key}']")
                                    return parsed_data
                            except json.JSONDecodeError:
                                pass
                                
                    except Exception as e:
                        logger.warning(f"Error extracting data from {key}: {e}")
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting quiz data from storage: {e}")
            return None
    
    def extract_questions_from_page(self) -> List[Dict]:
        """
        Extract questions and options from the current page.
        
        Returns:
            List[Dict]: List of questions and options
        """
        questions = []
        
        try:
            logger.info("Extracting questions from page...")
            
            # Look for question containers
            question_containers = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'question') or contains(@class, 'quiz-question')]")
            
            if not question_containers:
                # Try alternative selectors
                question_containers = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'question') or contains(@class, 'quiz')]")
            
            logger.info(f"Found {len(question_containers)} question containers")
            
            for i, container in enumerate(question_containers):
                try:
                    # Extract question text
                    question_text = container.text.strip()
                    
                    # Look for answer options within this container
                    options = []
                    
                    # Try different option selectors
                    option_selectors = [
                        ".//input[@type='radio']/following-sibling::label",
                        ".//input[@type='checkbox']/following-sibling::label",
                        ".//label[contains(@class, 'option')]",
                        ".//label[contains(@class, 'answer')]",
                        ".//div[contains(@class, 'option')]",
                        ".//div[contains(@class, 'answer')]"
                    ]
                    
                    for selector in option_selectors:
                        option_elements = container.find_elements(By.XPATH, selector)
                        for element in option_elements:
                            option_text = element.text.strip()
                            if option_text and option_text not in options:
                                options.append(option_text)
                        if options:
                            break
                    
                    if question_text and options:
                        questions.append({
                            "question": question_text,
                            "options": options
                        })
                        logger.info(f"Extracted question {i+1}: {question_text[:50]}...")
                    
                except Exception as e:
                    logger.warning(f"Error extracting question {i+1}: {e}")
            
            logger.info(f"Successfully extracted {len(questions)} questions")
            return questions
            
        except Exception as e:
            logger.error(f"Error extracting questions from page: {e}")
            return questions
    
    def scrape_quiz(self, url: str) -> List[Dict]:
        """
        Scrape the timer-based quiz.
        
        Args:
            url (str): The quiz URL
            
        Returns:
            List[Dict]: List of questions and options
        """
        try:
            self.setup_driver()
            self.navigate_to_quiz(url)
            
            # Attempt to bypass timer
            if self.attempt_timer_bypass():
                logger.info("Timer bypass successful")
                
                # Try to extract data from storage first
                storage_data = self.extract_quiz_data_from_storage()
                if storage_data:
                    self.quiz_data = storage_data
                    logger.info(f"Successfully extracted {len(self.quiz_data)} questions from storage")
                    return self.quiz_data
                
                # Fallback to extracting from page
                self.quiz_data = self.extract_questions_from_page()
                if self.quiz_data:
                    logger.info(f"Successfully extracted {len(self.quiz_data)} questions from page")
                    return self.quiz_data
                
                logger.warning("No questions found after timer bypass")
            else:
                logger.warning("Timer bypass failed")
            
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
                self.driver.quit()
                logger.info("WebDriver cleaned up successfully")
            except OSError:
                # Handle WinError 6 gracefully
                pass
            except Exception as e:
                logger.warning(f"Error during cleanup: {e}")


def main():
    """Main function to run the timer bypass quiz scraper."""
    quiz_url = "https://www.proprofs.com/quiz-school/ugc/story.php?title=sfia-service-operations-practitioner0h&token=Z3FlYmVyaGFkZW1hbmRAY2FwYWNpdGkub3JnLnph"
    
    try:
        logger.info("Starting Timer Bypass ProProfs Quiz Scraper")
        
        # Initialize scraper
        scraper = TimerBypassQuizScraper(headless=False)  # Set to False for debugging
        
        # Scrape the quiz
        quiz_data = scraper.scrape_quiz(quiz_url)
        
        # Save to JSON
        scraper.save_to_json("timer_bypass_quiz_data.json")
        
        logger.info("Quiz scraping completed successfully!")
        logger.info(f"Total questions scraped: {len(quiz_data)}")
        
    except Exception as e:
        logger.error(f"Quiz scraping failed: {e}")
        raise


if __name__ == "__main__":
    main()
