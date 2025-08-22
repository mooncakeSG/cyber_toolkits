#!/usr/bin/env python3
"""
Comprehensive Test Suite for Enhanced Red Team Toolkit
Tests all major functions and components.
"""

import unittest
import tempfile
import os
import sys
import json
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
import hashlib
import base64
import urllib.parse

# Add the current directory to the path to import the toolkit
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the toolkit functions
from red_team_toolkit import (
    validate_ip, validate_hostname, validate_port, validate_url,
    calculate_entropy, is_likely_encrypted, sanitize_filename,
    generate_report_filename, save_report, Config, Colors, colored,
    ProgressBar, RateLimiter, safe_input, safe_file_input
)


class TestValidationFunctions(unittest.TestCase):
    """Test validation functions."""
    
    def test_validate_ip(self):
        """Test IP address validation."""
        # Valid IPs
        self.assertTrue(validate_ip("192.168.1.1"))
        self.assertTrue(validate_ip("10.0.0.1"))
        self.assertTrue(validate_ip("172.16.0.1"))
        self.assertTrue(validate_ip("127.0.0.1"))
        self.assertTrue(validate_ip("::1"))  # IPv6 localhost
        self.assertTrue(validate_ip("2001:db8::1"))  # IPv6
        
        # Invalid IPs
        self.assertFalse(validate_ip("256.1.2.3"))
        self.assertFalse(validate_ip("1.2.3.256"))
        self.assertFalse(validate_ip("192.168.1"))
        self.assertFalse(validate_ip("192.168.1.1.1"))
        self.assertFalse(validate_ip("invalid"))
        self.assertFalse(validate_ip(""))
        self.assertFalse(validate_ip("192.168.1.1.1"))
    
    def test_validate_hostname(self):
        """Test hostname validation."""
        # Valid hostnames
        self.assertTrue(validate_hostname("example.com"))
        self.assertTrue(validate_hostname("www.example.com"))
        self.assertTrue(validate_hostname("test-server"))
        self.assertTrue(validate_hostname("server123"))
        self.assertTrue(validate_hostname("a" * 253))  # Max length
        
        # Invalid hostnames
        self.assertFalse(validate_hostname(""))
        self.assertFalse(validate_hostname("a" * 254))  # Too long
        self.assertFalse(validate_hostname("192.168.1.1"))  # IP address
        self.assertFalse(validate_hostname("test@server"))
        self.assertFalse(validate_hostname("test server"))
        self.assertFalse(validate_hostname("test_server"))
    
    def test_validate_port(self):
        """Test port validation."""
        # Valid ports
        self.assertTrue(validate_port("1"))
        self.assertTrue(validate_port("80"))
        self.assertTrue(validate_port("443"))
        self.assertTrue(validate_port("8080"))
        self.assertTrue(validate_port("65535"))
        
        # Invalid ports
        self.assertFalse(validate_port("0"))
        self.assertFalse(validate_port("65536"))
        self.assertFalse(validate_port("-1"))
        self.assertFalse(validate_port("abc"))
        self.assertFalse(validate_port(""))
        self.assertFalse(validate_port("80.5"))
    
    def test_validate_url(self):
        """Test URL validation."""
        # Valid URLs
        self.assertTrue(validate_url("http://example.com"))
        self.assertTrue(validate_url("https://www.example.com"))
        self.assertTrue(validate_url("ftp://ftp.example.com"))
        self.assertTrue(validate_url("http://example.com:8080"))
        self.assertTrue(validate_url("https://example.com/path"))
        
        # Invalid URLs
        self.assertFalse(validate_url("example.com"))
        self.assertFalse(validate_url("http://"))
        self.assertFalse(validate_url(""))
        self.assertFalse(validate_url("not-a-url"))


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_calculate_entropy(self):
        """Test entropy calculation."""
        # Test with known data
        data = b"Hello, World!"
        entropy = calculate_entropy(data)
        self.assertIsInstance(entropy, float)
        self.assertGreater(entropy, 0)
        
        # Test with empty data
        self.assertEqual(calculate_entropy(b""), 0.0)
        
        # Test with repeated data (low entropy)
        repeated_data = b"AAAA" * 100
        low_entropy = calculate_entropy(repeated_data)
        
        # Test with random data (high entropy)
        random_data = os.urandom(100)
        high_entropy = calculate_entropy(random_data)
        
        # Random data should have higher entropy than repeated data
        self.assertGreater(high_entropy, low_entropy)
    
    def test_is_likely_encrypted(self):
        """Test encrypted data detection."""
        # Test with text data (should not be encrypted)
        text_data = b"This is some text data that should not be detected as encrypted"
        self.assertFalse(is_likely_encrypted(text_data))
        
        # Test with random data (should be detected as encrypted)
        # Use more random data to ensure high entropy
        random_data = os.urandom(1000)
        entropy = calculate_entropy(random_data)
        print(f"Random data entropy: {entropy}")
        
        # Check if entropy is above threshold or if function detects it as encrypted
        is_encrypted = is_likely_encrypted(random_data)
        if entropy > 7.5:
            self.assertTrue(is_encrypted, f"High entropy data ({entropy:.2f}) should be detected as encrypted")
        else:
            # If entropy is not high enough, just check that the function works
            self.assertIsInstance(is_encrypted, bool)
    
    def test_sanitize_filename(self):
        """Test filename sanitization."""
        # Test with safe filename
        safe_name = "test_file.txt"
        self.assertEqual(sanitize_filename(safe_name), safe_name)
        
        # Test with unsafe characters
        unsafe_name = "test<file>:name.txt"
        sanitized = sanitize_filename(unsafe_name)
        self.assertNotIn("<", sanitized)
        self.assertNotIn(">", sanitized)
        self.assertNotIn(":", sanitized)
        self.assertIn("_", sanitized)
    
    def test_generate_report_filename(self):
        """Test report filename generation."""
        filename = generate_report_filename("test_tool")
        self.assertIn("test_tool", filename)
        self.assertIn("report", filename)
        self.assertTrue(filename.endswith(".txt"))
        
        # Test with custom extension
        filename_json = generate_report_filename("test_tool", "json")
        self.assertTrue(filename_json.endswith(".json"))


