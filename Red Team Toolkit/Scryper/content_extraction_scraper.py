#!/usr/bin/env python3
"""
Content Extraction ProProfs Quiz Scraper

This script tries to extract any visible quiz content and analyze the page structure
to find quiz data that might be hidden or embedded.
"""

import json
import asyncio
import re
from playwright.async_api import async_playwright


async def extract_visible_content():
    """Extract any visible quiz content from the page."""
    
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
        
        print("Analyzing page content and structure...")
        
        # Get page title
        title = await page.title()
        print(f"Page title: {title}")
        
        # Get all text content
        all_text = await page.evaluate("document.body.innerText")
        print(f"Total text content length: {len(all_text)} characters")
        
        # Look for quiz-related text
        quiz_keywords = ['question', 'answer', 'quiz', 'test', 'exam', 'assessment']
        found_content = []
        
        for keyword in quiz_keywords:
            if keyword.lower() in all_text.lower():
                # Find context around the keyword
                lines = all_text.split('\n')
                for i, line in enumerate(lines):
                    if keyword.lower() in line.lower():
                        found_content.append({
                            'keyword': keyword,
                            'line': line.strip(),
                            'line_number': i
                        })
        
        print(f"Found {len(found_content)} lines containing quiz keywords:")
        for item in found_content[:10]:  # Show first 10
            print(f"  Line {item['line_number']}: {item['line'][:100]}...")
        
        # Look for numbered items that might be questions
        numbered_pattern = r'^\d+[\.\)]\s*(.+)'
        numbered_items = re.findall(numbered_pattern, all_text, re.MULTILINE)
        
        if numbered_items:
            print(f"\nFound {len(numbered_items)} numbered items (potential questions):")
            for i, item in enumerate(numbered_items[:5]):  # Show first 5
                print(f"  {i+1}. {item[:100]}...")
        
        # Look for multiple choice patterns (A, B, C, D)
        choice_pattern = r'^[A-D][\.\)]\s*(.+)'
        choice_items = re.findall(choice_pattern, all_text, re.MULTILINE)
        
        if choice_items:
            print(f"\nFound {len(choice_items)} choice items (potential answers):")
            for i, item in enumerate(choice_items[:10]):  # Show first 10
                print(f"  {chr(65+i)}. {item[:100]}...")
        
        # Check for hidden elements
        hidden_elements = await page.query_selector_all('[style*="display: none"], [style*="visibility: hidden"], [hidden]')
        print(f"\nFound {len(hidden_elements)} hidden elements")
        
        # Check for elements with quiz-related classes
        quiz_elements = await page.query_selector_all('[class*="quiz"], [class*="question"], [class*="test"], [class*="answer"]')
        print(f"Found {len(quiz_elements)} elements with quiz-related classes")
        
        # Extract text from quiz elements
        quiz_texts = []
        for element in quiz_elements:
            try:
                text = await element.text_content()
                if text and len(text.strip()) > 10:
                    quiz_texts.append(text.strip())
            except:
                continue
        
        if quiz_texts:
            print(f"\nText from quiz elements:")
            for i, text in enumerate(quiz_texts[:10]):  # Show first 10
                print(f"  {i+1}. {text[:100]}...")
        
        # Look for iframes that might contain quiz content
        iframes = await page.query_selector_all('iframe')
        print(f"\nFound {len(iframes)} iframes")
        
        for i, iframe in enumerate(iframes):
            try:
                src = await iframe.get_attribute('src')
                if src:
                    print(f"  Iframe {i+1} src: {src}")
            except:
                continue
        
        # Check for any JavaScript variables that might contain quiz data
        js_vars = await page.evaluate("""
            () => {
                const vars = {};
                for (let key in window) {
                    if (key.toLowerCase().includes('quiz') || 
                        key.toLowerCase().includes('question') || 
                        key.toLowerCase().includes('test')) {
                        try {
                            vars[key] = window[key];
                        } catch (e) {
                            vars[key] = '[Error accessing]';
                        }
                    }
                }
                return vars;
            }
        """)
        
        if js_vars:
            print(f"\nFound {len(js_vars)} JavaScript variables with quiz-related names:")
            for key, value in js_vars.items():
                print(f"  {key}: {str(value)[:100]}...")
        
        # Save all extracted content to a file for analysis
        extracted_data = {
            'page_title': title,
            'all_text_length': len(all_text),
            'quiz_keywords_found': found_content,
            'numbered_items': numbered_items[:20],  # First 20
            'choice_items': choice_items[:20],      # First 20
            'quiz_texts': quiz_texts[:20],          # First 20
            'javascript_vars': js_vars
        }
        
        with open('extracted_content.json', 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, indent=2, ensure_ascii=False)
        
        print(f"\nExtracted content saved to extracted_content.json")
        
        # Try to construct questions from the found content
        questions = []
        
        # If we found numbered items, try to pair them with choice items
        if numbered_items and choice_items:
            print("\nAttempting to construct questions from numbered items and choices...")
            
            # Group choices by proximity to numbered items
            for i, numbered_item in enumerate(numbered_items[:10]):  # First 10
                question_text = numbered_item.strip()
                options = []
                
                # Look for choices that might belong to this question
                # This is a simple heuristic - in practice, you'd need more sophisticated parsing
                start_idx = i * 4  # Assume 4 choices per question
                end_idx = start_idx + 4
                
                for j in range(start_idx, min(end_idx, len(choice_items))):
                    if j < len(choice_items):
                        options.append(choice_items[j].strip())
                
                if options:
                    questions.append({
                        "question": question_text,
                        "options": options
                    })
        
        return questions
        
    except Exception as e:
        print(f"Error during content extraction: {e}")
        return []
        
    finally:
        await context.close()
        await browser.close()
        await playwright.stop()


async def main():
    """Main function."""
    print("Starting content extraction ProProfs quiz scraper...")
    print("This will analyze the page structure and extract any visible content.")
    
    questions = await extract_visible_content()
    
    if questions:
        # Save to JSON file
        with open('quiz_data.json', 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)
        
        print(f"\nSuccessfully extracted {len(questions)} questions")
        print("Quiz data saved to quiz_data.json")
    else:
        print("\nNo questions could be constructed from the extracted content.")
        print("Check extracted_content.json for detailed analysis.")
    
    print(f"Total questions extracted: {len(questions)}")


if __name__ == "__main__":
    asyncio.run(main())
