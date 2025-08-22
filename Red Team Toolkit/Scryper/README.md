# ProProfs Quiz Scraper

A production-ready Python script that uses Selenium with ChromeDriver to scrape quiz questions and answers from ProProfs.

## Features

- ✅ Launches Chrome in headless mode
- ✅ Automatically bypasses intro pages by clicking "Start Quiz" buttons
- ✅ Waits for each question to load properly
- ✅ Extracts question text and all answer options
- ✅ Handles pagination by clicking "Next" buttons
- ✅ Saves data in the specified JSON format
- ✅ Production-ready with WebDriverWait, error handling, and proper cleanup
- ✅ Comprehensive logging for debugging
- ✅ Duplicate question detection
- ✅ Multiple selector strategies for robust element detection

## Prerequisites

1. **Python 3.7+** installed on your system
2. **Google Chrome** browser installed
3. **ChromeDriver** (will be automatically managed by webdriver-manager)

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Simply run the script:

```bash
python quiz_scraper.py
```

The script will:
1. Navigate to the specified ProProfs quiz URL
2. Automatically handle the quiz flow
3. Extract all questions and answer options
4. Save the results to `quiz_data.json`

### Custom Usage

You can also use the scraper class in your own code:

```python
from quiz_scraper import ProProfsQuizScraper

# Initialize scraper (headless=True for background execution)
scraper = ProProfsQuizScraper(headless=True)

# Scrape a specific quiz
quiz_data = scraper.scrape_quiz("https://your-quiz-url.com")

# Save to custom filename
scraper.save_to_json("my_quiz_data.json")
```

## Output Format

The script generates a JSON file with the following structure:

```json
[
  {
    "question": "What is the primary purpose of service operations?",
    "options": [
      "To manage IT infrastructure",
      "To deliver business value",
      "To reduce costs",
      "To improve security"
    ]
  },
  {
    "question": "Which framework is commonly used for service operations?",
    "options": [
      "ITIL",
      "COBIT",
      "ISO 20000",
      "All of the above"
    ]
  }
]
```

## Configuration

### Chrome Options

The script includes several Chrome options for optimal performance:

- **Headless mode**: Runs Chrome in the background
- **No sandbox**: Improves stability on some systems
- **Disabled GPU**: Prevents graphics-related issues
- **Custom user agent**: Mimics a real browser
- **Disabled images/CSS**: Faster loading times

### Timeouts and Delays

- **WebDriverWait timeout**: 10 seconds for element detection
- **Page transition delay**: 2 seconds after clicking buttons
- **Question extraction delay**: 1 second for dynamic content
- **Maximum questions**: 100 (safety limit to prevent infinite loops)

## Error Handling

The script includes comprehensive error handling for:

- WebDriver initialization failures
- Navigation errors
- Element not found exceptions
- Timeout exceptions
- Click intercepted exceptions
- File I/O errors

## Logging

The script provides detailed logging with timestamps:

```
2024-01-15 10:30:15,123 - INFO - Starting ProProfs Quiz Scraper
2024-01-15 10:30:16,456 - INFO - Chrome WebDriver initialized successfully
2024-01-15 10:30:18,789 - INFO - Successfully navigated to quiz page
2024-01-15 10:30:20,012 - INFO - Successfully clicked 'Start Quiz' button
2024-01-15 10:30:22,345 - INFO - Extracted question: What is the primary purpose...
2024-01-15 10:30:22,346 - INFO - Found 4 options
2024-01-15 10:30:22,347 - INFO - Scraped question 1
```

## Troubleshooting

### Common Issues

1. **ChromeDriver not found**: The script uses webdriver-manager to automatically download and manage ChromeDriver.

2. **Element not found**: The script uses multiple selector strategies to find elements. If one fails, it tries others.

3. **Quiz structure changes**: ProProfs may update their website structure. The script includes multiple selectors to handle variations.

4. **Network issues**: The script includes retry logic and proper error handling for network-related problems.

### Debug Mode

To run in non-headless mode for debugging:

```python
scraper = ProProfsQuizScraper(headless=False)
```

This will open a visible Chrome window so you can see what the script is doing.

## Legal Considerations

- Ensure you have permission to scrape the quiz content
- Respect the website's robots.txt and terms of service
- Consider rate limiting for large-scale scraping
- Use the scraped data responsibly and in accordance with applicable laws

## License

This script is provided for educational and research purposes. Please ensure compliance with applicable laws and website terms of service.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the script.
