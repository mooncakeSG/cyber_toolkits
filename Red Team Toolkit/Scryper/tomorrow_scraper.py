#!/usr/bin/env python3
"""
Tomorrow ProProfs Quiz Scraper

Run this script tomorrow (August 19, 2025) after 10 AM when the timer expires.
Based on HasData/playwright-scraping examples.
"""

import json
import asyncio
from playwright.async_api import async_playwright


async def scrape_quiz():
    """Scrape the ProProfs quiz after timer expiration."""
    
    # Initialize Playwright
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()
    page = await context.new_page()
    
    try:
        # Navigate to quiz URL
        url = "https://www.proprofs.com/quiz-school/ugc/story.php?title=sfia-service-operations-practitioner0h&token=Z3FlYmVyaGFkZW1hbmRAY2FwYWNpdGkub3JnLnph"
        await page.goto(url, wait_until='networkidle')
        await page.wait_for_load_state('domcontentloaded')
        
        # Wait for quiz data to appear in sessionStorage (poll every second for 30 seconds)
        quiz_data = None
        for i in range(30):
            try:
                # Check sessionStorage for quiz data
                storage_data = await page.evaluate("""
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
                                quiz_data = parsed_data
                                break
                            elif isinstance(parsed_data, dict) and 'questions' in parsed_data:
                                quiz_data = parsed_data['questions']
                                break
                        except json.JSONDecodeError:
                            continue
                
                if quiz_data:
                    break
                
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"Error checking sessionStorage: {e}")
                await asyncio.sleep(1)
        
        # Extract questions and options
        questions = []
        if quiz_data:
            for item in quiz_data:
                try:
                    if isinstance(item, dict):
                        question_text = None
                        options = []
                        
                        # Extract question text
                        if 'question' in item:
                            question_text = item['question']
                        elif 'text' in item:
                            question_text = item['text']
                        elif 'title' in item:
                            question_text = item['title']
                        
                        # Extract options
                        if 'options' in item and isinstance(item['options'], list):
                            options = item['options']
                        elif 'answers' in item and isinstance(item['answers'], list):
                            options = item['answers']
                        elif 'choices' in item and isinstance(item['choices'], list):
                            options = item['choices']
                        
                        # Clean up options
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
        
        # Save to JSON file
        with open('quiz_data.json', 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully extracted {len(questions)} questions")
        print("Quiz data saved to quiz_data.json")
        
        return questions
        
    except Exception as e:
        print(f"Error during scraping: {e}")
        return []
        
    finally:
        # Clean up
        await context.close()
        await browser.close()
        await playwright.stop()


async def main():
    """Main function."""
    print("Starting ProProfs quiz scraper...")
    print("Make sure the timer has expired (after August 19, 2025, 10 AM)")
    
    questions = await scrape_quiz()
    print(f"Total questions scraped: {len(questions)}")


if __name__ == "__main__":
    asyncio.run(main())
