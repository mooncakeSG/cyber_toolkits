#!/usr/bin/env python3
"""
Enhanced Red Team Toolkit v2.0 - Demonstration Script
This script demonstrates the new features and improvements in the toolkit.
"""

import sys
import os
from pathlib import Path

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_configuration():
    """Demonstrate configuration management."""
    print("=" * 60)
    print("CONFIGURATION MANAGEMENT DEMO")
    print("=" * 60)
    
    from red_team_toolkit import config, colored, Colors
    
    print("✓ Configuration system loaded")
    print(f"Config file: {config.config_file}")
    
    # Show current configuration
    print("\nCurrent Configuration:")
    for section in config.config.sections():
        print(f"\n[{section}]")
        for option, value in config.config.items(section):
            print(f"  {option} = {value}")
    
    # Test configuration access
    max_threads = config.getint('DEFAULT', 'max_threads')
    save_reports = config.getboolean('DEFAULT', 'save_reports')
    
    print(f"\n✓ Max threads: {max_threads}")
    print(f"✓ Save reports: {save_reports}")


def demo_validation():
    """Demonstrate enhanced validation functions."""
    print("\n" + "=" * 60)
    print("ENHANCED VALIDATION DEMO")
    print("=" * 60)
    
    from red_team_toolkit import validate_ip, validate_hostname, validate_port, validate_url, colored, Colors
    
    # Test IP validation
    test_ips = ["192.168.1.1", "256.1.2.3", "10.0.0.1", "invalid"]
    print("IP Address Validation:")
    for ip in test_ips:
        is_valid = validate_ip(ip)
        status = colored("✓ Valid", Colors.OKGREEN) if is_valid else colored("✗ Invalid", Colors.FAIL)
        print(f"  {ip}: {status}")
    
    # Test hostname validation
    test_hostnames = ["example.com", "test-server", "192.168.1.1", "invalid@host"]
    print("\nHostname Validation:")
    for hostname in test_hostnames:
        is_valid = validate_hostname(hostname)
        status = colored("✓ Valid", Colors.OKGREEN) if is_valid else colored("✗ Invalid", Colors.FAIL)
        print(f"  {hostname}: {status}")
    
    # Test URL validation
    test_urls = ["http://example.com", "https://www.test.com", "example.com", "invalid"]
    print("\nURL Validation:")
    for url in test_urls:
        is_valid = validate_url(url)
        status = colored("✓ Valid", Colors.OKGREEN) if is_valid else colored("✗ Invalid", Colors.FAIL)
        print(f"  {url}: {status}")


def demo_utilities():
    """Demonstrate utility functions."""
    print("\n" + "=" * 60)
    print("UTILITY FUNCTIONS DEMO")
    print("=" * 60)
    
    from red_team_toolkit import calculate_entropy, is_likely_encrypted, sanitize_filename, generate_report_filename, colored, Colors
    
    # Test entropy calculation
    text_data = b"This is some text data for entropy testing"
    random_data = os.urandom(100)
    
    text_entropy = calculate_entropy(text_data)
    random_entropy = calculate_entropy(random_data)
    
    print("Entropy Calculation:")
    print(f"  Text data entropy: {text_entropy:.4f}")
    print(f"  Random data entropy: {random_entropy:.4f}")
    
    # Test encryption detection
    text_encrypted = is_likely_encrypted(text_data)
    random_encrypted = is_likely_encrypted(random_data)
    
    print("\nEncryption Detection:")
    print(f"  Text data encrypted: {text_encrypted}")
    print(f"  Random data encrypted: {random_encrypted}")
    
    # Test filename sanitization
    unsafe_filename = "test<file>:name.txt"
    safe_filename = sanitize_filename(unsafe_filename)
    
    print("\nFilename Sanitization:")
    print(f"  Original: {unsafe_filename}")
    print(f"  Sanitized: {safe_filename}")
    
    # Test report filename generation
    report_filename = generate_report_filename("demo_tool")
    print(f"\nReport filename: {report_filename}")


