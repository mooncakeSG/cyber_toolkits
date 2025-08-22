#!/usr/bin/env python3
"""
Simple API Testing Tools Generator

This script generates endpoint lists and curl commands for testing
ProProfs API endpoints with Postman, JMeter, or other tools.
"""

import json
from urllib.parse import urlparse, parse_qs


def extract_url_parameters(quiz_url):
    """Extract parameters from the quiz URL."""
    parsed = urlparse(quiz_url)
    params = parse_qs(parsed.query)
    return {k: v[0] for k, v in params.items()}


def generate_endpoints():
    """Generate comprehensive list of API endpoints to test."""
    base_url = "https://www.proprofs.com"
    quiz_url = "https://www.proprofs.com/quiz-school/ugc/story.php?title=sfia-service-operations-practitioner0h&token=Z3FlYmVyaGFkZW1hbmRAY2FwYWNpdGkub3JnLnza"
    
    url_params = extract_url_parameters(quiz_url)
    title = url_params.get('title', '')
    token = url_params.get('token', '')
    
    endpoints = []
    
    # Common API patterns
    api_patterns = [
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
    
    for pattern in api_patterns:
        endpoints.append(f"{base_url}{pattern}")
    
    return endpoints


def generate_bypass_endpoints():
    """Generate endpoints with bypass attempts."""
    base_url = "https://www.proprofs.com"
    quiz_url = "https://www.proprofs.com/quiz-school/ugc/story.php?title=sfia-service-operations-practitioner0h&token=Z3FlYmVyaGFkZW1hbmRAY2FwYWNpdGkub3JnLnza"
    
    url_params = extract_url_parameters(quiz_url)
    title = url_params.get('title', '')
    
    bypass_endpoints = []
    
    # Bypass patterns
    bypass_patterns = [
        # Time-related bypasses
        f"/quiz-school/api/quiz/{title}?time=expired",
        f"/quiz-school/api/quiz/{title}?timer=0",
        f"/quiz-school/api/quiz/{title}?countdown=complete",
        f"/quiz-school/api/quiz/{title}?time_bypass=true",
        
        # Admin bypasses
        f"/quiz-school/api/quiz/{title}?admin=true",
        f"/quiz-school/api/quiz/{title}?bypass=true",
        f"/quiz-school/api/quiz/{title}?debug=true",
        f"/quiz-school/api/quiz/{title}?superuser=true",
        
        # Role bypasses
        f"/quiz-school/api/quiz/{title}?role=admin",
        f"/quiz-school/api/quiz/{title}?user_type=admin",
        f"/quiz-school/api/quiz/{title}?access_level=admin",
        
        # Session bypasses
        f"/quiz-school/api/quiz/{title}?session=admin",
        f"/quiz-school/api/quiz/{title}?auth=admin",
        f"/quiz-school/api/quiz/{title}?token=admin",
    ]
    
    for pattern in bypass_patterns:
        bypass_endpoints.append(f"{base_url}{pattern}")
    
    return bypass_endpoints


def generate_curl_commands(endpoints, filename):
    """Generate curl commands for testing endpoints."""
    quiz_url = "https://www.proprofs.com/quiz-school/ugc/story.php?title=sfia-service-operations-practitioner0h&token=Z3FlYmVyaGFkZW1hbmRAY2FwYWNpdGkub3JnLnza"
    
    with open(filename, 'w') as f:
        f.write("# Curl Commands for ProProfs API Testing\n")
        f.write("# Generated for testing timer bypass attempts\n\n")
        
        for i, endpoint in enumerate(endpoints, 1):
            f.write(f"# Test {i}: {endpoint}\n")
            f.write(f'curl -X GET "{endpoint}" \\\n')
            f.write('  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \\\n')
            f.write('  -H "Accept: application/json, text/plain, */*" \\\n')
            f.write('  -H "Accept-Language: en-US,en;q=0.9" \\\n')
            f.write(f'  -H "Referer: {quiz_url}" \\\n')
            f.write('  -H "Connection: keep-alive" \\\n')
            f.write('  -H "Upgrade-Insecure-Requests: 1" \\\n')
            f.write('  --compressed \\\n')
            f.write('  --silent \\\n')
            f.write('  --show-error \\\n')
            f.write('  --max-time 10\n\n')


def generate_postman_collection(endpoints, filename):
    """Generate a Postman collection JSON file."""
    quiz_url = "https://www.proprofs.com/quiz-school/ugc/story.php?title=sfia-service-operations-practitioner0h&token=Z3FlYmVyaGFkZW1hbmRAY2FwYWNpdGkub3JnLnza"
    
    collection = {
        "info": {
            "name": "ProProfs API Testing",
            "description": "Collection for testing ProProfs quiz API endpoints and bypass attempts",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": []
    }
    
    for i, endpoint in enumerate(endpoints, 1):
        # Parse the endpoint to extract path and query parameters
        parsed = urlparse(endpoint)
        path_parts = [part for part in parsed.path.split('/') if part]
        
        request = {
            "name": f"Test {i} - {path_parts[-1] if path_parts else 'root'}",
            "request": {
                "method": "GET",
                "header": [
                    {
                        "key": "User-Agent",
                        "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    },
                    {
                        "key": "Accept",
                        "value": "application/json, text/plain, */*"
                    },
                    {
                        "key": "Accept-Language",
                        "value": "en-US,en;q=0.9"
                    },
                    {
                        "key": "Referer",
                        "value": quiz_url
                    },
                    {
                        "key": "Connection",
                        "value": "keep-alive"
                    },
                    {
                        "key": "Upgrade-Insecure-Requests",
                        "value": "1"
                    }
                ],
                "url": {
                    "raw": endpoint,
                    "protocol": "https",
                    "host": ["www", "proprofs", "com"],
                    "path": path_parts,
                    "query": []
                }
            }
        }
        
        # Add query parameters if any
        if parsed.query:
            for param in parsed.query.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    request["request"]["url"]["query"].append({
                        "key": key,
                        "value": value
                    })
        
        collection["item"].append(request)
    
    # Write to file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(collection, f, indent=2)
    
    return filename


def generate_jmeter_csv(endpoints, filename):
    """Generate a CSV file for JMeter import."""
    quiz_url = "https://www.proprofs.com/quiz-school/ugc/story.php?title=sfia-service-operations-practitioner0h&token=Z3FlYmVyaGFkZW1hbmRAY2FwYWNpdGkub3JnLnza"
    
    with open(filename, 'w') as f:
        # CSV header
        f.write("URL,Method,Headers,ExpectedStatus\n")
        
        for endpoint in endpoints:
            headers = f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36; Accept: application/json, text/plain, */*; Accept-Language: en-US,en;q=0.9; Referer: {quiz_url}; Connection: keep-alive; Upgrade-Insecure-Requests: 1"
            f.write(f'"{endpoint}",GET,"{headers}",200\n')


def main():
    """Main function."""
    print("ProProfs API Testing Tools Generator")
    print("====================================")
    
    # Generate endpoints
    api_endpoints = generate_endpoints()
    bypass_endpoints = generate_bypass_endpoints()
    all_endpoints = api_endpoints + bypass_endpoints
    
    print(f"Generated {len(api_endpoints)} API endpoints")
    print(f"Generated {len(bypass_endpoints)} bypass endpoints")
    print(f"Total: {len(all_endpoints)} endpoints to test")
    
    # Generate tools
    print("\nGenerating testing tools...")
    
    # 1. Endpoint lists
    with open('api_endpoints.txt', 'w') as f:
        for endpoint in api_endpoints:
            f.write(f"{endpoint}\n")
    
    with open('bypass_endpoints.txt', 'w') as f:
        for endpoint in bypass_endpoints:
            f.write(f"{endpoint}\n")
    
    with open('all_endpoints.txt', 'w') as f:
        for endpoint in all_endpoints:
            f.write(f"{endpoint}\n")
    
    # 2. Curl commands
    generate_curl_commands(all_endpoints, 'curl_commands.sh')
    
    # 3. Postman collection
    postman_file = generate_postman_collection(all_endpoints, 'proprofs_api_collection.json')
    
    # 4. JMeter CSV
    generate_jmeter_csv(all_endpoints, 'jmeter_endpoints.csv')
    
    # 5. Summary report
    with open('testing_summary.md', 'w') as f:
        f.write("# ProProfs API Testing Summary\n\n")
        f.write("## Generated Files\n\n")
        f.write("- `api_endpoints.txt` - Standard API endpoints to test\n")
        f.write("- `bypass_endpoints.txt` - Bypass attempt endpoints\n")
        f.write("- `all_endpoints.txt` - All endpoints combined\n")
        f.write("- `curl_commands.sh` - Curl commands for testing\n")
        f.write("- `proprofs_api_collection.json` - Postman collection\n")
        f.write("- `jmeter_endpoints.csv` - CSV for JMeter import\n\n")
        f.write("## Usage Instructions\n\n")
        f.write("### Postman\n")
        f.write("1. Open Postman\n")
        f.write("2. Import the `proprofs_api_collection.json` file\n")
        f.write("3. Run the collection to test all endpoints\n\n")
        f.write("### JMeter\n")
        f.write("1. Open JMeter\n")
        f.write("2. Create a CSV Data Set Config\n")
        f.write("3. Point it to `jmeter_endpoints.csv`\n")
        f.write("4. Create HTTP Request sampler using CSV variables\n\n")
        f.write("### Curl\n")
        f.write("1. Make the script executable: `chmod +x curl_commands.sh`\n")
        f.write("2. Run: `./curl_commands.sh`\n\n")
        f.write("### Manual Testing\n")
        f.write("Use the endpoint lists in any HTTP client\n\n")
        f.write(f"## Endpoint Summary\n\n")
        f.write(f"- API Endpoints: {len(api_endpoints)}\n")
        f.write(f"- Bypass Endpoints: {len(bypass_endpoints)}\n")
        f.write(f"- Total Endpoints: {len(all_endpoints)}\n")
    
    print("\n" + "="*50)
    print("GENERATION COMPLETE")
    print("="*50)
    print("Generated files:")
    print("✅ api_endpoints.txt")
    print("✅ bypass_endpoints.txt") 
    print("✅ all_endpoints.txt")
    print("✅ curl_commands.sh")
    print("✅ proprofs_api_collection.json")
    print("✅ jmeter_endpoints.csv")
    print("✅ testing_summary.md")
    print("\nUSAGE:")
    print("1. Postman: Import proprofs_api_collection.json")
    print("2. JMeter: Use jmeter_endpoints.csv with CSV Data Set Config")
    print("3. Curl: Run curl_commands.sh")
    print("4. Manual: Use endpoint lists in any HTTP client")
    print("\nThis will systematically test all possible API endpoints")
    print("and bypass attempts to find vulnerabilities in the timer protection.")


if __name__ == "__main__":
    main()