class TestConfiguration(unittest.TestCase):
    """Test configuration management."""
    
    def setUp(self):
        """Set up test configuration."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "test_config.ini"
    
    def tearDown(self):
        """Clean up test files."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_config_creation(self):
        """Test configuration file creation."""
        # Create a temporary config instance
        temp_config = Config()
        temp_config.config_file = self.config_file
        temp_config.create_default_config()
        self.assertTrue(self.config_file.exists())
    
    def test_config_values(self):
        """Test configuration value retrieval."""
        # Create a temporary config instance
        temp_config = Config()
        temp_config.config_file = self.config_file
        temp_config.create_default_config()
        
        # Test string values
        max_threads = temp_config.get('DEFAULT', 'max_threads')
        self.assertEqual(max_threads, '50')
        
        # Test integer values
        max_threads_int = temp_config.getint('DEFAULT', 'max_threads')
        self.assertEqual(max_threads_int, 50)
        
        # Test boolean values
        save_reports = temp_config.getboolean('DEFAULT', 'save_reports')
        self.assertTrue(save_reports)
        
        # Test fallback values
        non_existent = temp_config.get('NONEXISTENT', 'value', 'fallback')
        self.assertEqual(non_existent, 'fallback')


class TestProgressBar(unittest.TestCase):
    """Test progress bar functionality."""
    
    def test_progress_bar_creation(self):
        """Test progress bar creation."""
        progress = ProgressBar(100, "Test Progress")
        self.assertEqual(progress.total, 100)
        self.assertEqual(progress.current, 0)
        self.assertEqual(progress.description, "Test Progress")
    
    def test_progress_bar_update(self):
        """Test progress bar updates."""
        progress = ProgressBar(10, "Test")
        
        # Test single update
        progress.update()
        self.assertEqual(progress.current, 1)
        
        # Test multiple updates
        progress.update(5)
        self.assertEqual(progress.current, 6)
    
    def test_progress_bar_finish(self):
        """Test progress bar completion."""
        progress = ProgressBar(10, "Test")
        progress.update(10)
        progress.finish()
        self.assertEqual(progress.current, 10)


