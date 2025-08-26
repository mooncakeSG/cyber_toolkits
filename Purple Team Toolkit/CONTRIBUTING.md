# Contributing to Purple Team Toolkit

Thank you for your interest in contributing to the Purple Team Toolkit! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Release Process](#release-process)

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code.

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- Virtual environment (recommended)
- Basic understanding of cybersecurity concepts

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

   ```bash
   git clone https://github.com/mooncakesg/cyber_toolkits.git
   cd purple-team-toolkit
   ```

## Development Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Development Dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

### 3. Install Development Tools

```bash
pip install black flake8 mypy pytest pytest-cov
```

### 4. Setup Pre-commit Hooks (Optional)

```bash
pip install pre-commit
pre-commit install
```

## Contributing Guidelines

### Types of Contributions

We welcome various types of contributions:

#### 🐛 Bug Reports

- Clear and descriptive bug reports
- Steps to reproduce the issue
- Expected vs actual behavior
- Environment information

#### ✨ Feature Requests

- Clear description of the feature
- Use case and motivation
- Proposed implementation approach
- Impact on existing functionality

#### 📝 Documentation

- README improvements
- API documentation
- Code comments
- Tutorials and guides

#### 🔧 Code Contributions

- Bug fixes
- New features
- Performance improvements
- Test coverage

#### 🧪 Test Scenarios

- New attack scenarios
- Detection rules
- Correlation logic
- Edge case testing

### Contribution Areas

#### Red Team Modules

- New reconnaissance techniques
- Exploitation methods
- Post-exploitation activities
- Payload management

#### Blue Team Modules

- Log collection methods
- Detection rules
- Alert mechanisms
- Event normalization

#### Purple Logic

- Correlation algorithms
- Coverage analysis
- Reporting improvements
- MITRE ATT&CK mapping

#### Infrastructure

- CLI improvements
- Configuration management
- Plugin system
- Testing framework

## Code Style

### Python Style Guide

We follow PEP 8 with some modifications:

- Line length: 88 characters (Black default)
- Use type hints for all function parameters and return values
- Use docstrings for all public functions and classes
- Follow Google-style docstrings

### Code Formatting

We use Black for code formatting:

```bash
black purple_team_toolkit/
```

### Linting

We use flake8 for linting:

```bash
flake8 purple_team_toolkit/
```

### Type Checking

We use mypy for type checking:

```bash
mypy purple_team_toolkit/
```

### Example Code Style

```python
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ExampleClass:
    """Example class demonstrating code style.
  
    This class shows the preferred coding style for the project.
  
    Args:
        name: The name of the example
        value: The numeric value
      
    Attributes:
        name: The name of the example
        value: The numeric value
        metadata: Optional metadata dictionary
    """
  
    name: str
    value: int
    metadata: Optional[Dict[str, str]] = None
  
    def process_data(self, data: List[str]) -> Dict[str, int]:
        """Process the input data and return results.
      
        Args:
            data: List of strings to process
          
        Returns:
            Dictionary mapping strings to their processed values
          
        Raises:
            ValueError: If data is empty
        """
        if not data:
            raise ValueError("Data cannot be empty")
      
        return {item: len(item) for item in data}
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=purple_team_toolkit

# Run specific test file
pytest tests/test_red_team.py

# Run with verbose output
pytest -v
```

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names
- Mock external dependencies
- Test both success and failure cases
- Aim for high test coverage

### Test Structure

```python
import unittest
from unittest.mock import Mock, patch

class TestExampleModule(unittest.TestCase):
    """Test cases for ExampleModule."""
  
    def setUp(self):
        """Set up test fixtures."""
        self.config = {'test': 'value'}
        self.module = ExampleModule(self.config)
  
    def test_successful_operation(self):
        """Test successful operation."""
        result = self.module.operation('test_input')
        self.assertTrue(result.success)
        self.assertEqual(result.data['key'], 'expected_value')
  
    def test_failed_operation(self):
        """Test failed operation."""
        with patch('module.external_dependency') as mock_dep:
            mock_dep.side_effect = Exception("Test error")
            result = self.module.operation('test_input')
            self.assertFalse(result.success)
            self.assertIn('error', result.data)
```

## Documentation

### Code Documentation

- Use Google-style docstrings
- Document all public functions and classes
- Include type hints
- Provide usage examples

### User Documentation

- Keep README.md up to date
- Document new features
- Provide clear examples
- Include troubleshooting guides

### API Documentation

- Document all public APIs
- Include parameter descriptions
- Provide return value documentation
- Show usage examples

## Submitting Changes

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

- Write your code following the style guidelines
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 3. Commit Your Changes

```bash
git add .
git commit -m "feat: add new reconnaissance technique

- Add DNS zone transfer capability
- Include comprehensive tests
- Update documentation
- Fixes #123"
```

### 4. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:

- Clear title and description
- Reference to related issues
- Summary of changes
- Testing information

### 5. Pull Request Review

- Address review comments
- Make requested changes
- Ensure CI/CD passes
- Get approval from maintainers

## Release Process

### Versioning

We follow Semantic Versioning (SemVer):

- MAJOR.MINOR.PATCH
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests passing
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version bumped
- [ ] Release notes prepared
- [ ] Security review completed

## Security Considerations

### Responsible Disclosure

- Report security vulnerabilities privately
- Provide detailed reproduction steps
- Allow reasonable time for fixes
- Coordinate public disclosure

### Code Security

- Follow secure coding practices
- Validate all inputs
- Use parameterized queries
- Implement proper error handling
- Avoid hardcoded secrets

## Getting Help

### Communication Channels

- GitHub Issues: Bug reports and feature requests
- GitHub Discussions: General questions and discussions
- Security Issues: Private security reports

### Resources

- [Python Security Best Practices](https://python-security.readthedocs.io/)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- [MITRE ATT&amp;CK Framework](https://attack.mitre.org/)

## Recognition

Contributors will be recognized in:

- README.md contributors section
- Release notes
- Project documentation
- Community acknowledgments

---

Thank you for contributing to Purple Team Toolkit! Your contributions help make cybersecurity testing more effective and accessible for everyone. 🟣
