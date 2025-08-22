#!/usr/bin/env python3
"""
Final Comprehensive ProProfs Quiz Scraper

This script combines the best features from all previous attempts:
- Playwright for superior browser automation
- Multiple timer bypass strategies
- Network interception for API data
- Storage extraction
- Page content analysis
"""

import json
import time
import logging
import asyncio
from typing import List, Dict, Optional
from playwright.async_api import async_playwright

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FinalQuizScraper:
    """Comprehensive scraper for ProProfs quizzes with multiple strategies."""
    
    def __init__(self, headless: bool = True):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.headless = headless
        self.quiz_data = []
        self.intercepted_responses = []
        
    async def setup_browser(self) -> None:
        """Set up Playwright browser with appropriate options."""
        try:
            self.playwright = await async_playwright().start()
            
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--window-size=1920,1080'
                ]
            )
            
            self.context = await self.browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                viewport={'width': 1920, 'height': 1080}
            )
            
            self.page = await self.context.new_page()
            await self.setup_network_interception()
            
            logger.info("Playwright browser initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            raise
    
    async def setup_network_interception(self) -> None:
        """Set up network request/response interception."""
        try:
            self.page.on("response", self.handle_response)
            await self.page.route("**/*", self.handle_request)
            logger.info("Network interception enabled")
        except Exception as e:
            logger.warning(f"Could not enable network interception: {e}")
    
    async def handle_request(self, route) -> None:
        """Handle intercepted requests."""
        try:
            request = route.request
            url = request.url
            if any(term in url.lower() for term in ['quiz', 'question', 'api', 'data']):
                logger.info(f"Intercepted request: {url}")
            await route.continue_()
        except Exception as e:
            logger.warning(f"Error handling request: {e}")
            await route.continue_()
    
    async def handle_response(self, response) -> None:
        """Handle intercepted responses."""
        try:
            url = response.url
            if any(term in url.lower() for term in ['quiz', 'question', 'api', 'data']):
                logger.info(f"Intercepted response: {url} - Status: {response.status}")
                if response.status == 200:
                    try:
                        content_type = response.headers.get('content-type', '')
                        if 'application/json' in content_type or 'text/json' in content_type:
                            response_data = await response.json()
                            if isinstance(response_data, (list, dict)):
                                self.intercepted_responses.append({
                                    'url': url,
                                    'data': response_data
                                })
                                logger.info(f"Captured JSON data from {url}")
                    except:
                        pass
        except Exception as e:
            logger.warning(f"Error handling response: {e}")
    
    async def navigate_to_quiz(self, url: str) -> None:
        """Navigate to the quiz URL."""
        try:
            logger.info(f"Navigating to quiz URL: {url}")
            await self.page.goto(url, wait_until='networkidle')
            await self.page.wait_for_load_state('domcontentloaded')
            await asyncio.sleep(3)
            logger.info("Successfully navigated to quiz page")
        except Exception as e:
            logger.error(f"Failed to navigate to quiz: {e}")
            raise
    
    async def attempt_timer_bypass(self) -> bool:
        """Attempt to bypass the timer using multiple strategies."""
        try:
            logger.info("Attempting to bypass timer with comprehensive strategies...")
            
            # JavaScript timer manipulation
            timer_scripts = [
                """
                window.quizTimer = 0;
                window.timer = 0;
                window.countdown = 0;
                window.quizCountdown = 0;
                window.timeLeft = 0;
                window.remainingTime = 0;
                window.quizTime = 0;
                """,
                """
                if(typeof setInterval === 'function') {
                    const originalSetInterval = setInterval;
                    setInterval = function(fn, delay) {
                        if(delay > 1000) return;
                        return originalSetInterval(fn, delay);
                    };
                }
                """,
                """
                if(typeof localStorage !== 'undefined') {
                    localStorage.setItem('quizStarted', 'true');
                    localStorage.setItem('timerComplete', 'true');
                }
                if(typeof sessionStorage !== 'undefined') {
                    sessionStorage.setItem('quizStarted', 'true');
                    sessionStorage.setItem('timerComplete', 'true');
                }
                """,
                """
                if(typeof GetCount === 'function') { GetCount(); }
                if(typeof startQuiz === 'function') { startQuiz(); }
                if(typeof beginQuiz === 'function') { beginQuiz(); }
                if(typeof submit_p_form === 'function') { submit_p_form(); }
                """
            ]
            
            for script in timer_scripts:
                try:
                    await self.page.evaluate(script)
                    logger.info("Executed timer bypass script")
                    await asyncio.sleep(1)
                except Exception as e:
                    logger.warning(f"Timer script failed: {e}")
            
            # Wait for quiz content
            max_wait_time = 60
            poll_interval = 2
            elapsed_time = 0
            
            while elapsed_time < max_wait_time:
                try:
                    questions = await self.page.query_selector_all('[class*="question"], [class*="quiz"]')
                    if len(questions) > 0:
                        logger.info(f"Found {len(questions)} question elements after {elapsed_time} seconds")
                        return True
                    
                    if self.intercepted_responses:
                        logger.info(f"Found {len(self.intercepted_responses)} quiz-related responses")
                        return True
                    
                    logger.info(f"Waiting for timer... ({elapsed_time}/{max_wait_time} seconds)")
                    await asyncio.sleep(poll_interval)
                    elapsed_time += poll_interval
                    
                except Exception as e:
                    logger.warning(f"Error during polling: {e}")
                    await asyncio.sleep(poll_interval)
                    elapsed_time += poll_interval
            
            logger.warning("Timer bypass timeout reached")
            return False
            
        except Exception as e:
            logger.error(f"Error during timer bypass: {e}")
            return False
    
    async def extract_quiz_data_from_responses(self) -> Optional[List[Dict]]:
        """Extract quiz data from intercepted network responses."""
        try:
            logger.info("Extracting quiz data from intercepted responses...")
            
            for response in self.intercepted_responses:
                try:
                    data = response['data']
                    
                    if isinstance(data, list) and len(data) > 0:
                        first_item = data[0]
                        if isinstance(first_item, dict) and ('question' in first_item or 'text' in first_item):
                            logger.info(f"Found quiz data in response: {len(data)} questions")
                            return data
                    
                    elif isinstance(data, dict):
                        if 'questions' in data and isinstance(data['questions'], list):
                            logger.info(f"Found quiz data in response: {len(data['questions'])} questions")
                            return data['questions']
                        elif 'data' in data and isinstance(data['data'], list):
                            logger.info(f"Found quiz data in response: {len(data['data'])} questions")
                            return data['data']
                            
                except Exception as e:
                    logger.warning(f"Error processing response: {e}")
                    continue
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting from responses: {e}")
            return None
    
    async def extract_quiz_data_from_storage(self) -> Optional[List[Dict]]:
        """Extract quiz data from browser storage."""
        try:
            logger.info("Extracting quiz data from browser storage...")
            
            storage_data = await self.page.evaluate("""
                () => {
                    const data = {};
                    if(typeof localStorage !== 'undefined') {
                        for(let i = 0; i < localStorage.length; i++) {
                            const key = localStorage.key(i);
                            if(key) {
                                data[`local_${key}`] = localStorage.getItem(key);
                            }
                        }
                    }
                    if(typeof sessionStorage !== 'undefined') {
                        for(let i = 0; i < sessionStorage.length; i++) {
                            const key = sessionStorage.key(i);
                            if(key) {
                                data[`session_${key}`] = sessionStorage.getItem(key);
                            }
                        }
                    }
                    return data;
                }
            """)
            
            for key, value in storage_data.items():
                if value:
                    try:
                        parsed_data = json.loads(value)
                        if isinstance(parsed_data, list) and len(parsed_data) > 0:
                            logger.info(f"Found quiz data in storage '{key}': {len(parsed_data)} questions")
                            return parsed_data
                        elif isinstance(parsed_data, dict) and 'questions' in parsed_data:
                            logger.info(f"Found quiz data in storage '{key}': {len(parsed_data['questions'])} questions")
                            return parsed_data['questions']
                    except json.JSONDecodeError:
                        continue
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting from storage: {e}")
            return None
    
    async def extract_questions_from_page(self) -> List[Dict]:
        """Extract questions and options from the current page."""
        questions = []
        
        try:
            logger.info("Extracting questions from page...")
            
            # Take a screenshot for debugging
            await self.page.screenshot(path="final_quiz_page.png")
            logger.info("Screenshot saved to final_quiz_page.png")
            
            # Save page source for debugging
            page_source = await self.page.content()
            with open("final_quiz_source.html", "w", encoding="utf-8") as f:
                f.write(page_source)
            logger.info("Page source saved to final_quiz_source.html")
            
            # Look for question containers
            question_selectors = [
                '[class*="question"]',
                '[class*="quiz-question"]',
                '[class*="quiz"]',
                '[class*="test"]'
            ]
            
            question_elements = []
            for selector in question_selectors:
                elements = await self.page.query_selector_all(selector)
                question_elements.extend(elements)
            
            question_elements = list(set(question_elements))
            logger.info(f"Found {len(question_elements)} question elements")
            
            for i, element in enumerate(question_elements):
                try:
                    question_text = await element.text_content()
                    if question_text:
                        question_text = question_text.strip()
                    
                    options = []
                    option_selectors = [
                        'input[type="radio"] + label',
                        'input[type="checkbox"] + label',
                        'label[class*="option"]',
                        'label[class*="answer"]',
                        '[class*="option"]',
                        '[class*="answer"]'
                    ]
                    
                    for selector in option_selectors:
                        option_elements = await element.query_selector_all(selector)
                        for option_element in option_elements:
                            option_text = await option_element.text_content()
                            if option_text:
                                option_text = option_text.strip()
                                if option_text and option_text not in options and len(option_text) > 1:
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
    
    async def scrape_quiz(self, url: str) -> List[Dict]:
        """Scrape the quiz using comprehensive strategies."""
        try:
            await self.setup_browser()
            await self.navigate_to_quiz(url)
            
            if await self.attempt_timer_bypass():
                logger.info("Timer bypass successful")
                
                # Strategy 1: Extract from intercepted responses
                response_data = await self.extract_quiz_data_from_responses()
                if response_data:
                    self.quiz_data = response_data
                    logger.info(f"Successfully extracted {len(self.quiz_data)} questions from responses")
                    return self.quiz_data
                
                # Strategy 2: Extract from storage
                storage_data = await self.extract_quiz_data_from_storage()
                if storage_data:
                    self.quiz_data = storage_data
                    logger.info(f"Successfully extracted {len(self.quiz_data)} questions from storage")
                    return self.quiz_data
                
                # Strategy 3: Extract from page
                page_data = await self.extract_questions_from_page()
                if page_data:
                    self.quiz_data = page_data
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
            await self.cleanup()
    
    async def save_to_json(self, filename: str = "final_quiz_data.json") -> None:
        """Save scraped data to JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.quiz_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Quiz data saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")
            raise
    
    async def cleanup(self) -> None:
        """Clean up Playwright resources."""
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            logger.info("Playwright resources cleaned up successfully")
        except Exception as e:
            logger.warning(f"Error during cleanup: {e}")


async def main():
    """Main function to run the final comprehensive quiz scraper."""
    quiz_url = "https://www.proprofs.com/quiz-school/ugc/story.php?title=sfia-service-operations-practitioner0h&token=Z3FlYmVyaGFkZW1hbmRAY2FwYWNpdGkub3JnLnph"
    
    try:
        logger.info("Starting Final Comprehensive ProProfs Quiz Scraper")
        
        scraper = FinalQuizScraper(headless=False)
        quiz_data = await scraper.scrape_quiz(quiz_url)
        await scraper.save_to_json("final_quiz_data.json")
        
        logger.info("Quiz scraping completed successfully!")
        logger.info(f"Total questions scraped: {len(quiz_data)}")
        
        if len(quiz_data) == 0:
            logger.info("No questions found. This might be due to:")
            logger.info("1. Timer-based quiz that requires waiting")
            logger.info("2. Quiz content is loaded dynamically")
            logger.info("3. Quiz requires specific user interaction")
        
    except Exception as e:
        logger.error(f"Quiz scraping failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
