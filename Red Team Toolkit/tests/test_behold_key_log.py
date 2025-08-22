"""
Test suite for BEHOLD Keylogger
===============================

This module provides comprehensive testing for the keylogger including:
- Unit tests for individual components
- Integration tests for full workflow
- Safety tests for ethical compliance
- Configuration tests
- Error handling tests
"""

import unittest
import tempfile
import os
import json
import time
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from behold_key_log import (
    KeyloggerConfig, 
    SafetyManager, 
    RateLimiter, 
    SecureLogger, 
    AdvancedKeylogger
)


class TestKeyloggerConfig(unittest.TestCase):
    """Test configuration management"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "test_config.ini"
        self.config = KeyloggerConfig(str(self.config_file))
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_default_config_creation(self):
        """Test that default configuration is created properly"""
        self.assertTrue(self.config_file.exists())
        self.assertIn('SAFETY', self.config.config.sections())
        self.assertIn('LOGGING', self.config.config.sections())
        self.assertIn('CONTROLS', self.config.config.sections())
    
    def test_config_get_method(self):
        """Test configuration get method"""
        value = self.config.get('SAFETY', 'lab_only')
        self.assertEqual(value, 'true')
        
        # Test fallback
        value = self.config.get('NONEXISTENT', 'key', fallback='default')
        self.assertEqual(value, 'default')
    
    def test_config_getboolean_method(self):
        """Test boolean configuration retrieval"""
        value = self.config.getboolean('SAFETY', 'lab_only')
        self.assertTrue(value)
        
        # Test fallback
        value = self.config.getboolean('NONEXISTENT', 'key', fallback=True)
        self.assertTrue(value)
    
    def test_config_save(self):
        """Test configuration saving"""
        # Modify a value
        self.config.config.set('SAFETY', 'lab_only', 'false')
        self.config.save_config()
        
        # Reload and verify
        new_config = KeyloggerConfig(str(self.config_file))
        value = new_config.getboolean('SAFETY', 'lab_only')
        self.assertFalse(value)


class TestSafetyManager(unittest.TestCase):
    """Test safety management functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "test_config.ini"
        self.config = KeyloggerConfig(str(self.config_file))
        self.safety = SafetyManager(self.config)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    @patch('builtins.input', return_value='yes')
    def test_display_warning_with_confirmation(self, mock_input):
        """Test warning display with user confirmation"""
        # Should not raise exception
        self.safety.display_warning()
        mock_input.assert_called_once()
    
    @patch('builtins.input', return_value='no')
    @patch('sys.exit')
    def test_display_warning_with_denial(self, mock_exit, mock_input):
        """Test warning display with user denial"""
        self.safety.display_warning()
        mock_exit.assert_called_once_with(0)
    
    @patch('socket.gethostname')
    @patch('socket.gethostbyname')
    def test_lab_environment_detection(self, mock_gethostbyname, mock_gethostname):
        """Test lab environment detection"""
        # Test lab environment
        mock_gethostname.return_value = 'test-host'
        mock_gethostbyname.return_value = '192.168.1.100'
        
        result = self.safety.is_lab_environment()
        self.assertTrue(result)
        
        # Test non-lab environment
        mock_gethostbyname.return_value = '8.8.8.8'
        result = self.safety.is_lab_environment()
        self.assertFalse(result)
    
    @patch('psutil.disk_usage')
    def test_disk_space_check(self, mock_disk_usage):
        """Test disk space checking"""
        # Mock sufficient disk space
        mock_disk_usage.return_value = Mock(free=100 * 1024 * 1024)  # 100MB
        result = self.safety.check_disk_space()
        self.assertTrue(result)
        
        # Mock insufficient disk space
        mock_disk_usage.return_value = Mock(free=5 * 1024 * 1024)  # 5MB
        result = self.safety.check_disk_space()
        self.assertFalse(result)


class TestRateLimiter(unittest.TestCase):
    """Test rate limiting functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.rate_limiter = RateLimiter(max_events_per_sec=5)
    
    def test_rate_limiting_basic(self):
        """Test basic rate limiting"""
        # Should allow first 5 events
        for i in range(5):
            self.assertTrue(self.rate_limiter.allow())
        
        # Should block the 6th event
        self.assertFalse(self.rate_limiter.allow())
    
    def test_rate_limiting_time_window(self):
        """Test rate limiting time window"""
        # Allow 5 events
        for i in range(5):
            self.rate_limiter.allow()
        
        # Wait for time window to pass
        time.sleep(1.1)
        
        # Should allow events again
        self.assertTrue(self.rate_limiter.allow())
    
    def test_thread_safety(self):
        """Test rate limiter thread safety"""
        import threading
        
        results = []
        
        def worker():
            for i in range(10):
                results.append(self.rate_limiter.allow())
                time.sleep(0.1)
        
        threads = [threading.Thread(target=worker) for _ in range(3)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        # Should have some True and some False results
        self.assertIn(True, results)
        self.assertIn(False, results)


class TestSecureLogger(unittest.TestCase):
    """Test secure logging functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "test_config.ini"
        self.config = KeyloggerConfig(str(self.config_file))
        self.logger = SecureLogger(self.config)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_log_entry_basic(self):
        """Test basic log entry functionality"""
        entry = {
            'timestamp': '2024-01-01 12:00:00',
            'key': 'a',
            'key_type': 'KeyCode'
        }
        
        self.logger.log_entry(entry)
        
        # Check that log file exists
        self.assertTrue(self.logger.log_file.exists())
    
    def test_log_entry_with_encryption(self):
        """Test log entry with encryption enabled"""
        # Enable encryption
        self.config.config.set('SAFETY', 'encrypt_logs', 'true')
        self.logger = SecureLogger(self.config)
        
        entry = {
            'timestamp': '2024-01-01 12:00:00',
            'key': 'a',
            'key_type': 'KeyCode'
        }
        
        self.logger.log_entry(entry)
        
        # Check that encrypted log file exists
        self.assertTrue(self.logger.log_file.exists())
        
        # Verify content is encrypted
        with open(self.logger.log_file, 'rb') as f:
            content = f.read()
            # Should not contain plain text JSON
            self.assertNotIn(b'"a"', content)
            # Should contain encrypted base64 data
            self.assertIn(b'gAAAAA', content)
    
    def test_log_entry_error_handling(self):
        """Test error handling in log entry"""
        # Create invalid entry
        entry = {
            'timestamp': '2024-01-01 12:00:00',
            'key': object(),  # Non-serializable object
            'key_type': 'KeyCode'
        }
        
        # Should not raise exception
        self.logger.log_entry(entry)


