#!/usr/bin/env python3
"""
Demo script for Interactive DNS Troubleshooting Toolkit
This script demonstrates the interactive features without making network changes.
"""

import os
import sys
import platform
from typing import Dict


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


def print_header(title: str):
    """Print a formatted header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{Colors.ENDC}\n")


def print_step(step_num: int, title: str):
    """Print a formatted step header."""
    print(f"{Colors.OKBLUE}{Colors.BOLD}[Step {step_num}] {title}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}{'-' * (len(title) + 10)}{Colors.ENDC}")


def print_success(message: str):
    """Print a success message."""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")


def print_warning(message: str):
    """Print a warning message."""
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")


def print_error(message: str):
    """Print an error message."""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")


def print_info(message: str):
    """Print an info message."""
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")


def demo_interactive_features():
    """Demonstrate the interactive features."""
    print_header("Interactive DNS Troubleshooting Toolkit - Demo")
    
    print(f"{Colors.BOLD}This demo shows the interactive features of the toolkit{Colors.ENDC}")
    print(f"{Colors.WARNING}No network changes will be made{Colors.ENDC}")
    
    # Step 1: Dependency Check
    print_step(1, "Dependency Check")
    print_info("The toolkit automatically checks for required dependencies:")
    print("  • tshark (Wireshark CLI tools)")
    print("  • resolvectl (systemd-resolved)")
    print("  • dig (dnsutils package)")
    print("  • ping (iputils-ping package)")
    
    if platform.system() == "Windows":
        print("  • nslookup (Built-in Windows tool)")
        print("  • ping (Built-in Windows tool)")
        print("  • tshark (Wireshark CLI tools)")
    
    print_success("Missing dependencies are automatically installed")
    
    # Step 2: Network Interface Selection
    print_step(2, "Network Interface Selection")
    print_info("The toolkit detects and lists available network interfaces:")
    print("  • Automatically finds active interfaces")
    print("  • Filters out loopback and down interfaces")
    print("  • Allows user to choose from multiple interfaces")
    print("  • Provides default selection for single interface")
    
    # Step 3: Configuration
    print_step(3, "Interactive Configuration")
    print_info("Users can configure simulation parameters:")
    print("  • Target domain (default: google.com)")
    print("  • Invalid DNS server (default: 123.123.123.123)")
    print("  • Working DNS server (default: 8.8.8.8)")
    print("  • Capture duration (default: 30 seconds)")
    print("  • Capture file name (default: dns_capture.pcap)")
    
    # Step 4: Simulation Flow
    print_step(4, "Simulation Flow")
    print_info("The toolkit guides users through each step:")
    print("  • Network information display")
    print("  • Wireshark capture setup")
    print("  • DNS failure simulation")
    print("  • Failure testing")
    print("  • DNS restoration")
    print("  • Recovery verification")
    print("  • Analysis tips")
    
    # Step 5: User Interaction
    print_step(5, "User Interaction Features")
    print_info("Interactive prompts and confirmations:")
    print("  • Y/N confirmations with defaults")
    print("  • Numbered choice menus")
    print("  • Input validation")
    print("  • Default value suggestions")
    print("  • Error handling and recovery")
    
    # Step 6: Analysis Integration
    print_step(6, "Analysis Integration")
    print_info("Post-simulation analysis features:")
    print("  • Automatic Wireshark file opening")
    print("  • Analysis tips and guidance")
    print("  • Wireshark filter suggestions")
    print("  • Capture file management")
    
    print_header("Demo Complete")
    print_success("Interactive features demonstrated successfully!")
    
    # Show usage instructions
    print(f"\n{Colors.BOLD}To try the interactive toolkit:{Colors.ENDC}")
    if platform.system() == "Windows":
        print("  python dns_resolve_interactive_windows.py")
    else:
        print("  sudo python3 dns_resolve_interactive.py")


def show_feature_comparison():
    """Show comparison between standard and interactive versions."""
    print_header("Feature Comparison")
    
    comparison = {
        "Feature": ["Dependency Check", "Auto-Installation", "Interface Selection", "Configuration", "User Prompts", "Error Recovery"],
        "Standard": ["Manual", "No", "Automatic", "Hardcoded", "Minimal", "Basic"],
        "Interactive": ["Automatic", "Yes", "User Choice", "Interactive", "Rich", "Advanced"]
    }
    
    print(f"{Colors.BOLD}{'Feature':<20} {'Standard':<15} {'Interactive':<15}{Colors.ENDC}")
    print("-" * 50)
    
    for i in range(len(comparison["Feature"])):
        feature = comparison["Feature"][i]
        standard = comparison["Standard"][i]
        interactive = comparison["Interactive"][i]
        
        # Color code based on feature quality
        if interactive == "Yes" or interactive == "Automatic" or interactive == "Rich":
            interactive = f"{Colors.OKGREEN}{interactive}{Colors.ENDC}"
        elif interactive == "Advanced":
            interactive = f"{Colors.OKBLUE}{interactive}{Colors.ENDC}"
        
        print(f"{feature:<20} {standard:<15} {interactive}")


def main():
    """Main demo function."""
    demo_interactive_features()
    show_feature_comparison()
    
    print(f"\n{Colors.BOLD}Key Benefits of Interactive Version:{Colors.ENDC}")
    print(f"{Colors.OKGREEN}✓ Zero-configuration setup{Colors.ENDC}")
    print(f"{Colors.OKGREEN}✓ Automatic dependency management{Colors.ENDC}")
    print(f"{Colors.OKGREEN}✓ User-friendly interface{Colors.ENDC}")
    print(f"{Colors.OKGREEN}✓ Guided simulation process{Colors.ENDC}")
    print(f"{Colors.OKGREEN}✓ Enhanced error handling{Colors.ENDC}")
    print(f"{Colors.OKGREEN}✓ Professional presentation ready{Colors.ENDC}")


if __name__ == "__main__":
    main()
