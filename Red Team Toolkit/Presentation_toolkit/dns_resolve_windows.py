#!/usr/bin/env python3
"""
DNS Troubleshooter Simulation Toolkit for Windows
A presentation-ready tool for demonstrating DNS troubleshooting with Wireshark integration.
"""

import os
import sys
import subprocess
import time
import signal
import threading
import platform
from typing import Optional, List, Dict


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


def run_powershell(command: str, capture_output: bool = False) -> Optional[str]:
    """Run a PowerShell command and return output if requested."""
    try:
        ps_command = f"powershell.exe -Command \"{command}\""
        if capture_output:
            result = subprocess.run(ps_command, shell=True, capture_output=True, text=True, timeout=30)
            return result.stdout.strip()
        else:
            subprocess.run(ps_command, shell=True, check=True, timeout=30)
            return None
    except subprocess.TimeoutExpired:
        print_error(f"PowerShell command timed out: {command}")
        return None
    except subprocess.CalledProcessError as e:
        print_error(f"PowerShell command failed: {command}")
        return None
    except Exception as e:
        print_error(f"Error running PowerShell command: {e}")
        return None


def run_cmd(command: str, capture_output: bool = False) -> Optional[str]:
    """Run a CMD command and return output if requested."""
    try:
        if capture_output:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            return result.stdout.strip()
        else:
            subprocess.run(command, shell=True, check=True, timeout=30)
            return None
    except subprocess.TimeoutExpired:
        print_error(f"Command timed out: {command}")
        return None
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {command}")
        return None
    except Exception as e:
        print_error(f"Error running command: {e}")
        return None


def get_network_interface() -> Optional[str]:
    """Get the active network interface."""
    try:
        # Get active network adapter
        result = run_powershell("Get-NetAdapter | Where-Object {$_.Status -eq 'Up'} | Select-Object -First 1 -ExpandProperty Name", True)
        if result:
            return result.strip()
        
        # Fallback: get first interface
        result = run_powershell("Get-NetAdapter | Select-Object -First 1 -ExpandProperty Name", True)
        if result:
            return result.strip()
        
        return None
    except Exception as e:
        print_error(f"Error getting network interface: {e}")
        return None


def check_dependencies() -> bool:
    """Check if required dependencies are installed."""
    dependencies = {
        'tshark': 'Wireshark CLI tools',
        'nslookup': 'Built-in Windows tool',
        'ping': 'Built-in Windows tool'
    }
    
    missing = []
    
    for dep, description in dependencies.items():
        if dep == 'tshark':
            # Check for tshark in common Wireshark locations
            tshark_paths = [
                r"C:\Program Files\Wireshark\tshark.exe",
                r"C:\Program Files (x86)\Wireshark\tshark.exe"
            ]
            found = False
            for path in tshark_paths:
                if os.path.exists(path):
                    found = True
                    break
            if not found:
                missing.append(f"{dep} ({description})")
        else:
            # Check if command is available
            if run_cmd(f"where {dep}", True) is None:
                missing.append(f"{dep} ({description})")
    
    if missing:
        print_error(f"Missing dependencies: {', '.join(missing)}")
        print_warning("Please install Wireshark from: https://www.wireshark.org/download.html")
        return False
    
    return True


def display_network_info(interface: str):
    """Display current network information."""
    print_step(1, "Displaying Current Network Information")
    
    print(f"{Colors.OKCYAN}Network Interface: {interface}{Colors.ENDC}")
    
    # Show interface details
    print(f"\n{Colors.BOLD}Interface Details:{Colors.ENDC}")
    run_powershell(f"Get-NetAdapter -Name '{interface}' | Format-List")
    
    # Show IP configuration
    print(f"\n{Colors.BOLD}IP Configuration:{Colors.ENDC}")
    run_powershell(f"Get-NetIPAddress -InterfaceAlias '{interface}' | Format-Table")
    
    # Show DNS configuration
    print(f"\n{Colors.BOLD}DNS Configuration:{Colors.ENDC}")
    run_powershell(f"Get-DnsClientServerAddress -InterfaceAlias '{interface}' | Format-Table")
    
    # Show current DNS servers
    print(f"\n{Colors.BOLD}Current DNS Servers:{Colors.ENDC}")
    run_powershell("Get-DnsClientServerAddress | Where-Object {$_.ServerAddresses -ne $null} | Format-Table")


