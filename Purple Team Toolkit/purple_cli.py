#!/usr/bin/env python3
"""
Purple Team Toolkit CLI Launcher

A comprehensive command-line interface for the Purple Team Toolkit
that provides easy access to all Red Team, Blue Team, and Purple Team operations.
"""

import sys
import os
from pathlib import Path

# Add the toolkit to Python path
toolkit_path = Path(__file__).parent / "purple_team_toolkit"
sys.path.insert(0, str(toolkit_path))

from purple_team_toolkit.cli.commands import main

if __name__ == "__main__":
    main()
