#!/usr/bin/env python3
"""
SessionStorage ProProfs Quiz Scraper

This script uses Playwright to scrape ProProfs quizzes by polling sessionStorage
for quiz data, following the HasData/playwright-scraping coding style.
"""

import json
import asyncio
from playwright.async_api import async_playwright


class SessionStorageQuizScraper:
    """Scraper that polls sessionStorage for quiz data."""
    
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.quiz_data = []
    
    async def setup_browser(self):
        """Set up Playwright browser in headless mode."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
    
    async def navigate_to_quiz(self, url):
        """Navigate to the quiz URL."""
        await self.page.goto(url, wait_until='networkidle')
        await self.page.wait_for_load_state('domcontentloaded')
    
    async def wait_for_quiz_data_in_storage(self, max_wait_time=30):
        """
        Wait for quiz data to appear in sessionStorage.
        
        Args:
            max_wait_time (int): Maximum time to wait in seconds
            
        Returns:
            dict: Quiz data from sessionStorage or None if not found
        """
        for i in range(max_wait_time):
            try:
                # Check sessionStorage for quiz data
                storage_data = await self.page.evaluate("""
                    () => {
                        const data = {};
                        if (typeof sessionStorage !== 'undefined') {
                            for (let i = 0; i < sessionStorage.length; i++) {
                                const key = sessionStorage.key(i);
                                if (key && (key.includes('quiz') || key.includes('question') || key.includes('test'))) {
                                    data[key] = sessionStorage.getItem(key);
                                }
                            }
                        }
                        return data;
                    }
                """)
                
                # Check if we found quiz data
                for key, value in storage_data.items():
                    if value and len(value) > 10:
                        try:
                            parsed_data = json.loads(value)
                            if isinstance(parsed_data, list) and len(parsed_data) > 0:
                                return parsed_data
                            elif isinstance(parsed_data, dict) and 'questions' in parsed_data:
                                return parsed_data['questions']
                        except json.JSONDecodeError:
                            continue
                
                # Wait 1 second before next check
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"Error checking sessionStorage: {e}")
                await asyncio.sleep(1)
        
        return None
    
    async def extract_questions_from_storage(self, storage_data):
        """
        Extract questions and options from sessionStorage data.
        
        Args:
            storage_data (list): Raw quiz data from sessionStorage
            
        Returns:
            list: Formatted quiz data
        """
        questions = []
        
        for item in storage_data:
            try:
                if isinstance(item, dict):
                    # Handle different possible data structures
                    question_text = None
                    options = []
                    
                    # Try to extract question text
                    if 'question' in item:
                        question_text = item['question']
                    elif 'text' in item:
                        question_text = item['text']
                    elif 'title' in item:
                        question_text = item['title']
                    
                    # Try to extract options
                    if 'options' in item and isinstance(item['options'], list):
                        options = item['options']
                    elif 'answers' in item and isinstance(item['answers'], list):
                        options = item['answers']
                    elif 'choices' in item and isinstance(item['choices'], list):
                        options = item['choices']
                    
                    # Clean up options (remove empty strings, etc.)
                    if options:
                        options = [str(opt).strip() for opt in options if opt and str(opt).strip()]
                    
                    if question_text and options:
                        questions.append({
                            "question": str(question_text).strip(),
                            "options": options
                        })
                        
            except Exception as e:
                print(f"Error processing quiz item: {e}")
                continue
        
        return questions
    
    async def scrape_quiz(self, url):
        """
        Scrape the quiz by polling sessionStorage.
        
        Args:
            url (str): The quiz URL
            
        Returns:
            list: Extracted quiz data
        """
        try:
            await self.setup_browser()
            await self.navigate_to_quiz(url)
            
            # Wait for quiz data to appear in sessionStorage
            storage_data = await self.wait_for_quiz_data_in_storage()
            
            if storage_data:
                self.quiz_data = await self.extract_questions_from_storage(storage_data)
                print(f"Successfully extracted {len(self.quiz_data)} questions from sessionStorage")
            else:
                print("No quiz data found in sessionStorage within the timeout period")
            
            return self.quiz_data
            
        except Exception as e:
            print(f"Error during quiz scraping: {e}")
            return []
        finally:
            await self.cleanup()
    
    async def save_to_json(self, filename="quiz_data.json"):
        """Save extracted data to JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.quiz_data, f, indent=2, ensure_ascii=False)
            print(f"Quiz data saved to {filename}")
        except Exception as e:
            print(f"Error saving to JSON: {e}")
    
    async def cleanup(self):
        """Clean up Playwright resources."""
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
        except Exception as e:
            print(f"Error during cleanup: {e}")


async def main():
    """Main function to run the session storage quiz scraper."""
    quiz_url = "https://www.proprofs.com/quiz-school/ugc/story.php?title=sfia-service-operations-practitioner0h&token=Z3FlYmVyaGFkZW1hbmRAY2FwYWNpdGkub3JnLnph"
    
    scraper = SessionStorageQuizScraper()
    quiz_data = await scraper.scrape_quiz(quiz_url)
    await scraper.save_to_json("quiz_data.json")
    
    print(f"Total questions scraped: {len(quiz_data)}")


if __name__ == "__main__":
    asyncio.run(main())