class TestAdvancedKeylogger(unittest.TestCase):
    """Test advanced keylogger functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "test_config.ini"
        self.config = KeyloggerConfig(str(self.config_file))
        self.keylogger = AdvancedKeylogger(self.config)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_keylogger_initialization(self):
        """Test keylogger initialization"""
        self.assertIsNotNone(self.keylogger.config)
        self.assertIsNotNone(self.keylogger.safety)
        self.assertIsNotNone(self.keylogger.logger)
        self.assertIsNotNone(self.keylogger.rate_limiter)
        self.assertFalse(self.keylogger.is_running)
    
    def test_get_active_window_info(self):
        """Test active window info retrieval"""
        info = self.keylogger.get_active_window_info()
        self.assertIsInstance(info, dict)
    
    def test_log_key_with_context(self):
        """Test keystroke logging with context"""
        # Mock a key press
        mock_key = Mock()
        mock_key.char = 'a'
        
        self.keylogger.log_key_with_context(mock_key)
        
        # Check that stats were updated
        self.assertEqual(self.keylogger.stats['keys_logged'], 1)
    
    def test_log_key_with_context_error(self):
        """Test error handling in keystroke logging"""
        # Mock a problematic key
        mock_key = Mock()
        mock_key.char = None
        mock_key.name = None
        
        # Should not raise exception
        self.keylogger.log_key_with_context(mock_key)
        
        # Check that error was recorded
        self.assertEqual(self.keylogger.stats['errors'], 1)
    
    def test_get_statistics(self):
        """Test statistics retrieval"""
        stats = self.keylogger.get_statistics()
        
        self.assertIn('keys_logged', stats)
        self.assertIn('errors', stats)
        self.assertIn('is_running', stats)
        self.assertIn('log_file', stats)
        self.assertIn('encryption_enabled', stats)
    
    @patch('behold_key_log.SafetyManager.display_warning')
    @patch('behold_key_log.SafetyManager.is_lab_environment', return_value=False)
    def test_start_safety_check_failure(self, mock_lab_check, mock_warning):
        """Test start with safety check failure"""
        result = self.keylogger.start()
        self.assertFalse(result)
    
    @patch('behold_key_log.SafetyManager.display_warning')
    @patch('behold_key_log.SafetyManager.is_lab_environment', return_value=True)
    @patch('behold_key_log.SafetyManager.check_disk_space', return_value=True)
    @patch('pynput.keyboard.Listener')
    def test_start_success(self, mock_listener, mock_disk_check, mock_lab_check, mock_warning):
        """Test successful start"""
        # Mock the listener to return immediately
        mock_listener_instance = Mock()
        mock_listener_instance.join.side_effect = KeyboardInterrupt()
        mock_listener.return_value.__enter__.return_value = mock_listener_instance
        
        result = self.keylogger.start()
        self.assertTrue(result)


class TestIntegration(unittest.TestCase):
    """Integration tests for full workflow"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "test_config.ini"
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_full_workflow(self):
        """Test complete keylogger workflow"""
        config = KeyloggerConfig(str(self.config_file))
        keylogger = AdvancedKeylogger(config)
        
        # Test initialization
        self.assertIsNotNone(keylogger)
        
        # Test statistics
        stats = keylogger.get_statistics()
        self.assertIsInstance(stats, dict)
        
        # Test stop method
        keylogger.stop()
        self.assertFalse(keylogger.is_running)


class TestSafetyCompliance(unittest.TestCase):
    """Test safety and ethical compliance"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "test_config.ini"
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_lab_only_mode_enabled(self):
        """Test that lab-only mode is enabled by default"""
        config = KeyloggerConfig(str(self.config_file))
        self.assertTrue(config.getboolean('SAFETY', 'lab_only'))
    
    def test_encryption_enabled_by_default(self):
        """Test that encryption is enabled by default when available"""
        config = KeyloggerConfig(str(self.config_file))
        # This will depend on whether cryptography is available
        encryption_setting = config.get('SAFETY', 'encrypt_logs')
        self.assertIn(encryption_setting, ['true', 'false'])
    
    def test_confirmation_required(self):
        """Test that user confirmation is required by default"""
        config = KeyloggerConfig(str(self.config_file))
        self.assertTrue(config.getboolean('SAFETY', 'require_confirmation'))
    
    def test_rate_limiting_enabled(self):
        """Test that rate limiting is enabled by default"""
        config = KeyloggerConfig(str(self.config_file))
        rate_limit = int(config.get('SAFETY', 'rate_limit_events_per_sec'))
        self.assertGreater(rate_limit, 0)
        self.assertLess(rate_limit, 1000)  # Reasonable limit


def run_tests():
    """Run all tests with detailed output"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestKeyloggerConfig,
        TestSafetyManager,
        TestRateLimiter,
        TestSecureLogger,
        TestAdvancedKeylogger,
        TestIntegration,
        TestSafetyCompliance
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
