#!/usr/bin/env python3
"""
Direct quiz access script to try different approaches for accessing ProProfs quiz content.
"""

import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def try_direct_quiz_access():
    """Try different approaches to access the quiz content."""
    
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Install and initialize ChromeDriver
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)
    
    try:
        # Try the original URL first
        original_url = "https://www.proprofs.com/quiz-school/ugc/story.php?title=sfia-service-operations-practitioner0h&token=Z3FlYmVyaGFkZW1hbmRAY2FwYWNpdGkub3JnLnph"
        logger.info(f"Trying original URL: {original_url}")
        driver.get(original_url)
        time.sleep(5)
        
        # Check if we can find any quiz content
        logger.info("Checking for quiz content...")
        
        # Look for any text that might be quiz-related
        all_text = driver.find_element(By.TAG_NAME, "body").text
        logger.info(f"Page text length: {len(all_text)} characters")
        logger.info(f"First 500 characters: {all_text[:500]}")
        
        # Try to find any interactive elements
        clickable_elements = driver.find_elements(By.XPATH, "//button | //a | //input[@type='button'] | //input[@type='submit']")
        logger.info(f"Found {len(clickable_elements)} clickable elements")
        
        for i, elem in enumerate(clickable_elements[:5]):
            try:
                text = elem.text.strip()
                tag = elem.tag_name
                classes = elem.get_attribute("class")
                logger.info(f"  Element {i+1}: {tag} - text='{text}', class='{classes}'")
            except:
                pass
        
        # Try to find any forms
        forms = driver.find_elements(By.TAG_NAME, "form")
        logger.info(f"Found {len(forms)} forms")
        
        # Try to find any divs with quiz-related classes
        quiz_divs = driver.find_elements(By.XPATH, "//div[contains(@class, 'quiz') or contains(@class, 'question') or contains(@class, 'test')]")
        logger.info(f"Found {len(quiz_divs)} quiz-related divs")
        
        for i, div in enumerate(quiz_divs[:3]):
            try:
                text = div.text.strip()[:200]
                classes = div.get_attribute("class")
                logger.info(f"  Quiz div {i+1}: class='{classes}', text='{text}...'")
            except:
                pass
        
        # Try to find any JavaScript that might load the quiz
        scripts = driver.find_elements(By.TAG_NAME, "script")
        logger.info(f"Found {len(scripts)} script tags")
        
        # Look for any script that contains quiz-related content
        for script in scripts:
            try:
                src = script.get_attribute("src")
                if src and ("quiz" in src.lower() or "story" in src.lower()):
                    logger.info(f"Found quiz-related script: {src}")
            except:
                pass
        
        # Try to wait for dynamic content
        logger.info("Waiting for dynamic content to load...")
        time.sleep(10)
        
        # Check again for new content
        new_clickable = driver.find_elements(By.XPATH, "//button | //a | //input[@type='button'] | //input[@type='submit']")
        logger.info(f"After waiting, found {len(new_clickable)} clickable elements")
        
        # Try to click on any element that might start the quiz
        for elem in new_clickable:
            try:
                text = elem.text.strip().lower()
                if any(keyword in text for keyword in ['start', 'begin', 'quiz', 'test', 'continue']):
                    logger.info(f"Found potential start element: {elem.text}")
                    elem.click()
                    logger.info("Clicked on potential start element")
                    time.sleep(3)
                    break
            except:
                continue
        
        # Take a screenshot
        driver.save_screenshot("direct_access.png")
        logger.info("Screenshot saved to direct_access.png")
        
        # Save the final page source
        with open("direct_access_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        logger.info("Page source saved to direct_access_source.html")
        
    except Exception as e:
        logger.error(f"Error during direct access: {e}")
    finally:
        try:
            driver.quit()
        except OSError:
            pass

if __name__ == "__main__":
    try_direct_quiz_access()
