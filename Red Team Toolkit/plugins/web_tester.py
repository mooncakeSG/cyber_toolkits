#!/usr/bin/env python3
"""
Web Tester Plugin for Enhanced Red Team Toolkit
Provides advanced web testing and reconnaissance capabilities.
"""

__version__ = "1.0.0"
__description__ = "Advanced web testing and reconnaissance plugin"
__author__ = "Red Team Toolkit"
__requires_sandbox__ = True
__category__ = "Web"

import requests
import re
import time
import logging
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def scan_web_vulnerabilities(url: str, timeout: int = 10) -> Dict[str, Any]:
    """
    Scan for common web vulnerabilities.
    
    Args:
        url: Target URL to scan
        timeout: Request timeout in seconds
    
    Returns:
        Dictionary with vulnerability scan results
    """
    logger.info(f"Starting web vulnerability scan on {url}")
    
    results = {
        'target': url,
        'scan_time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'vulnerabilities': [],
        'headers': {},
        'technologies': [],
        'errors': []
    }
    
    try:
        # Basic request to get headers and content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=timeout, verify=False)
        results['headers'] = dict(response.headers)
        
        # Check for security headers
        security_headers = {
            'X-Frame-Options': 'Missing X-Frame-Options (Clickjacking vulnerability)',
            'X-Content-Type-Options': 'Missing X-Content-Type-Options (MIME sniffing vulnerability)',
            'X-XSS-Protection': 'Missing X-XSS-Protection (XSS protection)',
            'Strict-Transport-Security': 'Missing HSTS (HTTPS enforcement)',
            'Content-Security-Policy': 'Missing CSP (Content Security Policy)'
        }
        
        for header, description in security_headers.items():
            if header not in response.headers:
                results['vulnerabilities'].append({
                    'type': 'Missing Security Header',
                    'severity': 'Medium',
                    'description': description,
                    'header': header
                })
        
        # Detect technologies
        server = response.headers.get('Server', '')
        if server:
            results['technologies'].append(f"Server: {server}")
        
        # Check for common vulnerabilities in response
        content = response.text.lower()
        
        # Check for error messages that might reveal information
        error_patterns = [
            'error in your sql syntax',
            'mysql_fetch_array()',
            'ora-',
            'microsoft ole db provider for sql server',
            'postgresql query failed',
            'sqlite3::',
            'warning: mysql_',
            'unclosed quotation mark after the character string',
            'quoted string not properly terminated'
        ]
        
        for pattern in error_patterns:
            if pattern in content:
                results['vulnerabilities'].append({
                    'type': 'SQL Error Information Disclosure',
                    'severity': 'High',
                    'description': f'SQL error message found: {pattern}',
                    'pattern': pattern
                })
        
        # Check for directory listing
        if 'index of /' in content and 'parent directory' in content:
            results['vulnerabilities'].append({
                'type': 'Directory Listing',
                'severity': 'Medium',
                'description': 'Directory listing is enabled',
                'details': 'Directory listing can expose sensitive files'
            })
        
        # Check for default pages
        default_pages = ['/admin', '/administrator', '/login', '/wp-admin', '/phpmyadmin']
        for page in default_pages:
            try:
                test_url = urljoin(url, page)
                test_response = requests.get(test_url, headers=headers, timeout=5, verify=False)
                if test_response.status_code == 200:
                    results['vulnerabilities'].append({
                        'type': 'Default Page Accessible',
                        'severity': 'Low',
                        'description': f'Default page accessible: {page}',
                        'url': test_url
                    })
            except:
                continue
        
        logger.info(f"Web vulnerability scan completed. Found {len(results['vulnerabilities'])} issues")
        
    except Exception as e:
        error_msg = f"Error during web vulnerability scan: {e}"
        results['errors'].append(error_msg)
        logger.error(error_msg)
    
    return results