def demo_progress_bar():
    """Demonstrate progress bar functionality."""
    print("\n" + "=" * 60)
    print("PROGRESS BAR DEMO")
    print("=" * 60)
    
    from red_team_toolkit import ProgressBar
    import time
    
    # Create a progress bar
    progress = ProgressBar(10, "Demo Progress")
    
    print("Simulating work with progress bar...")
    for i in range(10):
        time.sleep(0.1)  # Simulate work
        progress.update()
    
    progress.finish()


def demo_rate_limiter():
    """Demonstrate rate limiting functionality."""
    print("\n" + "=" * 60)
    print("RATE LIMITER DEMO")
    print("=" * 60)
    
    from red_team_toolkit import RateLimiter
    import time
    
    # Create a rate limiter (5 requests per 10 seconds)
    limiter = RateLimiter(5, 10)
    
    print("Testing rate limiter (5 requests per 10 seconds):")
    
    for i in range(8):
        can_proceed = limiter.can_proceed()
        status = "✓ Allowed" if can_proceed else "✗ Blocked"
        print(f"  Request {i+1}: {status}")
        time.sleep(0.5)


def demo_colors():
    """Demonstrate colored output."""
    print("\n" + "=" * 60)
    print("COLORED OUTPUT DEMO")
    print("=" * 60)
    
    from red_team_toolkit import colored, Colors
    
    print(colored("This is a header", Colors.HEADER))
    print(colored("This is blue text", Colors.OKBLUE))
    print(colored("This is cyan text", Colors.OKCYAN))
    print(colored("This is green text", Colors.OKGREEN))
    print(colored("This is a warning", Colors.WARNING))
    print(colored("This is an error", Colors.FAIL))
    print(colored("This is bold text", Colors.BOLD))
    print(colored("This is underlined text", Colors.UNDERLINE))


def demo_reporting():
    """Demonstrate reporting functionality."""
    print("\n" + "=" * 60)
    print("REPORTING DEMO")
    print("=" * 60)
    
    from red_team_toolkit import save_report, colored, Colors
    
    # Create a sample report
    report_content = """
Demo Report
==========
This is a demonstration of the enhanced reporting system.

Features:
- Automatic timestamping
- Configurable save location
- Multiple format support
- Error handling

Timestamp: Demo run
Tool: Enhanced Red Team Toolkit v2.0
    """
    
    # Save the report
    report_file = save_report(report_content.strip(), "demo_report")
    
    if report_file:
        print(colored(f"✓ Report saved: {report_file}", Colors.OKGREEN))
    else:
        print(colored("✗ Failed to save report", Colors.FAIL))


def main():
    """Run all demonstrations."""
    print("Enhanced Red Team Toolkit v2.0 - Feature Demonstration")
    print("=" * 60)
    
    demos = [
        ("Configuration Management", demo_configuration),
        ("Enhanced Validation", demo_validation),
        ("Utility Functions", demo_utilities),
        ("Progress Bar", demo_progress_bar),
        ("Rate Limiter", demo_rate_limiter),
        ("Colored Output", demo_colors),
        ("Reporting System", demo_reporting)
    ]
    
    for demo_name, demo_func in demos:
        try:
            demo_func()
        except Exception as e:
            print(f"\n❌ Error in {demo_name}: {e}")
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("The enhanced toolkit includes:")
    print("✓ Configuration management system")
    print("✓ Enhanced validation functions")
    print("✓ Utility functions with better error handling")
    print("✓ Progress bars for long operations")
    print("✓ Rate limiting for network requests")
    print("✓ Colored output for better UX")
    print("✓ Automatic reporting system")
    print("✓ Comprehensive test suite")
    print("✓ New advanced tools (SSH brute force, web scraping, network mapping)")
    
    print("\nTo run the full toolkit:")
    print("python red_team_toolkit.py")
    
    print("\nTo run the test suite:")
    print("python test_red_team_toolkit.py")


if __name__ == "__main__":
    main()
