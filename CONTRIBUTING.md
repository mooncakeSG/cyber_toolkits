# Contributing to Cyber Security Toolkits 🛡️⚔️

Thank you for your interest in contributing to the Cyber Security Toolkits! This document provides guidelines and information for contributors who want to help improve both the Blue Team and Red Team toolkits.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contribution Guidelines](#contribution-guidelines)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Security Guidelines](#security-guidelines)
- [Pull Request Process](#pull-request-process)
- [Code of Conduct](#code-of-conduct)

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** (recommended: Python 3.9+)
- **Git** for version control
- **Administrative privileges** (for testing advanced features)
- **Cross-platform development environment** (Windows, Linux, macOS)

### Areas for Contribution

#### Blue Team Toolkit
- **Bug Fixes**: Report and fix issues in defensive security tools
- **Feature Enhancements**: Add new incident response capabilities
- **SIEM Integrations**: Expand SIEM platform support
- **Threat Hunting**: Add new MITRE ATT&CK techniques
- **Automation**: Improve scheduling and automation features
- **Documentation**: Enhance user guides and examples

#### Red Team Toolkit
- **New Tools**: Add new penetration testing tools
- **Plugin Development**: Create plugins for the extensible architecture
- **Web Security**: Enhance web vulnerability scanning capabilities
- **Network Tools**: Improve network reconnaissance features
- **Reporting**: Enhance reporting and visualization features
- **Testing**: Expand test coverage and quality assurance

## 🔧 Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/yourusername/cyber-security-toolkits.git
cd cyber-security-toolkits
```

### 2. Set Up Development Environment

#### Blue Team Toolkit
```bash
cd "Blueteam Toolkit"

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

#### Red Team Toolkit
```bash
cd "Red Team Toolkit"

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Verify Installation

#### Blue Team Toolkit
```bash
cd "Blueteam Toolkit"
python main.py --help
python main.py logs --os windows --lines 5
```

#### Red Team Toolkit
```bash
cd "Red Team Toolkit"
python red_team_toolkit.py
# Test basic functionality
python test_red_team_toolkit.py
```

## 📝 Contribution Guidelines

### Before You Start

1. **Check Existing Issues**: Search for existing issues or feature requests
2. **Create an Issue**: If no existing issue, create one to discuss your contribution
3. **Plan Your Changes**: Document your approach and get feedback
4. **Follow Security Guidelines**: Ensure your changes maintain security best practices

### Types of Contributions

#### 🐛 Bug Reports
- **Clear Description**: Provide detailed steps to reproduce
- **Environment Info**: Include OS, Python version, toolkit version
- **Error Messages**: Include full error traces and logs
- **Expected vs Actual**: Describe expected and actual behavior

#### ✨ Feature Requests
- **Use Case**: Explain the problem you're solving
- **Proposed Solution**: Describe your proposed approach
- **Benefits**: Explain how it improves the toolkit
- **Implementation**: Suggest implementation details if possible

#### 🔧 Code Contributions
- **Small Changes**: Keep changes focused and manageable
- **One Feature**: One feature or fix per pull request
- **Backward Compatibility**: Maintain compatibility with existing functionality
- **Documentation**: Update documentation for new features

## 🎯 Code Standards

### Python Style Guide

#### General Standards
- **PEP 8 Compliance**: Follow Python style guidelines
- **Type Hints**: Use type hints for function parameters and return values
- **Docstrings**: Include comprehensive docstrings for all functions
- **Comments**: Add comments for complex logic

#### Example Code Structure
```python
#!/usr/bin/env python3
"""
Module description.
"""

from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


def example_function(param1: str, param2: Optional[int] = None) -> Dict[str, Any]:
    """
    Function description.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (optional)
        
    Returns:
        Dictionary containing results
        
    Raises:
        ValueError: If parameters are invalid
    """
    try:
        # Implementation
        result = {"status": "success", "data": param1}
        logger.info(f"Function completed successfully: {result}")
        return result
    except Exception as e:
        logger.error(f"Function failed: {e}")
        raise
```

### Security Standards

#### Input Validation
```python
def validate_input(value: str) -> bool:
    """Validate user input for security."""
    if not value or len(value) > 1000:
        return False
    # Add specific validation rules
    return True
```

#### Error Handling
```python
def safe_operation():
    """Perform operation with proper error handling."""
    try:
        # Operation code
        pass
    except PermissionError:
        logger.error("Insufficient privileges for operation")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False
    return True
```

### File Organization

#### Blue Team Toolkit Structure
```
Blueteam Toolkit/
├── main.py              # Main entry point
├── logs.py              # Log collection module
├── hunt.py              # Threat hunting module
├── ir.py                # Incident response module
├── ioc.py               # IOC scanning module
├── net.py               # Network defense module
├── mem.py               # Memory forensics module
├── siem.py              # SIEM integration module
├── automation.py        # Automation module
├── alerts.py            # Alerting module
├── utils.py             # Utility functions
├── sigma_rules/         # Sigma detection rules
├── tests/               # Test files
├── requirements.txt     # Dependencies
└── README.md           # Documentation
```

#### Red Team Toolkit Structure
```
Red Team Toolkit/
├── red_team_toolkit.py  # Main toolkit script
├── plugins/             # Plugin directory
├── tests/               # Test suite
├── reports/             # Generated reports
├── requirements.txt     # Dependencies
├── README.md           # Documentation
└── Progress/           # Development progress
```

## 🧪 Testing

### Running Tests

#### Blue Team Toolkit
```bash
cd "Blueteam Toolkit"

# Run basic functionality tests
python main.py logs --os windows --lines 5
python main.py hunt --technique T1053
python main.py ir
python main.py ioc --type ip --value 8.8.8.8
```

#### Red Team Toolkit
```bash
cd "Red Team Toolkit"

# Run comprehensive test suite
python test_red_team_toolkit.py

# Run specific test categories
python tests/run_tests.py all
python tests/run_tests.py plugin
python tests/run_tests.py scheduler
```

### Writing Tests

#### Test Structure
```python
#!/usr/bin/env python3
"""
Test module for example functionality.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from example_module import example_function


class TestExampleFunction(unittest.TestCase):
    """Test cases for example_function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_data = "test_value"
    
    def test_basic_functionality(self):
        """Test basic functionality."""
        result = example_function(self.test_data)
        self.assertIsInstance(result, dict)
        self.assertIn("status", result)
    
    def test_error_handling(self):
        """Test error handling."""
        with self.assertRaises(ValueError):
            example_function("")
    
    @patch('example_module.logger')
    def test_logging(self, mock_logger):
        """Test logging functionality."""
        example_function(self.test_data)
        mock_logger.info.assert_called_once()


if __name__ == '__main__':
    unittest.main()
```

### Test Coverage

- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test module interactions
- **Error Tests**: Test error conditions and edge cases
- **Security Tests**: Test input validation and security features
- **Cross-Platform Tests**: Test on different operating systems

## 📚 Documentation

### Documentation Standards

#### Code Documentation
- **Module Docstrings**: Describe module purpose and functionality
- **Function Docstrings**: Include parameters, returns, and examples
- **Inline Comments**: Explain complex logic
- **Type Hints**: Use type annotations for clarity

#### User Documentation
- **README Files**: Comprehensive project overview
- **Installation Guides**: Step-by-step setup instructions
- **Usage Examples**: Practical examples for common use cases
- **Troubleshooting**: Common issues and solutions

### Documentation Updates

When adding new features:
1. **Update README**: Add new features to documentation
2. **Add Examples**: Include usage examples
3. **Update Help**: Ensure help text is current
4. **Version Notes**: Document changes in version history

## 🛡️ Security Guidelines

### Security Best Practices

#### Input Validation
- **Sanitize Inputs**: Validate and sanitize all user inputs
- **Length Limits**: Implement reasonable length limits
- **Type Checking**: Verify data types and formats
- **Whitelist Approach**: Use whitelisting for allowed values

#### Error Handling
- **No Information Disclosure**: Don't expose sensitive information in errors
- **Graceful Degradation**: Handle errors without crashing
- **Logging**: Log errors for debugging without exposing details
- **User-Friendly Messages**: Provide helpful error messages

#### Privilege Management
- **Least Privilege**: Use minimum required privileges
- **Privilege Checks**: Verify permissions before operations
- **Safe Defaults**: Use safe default configurations
- **Administrative Warnings**: Warn users about privileged operations

### Security Review Checklist

- [ ] Input validation implemented
- [ ] Error handling secure
- [ ] No sensitive data in logs
- [ ] Privilege checks in place
- [ ] Safe default configurations
- [ ] Security warnings included
- [ ] Documentation includes security notes

## 🔄 Pull Request Process

### Before Submitting

1. **Test Your Changes**: Ensure all tests pass
2. **Update Documentation**: Update relevant documentation
3. **Check Style**: Verify code follows style guidelines
4. **Security Review**: Ensure security best practices are followed

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Test addition
- [ ] Other (please describe)

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Cross-platform testing (if applicable)

## Security
- [ ] Input validation implemented
- [ ] Error handling secure
- [ ] No sensitive data exposed
- [ ] Privilege checks in place

## Documentation
- [ ] README updated
- [ ] Help text updated
- [ ] Examples provided
- [ ] Version notes added

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] Tests added/updated
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs tests
2. **Code Review**: Maintainers review code changes
3. **Security Review**: Security-focused review
4. **Documentation Review**: Ensure documentation is updated
5. **Final Approval**: Maintainer approval required

## 📋 Code of Conduct

### Our Standards

- **Respectful Communication**: Be respectful and inclusive
- **Constructive Feedback**: Provide helpful, constructive feedback
- **Collaboration**: Work together to improve the project
- **Professional Behavior**: Maintain professional standards

### Reporting Issues

If you experience or witness unacceptable behavior:
1. **Contact Maintainers**: Reach out to project maintainers
2. **Provide Details**: Include specific details about the incident
3. **Confidentiality**: Reports will be handled confidentially
4. **Action**: Appropriate action will be taken

## 🎯 Getting Help

### Resources

- **Documentation**: Check README files and documentation
- **Issues**: Search existing issues for solutions
- **Discussions**: Use GitHub Discussions for questions
- **Maintainers**: Contact maintainers for guidance

### Communication Channels

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Pull Requests**: For code contributions and reviews

## 🏆 Recognition

### Contributor Recognition

- **Contributors List**: All contributors will be recognized
- **Commit History**: Contributions preserved in git history
- **Release Notes**: Contributors acknowledged in releases
- **Documentation**: Contributors listed in documentation

### Contribution Levels

- **Bug Fixes**: Small fixes and improvements
- **Feature Development**: New features and enhancements
- **Documentation**: Documentation improvements
- **Testing**: Test development and maintenance
- **Maintenance**: Ongoing maintenance and support

---

Thank you for contributing to the Cyber Security Toolkits! Your contributions help make these tools better for the entire security community. 🛡️⚔️
