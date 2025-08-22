#!/usr/bin/env python3
"""
JMeter Test Plan Generator for ProProfs Quiz API Testing

This script generates JMeter test plans to systematically test API endpoints
and potentially discover vulnerabilities in the timer protection system.
"""

import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import List, Dict


class JMeterTestPlanGenerator:
    """Generator for JMeter test plans to test ProProfs API endpoints."""
    
    def __init__(self):
        self.base_url = "https://www.proprofs.com"
        self.quiz_url = "https://www.proprofs.com/quiz-school/ugc/story.php?title=sfia-service-operations-practitioner0h&token=Z3FlYmVyaGFkZW1hbmRAY2FwYWNpdGkub3JnLnza"
        
    def extract_url_parameters(self) -> Dict[str, str]:
        """Extract parameters from the quiz URL."""
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(self.quiz_url)
        params = parse_qs(parsed.query)
        return {k: v[0] for k, v in params.items()}
    
    def generate_api_endpoints(self) -> List[str]:
        """Generate a comprehensive list of API endpoints to test."""
        url_params = self.extract_url_parameters()
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
            endpoints.append(f"{self.base_url}{pattern}")
        
        return endpoints
    
    def generate_bypass_endpoints(self) -> List[str]:
        """Generate endpoints with bypass attempts."""
        url_params = self.extract_url_parameters()
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
            bypass_endpoints.append(f"{self.base_url}{pattern}")
        
        return bypass_endpoints
    
    def create_http_request_element(self, url: str, method: str = "GET", headers: Dict = None) -> ET.Element:
        """Create an HTTP Request element for JMeter."""
        http_request = ET.Element("HTTPSamplerProxy")
        http_request.set("guiclass", "HttpTestSampleGui")
        http_request.set("testclass", "HTTPSamplerProxy")
        http_request.set("testname", f"HTTP Request - {url.split('/')[-1]}")
        http_request.set("enabled", "true")
        
        # Set the URL
        string_prop = ET.SubElement(http_request, "stringProp")
        string_prop.set("name", "HTTPSampler.domain")
        string_prop.text = urlparse(url).netloc
        
        string_prop = ET.SubElement(http_request, "stringProp")
        string_prop.set("name", "HTTPSampler.protocol")
        string_prop.text = "https"
        
        string_prop = ET.SubElement(http_request, "stringProp")
        string_prop.set("name", "HTTPSampler.path")
        path = urlparse(url).path
        query = urlparse(url).query
        string_prop.text = path + ("?" + query if query else "")
        
        string_prop = ET.SubElement(http_request, "stringProp")
        string_prop.set("name", "HTTPSampler.method")
        string_prop.text = method
        
        # Add headers
        if headers:
            header_manager = ET.SubElement(http_request, "HeaderManager")
            header_manager.set("guiclass", "HeaderPanel")
            header_manager.set("testclass", "HeaderManager")
            header_manager.set("testname", "HTTP Header Manager")
            header_manager.set("enabled", "true")
            
            collection_prop = ET.SubElement(header_manager, "collectionProp")
            collection_prop.set("name", "HeaderManager.headers")
            
            for key, value in headers.items():
                element_prop = ET.SubElement(collection_prop, "elementProp")
                element_prop.set("name", "")
                element_prop.set("elementType", "Header")
                
                string_prop = ET.SubElement(element_prop, "stringProp")
                string_prop.set("name", "Header.name")
                string_prop.text = key
                
                string_prop = ET.SubElement(element_prop, "stringProp")
                string_prop.set("name", "Header.value")
                string_prop.text = value
        
        return http_request
    
    def create_thread_group(self, name: str, requests: List[ET.Element]) -> ET.Element:
        """Create a Thread Group element for JMeter."""
        thread_group = ET.Element("ThreadGroup")
        thread_group.set("guiclass", "ThreadGroupGui")
        thread_group.set("testclass", "ThreadGroup")
        thread_group.set("testname", name)
        thread_group.set("enabled", "true")
        
        # Thread group properties
        string_prop = ET.SubElement(thread_group, "stringProp")
        string_prop.set("name", "ThreadGroup.on_sample_error")
        string_prop.text = "continue"
        
        element_prop = ET.SubElement(thread_group, "elementProp")
        element_prop.set("name", "ThreadGroup.main_controller")
        element_prop.set("elementType", "LoopController")
        element_prop.set("guiclass", "LoopControlPanel")
        element_prop.set("testclass", "LoopController")
        element_prop.set("testname", "Loop Controller")
        element_prop.set("enabled", "true")
        
        bool_prop = ET.SubElement(element_prop, "boolProp")
        bool_prop.set("name", "LoopController.continue_forever")
        bool_prop.text = "false"
        
        string_prop = ET.SubElement(element_prop, "stringProp")
        string_prop.set("name", "LoopController.loops")
        string_prop.text = "1"
        
        # Add requests to thread group
        for request in requests:
            thread_group.append(request)
        
        return thread_group
    
    def create_test_plan(self, name: str = "ProProfs API Test Plan") -> ET.Element:
        """Create the main test plan element."""
        test_plan = ET.Element("TestPlan")
        test_plan.set("guiclass", "TestPlanGui")
        test_plan.set("testclass", "TestPlan")
        test_plan.set("testname", name)
        test_plan.set("enabled", "true")
        
        bool_prop = ET.SubElement(test_plan, "boolProp")
        bool_prop.set("name", "TestPlan.functional_mode")
        bool_prop.text = "false"
        
        bool_prop = ET.SubElement(test_plan, "boolProp")
        bool_prop.set("name", "TestPlan.tearDown_on_shutdown")
        bool_prop.text = "true"
        
        bool_prop = ET.SubElement(test_plan, "boolProp")
        bool_prop.set("name", "TestPlan.serialize_threadgroups")
        bool_prop.text = "false"
        
        return test_plan
    
    def create_hash_tree(self, parent: ET.Element, children: List[ET.Element]) -> ET.Element:
        """Create a hash tree element for JMeter."""
        hash_tree = ET.SubElement(parent, "hashTree")
        for child in children:
            hash_tree.append(child)
        return hash_tree
    
    def generate_jmeter_test_plan(self, filename: str = "proprofs_api_test_plan.jmx"):
        """Generate a complete JMeter test plan."""
        print("Generating JMeter test plan...")
        
        # Create test plan
        test_plan = self.create_test_plan()
        
        # Generate endpoints
        api_endpoints = self.generate_api_endpoints()
        bypass_endpoints = self.generate_bypass_endpoints()
        
        print(f"Generated {len(api_endpoints)} API endpoints")
        print(f"Generated {len(bypass_endpoints)} bypass endpoints")
        
        # Create HTTP requests for API endpoints
        api_requests = []
        for endpoint in api_endpoints:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': self.quiz_url
            }
            request = self.create_http_request_element(endpoint, "GET", headers)
            api_requests.append(request)
        
        # Create HTTP requests for bypass endpoints
        bypass_requests = []
        for endpoint in bypass_endpoints:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': self.quiz_url,
                'X-Admin': 'true',
                'X-Bypass': 'true',
                'Authorization': 'Bearer admin'
            }
            request = self.create_http_request_element(endpoint, "GET", headers)
            bypass_requests.append(request)
        
        # Create thread groups
        api_thread_group = self.create_thread_group("API Endpoints Test", api_requests)
        bypass_thread_group = self.create_thread_group("Bypass Endpoints Test", bypass_requests)
        
        # Add thread groups to test plan
        test_plan.append(api_thread_group)
        test_plan.append(bypass_thread_group)
        
        # Create the complete JMeter structure
        jmeter_test_plan = ET.Element("jmeterTestPlan")
        jmeter_test_plan.set("version", "1.2")
        jmeter_test_plan.set("properties", "5.0")
        jmeter_test_plan.set("jmeter", "5.6.2")
        
        hash_tree = ET.SubElement(jmeter_test_plan, "hashTree")
        hash_tree.append(test_plan)
        
        # Add hash tree for test plan
        test_plan_hash_tree = ET.SubElement(hash_tree, "hashTree")
        test_plan_hash_tree.append(api_thread_group)
        test_plan_hash_tree.append(bypass_thread_group)
        
        # Add hash trees for thread groups
        api_hash_tree = ET.SubElement(test_plan_hash_tree, "hashTree")
        for request in api_requests:
            api_hash_tree.append(request)
            api_hash_tree.append(ET.Element("hashTree"))
        
        bypass_hash_tree = ET.SubElement(test_plan_hash_tree, "hashTree")
        for request in bypass_requests:
            bypass_hash_tree.append(request)
            bypass_hash_tree.append(ET.Element("hashTree"))
        
        # Write to file
        xml_str = minidom.parseString(ET.tostring(jmeter_test_plan)).toprettyxml(indent="  ")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(xml_str)
        
        print(f"JMeter test plan saved to {filename}")
        
        # Also save endpoint lists for manual testing
        with open('api_endpoints.txt', 'w') as f:
            for endpoint in api_endpoints:
                f.write(f"{endpoint}\n")
        
        with open('bypass_endpoints.txt', 'w') as f:
            for endpoint in bypass_endpoints:
                f.write(f"{endpoint}\n")
        
        print("Endpoint lists saved to api_endpoints.txt and bypass_endpoints.txt")
        
        return filename
    
    def generate_postman_collection(self, filename: str = "proprofs_api_collection.json"):
        """Generate a Postman collection for API testing."""
        print("Generating Postman collection...")
        
        collection = {
            "info": {
                "name": "ProProfs API Testing",
                "description": "Collection for testing ProProfs quiz API endpoints",
                "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
            },
            "item": []
        }
        
        # Add API endpoints
        api_endpoints = self.generate_api_endpoints()
        for i, endpoint in enumerate(api_endpoints):
            request = {
                "name": f"API Test {i+1} - {endpoint.split('/')[-1]}",
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
                            "key": "Referer",
                            "value": self.quiz_url
                        }
                    ],
                    "url": {
                        "raw": endpoint,
                        "protocol": "https",
                        "host": ["www", "proprofs", "com"],
                        "path": endpoint.split("https://www.proprofs.com")[1].split("?")[0].split("/")[1:],
                        "query": []
                    }
                }
            }
            
            # Add query parameters if any
            if "?" in endpoint:
                query_part = endpoint.split("?")[1]
                for param in query_part.split("&"):
                    if "=" in param:
                        key, value = param.split("=", 1)
                        request["request"]["url"]["query"].append({
                            "key": key,
                            "value": value
                        })
            
            collection["item"].append(request)
        
        # Add bypass endpoints
        bypass_endpoints = self.generate_bypass_endpoints()
        for i, endpoint in enumerate(bypass_endpoints):
            request = {
                "name": f"Bypass Test {i+1} - {endpoint.split('/')[-1]}",
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
                            "key": "Referer",
                            "value": self.quiz_url
                        },
                        {
                            "key": "X-Admin",
                            "value": "true"
                        },
                        {
                            "key": "X-Bypass",
                            "value": "true"
                        },
                        {
                            "key": "Authorization",
                            "value": "Bearer admin"
                        }
                    ],
                    "url": {
                        "raw": endpoint,
                        "protocol": "https",
                        "host": ["www", "proprofs", "com"],
                        "path": endpoint.split("https://www.proprofs.com")[1].split("?")[0].split("/")[1:],
                        "query": []
                    }
                }
            }
            
            # Add query parameters if any
            if "?" in endpoint:
                query_part = endpoint.split("?")[1]
                for param in query_part.split("&"):
                    if "=" in param:
                        key, value = param.split("=", 1)
                        request["request"]["url"]["query"].append({
                            "key": key,
                            "value": value
                        })
            
            collection["item"].append(request)
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(collection, f, indent=2)
        
        print(f"Postman collection saved to {filename}")
        return filename


def main():
    """Main function."""
    print("ProProfs API Testing Tools Generator")
    print("====================================")
    
    generator = JMeterTestPlanGenerator()
    
    # Generate JMeter test plan
    jmeter_file = generator.generate_jmeter_test_plan()
    
    # Generate Postman collection
    postman_file = generator.generate_postman_collection()
    
    print("\n" + "="*50)
    print("GENERATION COMPLETE")
    print("="*50)
    print(f"JMeter Test Plan: {jmeter_file}")
    print(f"Postman Collection: {postman_file}")
    print("Endpoint Lists: api_endpoints.txt, bypass_endpoints.txt")
    print("\nUSAGE INSTRUCTIONS:")
    print("1. JMeter: Open the .jmx file in JMeter and run the test plan")
    print("2. Postman: Import the .json file and run the collection")
    print("3. Manual: Use the endpoint lists for curl or other HTTP clients")
    print("\nThis will systematically test all possible API endpoints")
    print("and bypass attempts to find vulnerabilities in the timer protection.")


if __name__ == "__main__":
    main()
