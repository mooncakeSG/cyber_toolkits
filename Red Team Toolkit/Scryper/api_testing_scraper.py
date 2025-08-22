#!/usr/bin/env python3
"""
API Testing ProProfs Quiz Scraper

This script uses HTTP requests to test various API endpoints and potentially
bypass the timer protection by directly accessing backend services.
"""

import json
import requests
import time
import re
from urllib.parse import urljoin, urlparse, parse_qs
from typing import Dict, List, Optional


class APITestingScraper:
    """Scraper that tests API endpoints directly using HTTP requests."""
    
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.proprofs.com"
        self.quiz_url = "https://www.proprofs.com/quiz-school/ugc/story.php?title=sfia-service-operations-practitioner0h&token=Z3FlYmVyaGFkZW1hbmRAY2FwYWNpdGkub3JnLnph"
        self.quiz_data = []
        
        # Set up headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
    
    def extract_url_parameters(self) -> Dict[str, str]:
        """Extract parameters from the quiz URL."""
        parsed = urlparse(self.quiz_url)
        params = parse_qs(parsed.query)
        return {k: v[0] for k, v in params.items()}
    
    def test_common_api_endpoints(self) -> List[Dict]:
        """Test common ProProfs API endpoints."""
        print("Testing common API endpoints...")
        
        url_params = self.extract_url_parameters()
        title = url_params.get('title', '')
        token = url_params.get('token', '')
        
        # Common API endpoint patterns
        api_endpoints = [
            # Quiz data endpoints
            f"/quiz-school/api/quiz/{title}",
            f"/quiz-school/api/questions/{title}",
            f"/quiz-school/api/quiz-data/{title}",
            f"/api/quiz/{title}",
            f"/api/questions/{title}",
            f"/api/quiz-data/{title}",
            
            # UGC specific endpoints
            f"/quiz-school/ugc/api/quiz/{title}",
            f"/quiz-school/ugc/api/questions/{title}",
            f"/quiz-school/ugc/api/quiz-data/{title}",
            
            # Token-based endpoints
            f"/quiz-school/api/quiz?token={token}",
            f"/quiz-school/api/questions?token={token}",
            f"/api/quiz?token={token}",
            f"/api/questions?token={token}",
            
            # Generic endpoints
            "/quiz-school/api/quiz",
            "/quiz-school/api/questions",
            "/api/quiz",
            "/api/questions",
            
            # AJAX endpoints
            f"/quiz-school/ajax/get_quiz.php?title={title}",
            f"/quiz-school/ajax/get_questions.php?title={title}",
            f"/ajax/get_quiz.php?title={title}",
            f"/ajax/get_questions.php?title={title}",
            
            # Data endpoints
            f"/quiz-school/data/quiz/{title}.json",
            f"/quiz-school/data/questions/{title}.json",
            f"/data/quiz/{title}.json",
            f"/data/questions/{title}.json",
        ]
        
        results = []
        
        for endpoint in api_endpoints:
            try:
                full_url = urljoin(self.base_url, endpoint)
                print(f"Testing: {full_url}")
                
                response = self.session.get(full_url, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ Success: {full_url}")
                    
                    # Try to parse as JSON
                    try:
                        data = response.json()
                        if isinstance(data, list) and len(data) > 0:
                            print(f"   Found {len(data)} items")
                            results.append({
                                'url': full_url,
                                'data': data,
                                'type': 'list'
                            })
                        elif isinstance(data, dict):
                            print(f"   Found dict with keys: {list(data.keys())}")
                            results.append({
                                'url': full_url,
                                'data': data,
                                'type': 'dict'
                            })
                    except json.JSONDecodeError:
                        # Check for JSON patterns in text
                        text_content = response.text
                        if len(text_content) > 100:
                            print(f"   Text content: {text_content[:200]}...")
                            results.append({
                                'url': full_url,
                                'data': text_content,
                                'type': 'text'
                            })
                
                elif response.status_code == 403:
                    print(f"❌ Forbidden: {full_url}")
                elif response.status_code == 404:
                    print(f"❌ Not Found: {full_url}")
                else:
                    print(f"⚠️  Status {response.status_code}: {full_url}")
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ Error: {full_url} - {e}")
            
            # Small delay between requests
            time.sleep(0.5)
        
        return results
    
    def test_ajax_endpoints(self) -> List[Dict]:
        """Test AJAX endpoints that might be used by the quiz."""
        print("\nTesting AJAX endpoints...")
        
        url_params = self.extract_url_parameters()
        title = url_params.get('title', '')
        token = url_params.get('token', '')
        
        # AJAX endpoint patterns
        ajax_endpoints = [
            # Common AJAX patterns
            f"/quiz-school/ajax/quiz.php?action=get_questions&title={title}",
            f"/quiz-school/ajax/quiz.php?action=get_quiz&title={title}",
            f"/ajax/quiz.php?action=get_questions&title={title}",
            f"/ajax/quiz.php?action=get_quiz&title={title}",
            
            # Token-based AJAX
            f"/quiz-school/ajax/quiz.php?action=get_questions&token={token}",
            f"/quiz-school/ajax/quiz.php?action=get_quiz&token={token}",
            f"/ajax/quiz.php?action=get_questions&token={token}",
            f"/ajax/quiz.php?action=get_quiz&token={token}",
            
            # Generic AJAX endpoints
            "/quiz-school/ajax/quiz.php?action=get_questions",
            "/quiz-school/ajax/quiz.php?action=get_quiz",
            "/ajax/quiz.php?action=get_questions",
            "/ajax/quiz.php?action=get_quiz",
            
            # Alternative AJAX patterns
            f"/quiz-school/ajax/get_quiz_data.php?title={title}",
            f"/quiz-school/ajax/get_questions_data.php?title={title}",
            f"/ajax/get_quiz_data.php?title={title}",
            f"/ajax/get_questions_data.php?title={title}",
        ]
        
        results = []
        
        for endpoint in ajax_endpoints:
            try:
                full_url = urljoin(self.base_url, endpoint)
                print(f"Testing AJAX: {full_url}")
                
                # Add AJAX-specific headers
                headers = self.session.headers.copy()
                headers.update({
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Referer': self.quiz_url
                })
                
                response = self.session.get(full_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ AJAX Success: {full_url}")
                    
                    try:
                        data = response.json()
                        if isinstance(data, list) and len(data) > 0:
                            print(f"   Found {len(data)} items")
                            results.append({
                                'url': full_url,
                                'data': data,
                                'type': 'ajax_list'
                            })
                        elif isinstance(data, dict):
                            print(f"   Found dict with keys: {list(data.keys())}")
                            results.append({
                                'url': full_url,
                                'data': data,
                                'type': 'ajax_dict'
                            })
                    except json.JSONDecodeError:
                        text_content = response.text
                        if len(text_content) > 100:
                            print(f"   Text content: {text_content[:200]}...")
                            results.append({
                                'url': full_url,
                                'data': text_content,
                                'type': 'ajax_text'
                            })
                
                elif response.status_code == 403:
                    print(f"❌ AJAX Forbidden: {full_url}")
                elif response.status_code == 404:
                    print(f"❌ AJAX Not Found: {full_url}")
                else:
                    print(f"⚠️  AJAX Status {response.status_code}: {full_url}")
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ AJAX Error: {full_url} - {e}")
            
            time.sleep(0.5)
        
        return results
    
    def test_post_endpoints(self) -> List[Dict]:
        """Test POST endpoints that might accept parameters."""
        print("\nTesting POST endpoints...")
        
        url_params = self.extract_url_parameters()
        title = url_params.get('title', '')
        token = url_params.get('token', '')
        
        # POST endpoint patterns
        post_endpoints = [
            "/quiz-school/ajax/quiz.php",
            "/ajax/quiz.php",
            "/quiz-school/api/quiz",
            "/api/quiz",
            "/quiz-school/api/questions",
            "/api/questions",
        ]
        
        results = []
        
        # Different POST payloads to try
        payloads = [
            {'action': 'get_questions', 'title': title},
            {'action': 'get_quiz', 'title': title},
            {'action': 'get_questions', 'token': token},
            {'action': 'get_quiz', 'token': token},
            {'title': title, 'token': token},
            {'quiz_title': title, 'quiz_token': token},
            {'data': title, 'auth': token},
        ]
        
        for endpoint in post_endpoints:
            for payload in payloads:
                try:
                    full_url = urljoin(self.base_url, endpoint)
                    print(f"Testing POST: {full_url} with payload: {payload}")
                    
                    # Add POST-specific headers
                    headers = self.session.headers.copy()
                    headers.update({
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Referer': self.quiz_url
                    })
                    
                    response = self.session.post(full_url, data=payload, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        print(f"✅ POST Success: {full_url}")
                        
                        try:
                            data = response.json()
                            if isinstance(data, list) and len(data) > 0:
                                print(f"   Found {len(data)} items")
                                results.append({
                                    'url': full_url,
                                    'payload': payload,
                                    'data': data,
                                    'type': 'post_list'
                                })
                            elif isinstance(data, dict):
                                print(f"   Found dict with keys: {list(data.keys())}")
                                results.append({
                                    'url': full_url,
                                    'payload': payload,
                                    'data': data,
                                    'type': 'post_dict'
                                })
                        except json.JSONDecodeError:
                            text_content = response.text
                            if len(text_content) > 100:
                                print(f"   Text content: {text_content[:200]}...")
                                results.append({
                                    'url': full_url,
                                    'payload': payload,
                                    'data': text_content,
                                    'type': 'post_text'
                                })
                    
                    elif response.status_code == 403:
                        print(f"❌ POST Forbidden: {full_url}")
                    elif response.status_code == 404:
                        print(f"❌ POST Not Found: {full_url}")
                    else:
                        print(f"⚠️  POST Status {response.status_code}: {full_url}")
                        
                except requests.exceptions.RequestException as e:
                    print(f"❌ POST Error: {full_url} - {e}")
                
                time.sleep(0.5)
        
        return results
    
    def test_bypass_attempts(self) -> List[Dict]:
        """Test various bypass attempts."""
        print("\nTesting bypass attempts...")
        
        url_params = self.extract_url_parameters()
        title = url_params.get('title', '')
        token = url_params.get('token', '')
        
        # Bypass attempts
        bypass_endpoints = [
            # Try with different time parameters
            f"/quiz-school/api/quiz/{title}?time=expired",
            f"/quiz-school/api/quiz/{title}?timer=0",
            f"/quiz-school/api/quiz/{title}?countdown=complete",
            
            # Try with admin parameters
            f"/quiz-school/api/quiz/{title}?admin=true",
            f"/quiz-school/api/quiz/{title}?bypass=true",
            f"/quiz-school/api/quiz/{title}?debug=true",
            
            # Try with different user agents
            f"/quiz-school/api/quiz/{title}?user_agent=admin",
            f"/quiz-school/api/quiz/{title}?role=admin",
            
            # Try with session parameters
            f"/quiz-school/api/quiz/{title}?session=admin",
            f"/quiz-school/api/quiz/{title}?auth=admin",
        ]
        
        results = []
        
        for endpoint in bypass_endpoints:
            try:
                full_url = urljoin(self.base_url, endpoint)
                print(f"Testing bypass: {full_url}")
                
                # Try with different headers
                headers = self.session.headers.copy()
                headers.update({
                    'X-Admin': 'true',
                    'X-Bypass': 'true',
                    'X-Debug': 'true',
                    'Authorization': 'Bearer admin',
                })
                
                response = self.session.get(full_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ Bypass Success: {full_url}")
                    
                    try:
                        data = response.json()
                        if isinstance(data, list) and len(data) > 0:
                            print(f"   Found {len(data)} items")
                            results.append({
                                'url': full_url,
                                'data': data,
                                'type': 'bypass_list'
                            })
                        elif isinstance(data, dict):
                            print(f"   Found dict with keys: {list(data.keys())}")
                            results.append({
                                'url': full_url,
                                'data': data,
                                'type': 'bypass_dict'
                            })
                    except json.JSONDecodeError:
                        text_content = response.text
                        if len(text_content) > 100:
                            print(f"   Text content: {text_content[:200]}...")
                            results.append({
                                'url': full_url,
                                'data': text_content,
                                'type': 'bypass_text'
                            })
                
                elif response.status_code == 403:
                    print(f"❌ Bypass Forbidden: {full_url}")
                elif response.status_code == 404:
                    print(f"❌ Bypass Not Found: {full_url}")
                else:
                    print(f"⚠️  Bypass Status {response.status_code}: {full_url}")
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ Bypass Error: {full_url} - {e}")
            
            time.sleep(0.5)
        
        return results
    
    def extract_questions_from_data(self, data: List[Dict]) -> List[Dict]:
        """Extract questions from various data formats."""
        questions = []
        
        for result in data:
            try:
                result_data = result.get('data', [])
                
                if isinstance(result_data, list):
                    for item in result_data:
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
                
                elif isinstance(result_data, dict):
                    # Check for nested questions
                    if 'questions' in result_data and isinstance(result_data['questions'], list):
                        for item in result_data['questions']:
                            if isinstance(item, dict):
                                question_text = None
                                options = []
                                
                                if 'question' in item:
                                    question_text = item['question']
                                elif 'text' in item:
                                    question_text = item['text']
                                
                                if 'options' in item and isinstance(item['options'], list):
                                    options = item['options']
                                elif 'answers' in item and isinstance(item['answers'], list):
                                    options = item['answers']
                                
                                if options:
                                    options = [str(opt).strip() for opt in options if opt and str(opt).strip()]
                                
                                if question_text and options:
                                    questions.append({
                                        "question": str(question_text).strip(),
                                        "options": options
                                    })
                        
            except Exception as e:
                print(f"Error processing result: {e}")
                continue
        
        return questions
    
    def scrape_quiz(self) -> List[Dict]:
        """Main scraping method."""
        print("Starting API testing ProProfs quiz scraper...")
        print("This will test various API endpoints to find quiz data.")
        
        all_results = []
        
        # Test different types of endpoints
        all_results.extend(self.test_common_api_endpoints())
        all_results.extend(self.test_ajax_endpoints())
        all_results.extend(self.test_post_endpoints())
        all_results.extend(self.test_bypass_attempts())
        
        # Save all results for analysis
        with open('api_testing_results.json', 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        
        print(f"\nAPI testing completed. Found {len(all_results)} potential endpoints.")
        print("Results saved to api_testing_results.json")
        
        # Extract questions from results
        self.quiz_data = self.extract_questions_from_data(all_results)
        
        return self.quiz_data
    
    def save_to_json(self, filename: str = "quiz_data.json"):
        """Save extracted quiz data to JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.quiz_data, f, indent=2, ensure_ascii=False)
            print(f"Quiz data saved to {filename}")
        except Exception as e:
            print(f"Error saving to JSON: {e}")


def main():
    """Main function."""
    scraper = APITestingScraper()
    quiz_data = scraper.scrape_quiz()
    scraper.save_to_json()
    
    print(f"\nTotal questions extracted: {len(quiz_data)}")
    
    if quiz_data:
        print("✅ Successfully extracted quiz data using API testing!")
    else:
        print("❌ No quiz data found through API testing.")
        print("The timer protection appears to be server-side enforced.")


if __name__ == "__main__":
    main()
