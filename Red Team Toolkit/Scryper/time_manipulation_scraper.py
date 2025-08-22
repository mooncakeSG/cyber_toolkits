#!/usr/bin/env python3
"""
Time Manipulation ProProfs Quiz Scraper

This script attempts to bypass the timer by manipulating the browser's
time and date settings to make it appear as if the timer has expired.
"""

import json
import asyncio
from playwright.async_api import async_playwright


async def manipulate_time_and_scrape():
    """Manipulate browser time and attempt to scrape quiz data."""
    
    # Initialize Playwright
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()
    page = await context.new_page()
    
    try:
        print("Attempting time manipulation to bypass timer...")
        
        # Navigate to quiz URL
        url = "https://www.proprofs.com/quiz-school/ugc/story.php?title=sfia-service-operations-practitioner0h&token=Z3FlYmVyaGFkZW1hbmRAY2FwYWNpdGkub3JnLnph"
        await page.goto(url, wait_until='networkidle')
        await page.wait_for_load_state('domcontentloaded')
        
        # Strategy 1: Override Date object to fake future time
        print("Strategy 1: Overriding Date object...")
        
        await page.evaluate("""
            // Override Date constructor to return a future date
            const originalDate = Date;
            const futureTime = new Date('2025-08-19T10:00:00Z').getTime();
            
            Date = function(...args) {
                if (args.length === 0) {
                    // No arguments - return future date
                    const date = new originalDate(futureTime);
                    date.getTime = () => futureTime;
                    date.valueOf = () => futureTime;
                    return date;
                } else {
                    // With arguments - use original constructor
                    return new originalDate(...args);
                }
            };
            
            // Copy static methods
            Date.now = () => futureTime;
            Date.parse = originalDate.parse;
            Date.UTC = originalDate.UTC;
            Date.prototype = originalDate.prototype;
        """)
        
        # Strategy 2: Override performance.now() to return future time
        print("Strategy 2: Overriding performance.now()...")
        
        await page.evaluate("""
            // Override performance.now to return future time
            const originalPerformanceNow = performance.now;
            const futureTimeMs = new Date('2025-08-19T10:00:00Z').getTime();
            const startTime = Date.now();
            
            performance.now = function() {
                return futureTimeMs - startTime + originalPerformanceNow.call(performance);
            };
        """)
        
        # Strategy 3: Override localStorage/sessionStorage to fake timer completion
        print("Strategy 3: Manipulating browser storage...")
        
        await page.evaluate("""
            // Override localStorage and sessionStorage
            const originalSetItem = Storage.prototype.setItem;
            const originalGetItem = Storage.prototype.getItem;
            
            // Intercept storage operations
            Storage.prototype.setItem = function(key, value) {
                // If setting timer-related values, set them to completed state
                if (key.toLowerCase().includes('timer') || key.toLowerCase().includes('countdown')) {
                    value = '0';
                } else if (key.toLowerCase().includes('complete') || key.toLowerCase().includes('expired')) {
                    value = 'true';
                }
                return originalSetItem.call(this, key, value);
            };
            
            Storage.prototype.getItem = function(key) {
                const value = originalGetItem.call(this, key);
                
                // If getting timer-related values, return completed state
                if (key.toLowerCase().includes('timer') || key.toLowerCase().includes('countdown')) {
                    return '0';
                } else if (key.toLowerCase().includes('complete') || key.toLowerCase().includes('expired')) {
                    return 'true';
                }
                
                return value;
            };
            
            // Set some fake completed states
            if (typeof localStorage !== 'undefined') {
                localStorage.setItem('timerComplete', 'true');
                localStorage.setItem('quizExpired', 'true');
                localStorage.setItem('countdownComplete', 'true');
            }
            
            if (typeof sessionStorage !== 'undefined') {
                sessionStorage.setItem('timerComplete', 'true');
                sessionStorage.setItem('quizExpired', 'true');
                sessionStorage.setItem('countdownComplete', 'true');
            }
        """)
        
        # Strategy 4: Override setInterval and setTimeout to skip timer delays
        print("Strategy 4: Overriding timer functions...")
        
        await page.evaluate("""
            // Override setInterval to skip long intervals (likely timers)
            const originalSetInterval = setInterval;
            setInterval = function(fn, delay) {
                if (delay > 1000) {
                    console.log('Skipping long interval:', delay);
                    // Execute immediately instead of waiting
                    fn();
                    return null;
                }
                return originalSetInterval(fn, delay);
            };
            
            // Override setTimeout to skip long timeouts
            const originalSetTimeout = setTimeout;
            setTimeout = function(fn, delay) {
                if (delay > 1000) {
                    console.log('Skipping long timeout:', delay);
                    // Execute immediately instead of waiting
                    fn();
                    return null;
                }
                return originalSetTimeout(fn, delay);
            };
        """)
        
        # Strategy 5: Remove timer elements from DOM
        print("Strategy 5: Removing timer elements...")
        
        await page.evaluate("""
            // Remove timer-related elements
            const timerSelectors = [
                '[class*="timer"]',
                '[class*="countdown"]',
                '[id*="timer"]',
                '[id*="countdown"]',
                '.timer',
                '.countdown',
                '#timer',
                '#countdown',
                '[data-timer]',
                '[data-countdown]'
            ];
            
            timerSelectors.forEach(selector => {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => {
                    console.log('Removing timer element:', el);
                    el.remove();
                });
            });
        """)
        
        # Strategy 6: Try to trigger quiz loading functions
        print("Strategy 6: Triggering quiz functions...")
        
        await page.evaluate("""
            // Try to trigger quiz loading functions
            const functions = [
                'loadQuiz', 'loadQuestions', 'initializeQuiz', 'startQuiz',
                'beginQuiz', 'GetCount', 'submit_p_form', 'showQuiz',
                'displayQuiz', 'loadTest', 'startTest', 'beginTest'
            ];
            
            functions.forEach(funcName => {
                if (typeof window[funcName] === 'function') {
                    try {
                        console.log('Executing function:', funcName);
                        window[funcName]();
                    } catch (e) {
                        console.log('Error executing function:', funcName, e);
                    }
                }
            });
        """)
        
        # Wait for any dynamic content to load
        await asyncio.sleep(5)
        
        # Try to extract quiz data
        print("Attempting to extract quiz data after time manipulation...")
        
        # Check sessionStorage for quiz data
        storage_data = await page.evaluate("""
            () => {
                const data = {};
                if (typeof sessionStorage !== 'undefined') {
                    for (let i = 0; i < sessionStorage.length; i++) {
                        const key = sessionStorage.key(i);
                        if (key) {
                            data[key] = sessionStorage.getItem(key);
                        }
                    }
                }
                return data;
            }
        """)
        
        # Check for quiz data in storage
        quiz_data = []
        for key, value in storage_data.items():
            if value and len(value) > 10:
                try:
                    parsed_data = json.loads(value)
                    if isinstance(parsed_data, list) and len(parsed_data) > 0:
                        print(f"Found quiz data in sessionStorage: {len(parsed_data)} items")
                        quiz_data.extend(parsed_data)
                except json.JSONDecodeError:
                    continue
        
        # Check for quiz elements on page
        quiz_elements = await page.query_selector_all('[class*="quiz"], [class*="question"]')
        if quiz_elements:
            print(f"Found {len(quiz_elements)} quiz elements after time manipulation")
            
            # Try to extract questions from visible elements
            for element in quiz_elements:
                try:
                    text = await element.text_content()
                    if text and len(text.strip()) > 20:
                        print(f"Found potential question: {text[:100]}...")
                except:
                    continue
        
        # Check if timer elements are still present
        timer_elements = await page.query_selector_all('[class*="timer"], [class*="countdown"]')
        if not timer_elements:
            print("Timer elements successfully removed")
        else:
            print(f"Timer elements still present: {len(timer_elements)}")
        
        return quiz_data
        
    except Exception as e:
        print(f"Error during time manipulation: {e}")
        return []
        
    finally:
        await context.close()
        await browser.close()
        await playwright.stop()


async def extract_questions_from_data(data):
    """Extract questions from data."""
    questions = []
    
    if isinstance(data, list):
        for item in data:
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
    
    return questions


async def main():
    """Main function."""
    print("Starting time manipulation ProProfs quiz scraper...")
    print("This will attempt to bypass the timer by manipulating browser time.")
    
    quiz_data = await manipulate_time_and_scrape()
    questions = await extract_questions_from_data(quiz_data)
    
    if questions:
        # Save to JSON file
        with open('quiz_data.json', 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)
        
        print(f"\nSuccessfully extracted {len(questions)} questions")
        print("Quiz data saved to quiz_data.json")
    else:
        print("\nTime manipulation did not yield quiz data.")
        print("The timer protection may be server-side enforced.")
    
    print(f"Total questions extracted: {len(questions)}")


if __name__ == "__main__":
    asyncio.run(main())
