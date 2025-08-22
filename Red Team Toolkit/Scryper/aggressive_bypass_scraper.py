#!/usr/bin/env python3
"""
Aggressive Bypass ProProfs Quiz Scraper

This script uses aggressive JavaScript manipulation to try to bypass
the timer and access quiz data immediately.
"""

import json
import asyncio
from playwright.async_api import async_playwright


async def aggressive_bypass_scrape():
    """Use aggressive techniques to bypass timer and extract quiz data."""
    
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
        
        print("Attempting aggressive timer bypass...")
        
        # Aggressive JavaScript injection to bypass timer
        aggressive_scripts = [
            # Override all timer-related functions
            """
            // Override setInterval to skip long intervals
            const originalSetInterval = setInterval;
            setInterval = function(fn, delay) {
                if (delay > 1000) {
                    console.log('Blocked timer interval:', delay);
                    return null;
                }
                return originalSetInterval(fn, delay);
            };
            
            // Override setTimeout to skip long timeouts
            const originalSetTimeout = setTimeout;
            setTimeout = function(fn, delay) {
                if (delay > 1000) {
                    console.log('Blocked timer timeout:', delay);
                    return null;
                }
                return originalSetTimeout(fn, delay);
            };
            """,
            
            # Force timer variables to 0
            """
            // Set all possible timer variables to 0
            window.quizTimer = 0;
            window.timer = 0;
            window.countdown = 0;
            window.quizCountdown = 0;
            window.timeLeft = 0;
            window.remainingTime = 0;
            window.quizTime = 0;
            window.seconds = 0;
            window.minutes = 0;
            window.hours = 0;
            window.days = 0;
            """,
            
            # Force quiz state
            """
            // Force quiz to be ready
            if (typeof localStorage !== 'undefined') {
                localStorage.setItem('quizStarted', 'true');
                localStorage.setItem('timerComplete', 'true');
                localStorage.setItem('quizState', 'ready');
                localStorage.setItem('timerExpired', 'true');
            }
            if (typeof sessionStorage !== 'undefined') {
                sessionStorage.setItem('quizStarted', 'true');
                sessionStorage.setItem('timerComplete', 'true');
                sessionStorage.setItem('quizState', 'ready');
                sessionStorage.setItem('timerExpired', 'true');
            }
            """,
            
            # Remove timer elements
            """
            // Remove timer elements from DOM
            const timerSelectors = [
                '[class*="timer"]',
                '[class*="countdown"]',
                '[id*="timer"]',
                '[id*="countdown"]',
                '.timer',
                '.countdown',
                '#timer',
                '#countdown'
            ];
            
            timerSelectors.forEach(selector => {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => el.remove());
            });
            """,
            
            # Try to trigger quiz functions
            """
            // Try to trigger quiz loading functions
            const functions = [
                'GetCount', 'startQuiz', 'beginQuiz', 'submit_p_form',
                'loadQuiz', 'loadQuestions', 'initializeQuiz', 'startTest',
                'beginTest', 'loadTest', 'showQuiz', 'displayQuiz'
            ];
            
            functions.forEach(funcName => {
                if (typeof window[funcName] === 'function') {
                    try {
                        window[funcName]();
                        console.log('Executed function:', funcName);
                    } catch (e) {
                        console.log('Error executing function:', funcName, e);
                    }
                }
            });
            """,
            
            # Override Date object to fake time
            """
            // Override Date to make it seem like time has passed
            const originalDate = Date;
            const fakeTime = new Date().getTime() + (24 * 60 * 60 * 1000); // Add 24 hours
            Date = function() {
                const date = new originalDate(fakeTime);
                date.getTime = () => fakeTime;
                return date;
            };
            Date.now = () => fakeTime;
            Date.prototype = originalDate.prototype;
            """,
            
            # Force page refresh to trigger quiz
            """
            // Force page refresh after a short delay
            setTimeout(() => {
                window.location.reload();
            }, 2000);
            """
        ]
        
        # Execute aggressive scripts
        for i, script in enumerate(aggressive_scripts):
            try:
                await page.evaluate(script)
                print(f"Executed aggressive script {i+1}")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Error executing aggressive script {i+1}: {e}")
        
        # Wait a bit for scripts to take effect
        await asyncio.sleep(5)
        
        # Try to extract quiz data
        print("Attempting to extract quiz data after bypass...")
        
        # Check sessionStorage
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
        for key, value in storage_data.items():
            if value and len(value) > 10:
                try:
                    parsed_data = json.loads(value)
                    if isinstance(parsed_data, list) and len(parsed_data) > 0:
                        print(f"Found quiz data in sessionStorage: {len(parsed_data)} items")
                        return await extract_questions_from_data(parsed_data)
                except json.JSONDecodeError:
                    continue
        
        # Check for quiz elements on page
        quiz_elements = await page.query_selector_all('[class*="quiz"], [class*="question"]')
        if quiz_elements:
            print(f"Found {len(quiz_elements)} quiz elements after bypass")
            
            # Try to extract questions from visible elements
            questions = []
            for element in quiz_elements:
                try:
                    text = await element.text_content()
                    if text and len(text.strip()) > 20:
                        # This might be a question
                        print(f"Found potential question: {text[:100]}...")
                except:
                    continue
        
        print("Aggressive bypass did not yield quiz data.")
        return []
        
    except Exception as e:
        print(f"Error during aggressive bypass: {e}")
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
    print("Starting aggressive bypass ProProfs quiz scraper...")
    print("Warning: This uses aggressive techniques to bypass the timer.")
    
    questions = await aggressive_bypass_scrape()
    
    if questions:
        # Save to JSON file
        with open('quiz_data.json', 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)
        
        print(f"\nSuccessfully extracted {len(questions)} questions")
        print("Quiz data saved to quiz_data.json")
    else:
        print("\nAggressive bypass did not yield quiz data.")
        print("The timer protection may be too strong to bypass.")
    
    print(f"Total questions scraped: {len(questions)}")


if __name__ == "__main__":
    asyncio.run(main())
