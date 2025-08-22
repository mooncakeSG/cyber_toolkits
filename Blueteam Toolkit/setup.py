#!/usr/bin/env python3
"""
Setup script for Blue Team CLI Toolkit.
Makes the toolkit pip-installable with proper packaging and distribution.
"""

from setuptools import setup, find_packages
import os
import re

# Read the README file
def read_readme():
    """Read README.md file."""
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Blue Team CLI Toolkit - Defensive Security Operations"

# Read requirements
def read_requirements():
    """Read requirements.txt file."""
    try:
        with open("requirements.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return [
            "psutil>=5.9.0",
            "requests>=2.28.0",
            "PyYAML>=6.0",
            "schedule>=1.2.0"
        ]

# Get version from main.py
def get_version():
    """Extract version from main.py."""
    try:
        with open("main.py", "r", encoding="utf-8") as f:
            content = f.read()
            # Look for version pattern
            version_match = re.search(r'VERSION\s*=\s*["\']([^"\']+)["\']', content)
            if version_match:
                return version_match.group(1)
    except FileNotFoundError:
        pass
    return "1.0.0"

# Package data
def get_package_data():
    """Get package data files."""
    return {
        "blueteam_toolkit": [
            "*.json",
            "*.yml",
            "*.yaml",
            "*.md",
            "*.txt"
        ]
    }

setup(
    name="blueteam-toolkit",
    version=get_version(),
    author="Blue Team CLI Toolkit",
    author_email="blueteam@example.com",
    description="A comprehensive Python-based command-line toolkit for defensive security operations",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/blueteam-toolkit",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/blueteam-toolkit/issues",
        "Source": "https://github.com/yourusername/blueteam-toolkit",
        "Documentation": "https://github.com/yourusername/blueteam-toolkit/blob/main/README.md",
    },
    packages=find_packages(),
    package_data=get_package_data(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Security Analysts",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: System :: Systems Administration",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
            "pre-commit>=2.0",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
            "myst-parser>=0.15",
        ],
    },
    entry_points={
        "console_scripts": [
            "blueteam=main:main",
            "btk=main:main",
        ],
    },
    keywords=[
        "security",
        "blue-team",
        "defense",
        "forensics",
        "incident-response",
        "threat-hunting",
        "siem",
        "automation",
        "cli",
        "toolkit",
        "cybersecurity",
        "monitoring",
        "detection",
        "response",
    ],
    license="MIT",
    platforms=["Windows", "Linux", "macOS"],
    zip_safe=False,
)