def extract_emails_from_url(url: str, max_pages: int = 5) -> Dict[str, Any]:
    """
    Extract email addresses from a website.
    
    Args:
        url: Target URL
        max_pages: Maximum pages to crawl
    
    Returns:
        Dictionary with extracted emails
    """
    logger.info(f"Extracting emails from {url}")
    
    results = {
        'target': url,
        'scan_time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'emails': [],
        'pages_crawled': 0,
        'errors': []
    }
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Get main page
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract emails from main page
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        page_text = soup.get_text()
        emails = re.findall(email_pattern, page_text)
        results['emails'].extend(emails)
        results['pages_crawled'] += 1
        
        # Find and crawl internal links
        internal_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/') or href.startswith(url):
                full_url = urljoin(url, href)
                if full_url not in internal_links and results['pages_crawled'] < max_pages:
                    internal_links.append(full_url)
        
        # Crawl internal pages
        for link_url in internal_links[:max_pages - 1]:
            try:
                link_response = requests.get(link_url, headers=headers, timeout=5, verify=False)
                link_soup = BeautifulSoup(link_response.content, 'html.parser')
                link_text = link_soup.get_text()
                link_emails = re.findall(email_pattern, link_text)
                results['emails'].extend(link_emails)
                results['pages_crawled'] += 1
                time.sleep(1)  # Be respectful
            except Exception as e:
                results['errors'].append(f"Error crawling {link_url}: {e}")
        
        # Remove duplicates
        results['emails'] = list(set(results['emails']))
        
        logger.info(f"Email extraction completed. Found {len(results['emails'])} unique emails")
        
    except Exception as e:
        error_msg = f"Error during email extraction: {e}"
        results['errors'].append(error_msg)
        logger.error(error_msg)
    
    return results

def check_ssl_certificate(url: str) -> Dict[str, Any]:
    """
    Check SSL certificate information.
    
    Args:
        url: Target URL
    
    Returns:
        Dictionary with SSL certificate information
    """
    import ssl
    import socket
    from datetime import datetime
    
    logger.info(f"Checking SSL certificate for {url}")
    
    results = {
        'target': url,
        'scan_time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'ssl_enabled': False,
        'certificate_info': {},
        'vulnerabilities': [],
        'errors': []
    }
    
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        port = parsed_url.port or (443 if parsed_url.scheme == 'https' else 80)
        
        if parsed_url.scheme == 'https':
            results['ssl_enabled'] = True
            
            # Create SSL context
            context = ssl.create_default_context()
            
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Extract certificate information
                    results['certificate_info'] = {
                        'subject': dict(x[0] for x in cert['subject']),
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'version': cert['version'],
                        'serial_number': cert['serialNumber'],
                        'not_before': cert['notBefore'],
                        'not_after': cert['notAfter'],
                        'san': cert.get('subjectAltName', [])
                    }
                    
                    # Check for vulnerabilities
                    not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_until_expiry = (not_after - datetime.now()).days
                    
                    if days_until_expiry < 30:
                        results['vulnerabilities'].append({
                            'type': 'Certificate Expiry',
                            'severity': 'High',
                            'description': f'Certificate expires in {days_until_expiry} days',
                            'expiry_date': cert['notAfter']
                        })
                    
                    if days_until_expiry < 0:
                        results['vulnerabilities'].append({
                            'type': 'Certificate Expired',
                            'severity': 'Critical',
                            'description': 'Certificate has expired',
                            'expiry_date': cert['notAfter']
                        })
                    
                    # Check for weak algorithms
                    cipher = ssock.cipher()
                    if cipher and 'RC4' in cipher[0]:
                        results['vulnerabilities'].append({
                            'type': 'Weak Cipher',
                            'severity': 'Medium',
                            'description': f'Weak cipher detected: {cipher[0]}',
                            'cipher': cipher[0]
                        })
        
        logger.info(f"SSL certificate check completed for {url}")
        
    except Exception as e:
        error_msg = f"Error checking SSL certificate: {e}"
        results['errors'].append(error_msg)
        logger.error(error_msg)
    
    return results

def plugin_info() -> Dict[str, Any]:
    """
    Return plugin information and available functions.
    
    Returns:
        Dictionary with plugin metadata
    """
    return {
        'name': 'web_tester',
        'version': __version__,
        'description': __description__,
        'author': __author__,
        'category': __category__,
        'functions': [
            'scan_web_vulnerabilities',
            'extract_emails_from_url',
            'check_ssl_certificate',
            'plugin_info'
        ],
        'examples': {
            'scan_web_vulnerabilities': 'scan_web_vulnerabilities("https://example.com")',
            'extract_emails_from_url': 'extract_emails_from_url("https://example.com")',
            'check_ssl_certificate': 'check_ssl_certificate("https://example.com")'
        }
    }
