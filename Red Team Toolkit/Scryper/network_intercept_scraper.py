#!/usr/bin/env python3
"""
Network Intercept ProProfs Quiz Scraper

This script uses network interception to discover API endpoints and potential
quiz data sources that might be accessible even with timer protection.
"""

import json
import asyncio
import re
from playwright.async_api import async_playwright


async def intercept_network_traffic():
    """Intercept and analyze all network traffic to find quiz data endpoints."""
    
    # Initialize Playwright
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()
    page = await context.new_page()
    
    # Store intercepted requests and responses
    intercepted_data = []
    
    # Set up request interception
    await page.route("**/*", lambda route: handle_request(route, intercepted_data))
    
    # Set up response interception
    page.on("response", lambda response: handle_response(response, intercepted_data))
    
    try:
        print("Starting network interception...")
        
        # Navigate to quiz URL
        url = "https://www.proprofs.com/quiz-school/ugc/story.php?title=sfia-service-operations-practitioner0h&token=Z3FlYmVyaGFkZW1hbmRAY2FwYWNpdGkub3JnLnph"
        await page.goto(url, wait_until='networkidle')
        await page.wait_for_load_state('domcontentloaded')
        
        # Wait for additional network activity
        await asyncio.sleep(5)
        
        print(f"Intercepted {len(intercepted_data)} network requests/responses")
        
        # Analyze intercepted data
        quiz_endpoints = []
        api_endpoints = []
        data_responses = []
        
        for item in intercepted_data:
            url = item.get('url', '')
            
            # Look for quiz-related endpoints
            if any(term in url.lower() for term in ['quiz', 'question', 'test', 'assessment']):
                quiz_endpoints.append(item)
            
            # Look for API endpoints
            if any(term in url.lower() for term in ['api', 'ajax', 'json', 'data']):
                api_endpoints.append(item)
            
            # Look for responses with data
            if item.get('response_data'):
                data_responses.append(item)
        
        print(f"Found {len(quiz_endpoints)} quiz-related endpoints")
        print(f"Found {len(api_endpoints)} API endpoints")
        print(f"Found {len(data_responses)} responses with data")
        
        # Try to extract quiz data from responses
        quiz_data = []
        
        for response in data_responses:
            try:
                data = response.get('response_data')
                if isinstance(data, list) and len(data) > 0:
                    # Check if it looks like quiz data
                    first_item = data[0]
                    if isinstance(first_item, dict) and ('question' in first_item or 'text' in first_item):
                        quiz_data.extend(data)
                elif isinstance(data, dict):
                    if 'questions' in data and isinstance(data['questions'], list):
                        quiz_data.extend(data['questions'])
                    elif 'data' in data and isinstance(data['data'], list):
                        quiz_data.extend(data['data'])
            except:
                continue
        
        # Try direct API calls to discovered endpoints
        print("\nTrying direct API calls to discovered endpoints...")
        
        for endpoint in api_endpoints:
            endpoint_url = endpoint.get('url')
            if endpoint_url:
                print(f"Trying endpoint: {endpoint_url}")
                
                try:
                    # Try to access the endpoint directly
                    response = await page.goto(endpoint_url, wait_until='networkidle')
                    content = await response.text()
                    
                    # Try to parse as JSON
                    try:
                        json_data = json.loads(content)
                        if isinstance(json_data, list) and len(json_data) > 0:
                            print(f"Found data in {endpoint_url}: {len(json_data)} items")
                            quiz_data.extend(json_data)
                    except json.JSONDecodeError:
                        # Look for JSON patterns in the content
                        json_patterns = [
                            r'\[.*?\]',
                            r'\{.*?\}',
                            r'"questions"\s*:\s*\[.*?\]',
                            r'"quizData"\s*:\s*\[.*?\]'
                        ]
                        
                        for pattern in json_patterns:
                            matches = re.findall(pattern, content, re.DOTALL)
                            for match in matches:
                                try:
                                    data = json.loads(match)
                                    if isinstance(data, list) and len(data) > 0:
                                        print(f"Found JSON data in {endpoint_url}: {len(data)} items")
                                        quiz_data.extend(data)
                                except:
                                    continue
                except Exception as e:
                    print(f"Error accessing {endpoint_url}: {e}")
        
        # Try common ProProfs API patterns
        print("\nTrying common ProProfs API patterns...")
        
        common_patterns = [
            f"{url.replace('story.php', 'api/quiz')}",
            f"{url.replace('story.php', 'api/questions')}",
            f"{url.replace('story.php', 'ajax/get_quiz')}",
            f"{url.replace('story.php', 'ajax/get_questions')}",
            f"{url.replace('story.php', 'data/quiz')}",
            f"{url.replace('story.php', 'data/questions')}"
        ]
        
        for pattern_url in common_patterns:
            try:
                print(f"Trying pattern: {pattern_url}")
                response = await page.goto(pattern_url, wait_until='networkidle')
                content = await response.text()
                
                # Try to parse as JSON
                try:
                    json_data = json.loads(content)
                    if isinstance(json_data, list) and len(json_data) > 0:
                        print(f"Found data in pattern URL: {len(json_data)} items")
                        quiz_data.extend(json_data)
                except json.JSONDecodeError:
                    pass
            except Exception as e:
                print(f"Error accessing pattern URL: {e}")
        
        # Save all intercepted data for analysis
        analysis_data = {
            'intercepted_data': intercepted_data,
            'quiz_endpoints': quiz_endpoints,
            'api_endpoints': api_endpoints,
            'data_responses': data_responses,
            'quiz_data_found': quiz_data
        }
        
        with open('network_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False)
        
        print(f"\nNetwork analysis saved to network_analysis.json")
        
        return quiz_data
        
    except Exception as e:
        print(f"Error during network interception: {e}")
        return []
        
    finally:
        await context.close()
        await browser.close()
        await playwright.stop()


async def handle_request(route, intercepted_data):
    """Handle intercepted requests."""
    try:
        request = route.request
        url = request.url
        
        # Log interesting requests
        if any(term in url.lower() for term in ['quiz', 'question', 'api', 'ajax', 'json']):
            print(f"Intercepted request: {url}")
        
        intercepted_data.append({
            'type': 'request',
            'url': url,
            'method': request.method,
            'headers': dict(request.headers)
        })
        
        # Continue the request
        await route.continue_()
        
    except Exception as e:
        print(f"Error handling request: {e}")
        await route.continue_()


async def handle_response(response, intercepted_data):
    """Handle intercepted responses."""
    try:
        url = response.url
        
        # Only process interesting responses
        if any(term in url.lower() for term in ['quiz', 'question', 'api', 'ajax', 'json']):
            print(f"Intercepted response: {url} - Status: {response.status}")
            
            if response.status == 200:
                try:
                    # Try to get JSON response
                    content_type = response.headers.get('content-type', '')
                    if 'application/json' in content_type or 'text/json' in content_type:
                        response_data = await response.json()
                        
                        intercepted_data.append({
                            'type': 'response',
                            'url': url,
                            'status': response.status,
                            'content_type': content_type,
                            'response_data': response_data
                        })
                        
                        print(f"Captured JSON data from {url}")
                except:
                    # Try to get text response
                    try:
                        text_data = await response.text()
                        intercepted_data.append({
                            'type': 'response',
                            'url': url,
                            'status': response.status,
                            'content_type': content_type,
                            'response_data': text_data
                        })
                    except:
                        pass
                        
    except Exception as e:
        print(f"Error handling response: {e}")


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
    print("Starting network intercept ProProfs quiz scraper...")
    print("This will intercept all network traffic to discover quiz data endpoints.")
    
    quiz_data = await intercept_network_traffic()
    questions = await extract_questions_from_data(quiz_data)
    
    if questions:
        # Save to JSON file
        with open('quiz_data.json', 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)
        
        print(f"\nSuccessfully extracted {len(questions)} questions")
        print("Quiz data saved to quiz_data.json")
    else:
        print("\nNo quiz data found through network interception.")
        print("Check network_analysis.json for detailed analysis.")
    
    print(f"Total questions extracted: {len(questions)}")


if __name__ == "__main__":
    asyncio.run(main())
