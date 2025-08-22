#!/usr/bin/env python3
"""
Alternative ProProfs Quiz Scraper

This script tries multiple alternative approaches to extract quiz data
even with the timer running, including network interception and page analysis.
"""

import json
import asyncio
import re
from playwright.async_api import async_playwright


async def scrape_with_alternatives():
    """Try multiple alternative approaches to get quiz data."""
    
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
        
        print("Trying alternative approaches to extract quiz data...")
        
        # Approach 1: Check for embedded quiz data in page source
        print("\n1. Checking for embedded quiz data in page source...")
        page_source = await page.content()
        
        # Look for JSON patterns in the page source
        json_patterns = [
            r'var\s+quizData\s*=\s*(\[.*?\]);',
            r'var\s+questions\s*=\s*(\[.*?\]);',
            r'window\.quizData\s*=\s*(\[.*?\]);',
            r'window\.questions\s*=\s*(\[.*?\]);',
            r'"questions"\s*:\s*(\[.*?\])',
            r'"quizData"\s*:\s*(\[.*?\])',
            r'data-questions\s*=\s*"(\[.*?\])"',
            r'data-quiz\s*=\s*"(\[.*?\])"'
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, page_source, re.DOTALL)
            for match in matches:
                try:
                    # Clean up the JSON string
                    json_str = match.replace('\\"', '"').replace('\\/', '/')
                    data = json.loads(json_str)
                    if isinstance(data, list) and len(data) > 0:
                        print(f"Found embedded quiz data: {len(data)} items")
                        return await extract_questions_from_data(data)
                except json.JSONDecodeError:
                    continue
        
        # Approach 2: Check for quiz data in script tags
        print("\n2. Checking script tags for quiz data...")
        script_tags = await page.query_selector_all('script')
        for script in script_tags:
            try:
                script_content = await script.text_content()
                if script_content:
                    # Look for quiz data in script content
                    for pattern in json_patterns:
                        matches = re.findall(pattern, script_content, re.DOTALL)
                        for match in matches:
                            try:
                                json_str = match.replace('\\"', '"').replace('\\/', '/')
                                data = json.loads(json_str)
                                if isinstance(data, list) and len(data) > 0:
                                    print(f"Found quiz data in script: {len(data)} items")
                                    return await extract_questions_from_data(data)
                            except json.JSONDecodeError:
                                continue
            except:
                continue
        
        # Approach 3: Check for quiz data in data attributes
        print("\n3. Checking data attributes for quiz data...")
        elements_with_data = await page.query_selector_all('[data-*]')
        for element in elements_with_data:
            try:
                # Get all data attributes
                data_attrs = await element.evaluate("""
                    (el) => {
                        const attrs = {};
                        for (let attr of el.attributes) {
                            if (attr.name.startsWith('data-')) {
                                attrs[attr.name] = attr.value;
                            }
                        }
                        return attrs;
                    }
                """)
                
                for attr_name, attr_value in data_attrs.items():
                    if any(term in attr_name.lower() for term in ['quiz', 'question', 'test']):
                        try:
                            data = json.loads(attr_value)
                            if isinstance(data, list) and len(data) > 0:
                                print(f"Found quiz data in {attr_name}: {len(data)} items")
                                return await extract_questions_from_data(data)
                        except json.JSONDecodeError:
                            continue
            except:
                continue
        
        # Approach 4: Try to extract from visible quiz elements
        print("\n4. Checking for visible quiz elements...")
        quiz_elements = await page.query_selector_all('[class*="quiz"], [class*="question"], [class*="test"]')
        if quiz_elements:
            print(f"Found {len(quiz_elements)} quiz-related elements")
            
            # Try to extract text from these elements
            questions = []
            for i, element in enumerate(quiz_elements[:10]):  # Limit to first 10
                try:
                    text = await element.text_content()
                    if text and len(text.strip()) > 20:  # Only meaningful text
                        print(f"Element {i+1}: {text[:100]}...")
                        # This might contain question text
                except:
                    continue
        
        # Approach 5: Check for quiz data in meta tags
        print("\n5. Checking meta tags for quiz data...")
        meta_tags = await page.query_selector_all('meta')
        for meta in meta_tags:
            try:
                name = await meta.get_attribute('name')
                content = await meta.get_attribute('content')
                if name and content and any(term in name.lower() for term in ['quiz', 'question', 'test']):
                    print(f"Found meta tag: {name} = {content[:100]}...")
                    try:
                        data = json.loads(content)
                        if isinstance(data, list) and len(data) > 0:
                            print(f"Found quiz data in meta tag: {len(data)} items")
                            return await extract_questions_from_data(data)
                    except json.JSONDecodeError:
                        continue
            except:
                continue
        
        # Approach 6: Try to access quiz data via JavaScript
        print("\n6. Trying JavaScript access to quiz data...")
        js_attempts = [
            "window.quizData",
            "window.questions",
            "window.quiz",
            "document.quizData",
            "document.questions",
            "quizData",
            "questions"
        ]
        
        for js_var in js_attempts:
            try:
                result = await page.evaluate(f"typeof {js_var} !== 'undefined' ? {js_var} : null")
                if result and isinstance(result, list) and len(result) > 0:
                    print(f"Found quiz data via JavaScript {js_var}: {len(result)} items")
                    return await extract_questions_from_data(result)
            except:
                continue
        
        # Approach 7: Check for quiz data in comments
        print("\n7. Checking HTML comments for quiz data...")
        comment_pattern = r'<!--(.*?)-->'
        comments = re.findall(comment_pattern, page_source, re.DOTALL)
        for comment in comments:
            if any(term in comment.lower() for term in ['quiz', 'question', 'test']):
                print(f"Found relevant comment: {comment[:100]}...")
                # Look for JSON in comments
                for pattern in json_patterns:
                    matches = re.findall(pattern, comment, re.DOTALL)
                    for match in matches:
                        try:
                            json_str = match.replace('\\"', '"').replace('\\/', '/')
                            data = json.loads(json_str)
                            if isinstance(data, list) and len(data) > 0:
                                print(f"Found quiz data in comment: {len(data)} items")
                                return await extract_questions_from_data(data)
                        except json.JSONDecodeError:
                            continue
        
        print("\nNo quiz data found using alternative approaches.")
        return []
        
    except Exception as e:
        print(f"Error during alternative scraping: {e}")
        return []
        
    finally:
        await context.close()
        await browser.close()
        await playwright.stop()


async def extract_questions_from_data(data):
    """Extract questions from various data formats."""
    questions = []
    
    if isinstance(data, list):
        for item in data:
            try:
                if isinstance(item, dict):
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
    print("Starting alternative ProProfs quiz scraper...")
    print("Trying multiple approaches to extract quiz data...")
    
    questions = await scrape_with_alternatives()
    
    if questions:
        # Save to JSON file
        with open('quiz_data.json', 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)
        
        print(f"\nSuccessfully extracted {len(questions)} questions")
        print("Quiz data saved to quiz_data.json")
    else:
        print("\nNo quiz data could be extracted using alternative approaches.")
        print("The quiz data may be protected by the timer system.")
    
    print(f"Total questions scraped: {len(questions)}")


if __name__ == "__main__":
    asyncio.run(main())
