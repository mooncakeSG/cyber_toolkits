#!/usr/bin/env python3
"""
Debug script to analyze the ProProfs quiz page structure.
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

def analyze_page_structure():
    """Analyze the quiz page structure to understand available elements."""
    
    # Set up Chrome options (non-headless for debugging)
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
        # Navigate to the quiz
        quiz_url = "https://www.proprofs.com/quiz-school/ugc/story.php?title=sfia-service-operations-practitioner0h&token=Z3FlYmVyaGFkZW1hbmRAY2FwYWNpdGkub3JnLnph"
        logger.info(f"Navigating to: {quiz_url}")
        driver.get(quiz_url)
        
        # Wait for page to load
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(3)
        
        # Get page title
        title = driver.title
        logger.info(f"Page title: {title}")
        
        # Check for iframes
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        logger.info(f"Found {len(iframes)} iframes")
        
        # Look for the main quiz iframe
        quiz_iframe = None
        for i, iframe in enumerate(iframes):
            try:
                src = iframe.get_attribute("src")
                id_attr = iframe.get_attribute("id")
                name_attr = iframe.get_attribute("name")
                logger.info(f"  Iframe {i+1}: src='{src}', id='{id_attr}', name='{name_attr}'")
                
                # Look for iframe containing quiz content
                if src and ("quiz" in src.lower() or "story" in src.lower()):
                    quiz_iframe = iframe
                    logger.info(f"  Found potential quiz iframe: {src}")
            except Exception as e:
                logger.warning(f"  Error checking iframe {i+1}: {e}")
        
        # If no specific quiz iframe found, try the first non-hidden iframe
        if not quiz_iframe and iframes:
            for iframe in iframes:
                try:
                    style = iframe.get_attribute("style")
                    if style and "display: none" not in style and "visibility: hidden" not in style:
                        quiz_iframe = iframe
                        logger.info("  Using first visible iframe")
                        break
                except:
                    continue
        
        # Switch to iframe if found
        if quiz_iframe:
            try:
                driver.switch_to.frame(quiz_iframe)
                logger.info("Switched to iframe")
                time.sleep(2)
                
                # Now analyze the iframe content
                logger.info("Analyzing iframe content...")
                
                # Check for buttons
                buttons = driver.find_elements(By.TAG_NAME, "button")
                logger.info(f"Found {len(buttons)} buttons in iframe:")
                for i, btn in enumerate(buttons[:10]):  # Show first 10
                    try:
                        text = btn.text.strip()
                        classes = btn.get_attribute("class")
                        logger.info(f"  Button {i+1}: text='{text}', class='{classes}'")
                    except:
                        pass
                
                # Check for links
                links = driver.find_elements(By.TAG_NAME, "a")
                logger.info(f"Found {len(links)} links in iframe:")
                for i, link in enumerate(links[:10]):  # Show first 10
                    try:
                        text = link.text.strip()
                        href = link.get_attribute("href")
                        classes = link.get_attribute("class")
                        logger.info(f"  Link {i+1}: text='{text}', href='{href}', class='{classes}'")
                    except:
                        pass
                
                # Check for input elements
                inputs = driver.find_elements(By.TAG_NAME, "input")
                logger.info(f"Found {len(inputs)} input elements in iframe:")
                for i, inp in enumerate(inputs[:10]):  # Show first 10
                    try:
                        input_type = inp.get_attribute("type")
                        value = inp.get_attribute("value")
                        classes = inp.get_attribute("class")
                        logger.info(f"  Input {i+1}: type='{input_type}', value='{value}', class='{classes}'")
                    except:
                        pass
                
                # Look for question-related elements
                question_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'question') or contains(@class, 'quiz')]")
                logger.info(f"Found {len(question_elements)} question-related elements in iframe:")
                for i, elem in enumerate(question_elements[:5]):  # Show first 5
                    try:
                        tag = elem.tag_name
                        text = elem.text.strip()[:100]  # First 100 chars
                        classes = elem.get_attribute("class")
                        logger.info(f"  Question element {i+1}: tag='{tag}', class='{classes}', text='{text}...'")
                    except:
                        pass
                
                # Look for option-related elements
                option_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'option') or contains(@class, 'answer') or contains(@class, 'choice')]")
                logger.info(f"Found {len(option_elements)} option-related elements in iframe:")
                for i, elem in enumerate(option_elements[:5]):  # Show first 5
                    try:
                        tag = elem.tag_name
                        text = elem.text.strip()[:100]  # First 100 chars
                        classes = elem.get_attribute("class")
                        logger.info(f"  Option element {i+1}: tag='{tag}', class='{classes}', text='{text}...'")
                    except:
                        pass
                
                # Save iframe page source
                iframe_source = driver.page_source
                with open("iframe_source.html", "w", encoding="utf-8") as f:
                    f.write(iframe_source)
                logger.info("Iframe source saved to iframe_source.html")
                
                # Switch back to main content
                driver.switch_to.default_content()
                
            except Exception as e:
                logger.error(f"Error analyzing iframe: {e}")
                driver.switch_to.default_content()
        
        # Get page source for analysis
        page_source = driver.page_source
        
        # Save page source for manual inspection
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(page_source)
        logger.info("Page source saved to page_source.html")
        
        # Take a screenshot
        driver.save_screenshot("quiz_page.png")
        logger.info("Screenshot saved to quiz_page.png")
        
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
    finally:
        try:
            driver.quit()
        except OSError:
            pass

if __name__ == "__main__":
    analyze_page_structure()