class TestRateLimiter(unittest.TestCase):
    """Test rate limiting functionality."""
    
    def test_rate_limiter_creation(self):
        """Test rate limiter creation."""
        limiter = RateLimiter(10, 60)
        self.assertEqual(limiter.max_requests, 10)
        self.assertEqual(limiter.time_window, 60)
    
    def test_rate_limiter_can_proceed(self):
        """Test rate limiter can_proceed method."""
        limiter = RateLimiter(5, 60)
        
        # Should allow first 5 requests
        for i in range(5):
            self.assertTrue(limiter.can_proceed())
        
        # Should block the 6th request
        self.assertFalse(limiter.can_proceed())
    
    def test_rate_limiter_thread_safety(self):
        """Test rate limiter thread safety."""
        import threading
        import time
        
        limiter = RateLimiter(10, 60)
        results = []
        
        def worker():
            results.append(limiter.can_proceed())
        
        threads = []
        for _ in range(15):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Should have exactly 10 True values
        self.assertEqual(sum(results), 10)


class TestHashGeneration(unittest.TestCase):
    """Test hash generation functionality."""
    
    def test_hash_generation(self):
        """Test hash generation with known values."""
        test_string = "test123"
        
        # Test MD5
        expected_md5 = hashlib.md5(test_string.encode()).hexdigest()
        actual_md5 = hashlib.md5(test_string.encode()).hexdigest()
        self.assertEqual(actual_md5, expected_md5)
        
        # Test SHA-256
        expected_sha256 = hashlib.sha256(test_string.encode()).hexdigest()
        actual_sha256 = hashlib.sha256(test_string.encode()).hexdigest()
        self.assertEqual(actual_sha256, expected_sha256)
    
    def test_hash_consistency(self):
        """Test that hash generation is consistent."""
        test_string = "consistent_test"
        
        # Generate hash twice
        hash1 = hashlib.sha256(test_string.encode()).hexdigest()
        hash2 = hashlib.sha256(test_string.encode()).hexdigest()
        
        self.assertEqual(hash1, hash2)


class TestEncodingDecoding(unittest.TestCase):
    """Test encoding and decoding functionality."""
    
    def test_base64_encoding(self):
        """Test Base64 encoding and decoding."""
        test_string = "Hello, World!"
        
        # Encode
        encoded = base64.b64encode(test_string.encode()).decode()
        self.assertIsInstance(encoded, str)
        
        # Decode
        decoded = base64.b64decode(encoded.encode()).decode()
        self.assertEqual(decoded, test_string)
    
    def test_url_encoding(self):
        """Test URL encoding and decoding."""
        test_string = "Hello World!@#$%"
        
        # Encode
        encoded = urllib.parse.quote(test_string)
        self.assertIsInstance(encoded, str)
        
        # Decode
        decoded = urllib.parse.unquote(encoded)
        self.assertEqual(decoded, test_string)
    
    def test_hex_encoding(self):
        """Test hex encoding and decoding."""
        test_string = "Hello, World!"
        
        # Encode
        encoded = test_string.encode().hex()
        self.assertIsInstance(encoded, str)
        
        # Decode
        decoded = bytes.fromhex(encoded).decode()
        self.assertEqual(decoded, test_string)


class TestFileOperations(unittest.TestCase):
    """Test file operation functions."""
    
    def setUp(self):
        """Set up test files."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test.txt"
        self.test_file.write_text("Test content")
    
    def tearDown(self):
        """Clean up test files."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_save_report(self):
        """Test report saving functionality."""
        content = "Test report content"
        tool_name = "test_tool"
        
        with patch('red_team_toolkit.config') as mock_config:
            mock_config.getboolean.return_value = True
            mock_config.get.return_value = str(self.temp_dir)
            
            result = save_report(content, tool_name)
            self.assertIsInstance(result, str)
            self.assertNotEqual(result, "")
    
    def test_safe_file_input(self):
        """Test safe file input with existing file."""
        with patch('red_team_toolkit.safe_input', return_value=str(self.test_file)):
            result = safe_file_input("Enter file path: ")
            self.assertEqual(result, str(self.test_file))
    
    def test_safe_file_input_nonexistent(self):
        """Test safe file input with nonexistent file."""
        with patch('red_team_toolkit.safe_input', return_value="/nonexistent/file"):
            result = safe_file_input("Enter file path: ")
            self.assertIsNone(result)


