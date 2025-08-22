# Contributing to Blue Team CLI Toolkit

Thank you for your interest in contributing to the Blue Team CLI Toolkit! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **🐛 Bug Reports** - Report issues and bugs
- **💡 Feature Requests** - Suggest new features and enhancements
- **📝 Documentation** - Improve documentation and examples
- **🔧 Code Contributions** - Submit code improvements and new modules
- **🧪 Testing** - Test features and report issues
- **🌍 Localization** - Help with translations and internationalization

### Getting Started

1. **Fork the Repository**
   ```bash
   git clone https://github.com/yourusername/blueteam-toolkit.git
   cd blueteam-toolkit
   ```

2. **Create a Development Environment**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Install in development mode
   pip install -e .
   ```

3. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/your-bug-fix
   ```

## 📋 Development Guidelines

### Code Style

- **Python**: Follow PEP 8 style guidelines
- **Documentation**: Use clear, descriptive docstrings
- **Comments**: Add comments for complex logic
- **Naming**: Use descriptive variable and function names

### Code Structure

```python
"""
Module description.

This module provides functionality for...
"""

import os
import sys
import platform
import subprocess
from typing import List, Dict, Any, Optional
from datetime import datetime
import utils

def function_name(param1: str, param2: int = None) -> Dict[str, Any]:
    """
    Function description.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (optional)
        
    Returns:
        Dictionary containing results
        
    Raises:
        ValueError: When invalid parameters are provided
    """
    # Implementation here
    pass

def main(args):
    """Main function for the module."""
    utils.print_banner()
    utils.print_section("Module Name")
    
    try:
        # Main logic here
        pass
    except Exception as e:
        utils.print_error(f"Module failed: {e}")
```

### Testing

- **Unit Tests**: Write tests for new functions
- **Integration Tests**: Test module interactions
- **Cross-Platform**: Test on Windows, Linux, and macOS
- **Error Handling**: Test error conditions and edge cases

### Security Considerations

- **Input Validation**: Validate all user inputs
- **Privilege Checks**: Check for administrative privileges when needed
- **Error Messages**: Don't expose sensitive information in error messages
- **API Keys**: Handle credentials securely

## 🚀 Adding New Features

### New Module Development

1. **Create Module File**
   ```python
   # new_module.py
   """
   New Module for the Blue Team CLI Toolkit.
   Provides functionality for...
   """
   ```

2. **Update main.py**
   - Add import for new module
   - Add subparser with arguments
   - Add dispatch logic

3. **Update Documentation**
   - Add module description to README.md
   - Update INSTALL.md with usage examples
   - Add help text and examples

### Example Module Structure

```python
"""
Example Module for the Blue Team CLI Toolkit.
Provides example functionality.
"""

import os
import sys
import platform
import subprocess
from typing import List, Dict, Any, Optional
from datetime import datetime
import utils

def example_function(param: str) -> Dict[str, Any]:
    """
    Example function that does something.
    
    Args:
        param: Input parameter
        
    Returns:
        Dictionary with results
    """
    results = {
        'timestamp': datetime.now().isoformat(),
        'parameter': param,
        'results': []
    }
    
    # Implementation here
    
    return results

def main(args):
    """Main function for the example module."""
    utils.print_banner()
    utils.print_section("Example Module")
    
    try:
        if hasattr(args, 'example_param') and args.example_param:
            results = example_function(args.example_param)
            
            # Display results
            utils.print_info(f"Processed: {args.example_param}")
            
            # Export if requested
            if hasattr(args, 'export') and args.export:
                utils.export_report_with_metadata(
                    results, 
                    'example', 
                    getattr(args, 'export_format', 'json'), 
                    args.export, 
                    getattr(args, 'compress', False)
                )
        
        utils.print_success("Example module completed")
        
    except Exception as e:
        utils.print_error(f"Example module failed: {e}")

if __name__ == "__main__":
    # For direct module testing
    import argparse
    
    parser = argparse.ArgumentParser(description="Example Module")
    parser.add_argument('--example-param', required=True, help='Example parameter')
    parser.add_argument('--export', help='Export results to file')
    parser.add_argument('--export-format', choices=['json', 'csv', 'txt'], default='json', help='Export format')
    parser.add_argument('--compress', action='store_true', help='Compress export file')
    
    args = parser.parse_args()
    main(args)
```

## 📝 Documentation Guidelines

### README Updates

- Add new features to the features section
- Include usage examples
- Update installation instructions if needed
- Add new modules to the module documentation

### Code Documentation

- Use clear, descriptive docstrings
- Include type hints
- Document parameters, return values, and exceptions
- Add examples for complex functions

### Help Text

- Write clear, concise help text for CLI arguments
- Include examples in help text
- Use consistent formatting

## 🐛 Bug Reports

### Before Submitting

1. **Check Existing Issues** - Search for similar issues
2. **Reproduce the Bug** - Ensure it's reproducible
3. **Test on Different Platforms** - Check if it's platform-specific
4. **Check Dependencies** - Verify all dependencies are installed

### Bug Report Template

```markdown
**Bug Description**
Brief description of the bug

**Steps to Reproduce**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [Windows/Linux/macOS]
- Python Version: [3.8/3.9/3.10/etc.]
- Toolkit Version: [if applicable]

**Additional Information**
- Error messages
- Screenshots
- Log files
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Feature Description**
Brief description of the requested feature

**Use Case**
Why this feature would be useful

**Proposed Implementation**
How you think it could be implemented

**Alternatives Considered**
Other approaches you've considered

**Additional Information**
Any other relevant information
```

## 🔄 Pull Request Process

### Before Submitting

1. **Test Your Changes**
   ```bash
   # Run basic tests
   python main.py --help
   python main.py your-module --help
   
   # Test functionality
   python main.py your-module --test-param value
   ```

2. **Update Documentation**
   - Update README.md if needed
   - Add/update docstrings
   - Update help text

3. **Check Code Style**
   - Follow PEP 8
   - Use type hints
   - Add appropriate comments

### Pull Request Template

```markdown
**Description**
Brief description of changes

**Type of Change**
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Test addition

**Testing**
- [ ] Tested on Windows
- [ ] Tested on Linux
- [ ] Tested on macOS
- [ ] Added unit tests
- [ ] Updated documentation

**Breaking Changes**
- [ ] Yes (describe changes)
- [ ] No

**Additional Notes**
Any additional information
```

## 🏷️ Issue Labels

We use the following labels to categorize issues:

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements or additions to documentation
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `question` - Further information is requested
- `wontfix` - This will not be worked on

## 📞 Getting Help

### Communication Channels

- **GitHub Issues** - For bug reports and feature requests
- **GitHub Discussions** - For questions and general discussion
- **Pull Requests** - For code contributions

### Code of Conduct

- Be respectful and inclusive
- Use welcoming and inclusive language
- Be collaborative and constructive
- Focus on what is best for the community

## 🎉 Recognition

Contributors will be recognized in:

- **README.md** - Contributors section
- **Release Notes** - For significant contributions
- **GitHub Contributors** - Automatic recognition

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the Blue Team CLI Toolkit! 🛡️
