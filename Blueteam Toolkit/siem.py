"""
SIEM API Integration Module for the Blue Team CLI Toolkit.
Provides connectors for major SIEM platforms (ELK, Wazuh, Splunk).
"""

import os
import sys
import platform
import subprocess
import json
import requests
import base64
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import utils


class SIEMConnector:
    """Base class for SIEM connectors."""
    
    def __init__(self, host: str, port: int = None, username: str = None, password: str = None, api_key: str = None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.api_key = api_key
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL warnings for internal SIEMs
        
    def test_connection(self) -> bool:
        """Test connection to SIEM."""
        raise NotImplementedError
        
    def search_alerts(self, query: str = None, time_range: str = "24h") -> List[Dict]:
        """Search for alerts."""
        raise NotImplementedError
        
    def get_alerts(self, limit: int = 100) -> List[Dict]:
        """Get recent alerts."""
        raise NotImplementedError
        
    def run_query(self, query: str, time_range: str = "24h") -> List[Dict]:
        """Run a custom query."""
        raise NotImplementedError


class ELKConnector(SIEMConnector):
    """Elasticsearch/Logstash/Kibana (ELK) connector."""
    
    def __init__(self, host: str, port: int = 9200, username: str = None, password: str = None, api_key: str = None):
        super().__init__(host, port, username, password, api_key)
        self.base_url = f"https://{host}:{port}"
        
        # Setup authentication
        if api_key:
            self.session.headers.update({'Authorization': f'ApiKey {api_key}'})
        elif username and password:
            self.session.auth = (username, password)
    
    def test_connection(self) -> bool:
        """Test connection to Elasticsearch."""
        try:
            response = self.session.get(f"{self.base_url}/_cluster/health", timeout=10)
            return response.status_code == 200
        except Exception as e:
            utils.print_error(f"Failed to connect to ELK: {e}")
            return False
    
    def search_alerts(self, query: str = None, time_range: str = "24h") -> List[Dict]:
        """Search for alerts in Elasticsearch."""
        try:
            # Calculate time range
            end_time = datetime.now()
            if time_range.endswith('h'):
                hours = int(time_range[:-1])
                start_time = end_time - timedelta(hours=hours)
            elif time_range.endswith('d'):
                days = int(time_range[:-1])
                start_time = end_time - timedelta(days=days)
            else:
                start_time = end_time - timedelta(hours=24)
            
            # Build search query
            search_body = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "range": {
                                    "@timestamp": {
                                        "gte": start_time.isoformat(),
                                        "lte": end_time.isoformat()
                                    }
                                }
                            }
                        ]
                    }
                },
                "sort": [{"@timestamp": {"order": "desc"}}],
                "size": 100
            }
            
            if query:
                search_body["query"]["bool"]["must"].append({
                    "query_string": {"query": query}
                })
            
            # Search in common alert indices
            indices = ["alerts-*", "security-*", "audit-*", "logs-*"]
            alerts = []
            
            for index in indices:
                try:
                    response = self.session.post(
                        f"{self.base_url}/{index}/_search",
                        json=search_body,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        for hit in data.get('hits', {}).get('hits', []):
                            alert = hit['_source']
                            alert['_index'] = hit['_index']
                            alert['_id'] = hit['_id']
                            alerts.append(alert)
                except Exception as e:
                    utils.print_warning(f"Failed to search index {index}: {e}")
                    continue
            
            return alerts
            
        except Exception as e:
            utils.print_error(f"Failed to search ELK alerts: {e}")
            return []
    
    def get_alerts(self, limit: int = 100) -> List[Dict]:
        """Get recent alerts from ELK."""
        return self.search_alerts(limit=limit)
    
    def run_query(self, query: str, time_range: str = "24h") -> List[Dict]:
        """Run a custom Elasticsearch query."""
        try:
            # Calculate time range
            end_time = datetime.now()
            if time_range.endswith('h'):
                hours = int(time_range[:-1])
                start_time = end_time - timedelta(hours=hours)
            elif time_range.endswith('d'):
                days = int(time_range[:-1])
                start_time = end_time - timedelta(days=days)
            else:
                start_time = end_time - timedelta(hours=24)
            
            search_body = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "range": {
                                    "@timestamp": {
                                        "gte": start_time.isoformat(),
                                        "lte": end_time.isoformat()
                                    }
                                }
                            },
                            {
                                "query_string": {"query": query}
                            }
                        ]
                    }
                },
                "sort": [{"@timestamp": {"order": "desc"}}],
                "size": 100
            }
            
            # Search in all indices
            response = self.session.post(
                f"{self.base_url}/_all/_search",
                json=search_body,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                results = []
                for hit in data.get('hits', {}).get('hits', []):
                    result = hit['_source']
                    result['_index'] = hit['_index']
                    result['_id'] = hit['_id']
                    results.append(result)
                return results
            else:
                utils.print_error(f"Query failed with status {response.status_code}")
                return []
                
        except Exception as e:
            utils.print_error(f"Failed to run ELK query: {e}")
            return []


class WazuhConnector(SIEMConnector):
    """Wazuh SIEM connector."""
    
    def __init__(self, host: str, port: int = 55000, username: str = None, password: str = None, api_key: str = None):
        super().__init__(host, port, username, password, api_key)
        self.base_url = f"https://{host}:{port}"
        
        # Setup authentication
        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})
        elif username and password:
            # Wazuh uses basic auth
            auth_string = f"{username}:{password}"
            auth_bytes = auth_string.encode('ascii')
            auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
            self.session.headers.update({'Authorization': f'Basic {auth_b64}'})
    
    def test_connection(self) -> bool:
        """Test connection to Wazuh."""
        try:
            response = self.session.get(f"{self.base_url}/", timeout=10)
            return response.status_code == 200
        except Exception as e:
            utils.print_error(f"Failed to connect to Wazuh: {e}")
            return False
    
    def search_alerts(self, query: str = None, time_range: str = "24h") -> List[Dict]:
        """Search for alerts in Wazuh."""
        try:
            # Calculate time range
            end_time = datetime.now()
            if time_range.endswith('h'):
                hours = int(time_range[:-1])
                start_time = end_time - timedelta(hours=hours)
            elif time_range.endswith('d'):
                days = int(time_range[:-1])
                start_time = end_time - timedelta(days=days)
            else:
                start_time = end_time - timedelta(hours=24)
            
            # Build search parameters
            params = {
                'limit': 100,
                'offset': 0,
                'sort': '-timestamp'
            }
            
            if query:
                params['q'] = query
            
            # Search for alerts
            response = self.session.get(
                f"{self.base_url}/alerts",
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('data', {}).get('affected_items', [])
            else:
                utils.print_error(f"Failed to get Wazuh alerts: {response.status_code}")
                return []
                
        except Exception as e:
            utils.print_error(f"Failed to search Wazuh alerts: {e}")
            return []
    
    def get_alerts(self, limit: int = 100) -> List[Dict]:
        """Get recent alerts from Wazuh."""
        return self.search_alerts(limit=limit)
    
    def run_query(self, query: str, time_range: str = "24h") -> List[Dict]:
        """Run a custom Wazuh query."""
        return self.search_alerts(query=query, time_range=time_range)


class SplunkConnector(SIEMConnector):
    """Splunk SIEM connector."""
    
    def __init__(self, host: str, port: int = 8089, username: str = None, password: str = None, api_key: str = None):
        super().__init__(host, port, username, password, api_key)
        self.base_url = f"https://{host}:{port}"
        
        # Setup authentication
        if api_key:
            self.session.headers.update({'Authorization': f'Splunk {api_key}'})
        elif username and password:
            self.session.auth = (username, password)
    
    def test_connection(self) -> bool:
        """Test connection to Splunk."""
        try:
            response = self.session.get(f"{self.base_url}/services/server/info", timeout=10)
            return response.status_code == 200
        except Exception as e:
            utils.print_error(f"Failed to connect to Splunk: {e}")
            return False
    
    def search_alerts(self, query: str = None, time_range: str = "24h") -> List[Dict]:
        """Search for alerts in Splunk."""
        try:
            # Build search query
            if query:
                search_query = f"search {query}"
            else:
                search_query = "search index=* sourcetype=*"
            
            # Add time range
            search_query += f" earliest=-{time_range} latest=now"
            
            # Execute search
            search_body = {
                'search': search_query,
                'output_mode': 'json',
                'count': 100
            }
            
            response = self.session.post(
                f"{self.base_url}/services/search/jobs/export",
                data=search_body,
                timeout=30
            )
            
            if response.status_code == 200:
                # Parse JSON lines response
                results = []
                for line in response.text.strip().split('\n'):
                    if line:
                        try:
                            result = json.loads(line)
                            results.append(result)
                        except json.JSONDecodeError:
                            continue
                return results
            else:
                utils.print_error(f"Failed to search Splunk: {response.status_code}")
                return []
                
        except Exception as e:
            utils.print_error(f"Failed to search Splunk alerts: {e}")
            return []
    
    def get_alerts(self, limit: int = 100) -> List[Dict]:
        """Get recent alerts from Splunk."""
        return self.search_alerts(limit=limit)
    
    def run_query(self, query: str, time_range: str = "24h") -> List[Dict]:
        """Run a custom Splunk query."""
        return self.search_alerts(query=query, time_range=time_range)


def create_siem_connector(siem_type: str, host: str, port: int = None, username: str = None, password: str = None, api_key: str = None) -> SIEMConnector:
    """Create a SIEM connector based on type."""
    siem_type = siem_type.lower()
    
    if siem_type in ['elk', 'elasticsearch', 'elastic']:
        return ELKConnector(host, port or 9200, username, password, api_key)
    elif siem_type in ['wazuh']:
        return WazuhConnector(host, port or 55000, username, password, api_key)
    elif siem_type in ['splunk']:
        return SplunkConnector(host, port or 8089, username, password, api_key)
    else:
        raise ValueError(f"Unsupported SIEM type: {siem_type}")


def display_siem_results(results: List[Dict], siem_type: str, query_type: str):
    """Display SIEM query results."""
    if not results:
        utils.print_info(f"No {query_type} found in {siem_type}")
        return
    
    utils.print_section(f"{siem_type.upper()} {query_type.title()}: {len(results)} results")
    
    for i, result in enumerate(results[:10], 1):  # Show first 10 results
        utils.print_warning(f"Result {i}:")
        
        # Display common fields
        if 'timestamp' in result:
            utils.print_info(f"  Timestamp: {result['timestamp']}")
        elif '@timestamp' in result:
            utils.print_info(f"  Timestamp: {result['@timestamp']}")
        
        if 'message' in result:
            utils.print_info(f"  Message: {result['message'][:100]}...")
        elif 'description' in result:
            utils.print_info(f"  Description: {result['description'][:100]}...")
        
        if 'level' in result:
            utils.print_info(f"  Level: {result['level']}")
        elif 'severity' in result:
            utils.print_info(f"  Severity: {result['severity']}")
        
        if 'source' in result:
            utils.print_info(f"  Source: {result['source']}")
        elif 'host' in result:
            utils.print_info(f"  Host: {result['host']}")
        
        print()
    
    if len(results) > 10:
        utils.print_info(f"... and {len(results) - 10} more results")


def main(args):
    """Main function for SIEM integration module."""
    utils.print_banner()
    utils.print_section("SIEM API Integration")
    
    try:
        # Create SIEM connector
        siem = create_siem_connector(
            args.type,
            args.host,
            args.port,
            args.username,
            args.password,
            args.api_key
        )
        
        # Test connection
        utils.print_info(f"Testing connection to {args.type.upper()} at {args.host}:{args.port}")
        if not siem.test_connection():
            utils.print_error(f"Failed to connect to {args.type.upper()}")
            return
        
        utils.print_success(f"Successfully connected to {args.type.upper()}")
        
        results = []
        
        # Execute based on command type
        if args.alerts:
            utils.print_info("Fetching recent alerts...")
            results = siem.get_alerts(args.limit)
            display_siem_results(results, args.type, "alerts")
            
        elif args.search:
            utils.print_info(f"Searching for: {args.search}")
            results = siem.search_alerts(args.search, args.time_range)
            display_siem_results(results, args.type, "search results")
            
        elif args.query:
            utils.print_info(f"Running query: {args.query}")
            results = siem.run_query(args.query, args.time_range)
            display_siem_results(results, args.type, "query results")
        
        # Export results if requested
        if results and hasattr(args, 'export') and args.export:
            export_format = getattr(args, 'export_format', 'json')
            compress = getattr(args, 'compress', False)
            
            export_data = {
                'siem_type': args.type,
                'host': args.host,
                'query_type': 'alerts' if args.alerts else 'search' if args.search else 'query',
                'query': args.search or args.query or 'recent_alerts',
                'time_range': args.time_range,
                'results_count': len(results),
                'results': results,
                'execution_timestamp': datetime.now().isoformat()
            }
            
            utils.export_report_with_metadata(
                export_data,
                'siem',
                export_format,
                args.export,
                compress
            )
        
        utils.print_success(f"SIEM {args.type.upper()} integration completed")
        
    except Exception as e:
        utils.print_error(f"SIEM integration failed: {e}")


if __name__ == "__main__":
    # For testing
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', choices=['elk', 'wazuh', 'splunk'], required=True)
    parser.add_argument('--host', required=True)
    parser.add_argument('--port', type=int)
    parser.add_argument('--username')
    parser.add_argument('--password')
    parser.add_argument('--api-key')
    parser.add_argument('--alerts', action='store_true')
    parser.add_argument('--search')
    parser.add_argument('--query')
    parser.add_argument('--limit', type=int, default=100)
    parser.add_argument('--time-range', default='24h')
    parser.add_argument('--export')
    parser.add_argument('--export-format', choices=['json', 'csv', 'txt'], default='json')
    parser.add_argument('--compress', action='store_true')
    args = parser.parse_args()
    main(args)