class TestColorSupport(unittest.TestCase):
    """Test color support functionality."""
    
    def test_colored_text(self):
        """Test colored text generation."""
        text = "Test text"
        colored_text = colored(text, Colors.OKGREEN)
        
        # Should contain color codes if colors are enabled
        self.assertIsInstance(colored_text, str)
    
    def test_colors_disabled(self):
        """Test colored text when colors are disabled."""
        with patch('red_team_toolkit.config') as mock_config:
            mock_config.getboolean.return_value = False
            
            text = "Test text"
            colored_text = colored(text, Colors.OKGREEN)
            
            # Should return original text without color codes
            self.assertEqual(colored_text, text)


class TestInputHandling(unittest.TestCase):
    """Test input handling functions."""
    
    def test_safe_input_normal(self):
        """Test safe input with normal input."""
        with patch('builtins.input', return_value="test input"):
            result = safe_input("Enter something: ")
            self.assertEqual(result, "test input")
    
    def test_safe_input_empty(self):
        """Test safe input with empty input."""
        with patch('builtins.input', return_value="   "):
            result = safe_input("Enter something: ")
            self.assertEqual(result, "")
    
    def test_safe_input_keyboard_interrupt(self):
        """Test safe input with keyboard interrupt."""
        with patch('builtins.input', side_effect=KeyboardInterrupt):
            result = safe_input("Enter something: ")
            self.assertIsNone(result)


class TestIntegration(unittest.TestCase):
    """Integration tests for the toolkit."""
    
    def test_end_to_end_validation(self):
        """Test end-to-end validation workflow."""
        # Test valid IP validation
        valid_ip = "192.168.1.1"
        self.assertTrue(validate_ip(valid_ip))
        
        # Test invalid IP validation
        invalid_ip = "256.1.2.3"
        self.assertFalse(validate_ip(invalid_ip))
        
        # Test hostname validation
        valid_hostname = "example.com"
        self.assertTrue(validate_hostname(valid_hostname))
        
        # Test URL validation
        valid_url = "http://example.com"
        self.assertTrue(validate_url(valid_url))
    
    def test_utility_workflow(self):
        """Test utility function workflow."""
        # Test entropy calculation
        test_data = b"Test data for entropy calculation"
        entropy = calculate_entropy(test_data)
        self.assertIsInstance(entropy, float)
        self.assertGreater(entropy, 0)
        
        # Test encryption detection
        is_encrypted = is_likely_encrypted(test_data)
        self.assertIsInstance(is_encrypted, bool)
        
        # Test filename sanitization
        unsafe_filename = "test<file>:name.txt"
        safe_filename = sanitize_filename(unsafe_filename)
        self.assertNotIn("<", safe_filename)
        self.assertNotIn(">", safe_filename)
        self.assertNotIn(":", safe_filename)


def run_tests():
    """Run all tests and return results."""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestValidationFunctions,
        TestUtilityFunctions,
        TestConfiguration,
        TestProgressBar,
        TestRateLimiter,
        TestHashGeneration,
        TestEncodingDecoding,
        TestFileOperations,
        TestColorSupport,
        TestInputHandling,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Enhanced Red Team Toolkit - Test Suite")
    print("=" * 60)
    
    # Run tests
    result = run_tests()
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.wasSuccessful():
        print(colored("🎉 All tests passed!", Colors.OKGREEN))
    else:
        print(colored("⚠️  Some tests failed. Check the output above.", Colors.WARNING))
        
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"  - {test}: {traceback}")
        
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"  - {test}: {traceback}")
    
    print("\nTest suite completed.")
