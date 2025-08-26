"""
Setup script for Purple Team Toolkit
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text() if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    with open(requirements_path, 'r') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="purple-team-toolkit",
    version="1.0.0",
    author="Purple Team Toolkit Contributors",
    author_email="contributors@purpleteam-toolkit.org",
    description="A comprehensive Purple Team cybersecurity toolkit for attack-defense correlation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/purple-team-toolkit/purple-team-toolkit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Networking :: Monitoring",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "purple-team-toolkit=purple_team_toolkit.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "purple_team_toolkit": [
            "configs/*.json",
            "configs/scenarios/*.yaml",
            "configs/scenarios/*.yml",
        ],
    },
    keywords="security, purple-team, red-team, blue-team, cybersecurity, detection, correlation",
    project_urls={
        "Bug Reports": "https://github.com/purple-team-toolkit/purple-team-toolkit/issues",
        "Source": "https://github.com/purple-team-toolkit/purple-team-toolkit",
        "Documentation": "https://purple-team-toolkit.readthedocs.io/",
    },
)