def start_wireshark_capture(interface: str, capture_file: str) -> Optional[int]:
    """Start Wireshark capture in background."""
    print_step(2, "Starting Wireshark Capture")
    
    print(f"Starting capture on interface: {interface}")
    print(f"Capture file: {capture_file}")
    
    try:
        # Find tshark path
        tshark_paths = [
            r"C:\Program Files\Wireshark\tshark.exe",
            r"C:\Program Files (x86)\Wireshark\tshark.exe"
        ]
        tshark_path = None
        for path in tshark_paths:
            if os.path.exists(path):
                tshark_path = path
                break
        
        if not tshark_path:
            print_error("tshark not found. Please install Wireshark.")
            return None
        
        # Start tshark in background
        process = subprocess.Popen(
            f'"{tshark_path}" -i "{interface}" -w "{capture_file}" -f "port 53"',
            shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        
        # Wait a moment for capture to start
        time.sleep(2)
        
        if process.poll() is None:  # Process is still running
            print_success("Wireshark capture started successfully")
            return process.pid
        else:
            print_error("Failed to start Wireshark capture")
            return None
            
    except Exception as e:
        print_error(f"Error starting capture: {e}")
        return None


def simulate_dns_failure(interface: str):
    """Simulate DNS failure by setting invalid DNS server."""
    print_step(3, "Simulating DNS Failure")
    
    print("Setting DNS to non-existent server: 123.123.123.123")
    run_powershell(f'Set-DnsClientServerAddress -InterfaceAlias "{interface}" -ServerAddresses "123.123.123.123"')
    
    # Flush DNS cache
    print("Flushing DNS cache...")
    run_powershell("Clear-DnsClientCache")
    
    time.sleep(2)
    print_success("DNS failure simulated")


def test_dns_failure():
    """Test DNS resolution (should fail)."""
    print_step(4, "Testing DNS Resolution (Expected to Fail)")
    
    print("Testing ping to google.com...")
    run_cmd("ping -n 3 google.com")
    
    print("\nTesting DNS lookup with nslookup...")
    run_cmd("nslookup google.com")
    
    print_warning("DNS resolution should be failing now")


def restore_dns(interface: str):
    """Restore DNS configuration."""
    print_step(5, "Restoring DNS Configuration")
    
    print("Setting DNS back to Google DNS: 8.8.8.8")
    run_powershell(f'Set-DnsClientServerAddress -InterfaceAlias "{interface}" -ServerAddresses "8.8.8.8"')
    
    print("Flushing DNS cache...")
    run_powershell("Clear-DnsClientCache")
    
    time.sleep(2)
    print_success("DNS configuration restored")


def test_dns_recovery():
    """Test DNS resolution (should work)."""
    print_step(6, "Testing DNS Resolution (Should Work Now)")
    
    print("Testing ping to google.com...")
    run_cmd("ping -n 3 google.com")
    
    print("\nTesting DNS lookup with nslookup...")
    run_cmd("nslookup google.com")
    
    print_success("DNS resolution should be working now")


def stop_wireshark_capture(pid: int, capture_file: str):
    """Stop Wireshark capture."""
    print_step(7, "Stopping Wireshark Capture")
    
    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(1)
        
        # Check if process is still running
        try:
            os.kill(pid, 0)
            print_warning("Process still running, force killing...")
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass
        
        print_success("Wireshark capture stopped")
        print(f"Capture saved as: {capture_file}")
        print_warning("You can open this file in Wireshark to analyze DNS queries")
        
    except Exception as e:
        print_error(f"Error stopping capture: {e}")


def display_analysis_tips():
    """Display tips for analyzing the capture file."""
    print_step(8, "Analysis Tips")
    
    tips = [
        "Open the capture file in Wireshark",
        "Filter by 'dns' to see only DNS traffic",
        "Look for failed DNS queries (NXDOMAIN responses)",
        "Analyze the timing of DNS requests",
        "Check for DNS server timeouts",
        "Compare before/after DNS resolution behavior",
        "Use 'ip.addr == 123.123.123.123' to see failed queries"
    ]
    
    for i, tip in enumerate(tips, 1):
        print(f"{Colors.OKCYAN}{i}. {tip}{Colors.ENDC}")


def check_admin_privileges() -> bool:
    """Check if running with administrator privileges."""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False


def main():
    """Main function for DNS troubleshooting simulation."""
    print_header("DNS Troubleshooter Simulation Toolkit for Windows")
    print(f"{Colors.BOLD}This tool demonstrates DNS troubleshooting with Wireshark integration{Colors.ENDC}")
    print(f"{Colors.WARNING}Requires administrator privileges for network configuration{Colors.ENDC}")
    
    # Check if running as administrator
    if not check_admin_privileges():
        print_error("This script requires administrator privileges")
        print_warning("Please run as Administrator")
        print_warning("Right-click Command Prompt/PowerShell and select 'Run as administrator'")
        sys.exit(1)
    
    # Check if running on Windows
    if platform.system() != "Windows":
        print_error("This script is designed for Windows systems")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Get network interface
    interface = get_network_interface()
    if not interface:
        print_error("Could not determine network interface")
        sys.exit(1)
    
    print_success(f"Using interface: {interface}")
    
    # Configuration
    capture_file = "dns_capture_windows.pcap"
    wireshark_pid = None
    
    try:
        # Step 1: Display network info
        display_network_info(interface)
        
        # Step 2: Start Wireshark capture
        wireshark_pid = start_wireshark_capture(interface, capture_file)
        if not wireshark_pid:
            print_error("Failed to start capture, continuing without it...")
        
        # Step 3: Simulate DNS failure
        simulate_dns_failure(interface)
        
        # Step 4: Test DNS failure
        test_dns_failure()
        
        # Step 5: Restore DNS
        restore_dns(interface)
        
        # Step 6: Test DNS recovery
        test_dns_recovery()
        
        # Step 7: Stop capture
        if wireshark_pid:
            stop_wireshark_capture(wireshark_pid, capture_file)
        
        # Step 8: Analysis tips
        display_analysis_tips()
        
        print_header("DNS Troubleshooting Simulation Complete")
        print_success("All steps completed successfully!")
        print(f"{Colors.BOLD}Capture file: {capture_file}{Colors.ENDC}")
        
    except KeyboardInterrupt:
        print_warning("\nSimulation interrupted by user")
        if wireshark_pid:
            print("Stopping Wireshark capture...")
            stop_wireshark_capture(wireshark_pid, capture_file)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        if wireshark_pid:
            stop_wireshark_capture(wireshark_pid, capture_file)


if __name__ == "__main__":
    main()
