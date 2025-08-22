#!/usr/bin/env python3
"""
Test script to verify the quiz scraper setup and dependencies.
"""

import sys
import logging

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import selenium
        print(f"✅ Selenium version: {selenium.__version__}")
    except ImportError as e:
        print(f"❌ Selenium import failed: {e}")
        return False
    
    try:
        import chromedriver_autoinstaller
        print("✅ chromedriver-autoinstaller imported successfully")
    except ImportError as e:
        print(f"❌ chromedriver-autoinstaller import failed: {e}")
        return False
    
    try:
        from quiz_scraper import ProProfsQuizScraper
        print("✅ ProProfsQuizScraper imported successfully")
    except ImportError as e:
        print(f"❌ quiz_scraper import failed: {e}")
        return False
    
    return True

def test_chrome_driver():
    """Test if ChromeDriver can be initialized."""
    print("\nTesting ChromeDriver setup...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        import chromedriver_autoinstaller
        
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        # Initialize driver
        chromedriver_autoinstaller.install()
        driver = webdriver.Chrome(options=chrome_options)
        
        # Test basic functionality
        driver.get("https://www.google.com")
        title = driver.title
        try:
            driver.quit()
        except OSError:
            pass  # Handle WinError 6 gracefully
        
        print(f"✅ ChromeDriver test successful - Page title: {title}")
        return True
        
    except Exception as e:
        print(f"❌ ChromeDriver test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("ProProfs Quiz Scraper - Setup Test")
    print("=" * 40)
    
    # Test Python version
    print(f"Python version: {sys.version}")
    
    # Test imports
    imports_ok = test_imports()
    
    # Test ChromeDriver
    driver_ok = test_chrome_driver()
    
    print("\n" + "=" * 40)
    if imports_ok and driver_ok:
        print("✅ All tests passed! The scraper is ready to use.")
        print("\nYou can now run: python quiz_scraper.py")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        print("\nTo install missing dependencies, run: pip install -r requirements.txt")
    
    return imports_ok and driver_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
