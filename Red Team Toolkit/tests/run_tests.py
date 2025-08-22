#!/usr/bin/env python3
"""
Comprehensive test runner for the Enhanced Red Team Toolkit.
"""

import unittest
import sys
import os
import time
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

def run_all_tests():
    """Run all test suites."""
    print("🧪 Enhanced Red Team Toolkit - Test Suite")
    print("=" * 50)
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\n❌ Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Exception:')[-1].strip()}")
    
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        return True
    else:
        print("\n❌ Some tests failed!")
        return False

def run_specific_test(test_name):
    """Run a specific test."""
    print(f"🧪 Running specific test: {test_name}")
    print("=" * 50)
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(test_name)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def run_test_category(category):
    """Run tests by category."""
    categories = {
        'plugin': 'test_plugin_system',
        'scheduler': 'test_plugin_system.TestTaskScheduler',
        'sandbox': 'test_plugin_system.TestSandboxMode',
        'integration': 'test_plugin_system.TestIntegration'
    }
    
    if category not in categories:
        print(f"❌ Unknown test category: {category}")
        print(f"Available categories: {', '.join(categories.keys())}")
        return False
    
    test_name = categories[category]
    return run_specific_test(test_name)

def main():
    """Main test runner."""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'all':
            return run_all_tests()
        elif command == 'plugin':
            return run_test_category('plugin')
        elif command == 'scheduler':
            return run_test_category('scheduler')
        elif command == 'sandbox':
            return run_test_category('sandbox')
        elif command == 'integration':
            return run_test_category('integration')
        elif command == 'help':
            print("🧪 Enhanced Red Team Toolkit - Test Runner")
            print("=" * 50)
            print("Usage:")
            print("  python run_tests.py all          - Run all tests")
            print("  python run_tests.py plugin       - Run plugin system tests")
            print("  python run_tests.py scheduler    - Run scheduler tests")
            print("  python run_tests.py sandbox      - Run sandbox mode tests")
            print("  python run_tests.py integration  - Run integration tests")
            print("  python run_tests.py help         - Show this help")
            return True
        else:
            print(f"❌ Unknown command: {command}")
            print("Use 'python run_tests.py help' for usage information")
            return False
    else:
        # Default: run all tests
        return run_all_tests()

if __name__ == '__main__':
    start_time = time.time()
    success = main()
    end_time = time.time()
    
    print(f"\n⏱️  Test execution time: {end_time - start_time:.2f} seconds")
    
    if success:
        print("🎉 Test suite completed successfully!")
        sys.exit(0)
    else:
        print("💥 Test suite completed with failures!")
        sys.exit(1)
